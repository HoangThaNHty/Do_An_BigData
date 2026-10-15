# Kiểm tra ứng viên v5 — 12/10/2026

100 tin mới được đọc toàn bộ tiêu đề/mô tả và gán nhãn AI trước khi xem dự đoán. Mã quality cross-field-v4-provisional, rules và dự đoán được cố định trước gán nhãn, loại trừ toàn bộ row_id mẫu trước.

| Kiểm tra | Kết quả |
|---|---:|
| Giao dịch bán phù hợp nguồn |100/100|
| Loại diện tích phù hợp nguồn |100/100|
| Giá và loại diện tích được hỗ trợ |99/100|
| Thêm đúng phạm vi nhà ở |98/100|

Đạt ngưỡng điểm nghiên cứu95% đã đặt trước, cho phép triển khai tập nghiên cứu và mô hình. KhoảngWilson95% của98/100 là92,999%–99,450%; **không khẳng định cận dưới95% hoặc 98% toàn bộ thị trường**. Nhãn AI không phải ground truth chuyên gia. Không có nhãn thuê trong mẫu ứng viên nên không đo recall/khả năng phát hiện thuê từ lượt này.

Theo loại:14/14nhà và84/86căn hộ được hỗ trợ đầy đủ. Mẫu nhà chỉ14tin nên độ bất định lớn; không quảng cáo100%chất lượng nhà trên toàn tập. Kết quả có điều kiện trên các ứng viên lọc, không đo tỷ lệ thu hồi tin hợp lệ bị cách ly.

Hai tin cần xem lại: index87 Privia có hai mãA07/A14 và khoảnggiá2,55–2,65 tỷ; index92 bảnggiỏSaigonIntela có cặp50m2/1,780 tỷ phù hợp nguồn nhưng chưa chọn rõ một căn. Không sửa bộ lọc dựa trên v5 rồi gọi đây là đánh giá độc lập của bản sửa. Không chọn riêng hai tin để sửa giá hoặc gán diện tích.

Tập thực nghiệm mô hình sẽ loại trừ toàn bộ row_id các phiếu review đã tạo (cả đúng và sai), giữ dữ liệu kiểm tra riêng ngoài thực nghiệm giá; báo cáo số loại thực tế ở manifest core. Bộ lọc có thể còn lỗi tương tự ở tin khác, cần nêu giới hạn khi demo. Không xác minh giá chốt, tính thật hay quyền sở hữu.

QualitySHA256:715b5b317087f9f347813d029f6114df7743dc3374dc158d46b9f5d58beb92d4. Bằng chứng trong artifacts/review/v5, gồm5file gán nhãn, CSV, evaluation.json, manifest, freeze và frozen_code.
