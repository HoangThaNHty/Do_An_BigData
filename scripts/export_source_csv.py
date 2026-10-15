"""Stream all pinned raw shards to one CSV, then independently parse/count it."""
import argparse
import hashlib
import json
import os
import gc
import time
from pathlib import Path

import pyarrow as pa
import pyarrow.csv as pc
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT/'data/raw/oceanng/vietnam_real_estates_full.csv')
    parser.add_argument('--verify-partial', action='store_true', help='Verify a completed .part export without writing it again')
    args = parser.parse_args()
    output = args.output.resolve()
    partial = output.with_name(output.name + '.part')
    report = output.with_suffix('.csv.manifest.json')
    if output.exists() or report.exists() or (partial.exists() and not args.verify_partial):
        raise FileExistsError('Preserve existing exports; use a fresh --output path.')
    source = ROOT/'data/raw/oceanng'
    manifest = json.loads((source/'manifest.json').read_text(encoding='utf-8'))
    parts = [source/item['path'] for item in manifest['files'] if item['path'].endswith('.parquet')]
    if len(parts) != 10:
        raise ValueError('Expected all 10 pinned source shards.')
    schema = pq.ParquetFile(parts[0]).schema_arrow.remove_metadata()
    expected = sum(pq.ParquetFile(p).metadata.num_rows for p in parts)
    if expected != 3500744 or len(schema) != 19:
        raise ValueError('Unexpected source row count/schema.')
    for path in parts:
        if not pq.ParquetFile(path).schema_arrow.remove_metadata().equals(schema):
            raise ValueError(f'Schema mismatch: {path.name}')
    output.parent.mkdir(parents=True, exist_ok=True)
    written = expected if args.verify_partial else 0
    if not args.verify_partial:
        with partial.open('wb') as sink:
            sink.write(b'\xef\xbb\xbf')
            with pc.CSVWriter(sink, schema, write_options=pc.WriteOptions(include_header=True)) as writer:
                for path in parts:
                    for batch in pq.ParquetFile(path).iter_batches(batch_size=8192):
                        writer.write_batch(batch)
                        written += batch.num_rows
                    print(f'{path.name}: {written:,}/{expected:,} records exported', flush=True)
        del writer
    print('Verifying CSV records/columns with a CSV parser (including quoted newlines)...', flush=True)
    parsed = 0
    with partial.open('rb') as csv_input, pc.open_csv(csv_input, read_options=pc.ReadOptions(block_size=8*1024*1024),
                     parse_options=pc.ParseOptions(newlines_in_values=True),
                     convert_options=pc.ConvertOptions(column_types={field.name: pa.string() for field in schema})) as reader:
        if reader.schema.names != schema.names:
            raise AssertionError('CSV column order mismatch')
        for batch in reader:
            parsed += batch.num_rows
    del reader
    gc.collect()
    if parsed != expected or written != expected:
        raise AssertionError(f'Count mismatch: parsed={parsed}, written={written}, expected={expected}')
    digest = hashlib.sha256()
    with partial.open('rb') as stream:
        for block in iter(lambda: stream.read(8*1024*1024), b''):
            digest.update(block)
    for attempt in range(10):
        try:
            os.rename(partial, output)
            break
        except PermissionError:
            if attempt == 9:
                raise
            time.sleep(0.2)
    result = {'csv':str(output), 'rows':parsed, 'columns':schema.names, 'column_count':len(schema),
              'bytes':output.stat().st_size, 'sha256':digest.hexdigest(), 'encoding':'UTF-8 BOM',
              'source_repository':manifest['repository'], 'source_revision':manifest['revision'],
              'source_shards':[p.name for p in parts], 'verification':'Arrow CSV parser record count and ordered header',
              'notes':['All source rows; no geographic/type/time filtering or deduplication.',
                       'CSV has embedded quoted newlines: physical line count is not record count.',
                       'Source text is unmodified; import text as text in spreadsheet applications.',
                       'CSV is a viewing/export copy; Parquet remains authoritative for null/type fidelity.']}
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    main()
