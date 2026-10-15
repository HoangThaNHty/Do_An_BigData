"""
Crawler dữ liệu Bất động sản từ Chợ Tốt REST API Gateway
Endpoint công khai: https://gateway.chotot.com/v1/public/ad-listing
Sử dụng chuẩn thư viện Python (urllib, json, csv) - KHÔNG CẦN CÀI ĐẶT THÊM THƯ VIỆN NGOÀI!
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import urllib.request
import urllib.parse
import json
import time
import os
import csv
from datetime import datetime

def crawl_chotot(region_code=13000, category_code=1020, max_pages=5, delay=0.3):
    """
    region_code:
      13000: TP. Hồ Chí Minh
      12000: Hà Nội
      10000: Đà Nẵng
    category_code:
      1000: Toàn bộ BĐS
      1010: Căn hộ chung cư
      1020: Nhà ở riêng lẻ
      1030: Đất nền
    """
    base_url = "https://gateway.chotot.com/v1/public/ad-listing"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://nha.chotot.com",
        "Referer": "https://nha.chotot.com/"
    }

    fieldnames = [
        "list_id", "subject", "price", "price_string", "area_m2",
        "rooms", "toilets", "floors", "direction", "legal",
        "district_name", "ward_name", "region_name",
        "latitude", "longitude", "property_type", "furnishing", "body", "date"
    ]

    records = []
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Bắt đầu thu thập dữ liệu khu vực {region_code} (Danh mục {category_code})...")

    for page in range(max_pages):
        offset = page * 20
        params = {
            "region_v2": region_code,
            "cg": category_code,
            "limit": 20,
            "o": offset
        }
        query_string = urllib.parse.urlencode(params)
        full_url = f"{base_url}?{query_string}"

        req = urllib.request.Request(full_url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                if response.status == 200:
                    raw_data = response.read().decode('utf-8')
                    data = json.loads(raw_data)
                    ads = data.get("ads", [])
                    if not ads:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] Hết dữ liệu tại trang {page+1}.")
                        break

                    for ad in ads:
                        records.append({
                            "list_id": ad.get("list_id", ""),
                            "subject": ad.get("subject", ""),
                            "price": ad.get("price", ""),
                            "price_string": ad.get("price_string", ""),
                            "area_m2": ad.get("size", ""),
                            "rooms": ad.get("rooms", ""),
                            "toilets": ad.get("toilets", ""),
                            "floors": ad.get("floors", ""),
                            "direction": ad.get("direction", ""),
                            "legal": ad.get("property_legal_document", ""),
                            "district_name": ad.get("area_name", ""),
                            "ward_name": ad.get("ward_name", ""),
                            "region_name": ad.get("region_name", ""),
                            "latitude": ad.get("latitude", ""),
                            "longitude": ad.get("longitude", ""),
                            "property_type": ad.get("property_road_sub_type", ""),
                            "furnishing": ad.get("furnishing_status", ""),
                            "body": (ad.get("body", "") or "").replace("\n", " ").replace("\r", " "),
                            "date": ad.get("date", "")
                        })

                    print(f"[Trang {page+1:02d}/{max_pages}] Lấy thành công {len(ads)} tin. Tổng tích lũy: {len(records)} tin.")
                    time.sleep(delay)
                else:
                    print(f"[-] HTTP Status {response.status}")
                    break
        except Exception as e:
            print(f"[-] Ngoại lệ kết nối: {e}")
            break

    if records:
        output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"chotot_raw_{region_code}_{category_code}.csv")
        with open(output_file, mode="w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)

        print(f"\n[THÀNH CÔNG] Đã lưu {len(records)} bản ghi BĐS sạch vào: {os.path.abspath(output_file)}")
    else:
        print("[!] Không thu thập được dữ liệu.")

if __name__ == "__main__":
    # Chạy thử nghiệm 5 trang (~100 tin nhà ở TP.HCM)
    crawl_chotot(region_code=13000, category_code=1020, max_pages=5, delay=0.3)
