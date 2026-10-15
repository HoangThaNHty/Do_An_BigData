# Brief thiết kế UI/UX V3 sau audit — đề xuất để trao đổi

Ngày 14/10/2026. Chưa tạo bản thiết kế qua MCP, chưa sửa giao diện. Đọc cùng PLAN_CAI_THIEN_TRAI_NGHIEM_V3.md và KIEM_THU_UI_UX_2026_10_14.md. Brief này định hướng bản mẫu tiếp theo; chưa phải thiết kế được người dùng duyệt.

## Mục tiêu và người dùng

Ứng dụng phân tích dữ liệu tin đăng và tham khảo giá rao bán, đồng thời demo đồ án Big Data. Người tìm mua đối chiếu giá rao; người muốn bán tham khảo giá đăng; giảng viên xem dữ liệu, ETL và thực nghiệm. Không biến ứng dụng thành sàn tin đang còn bán, công cụ định giá giao dịch hiện tại hoặc xác minh pháp lý.

Giữ tinh thần “Nhà & Dữ liệu”, xanh đậm trên nền sáng. Bứt phá bằng bản đồ và so sánh có hành trình rõ, chữ đọc được và phản hồi ngay. Không thêm hiệu ứng/ảnh nhà giả gợi ý có GPS/tài sản thật. Hai phương án visual có thể thử: xanh đậm/nền sáng gần thương hiệu hiện tại; xanh than/nền sáng/điểm nhấn màu ấm. Chọn palette cuối sau đối chiếu contrast và bản mẫu.

## Cấu trúc và bố cục đề xuất

- Giữ 6 chức năng nhưng nhóm điều hướng thành “Khám phá nhà ở” (Tổng quan, Tìm khu vực, Bản đồ, Ước tính giá rao bán) và “Hiểu dữ liệu” (Độ chính xác dự đoán, Dữ liệu & phương pháp). Chưa chốt bỏ/gộp trang; tránh mất chức năng đang có.
- Desktop: bộ lọc nhu cầu → kết quả/bản đồ cạnh nhau; panel chọn/so sánh ở cạnh, có thể giữ trong viewport khi cuộn. Bản đồ và list chia sẻ chọn khu vực, điều kiện và loại hình.
- Mobile: tab Kết quả/Bản đồ, thanh “Đã chọn n khu vực/căn” dễ chạm; bấm mở khung so sánh. Khung đóng được, không che nút chính; quản lý focus và tránh gây tràn ngang.
- Kết quả dự đoán đặt cạnh form desktop, mobile đưa focus/scroll hợp lý đến tiêu đề kết quả khi người dùng submit thành công. Chỉ cuộn theo hành động chủ động, không khi background refresh.

## Thiết kế trạng thái bắt buộc

| Luồng | Trạng thái cần thể hiện |
|---|---|
| Tìm kiếm | Form nháp/chưa áp dụng, đang tải, kết quả, rỗng, ít mẫu, lỗi/retry; label chỉ rõ điều kiện kết quả |
| So sánh vùng | Chưa chọn, đã chọn 1, đủ 2 để xem, tới giới hạn, bỏ/thay; lựa chọn giữ khi chuyển Khám phá/Bản đồ |
| Nền bản đồ | Offline địa bàn, đang tải online, đã tải, lỗi toàn phần/một phần, thử lại; không bật trạng thái thành công khi lỗi |
| Ước tính | Chưa tính, thiếu/sai input, đang tính khóa submit, thành công, cảnh báo extrapolation, API bận/lỗi |
| So sánh căn | Chưa lưu, đã lưu 1 căn, căn thứ hai chưa được tính, kết quả thứ hai khác input, thay/xóa, quay lại trang vẫn giữ |
| Mô hình | Toàn test vs mẫu biểu đồ, điểm chưa/chọn, không có điểm trong mẫu sau lọc, ít mẫu, bảng kỹ thuật mở rộng |
| Tin mẫu | Ví dụ tổng hợp, đang kiểm tra, ý định bán/thuê/chưa rõ, kiểm tra giá/diện tích, quyết định ứng viên, dấu vết kỹ thuật mở rộng |

Không hiển thị B giống A ngay khi vừa lưu một căn. Hai đối tượng cùng thông số vẫn có thể được người dùng chủ động so sánh, nhưng cần hai hành động tính rõ ràng. Lưu/so sánh căn và so sánh khu vực là hai khái niệm riêng, cần nhãn phân biệt.

## Quy ước chữ, khoảng cách và thao tác

Các quy ước dưới đây là đề xuất nội bộ; kiểm tra bằng bản mẫu trước chốt:

- Body/form/help quan trọng 15–16 px, chú thích cần đọc ít nhất 13–14 px; tránh 9–10 px cho giới hạn và giải thích kết quả. WCAG không quy định toàn bộ text phải 16 px.
- Heading 24–32 px, kết quả giá 32–40 px, line-height body khoảng 1,5–1,7. Font có đầy đủ tiếng Việt; không tải font ngoài bắt buộc để demo offline.
- Spacing 8/16/24/32 px, form/CTA cao khoảng 44–48 px, target thao tác chính/mobile ít nhất 44×44 theo mục tiêu UX nội bộ. Kiểm tra thêm target/spacing WCAG AA.
- Text thông thường đạt contrast ≥4,5:1; nội dung nhạt vẫn phải đọc được. Màu chọn, lỗi, cảnh báo có nhãn/icon kèm, không chỉ dựa vào màu.
- Hiển thị tiền nhất quán “3,75 tỷ VND”, diện tích “70 m²”, số lượng “tin”; giá/m² phải có đơn vị và cơ sở diện tích phù hợp nhà/căn hộ.
- Nhãn cần hiểu ngay: “Chọn để so sánh khu vực”, “Xem so sánh”, “Lưu căn này để so sánh”, “Căn đã lưu”, “Ước tính căn tiếp theo”, “Phân tích tin mẫu”. Tránh dùng riêng A/B hoặc Spark làm lời giải thích mục đích.
- Có focus visible, label đúng, trạng thái đọc được qua live region khi thích hợp. Khung so sánh cần thao tác mở/đóng/ESC/khôi phục focus hợp lý; chart có cách đọc điểm bằng bàn phím hoặc bảng tương đương.

## Nội dung và tính trung thực

- Scope ngắn, nhìn thấy: TP.HCM trước hợp nhất; tin 06/2025–03/2026, có cả trước/sau sáp nhập. Bỏ tra địa danh khỏi luồng chính theo đề xuất đã lưu; chi tiết địa giới ở phương pháp.
- Giải thích model là giá rao nguồn, chưa phải giá hiện tại/giá giao dịch. Vai trò mua/bán chỉ đổi hướng dẫn/nhãn, không tạo giả hai mô hình.
- Giá nhập đối chiếu không là feature mô hình. Nhóm ±15% chỉ là thống kê thô cùng loại/khu vực/diện tích, chưa tương đương pháp lý/chất lượng/dự án.
- Mô hình: giải thích tiền/phần trăm trên test trước MAE/RMSE/R²; ví dụ giá nguồn X, dự đoán Y, chênh Z. Không dùng test để chọn lại mô hình.
- Tin mẫu: quyết định “Không dùng để huấn luyện giá bán vì là tin thuê” trước chi tiết rule; không gọi là phát hiện tin giả. Đạt ứng viên không chứng minh đã qua toàn bộ bước cohort.

## Sử dụng MCP ở giai đoạn sau

Khi người dùng yêu cầu tạo bản mẫu: chuẩn bị brief và nguồn tham chiếu hiện tại, tạo hai hướng cho cùng 3 màn hình quan trọng (Tìm khu vực/Bản đồ, Ước tính, So sánh), chọn một hướng để hoàn thiện. Dùng cơ chế brief/run của MCP; chọn OpenDesign Cloud hoặc Local Codex theo khả năng thực tế, không tự đoán runtime hoặc khởi chạy phát sinh chi phí trong lượt trao đổi.

Bản mẫu có thể dùng fixture đúng số liệu đã kiểm chứng, nhưng phải ghi rõ chưa nối API. Thay thiết kế vào Next.js hiện có ở giai đoạn triển khai, kiểm tra bằng API/model thật; không nhận bản mẫu landing page là sản phẩm hoàn tất.

## Điều còn cần chốt

- Giới hạn vùng so sánh dùng chung 2 hay 3; đề xuất 3 ở desktop và vẫn cho xem từng cặp trên mobile.
- Panel tại chỗ/drawer/modal; đề xuất panel cạnh desktop, khung mở từ thanh dưới trên mobile.
- Có thêm lựa chọn vai trò mua/bán hay chỉ hai câu hướng dẫn; đề xuất hướng dẫn rõ trước, chỉ thêm lựa chọn nếu làm form dễ hiểu hơn.
- Lưu so sánh qua điều hướng là yêu cầu UX đề xuất; qua refresh/đóng trình duyệt còn chưa chốt.
- Trạng thái mạng và bảng địa giới cần xử lý thật khi triển khai; hình đẹp không thay thế kiểm tra kết nối hoặc chất lượng dữ liệu.
