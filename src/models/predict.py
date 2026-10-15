"""Command-line saved-model inference; JSON input, no target price required."""
import argparse,json
from pathlib import Path
from src.config.spark import ROOT,session
from src.models.inference import Estimator


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--input',type=Path,required=True)
    parser.add_argument('--models',type=Path,default=ROOT/'artifacts/models/v1')
    args=parser.parse_args()
    spark=session('saved-model-price-inference')
    try:
        result=Estimator(spark,args.models).estimate(json.loads(args.input.read_text(encoding='utf-8')))
        print(json.dumps(result,ensure_ascii=False,indent=2))
    finally:spark.stop()


if __name__=='__main__':main()
