# Kiểm tra ứng viên v4 — 12/10/2026

Mã quality v3 được cố định trước khi đọc 100 tin mới; dự đoán lưu riêng. Đã gán đủ 100 nhãn bằng AI đọc nội dung nguồn, rồi mới chấm điểm. Mẫu loại trừ row_id từng đọc trước đó.

| Kiểm tra | Kết quả |
|---|---:|
| Giao dịch bán phù hợp nguồn | 100/100 |
| Giá và loại diện tích được hỗ trợ | 97/100 |
| Thêm đúng phạm vi nhà ở | 94/100 |

94% chưa đạt ngưỡng nghiên cứu 95% đã đặt trước. Khoảng Wilson 95% xấp xỉ 87,5%–97,2%; đây là tham chiếu AI trên mẫu, không phải xác minh chuyên gia hay bảo đảm toàn bộ thị trường.

6 lỗi phạm vi/giá/diện tích: index4 officetel trong thân tin; index22 phép cộng diện tích101+40=151 sai; index26 căn OT và hoàn lại85triệu; index84 tổng công nhận126,8m2 mâu thuẫn đất4x13m; index86 văn phòng kết hợp lưu trú; index96 chỉ dự kiến cải tạo để ở, không nêu công năng hiện hữu. Tin có giá rẻ hoặc diện tích nhỏ không tự được gán sai nếu không có chứng cứ nội dung.

Giữ nguyên bộ nhãn và snapshot. Lượt ETL v3 dùng quality v3 chỉ là bản đã lọc chưa đạt tiêu chí huấn luyện. Phiên bản mới cần mở rộng kiểm tra thân tin, số liệu diện tích và phân biệt mục đích cải tạo với công năng đang có; đánh giá lại trên mẫu mới cùng ngưỡng, không chấm lại v4 rồi gọi là độc lập.

Bằng chứng: artifacts/review/v4/evaluation.json, blind_review.csv, evaluation_001.json đến evaluation_007.json, manifest.json, freeze.json và frozen_code.
