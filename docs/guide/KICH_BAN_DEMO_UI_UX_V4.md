# Kịch bản demo UI/UX V4 — 14/10/2026

## Khởi động trong VS Code

Mở folder D:\slider\real-estate-bigdata. Terminal → New Terminal → PowerShell. Chỉ nhập lệnh sau, không copy phần PS D:\...> của terminal:

```powershell
cd D:\slider\real-estate-bigdata
./scripts/start-local.ps1
```

Chờ nạp Spark/models, thấy Application startup complete và frontend Ready, mở http://localhost:3000/. Giữ terminal chạy; Ctrl+C dừng. Nếu có dịch vụ đang chạy, dùng phiên đó, không chạy thêm bản thứ hai. Xem HUONG_DAN_CHAY.md để build lại/cài máy khác/LAN.

## Demo sản phẩm khoảng 6–8 phút

1. **Tổng quan:** nêu kỳ tin 06/2025–03/2026 và địa bàn lịch sử. Thay tháng/loại nhà; xuất CSV tổng hợp. Nói rõ giá rao, không giá chốt hoặc giá hiện tại.
2. **Tìm khu vực:** căn hộ3–4 tỷ,60–80 m² → Tìm khu vực phù hợp; mặc định14.110 tin / 19 khu vực. Đổi ngân sách chưa apply để chỉ ra form nháp; áp dụng rồi số liệu đổi. Bấm vùng hoặc Định vị khu vực; chọn2–3 vùng → Xem so sánh. Chỉ số so cùng điều kiện, không phải số nhà còn bán.
3. **Bản đồ giá:** lựa chọn và ngân sách giữ từ tìm kiếm. Đổi lớp màu giá/m², giá tổng, số tin; chọn vùng xem thông tin. Bật nền online khi có Internet, thử tải lại nếu lỗi; có thể demo polygon offline đầy đủ. Nền online là đường phố hiện nay, ranh giới nghiên cứu vẫn lịch sử.
4. **Ước tính giá rao bán:** căn hộ70 m², Thủ Đức, 2 phòng ngủ, 2 WC; bỏ phường/dự án nếu không biết. Nhập4,2 tỷ để đối chiếu → chạy ước tính. Giải thích giá mô hình, dải thực nghiệm và giá nhập. Giá nhập không đi vào model. Lưu căn này để so sánh → đổi 90 m² → chạy lại → Xem so sánh căn. Chuyển trang/quay lại cho thấy snapshot giữ. Không hứa dải chứa đúng giá từng căn.
5. **Độ chính xác dự đoán:** nêu sai lệch bằng tiền và phần trăm; bấm điểm hoặc chọn tin từ danh sách để thấy giá nguồn/dự đoán/chênh lệch. Mở 10 sai lệch lớn và bảng kỹ thuật nếu cần. Chỉ số chung là toàn test; bộ lọc scatter chỉ đổi mẫu biểu đồ 300 điểm.
6. **Dữ liệu & phương pháp:** bấm sáu bước; chọn lần lượt tin bán rõ, cho thuê, trả trước → Phân tích tin mẫu. Dùng 4 quyết định để giải thích tại sao không trộn giá thuê tháng/trả trước vào giá bán tổng. Đây là rule thật bằng Spark; chưa phát hiện tin giả hoặc xác minh tài sản.

## Chứng minh công nghệ Big Data

Chu trình: Parquet nguồn → Spark SQL/ETL → cohort/split thời gian → Spark ML đã huấn luyện → FastAPI → Next.js.

- Mở http://127.0.0.1:8000/api/v1/health, http://127.0.0.1:8000/docs và terminal API để cho thấy backend thật.
- Chỉ số/pipeline trên web đọc artifact/manifest; có thể mở artifacts/etl/etl_v4/summary.json, data/processed/core_v1/manifest.json và artifacts/models/v1/results.json trong VS Code.
- Lưu trữ Parquet trên filesystem; Spark 3.5.7 local[4], driver 4 GB. Không có MongoDB/HDFS hoặc cluster nhiều máy; không gọi demo này là huấn luyện trực tiếp mỗi lần nhập.
- Nếu giảng viên cần xem huấn luyện/ETL thực tế, dừng API trước rồi dùng hướng dẫn tái hiện hiện hữu; khối lượng lớn không nên rerun toàn bộ trong vài phút demo. Có model đã lưu và kết quả train/validation/test để đối chiếu.

Word/PPT cập nhật sau. Đây là sản phẩm local/LAN, chưa publish Internet.
