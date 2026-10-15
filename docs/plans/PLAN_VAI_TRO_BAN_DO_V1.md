# Phân biệt Tìm khu vực và Bản đồ giá — đề xuất v1

Ngày 15/10/2026. **Chỉ trao đổi, chưa triển khai/xóa trang.**

Vấn đề: UI V4 đã có bản đồ trong Tìm khu vực. Trang bản đồ riêng nếu chỉ lặp chọn vùng/trung vị/thêm so sánh sẽ trùng nhiệm vụ.

| Trang | Câu hỏi | Vai trò đề xuất |
|---|---|---|
| Tìm khu vực | Ngân sách/diện tích này phù hợp nơi nào? | Nhập nhu cầu → kết quả → so sánh → ước tính; map hỗ trợ định vị |
| Bản đồ thị trường (tên đề xuất) | Giá rao và lượng dữ liệu khác nhau theo vùng/tháng ra sao? | Toàn địa bàn, lớp giá/m²/tổng giá/số tin; chi tiết vùng, xu hướng/cỡ mẫu |

Demo riêng: so sánh giá rao trung vị/m² tháng 01/2026 và 03/2026 theo cùng loại nhà, xem số tin mỗi kỳ. Đây là quan sát tập tin, không chứng minh tăng/giảm giá giao dịch hay giá hiện tại.

Ưu tiên P0: tên/description và mục tiêu hai trang rõ, map tìm kiếm tập trung kết quả nhu cầu, map riêng toàn địa bàn. P1: chi tiết vùng có biểu đồ theo tháng kèm cỡ mẫu. P2: đối chiếu hai tháng và lớp chênh lệch nếu hữu ích; chỉ tính khi hai kỳ hợp lệ/đủ mẫu, nêu ảnh hưởng thay đổi cơ cấu tin.

Kiểm tra district_month.json/serving/API hiện có trước khi thêm endpoint. P1/P2 là đề xuất, không coi đã có vì đã có dữ liệu tháng. Giữ 22 nhóm lịch sử/thời gian nguồn, không bịa GPS từng căn hoặc mapping địa giới mới. Leaflet đủ, chưa cần Google Maps.

Sau khi chốt mới sửa và test tháng/lớp/legend/click/vùng ít mẫu/shared comparison/liên kết/mobile/online-offline. Cập nhật plan Word, screenshot và demo theo chức năng thật.

Nếu không có hành trình riêng hữu ích: gộp thành tab Danh sách/Bản đồ trong Tìm khu vực và bỏ mục menu trùng, giữ các lớp phân tích và logic map. Không cần xóa khả năng địa bàn khỏi sản phẩm.
