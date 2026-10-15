> **Bổ sung V5:** Kiểm Khám phá khu vực thay hai menu cũ; đổi map/list phải giữ criteria/lớp màu/vùng so sánh, thống kê khớp cùng API. Kiểm Kế hoạch mua nhà với vốn 500 triệu và tích lũy 20 triệu/tháng ở giá 2,8/3,5/4,2 tỷ (115/150/185 tháng, 0 lãi/0 phí/giá cố định), dự phòng vượt vốn, thu nhập 0, lịch vay 0%, tăng lãi, sửa chưa áp dụng, giữ draft qua điều hướng, chuyển đúng giá/dải từ kết quả. Phương pháp ở liên kết phụ, minh họa kỹ thuật mặc định đóng; test mobile. Xem PLAN_KE_HOACH_MUA_NHA_V1 và check_product_v5.cjs.

# Tester thủ công và hiểu các chức năng

Mục tiêu: kiểm tra thao tác có tác dụng, số liệu có cùng điều kiện, trạng thái có dễ hiểu và không hứa quá phạm vi dữ liệu. Đánh dấu Đạt/Lỗi/Chưa thử, ghi input và ảnh bằng TEST_RESULT_TEMPLATE.md. Người dùng/nhóm thực hiện thêm kiểm thử thật; không đánh dấu trước rằng các thiết bị của nhóm đều đạt.

## Trước khi thử

Chạy start-local; mở health qua http://localhost:3000/api/v1/health: ready, data_version core_v1, model_version v1, analysis_rows 133779. Mở browser thường, tải lại để có trạng thái sạch. Mặc định là căn hộ; kỳ 06/2025–03/2026. Dữ liệu là tin lịch sử, không danh sách nhà đang còn bán. Khi đối chiếu số mặc định, chọn Căn hộ và Toàn giai đoạn; nếu đã đổi bộ lọc ở test trước thì đặt lại trước khi đọc số. Một số giá rất thấp/cao có thể là tin chưa xác minh, không kết luận là lỗi UI chỉ từ giá lạ.

## 1. Tổng quan — hiểu bức tranh dữ liệu

| ID | Thao tác | Kết quả cần thấy |
|---|---|---|
| T01 | Mở mặc định |114.312 tin căn hộ; đơn vị tỷ VND, triệu VND/m², m² rõ. |
| T02 | Đổi nhà riêng, khu vực, tháng | Số liệu/bảng cập nhật theo bộ lọc, loading không gắn nhãn mới với dữ liệu cũ. |
| T03 | Xuất thống kê | Tải CSV tổng hợp khu vực; không xuất mô tả/liên hệ tin. |

Trung vị là giá ở giữa tập tin; không phải giá trung bình hoặc giá hợp lý cho mọi căn.

## 2. Tìm khu vực — tìm theo nhu cầu, không chỉ xem dashboard

| ID | Thao tác | Kết quả cần thấy |
|---|---|---|
| T04 | Chọn Căn hộ, Toàn giai đoạn; 3–4 tỷ, 60–80 m²; bấm Tìm khu vực phù hợp |14.110 tin, 19 khu vực; các thẻ/bản đồ cùng điều kiện. |
| T05 | Đổi ngân sách đến 4,5 nhưng chưa apply | Có nhắc chưa áp dụng; kết quả vẫn theo 3–4. Bấm apply rồi số liệu đổi. |
| T06 | Chọn 2 khu vực → Xem so sánh | Thanh chọn rõ tên/số; mở modal với số tin, giá, diện tích, đơn giá. |
| T07 | Thêm vùng thứ 3/thử vùng thứ 4/bỏ một vùng | Tối đa 3; vùng thứ 4 không thêm; bỏ rồi thêm vùng khác được. |
| T08 | Chuyển sang Bản đồ rồi quay lại | Các vùng và điều kiện đã áp dụng giữ trong phiên. |
| T09 |0–0,1tỷ; diện tích 9999–10000 m² | Không có tin; không hiện giá 0 giả. So sánh vùng đã chọn hiển thị 0/—. |
| T10 | Định vị khu vực / Tham khảo giá | Bản đồ focus vùng; form ước tính nhận vùng và diện tích tham khảo, không auto tính khi chưa submit. |

Số tin không phải số tài sản duy nhất/còn bán; cùng ngân sách vẫn có thể khác thành phần dự án/diện tích. Bảng không kết luận vùng nào đáng mua hơn.

## 3. Bản đồ giá — khám phá địa bàn

| ID | Thao tác | Kết quả cần thấy |
|---|---|---|
| T11 | Đổi lớp màu:giá/m², giá tổng, số tin; bấm vùng | Màu/chú giải đổi đúng đơn vị; panel vùng cập nhật. |
| T12 | Bật nền online khi có Internet | Đường phố tải và trạng thái thành công; ghi công OSM. |
| T13 | Offline/lỗi nền, rồi thử lại | Báo lỗi/dự phòng rõ; lớp 22địa bàn vẫn thao tác, thử lại khi Internet có. |
| T14 | Chọn/bỏ vùng từ panel → mở so sánh | Dùng chung thanh chọn với Tìm khu vực; không phát sinh bộ so sánh riêng. |

Màu theo phân vị giữa các khu vực, không thang giá cố định mọi bộ lọc. Ranh giới lịch sử, nền phố hiện nay; không có chấm GPS từng nhà.

## 4. Ước tính giá rao bán — tính và đối chiếu thật

| ID | Thao tác | Kết quả cần thấy |
|---|---|---|
| T15 | Căn hộ 70 m², Thủ Đức, 2 phòng ngủ, 2 WC; chạy | Giá, dải, cảnh báo từ model thật. Bỏ dự án/phường nếu không biết. |
| T16 | Nhập 4,2 tỷ ở giá cân nhắc | Hiện cao/thấp hơn model và vị trí trên thang giá; không làm đổi giá model khi đầu vào nhà giữ nguyên. |
| T17 | Lưu căn này để so sánh | Thẻ đã lưu hiện; chưa có căn thứ 2, nút so sánh hai căn chưa bật. |
| T18 | Sửa 90 m² rồi chạy; mở so sánh | Hai kết quả/input riêng; căn 70đã lưu không bị sửa thành 90. |
| T19 | Chuyển trang/quay lại; thay/xóa căn đã lưu | Snapshot/form giữ khi điều hướng; thay/xóa có tác dụng. Refresh sẽ reset theo phạm vi hiện tại. |
| T20 | Diện tích 0/âm hoặc bỏ trống | Form chặn input không hợp lệ; không sinh giá giả. Diện tích cực lớn hợp lệ có thể nhận cảnh báo ngoài vùng train. |

Người mua dùng đối chiếu giá đang rao; người bán dùng tham khảo giá đăng. Cùng một model, không phải hai nghiệp vụ đã được định giá chuyên gia. Dải bao phủ thực nghiệm test không bảo đảm từng căn. Nhóm tin tham khảo chỉ cùng loại/vùng/diện tích ±15%, chưa phải tài sản tương đương đã xác minh.

## 5. Độ chính xác dự đoán — model sai như thế nào

| ID | Thao tác | Kết quả cần thấy |
|---|---|---|
| T21 | Chọn nhà/căn hộ; bấm điểm hoặc chọn tin | Giá nguồn, dự đoán, chênh lệch hiện gần biểu đồ. |
| T22 | Lọc mẫu theo vùng/khoảng giá; đổi log | Điểm mẫu thay đổi; chỉ số tổng test phía trên không bị hiểu là chỉ số của mẫu lọc. |
| T23 | Mở 10sai lệch lớn/bảng kỹ thuật | Có dự đoán test thật, MAE/RMSE/R², validation và lựa chọn model. |

MAE: sai lệch tuyệt đối trung bình, không phải mọi căn sai đúng mức đó. RMSE nhạy với sai lệch lớn. Median APE: một nửa tin sai số phần trăm ít hơn mức này. Scatter chỉ 300 điểm mẫu cố định; không có điểm trong vùng lọc không nghĩa toàn test không có dữ liệu.

## 6. Dữ liệu & phương pháp — chứng minh chu trình Spark

| ID | Thao tác | Kết quả cần thấy |
|---|---|---|
| T24 | Bấm sáu bước pipeline | Số liệu/giải thích đọc manifest; kỹ thuật và file mở rộng. |
| T25 | Tin bán rõ → Phân tích tin mẫu | Đạt kiểm tra ban đầu, còn các bước địa bàn/trùng/split. |
| T26 | Tin cho thuê → phân tích | Không dùng để học giá bán; giá tháng khác giá tổng. |
| T27 | Giá trả trước → phân tích | Cần làm rõ/không đủ điều kiện ứng viên; không xem0,5 tỷ trả trước là tổng giá 3,5 tỷ. |

Đây là bộ quy tắc ETL thật chạy Spark, chưa phát hiện tin giả hoặc xác minh người bán/pháp lý. Tin mẫu tổng hợp không được lưu/thêm train.

## Kiểm tra chung và phối hợp tiếp

- Thử desktop và điện thoại/LAN nếu có. Mobile menu, form, dialog không tràn ngang; với 3 vùng chọn cặp để đối chiếu.
- Dùng Tab để tới input/nút, Enter/Space chọn vùng, Escape đóng modal và focus quay về nút mở.
- Nếu API dừng, ghi lỗi và thử lại sau restart; không mở hai Spark. Nền online lỗi độc lập với API/model.
- Tester trong VS Code webview riêng; QA Edge trước đây không thay cho bằng chứng của môi trường này.
- Gửi mình ID test, input, các bước, ảnh/console nếu lỗi; mình sẽ cùng bạn phân biệt lỗi chức năng với giới hạn dữ liệu rồi xử lý.
