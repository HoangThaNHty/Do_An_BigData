# Nghiệm thu sản phẩm V5 — 15/10/2026

## Thay đổi

- Gộp Tìm khu vực và Bản đồ giá thành **Khám phá khu vực**. Một bộ lọc, mặc định toàn địa bàn, hai cách xem; giữ lớp màu, vùng focus, so sánh tối đa ba vùng, định vị và chuyển sang ước tính. Bỏ component trang map riêng không còn dùng.
- Thêm **Kế hoạch mua nhà**: công thức tích lũy, vốn tối thiểu, mốc có vốn và dòng tiền tháng đầu không âm, vay trả đều/gốc đều, bảng nợ, kiểm tra tăng lãi, ba mức giá và biểu đồ. Có nút chuyển snapshot giá/dải từ kết quả Spark.
- Dữ liệu & phương pháp là liên kết phụ, không mất nội dung nguồn/provenance/Spark. Form tin mẫu nằm dưới details mặc định đóng. Liên kết vẫn truy cập được trên mobile.
- Không thay backend, rules, raw/core, train/validation/test, model hoặc dependency lock. Không thêm Docker/HDFS hay model dự báo tài chính.

## Kết quả kiểm thử

| Kiểm tra | Kết quả |
|---|---|
| TypeScript và production build | PASS |
| `node scripts/check_home_plan.mjs` | PASS, 63 oracle/invariant; lãi 0, dòng tiền âm, đủ vốn ngay, giá tăng, compound, annuity/gốc đều, bảo toàn gốc/dư nợ cuối, validation |
| `node scripts/check_product_v5.cjs` | PASS, đã chạy lại trên bản build cuối sau chỉnh thứ tự menu/lời nhãn |
| Lọc/map/list/so sánh | Đối chiếu count/median với API dưới cùng điều kiện; 22 polygon; lớp màu/ba lựa chọn giữ qua tab; 0 tin và bỏ giới hạn |
| Model → kế hoạch | Suy luận Spark thật 70/90 m², snapshot A không đổi; giá/dải B truyền đúng tới kế hoạch, sai số đối chiếu dưới 1 VND |
| Form tài chính | 500 triệu khả dụng, 20 triệu/tháng, 2,8/3,5/4,2 tỷ → 115/150/185 tháng; chặn dự phòng vượt vốn; thu nhập 0; giữ draft/kết quả qua điều hướng |
| Bộ quy tắc | Ba ví dụ bán/thuê/trả trước chạy Spark thật; bốn quyết định và lý do |
| Mobile | Sáu trang gồm năm mục chính và phương pháp phụ ở 390×844, không tràn ngang; đã sửa liên kết phụ bị CSS cũ ẩn |
| Lỗi/khả năng đọc | PASS, 58 mẫu tương phản chữ ≥4,5:1; tìm kiếm 503/retry, 0 tin, dự đoán 429 và phục hồi thật |
| API regression | PASS 35 + 41 calls, Parquet count/median, map, model, invalid input và frozen methodology |

## Bằng chứng và giới hạn

Biên nhận và bộ screenshot đầy đủ nằm ở `.runtime/product-v5-qa/`, được Git ignore; bản JSON và ba ảnh tiêu biểu được chọn chia sẻ tại `artifacts/verification/product-v5/`. Biên nhận tính toán/API và manifest là các kiểm tra độc lập; kiểm UI mới dùng Edge/Playwright local vì kết nối Browser tích hợp không khởi tạo được trong phiên này. Không ghi đã điều khiển MCP browser khi thực tế dùng fallback.

Test nền online chủ động mô phỏng lỗi để xác nhận polygon/offline còn dùng được; **không chứng nhận tile Internet tải thành công ở lượt V5**. Tương phản chỉ là mẫu đại diện, chưa là chứng nhận WCAG đầy đủ hoặc user study. Không coi kiểm thử trên máy hiện tại là mọi laptop Windows đã đạt.

Các tính toán tài chính dùng giả định tự nhập, không quy đổi giá lịch sử thành giá hiện tại, không dự báo lãi/thu nhập/giá nhà, không phê duyệt tín dụng. Kiểm dòng tiền tại tháng đầu mua và mức lãi cố định hoặc stress toàn kỳ, không giả lịch thả nổi ngân hàng. Phí mua để 0 là chưa tính, không phải giao dịch miễn phí.

## Bàn giao

README, hướng dẫn chạy, checklist, plan Word, plan vai trò map và kịch bản thuyết trình đã bổ sung V5. Office chưa được tạo lại. Người dùng đã yêu cầu triển khai và cập nhật GitHub; chỉ đưa source/docs/tests cần thiết, không đưa raw/CSV/review/environment hoặc screenshot local tràn lan.

Entry kiểm thử cũ `check_web.cjs` và `check_ui_ux_v4.cjs` chuyển tiếp tới V5 để không còn gọi menu đã bỏ; không cần chạy lặp cùng suite. `check_ui_ux_v4_errors.cjs` giữ tên tương thích nhưng selector/nội dung đã cập nhật.
