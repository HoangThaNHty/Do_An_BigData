# Dataset ở đâu và cách xem CSV

Ngày 15/10/2026. **Đã xuất CSV toàn nguồn theo yêu cầu tiếp theo của người dùng.**

File: `data/raw/oceanng/vietnam_real_estates_full.csv` — 3.500.744 bản ghi, 19 trường, 3.266.488.214 byte, UTF-8 BOM. Đã đọc lại bằng CSV parser, kiểm tra số bản ghi/header; manifest SHA-256 nằm cạnh file tại `vietnam_real_estates_full.csv.manifest.json`. Dữ liệu có trường văn bản xuống dòng nên không dùng số dòng vật lý để kiểm số bản ghi. CSV là bản xuất, Parquet gốc vẫn giữ nguyên và có thông tin kiểu/null đầy đủ hơn.

File CSV giữ nguyên văn bản nguồn, không thêm escape để dùng như spreadsheet; khi nhập bằng Excel/Power Query đặt trường văn bản thành Text. Một sheet Excel tối đa 1.048.576 dòng nên không hiển thị hết 3.500.744 bản ghi; giới hạn hiển thị không có nghĩa file CSV thiếu dữ liệu. Xem nguồn Microsoft ở cuối hướng dẫn demo. Các lệnh mẫu bên dưới vẫn dành cho bản xem 1.000 dòng nhỏ hơn.

Xuất lại khi cần: `.\.venv\Scripts\python.exe -m scripts.export_source_csv --output data/raw/oceanng/ten_file_moi.csv`; chương trình không ghi đè file đã có. CSV lớn và manifest export được ignore Git cùng raw.

Repo trên máy: D:\slider\real-estate-bigdata, không phải FolderDoAnBigData.

| Tầng | Đường dẫn tương đối repo | Ý nghĩa |
|---|---|---|
| Nguồn tải | data/raw/oceanng/shard_0000.parquet … shard_0009.parquet | 3.500.744 dòng, 19 trường toàn nguồn |
| Nguồn/giấy phép | data/raw/oceanng/manifest.json và DATASET_CARD.md | Revision/hash/card |
| ETL | data/processed/etl_v4 | Đã xử lý |
| Cohort | data/processed/core_v1 | 133.779 tin, feature/split nghiên cứu |
| Serving | artifacts/market/serving/*.parquet | 133.779 tin, 7 trường cho web; không đủ feature để train lại |

CSV data/raw/chotot_raw_13000_1020.csv là crawler cũ, **không phải dataset oceanNG hiện hành**. Raw giữ local/ignored Git; clone có model/serving để demo. Nút CSV web xuất thống kê theo filter, không phải raw.

Trong PowerShell VS Code sau setup, xuất 1.000 dòng đầu shard đầu để đọc (không phải mẫu ngẫu nhiên hoặc riêng HCM):

```powershell
cd D:\slider\real-estate-bigdata
@'
from pathlib import Path
import csv
import pyarrow.parquet as pq
root = Path.cwd()
out = root / '.runtime' / 'data-preview'
out.mkdir(parents=True, exist_ok=True)
batch = next(pq.ParquetFile(root/'data/raw/oceanng/shard_0000.parquet').iter_batches(batch_size=1000))
def safe(v):
    return "'" + v if isinstance(v,str) and v.lstrip().startswith(('=','+','-','@')) else v
with (out/'raw_first_1000.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w = csv.DictWriter(f,fieldnames=batch.schema.names)
    w.writeheader()
    w.writerows({k:safe(v) for k,v in row.items()} for row in batch.to_pylist())
print(out/'raw_first_1000.csv')
'@ | .\.venv\Scripts\python.exe -
```

Bản xem UTF-8 BOM, có thể thêm dấu nháy đơn vào đầu ô văn bản có thể thành công thức; không đổi Parquet gốc. Trong Excel: Data → From Text/CSV, UTF-8, dấu phẩy; trường mã/tháng để Text. Nếu cần xem toàn tập web, xuất từng batch của các file serving vào một CSV tương tự; price là VND, area m², unit_price_vnd VND/m².

File xuất trong .runtime được ignore Git. Không xuất toàn bộ raw vào một sheet chỉ để đọc vài dòng; khi cần toàn nguồn chia theo shard và giới hạn công cụ đọc. Muốn huấn luyện lại đọc data/README.md và guide/SETUP.md để lấy đúng cohort/review/provenance.
