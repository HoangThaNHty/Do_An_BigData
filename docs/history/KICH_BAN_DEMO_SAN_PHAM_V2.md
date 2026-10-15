# Kịch bản demo sản phẩm và Spark — v2

Mã nguồn: D:\slider\real-estate-bigdata. Mục tiêu là chứng minh nguồn → xử lý bằng Spark → mô hình → API → chức năng phục vụ người dùng. Spark chạy local[4], chưa có cluster nhiều máy hoặc MongoDB. Parquet là định dạng lưu trữ hiện tại.

## Phần sản phẩm, khoảng 8–10 phút

1. Chạy `./scripts/start-local.ps1`, chờ API/Next Ready. Mở http://localhost:3000. Health http://localhost:3000/api/v1/health phải ready. Giữ tiến trình chạy; không chạy đồng thời một ETL/huấn luyện khác.
2. Tổng quan: giải thích số tin, giá rao, thời gian 06/2025–03/2026, phạm vi TP.HCM trước hợp nhất. Nhấn tra địa danh, thử Quận 9: về nhóm Thủ Đức lịch sử, không tự xác định phường hiện hành.
3. Khám phá: căn hộ, toàn kỳ/toàn khu vực, ngân sách 3–4 tỷ, diện tích 60–80 m². Số hiện tại 14.110 tin, 19 khu vực. Chọn hai khu vực để so sánh số tin/trung vị/tứ phân vị. Đây là tin lịch sử, chưa xác nhận còn bán.
4. Nhấn Xem bản đồ tại một khu vực: điều kiện ngân sách/diện tích được giữ. Đổi lớp màu thành Số tin; chọn vùng khác, thêm hai vùng để so sánh. Nền OSM chỉ bật khi Internet ổn; mặc định offline vẫn hoạt động. Không có GPS từng căn.
5. Nhấn Ước tính tại khu vực này: kiểm tra loại/khu vực/diện tích đã điền. Nhập giá rao đang cân nhắc 4,2 tỷ, chạy ước tính. Giải thích chênh lệch và dải thực nghiệm, không gọi kết quả là giá thẩm định hoặc kết luận đắt/rẻ.
6. Giữ phương án A; tăng diện tích lên 90 m², chạy B. Cho thấy snapshot A không thay đổi và model chạy thật. Nhóm dữ liệu tham khảo chỉ cùng loại/khu vực và diện tích ±15%, không xác nhận tương đương pháp lý/chất lượng.
7. Đánh giá mô hình: bấm một điểm scatter, giải thích đường chéo và sai lệch; lọc khoảng giá, xem bảng sai số và 10 ví dụ sai nhiều. Mở bảng kỹ thuật để so baseline/LR/RF/GBT. Mô hình chọn từ validation; không sửa theo test.
8. Phương pháp: chọn từng bước pipeline, đặc biệt bảng định tuyến và split. Thử tin cho thuê hoặc giá trả trước, nhấn Chạy bộ kiểm tra Spark. Có thể xem http://localhost:4040 Jobs/Stages/SQL trong lúc API Spark còn chạy; kiểm tra cổng thực nếu 4040 bị chiếm. Các ví dụ tổng hợp không phải tin nguồn; thao tác chỉ kiểm tra, không thêm vào train.

## Phần huấn luyện live, thêm khoảng 4–6 phút

Phần trước dùng model đã lưu. Muốn chứng minh fit thật, dừng API/web trước bằng Ctrl+C ở terminal sở hữu dịch vụ. Nếu dịch vụ do trợ lý chạy, yêu cầu dừng phiên đó trước; không mở thêm Spark JVM khi cổng API còn hoạt động.

```powershell
cd D:\slider\real-estate-bigdata
$DemoRunName = Get-Date -Format 'yyyyMMdd_HHmmss'
.\scripts\run.ps1 src.models.train --core data/processed/core_v1 --output "artifacts/models/demo_$DemoRunName"
```

Tên output mới tránh ghi đè model v1. Lệnh fit cả 9 pipeline/baseline trên cohort đã chuẩn bị, khoảng 188 giây ở thí nghiệm trước nhưng không cam kết thời gian. Khi Spark còn chạy mở Spark UI (thường 4040), cho thấy jobs/stages thật. UI biến mất sau spark.stop; chụp màn hình lúc đang chạy nếu cần.

Sau hoàn tất, mở thư mục experiment vừa tạo: validation_results.json → selection.json → results.json. Giải thích fit tiền xử lý trên train và selection trước test. Model mới không tự thay model v1 trên web; không cần thay bản demo đã kiểm chứng trong buổi bảo vệ.

## ETL toàn bộ và phương án dự phòng

Live toàn bộ ETL trước đó khoảng 504 giây, thường vượt thời lượng demo ngắn. Có thể trình bày Parquet/schema, code và manifest đã kiểm chứng; nói rõ không chạy lại toàn bộ ở bước đó. Lệnh tái hiện đầy đủ trong HUONG_DAN_CHAY.md, luôn output mới và dừng API trước.

Giữ ảnh QA ở artifacts/verification/product-web làm minh chứng dự phòng, nhưng phải nói rõ ảnh lần chạy đã kiểm tra. Nếu web báo không tải được dữ liệu, kiểm tra health cổng 8000 và 3000; giữ cả hai tiến trình. Trước buổi bảo vệ diễn tập trên đúng máy với Internet tắt để xác nhận đường chạy offline.
