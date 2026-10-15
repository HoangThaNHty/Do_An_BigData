"""One worker; launch through scripts/run.ps1 so Spark inherits Java config."""
import argparse
import uvicorn


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--host',default='127.0.0.1')
    parser.add_argument('--port',type=int,default=8000)
    args=parser.parse_args()
    uvicorn.run('src.api.main:app',host=args.host,port=args.port,workers=1)


if __name__=='__main__':main()
