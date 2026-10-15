# Kiểm tra ứng viên v3 — 12/10/2026

100 tin ứng viên mới được đọc nội dung và gán nhãn AI trước khi xem dự đoán. Mẫu không trùng row_id các lượt trước; mã quality v2 và dự đoán được lưu snapshot trước gán nhãn.

- Giao dịch bán: 100/100 phù hợp nội dung nguồn.
- Giá và loại diện tích: 96/100 được nội dung hỗ trợ.
- Thêm yêu cầu đúng phạm vi nhà ở: 83/100; chưa đạt ngưỡng nghiên cứu 95% đã định trước.
- Khoảng Wilson 95% cho 83/100: khoảng 74,5%–89,1%. Nhãn do AI đọc nguồn, không phải xác nhận chuyên gia hay xác minh tài sản.

Các lỗi gồm nhà/tòa nhà dùng kinh doanh chưa có công năng sinh hoạt rõ, biệt thự trong thân tin, giỏ hàng hoặc giá theo khoảng, điều chỉnh giá trừ thêm, diện tích chính mâu thuẫn và mã tháp mâu thuẫn.

Không dùng ETL v2 làm tập huấn luyện chính. Quality v3 bổ sung kiểm tra sau lượt này; v3 trở thành dữ liệu chẩn đoán cho phiên bản mới, không được gọi là đánh giá độc lập của quality v3. Tiếp theo lấy mẫu ứng viên v4 mới, cố định mã trước đọc, kiểm tra lại với cùng tiêu chí. Giữ rules.py gốc không đổi.

Bằng chứng: artifacts/review/v3/blind_review.csv, evaluation_001.json đến evaluation_005.json, evaluation.json, manifest.json và frozen_code. Việc có nội dung hỗ trợ không chứng minh giá giao dịch thật hoặc tính hợp pháp của tin.
