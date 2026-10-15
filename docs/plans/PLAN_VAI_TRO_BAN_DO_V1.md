> **Đã triển khai V5 — 15/10/2026:** Người dùng đã duyệt. Một mục Khám phá khu vực, mặc định bản đồ/toàn địa bàn, Danh sách/Bản đồ cùng criteria và lựa chọn so sánh, giữ lớp màu/chi tiết/offline. Không còn menu Bản đồ giá riêng. Đọc NGHIEM_THU_SAN_PHAM_V5 trong guide; các dòng chưa triển khai bên dưới là lịch sử đề xuất.

# Tìm khu vực và Bản đồ giá — V5 đã gộp, kèm lịch sử đề xuất

Ngày 15/10/2026. Hướng gộp đã được duyệt và triển khai. Giữ tên file V1 để không hỏng link; các mục dưới lưu đặc tả và phương án trước triển khai, kết quả thực tế đọc biên bản V5.

## 1. Khuyến nghị hiện tại: một mục điều hướng, hai cách xem

Tên đề xuất: **Khám phá khu vực**. Trong một không gian làm việc có **Bản đồ / Danh sách**, dùng cùng loại nhà, tháng, điều kiện ngân sách/diện tích, vùng đang xem và lựa chọn so sánh. Không đưa hai trang cũ vào hai tab nhưng để mỗi tab tự giữ bộ lọc/API khác nghĩa.

Hai câu hỏi cùng được giữ:

- Không giới hạn ngân sách/diện tích: xem giá rao và mức độ có dữ liệu trên toàn địa bàn nghiên cứu.
- Có nhu cầu cụ thể: lọc các tin phù hợp, xem những khu vực có dữ liệu và đối chiếu trước khi sang ước tính.

Không cần hai bộ lọc hoặc thêm một hệ thống dữ liệu. Nút **Bỏ giới hạn ngân sách và diện tích** giữ nguyên loại nhà/tháng để người dùng biết chính xác phạm vi sau thao tác. Chuyển Bản đồ/Danh sách không tự reset hoặc đổi điều kiện.

## 2. Bố cục đề xuất

1. Đầu trang: mô tả ngắn phạm vi và một thanh lọc loại nhà/tháng, ngân sách/diện tích tùy chọn; hiển thị điều kiện đã áp dụng.
2. Chuyển cách xem: Bản đồ / Danh sách. Khi sửa form nhưng chưa áp dụng, thể hiện rõ dữ liệu vẫn thuộc điều kiện cũ.
3. Bản đồ: giữ định hướng UI B xanh than, bản đồ là trọng tâm; thanh lớp màu giá/m², tổng giá, số tin; legend có đơn vị. Desktop có khung kết quả/chi tiết vùng bên cạnh, mobile mở khung chi tiết gọn thay vì ép hai cột.
4. Danh sách: các vùng cùng kết quả với map, có chỉ số/cỡ mẫu, Định vị, So sánh, Ước tính ở đây. Nút Định vị mở cách xem Bản đồ và focus vùng, không chuyển sang một mục menu khác.
5. Một thanh chọn so sánh chung, tối đa ba vùng, mở cùng một bảng/modal so sánh.

Có thể mặc định mở Bản đồ để giữ định hướng thiết kế đã chọn; vị trí và chiều rộng panel cần kiểm thử trên viewport thật trước khi chốt. Không tạo một bản đồ nhỏ trùng cạnh một bản đồ lớn trong cùng cách xem.

## 3. Các chức năng phải giữ

| Từ tìm khu vực | Từ bản đồ |
|---|---|
| Lọc ngân sách/diện tích, áp dụng rõ ràng | Xem toàn địa bàn khi không giới hạn nhu cầu |
| Số tin phù hợp, danh sách các vùng | Polygon lịch sử, zoom/pan, focus vùng |
| Giá/diện tích và cỡ mẫu theo điều kiện | Lớp giá/m², tổng giá, số tin và legend |
| Chọn 2–3 vùng để đối chiếu | Chi tiết vùng, nền online/offline |
| Chuyển sang form ước tính có ngữ cảnh | Liên kết vùng/so sánh/ước tính nhất quán |

Đổi lớp màu chỉ đổi cách thể hiện, không đổi dataset hoặc âm thầm bỏ bộ lọc. Chọn vùng trên bản đồ là focus để xem chi tiết, không tự thay ngân sách hoặc loại hết các vùng khác khỏi danh sách.

Map giữ geometry toàn địa bàn; vùng có 0 tin theo điều kiện dùng màu/nhãn **Không có tin phù hợp**, không gán trung vị giá bằng 0. Ít mẫu cần cảnh báo; nếu vùng đã chọn so sánh không còn tin sau đổi filter thì giữ lựa chọn với trạng thái thiếu dữ liệu và cho bỏ, không hiển thị số cũ hoặc tự biến mất không giải thích.

## 4. Lý do chọn gộp và phạm vi thực hiện nếu được chốt

Hiện `MarketFinder` đã có cách xem map/list, còn `MapWorkspace` có lớp màu và panel chi tiết. Chúng chia sẻ một phần state nhưng gọi các luồng dữ liệu riêng. Hướng hợp lý là hợp nhất ý nghĩa bộ lọc/kết quả, tái sử dụng map/selection/comparison, rồi bỏ mục menu trùng; không chỉ ẩn menu và để nút gọi trang cũ bị mất.

Nếu triển khai: rà request/search/map theo cùng criteria → thống nhất state → một điểm điều hướng → tích hợp lớp màu/chi tiết vào cách xem map → sửa Định vị/liên kết quay lại/ước tính → nghiệm thu desktop/mobile. Model, ETL, train/test và phạm vi dữ liệu không đổi.

Chưa cần thêm so sánh hai tháng/biểu đồ mới ở vòng gộp đầu. Đó là nâng cấp sau, không phải điều kiện để giữ đầy đủ hai chức năng hiện có. Leaflet/polygon hiện tại đủ; Google Maps không giải quyết vấn đề hai luồng đang trùng nhau.

## 5. Tiêu chí nghiệm thu sau khi triển khai

- Cùng bộ lọc phải cho cùng số tin/tập vùng/thống kê ở Danh sách, Bản đồ, panel và so sánh.
- Chuyển cách xem không mất draft/applied criteria, focused region hoặc lựa chọn so sánh; request trả chậm không ghi đè kết quả mới.
- Kiểm tra tất cả lớp màu, đơn vị/legend, vùng 0/ít tin, trạng thái đang tải/lỗi/retry và nền offline.
- Nút Định vị, thêm/bỏ so sánh, giới hạn ba vùng, Ước tính ở đây và quay lại phải hoạt động.
- Mobile, bàn phím/focus và đóng panel/modal có đường thao tác rõ.
- Sau nghiệm thu mới cập nhật README, kịch bản demo, plan Word, ảnh và test selector theo một mục khám phá; chưa nói sản phẩm đã gộp khi code chưa đổi.

## 6. Còn cần thống nhất khi trao đổi

Tên menu đề xuất là Khám phá khu vực; mặc định map hay list và bố trí panel sẽ chốt trước thiết kế/triển khai. Tinh thần đề xuất: **một trang, một bộ điều kiện, hai cách xem và một luồng so sánh**, giữ khả năng xem toàn địa bàn lẫn tìm theo nhu cầu.

---

## Phương án hai trang riêng đã trao đổi trước đó — không còn là ưu tiên

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
