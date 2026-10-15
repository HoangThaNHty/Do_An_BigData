> **Bổ sung chuẩn bị GitHub 14/10/2026:** API1.2.1, demo driver2GB; thực nghiệm vẫn4GB. Xem docs/guide/REPO_GITHUB_NGHIEM_THU.md về clone check, dọn cấu trúc và phụ thuộc nền online hiện không truy cập được. Các kết quả V4 ban đầu bên dưới giữ đúng mốc lịch sử.

# Nghiệm thu UI/UX V4 — 14/10/2026

Người dùng đã chọn **B — xanh than, bản đồ làm trung tâm** và yêu cầu tiếp tục theo plan đến hoàn thành. Đợt này hoàn thiện UI/UX, chức năng và gói chạy local/LAN; Word/PPT và publish Internet vẫn để sau.

## Kết quả tích hợp

- MCP đã xác nhận brief và tạo hai prototype A/B thành công bằng Local Codex. Bundle, DESIGN.md, fixture và ảnh được lưu ở artifacts/design/v4; người dùng chọn B. Prototype độc lập vẫn ghi chưa nối API; app chính là Next.js/React + FastAPI 1.2.0 + Spark thật.
- Áp dụng navy/petrol, nền sáng, điểm nhấn hổ phách; điều hướng ngang desktop/menu mobile, chữ lớn hơn và đơn vị thống nhất.
- Bỏ tra địa danh khỏi luồng chính; giữ thông báo phạm vi lịch sử. API tra cứu không bị xóa; chưa có crosswalk mới/cũ đầy đủ.
- Tìm khu vực có ngân sách/diện tích nháp và đã áp dụng, bản đồ/danh sách, định vị vùng và mở ước tính. Tối đa ba vùng; thanh chọn cố định và modal so sánh. State dùng chung với Bản đồ, không mất khi chuyển trang; mobile đối chiếu từng cặp.
- Bản đồ nền tải PNG OSM qua endpoint cùng ứng dụng /api/v1/map/tiles/z/x/y.png, cache tạm/conditional headers, có loading/success/error/retry. Khi lỗi, checkbox không giả báo bật nền và polygon offline vẫn thao tác. Nền đường phố hiện nay không biến polygon thành địa giới 2026.
- Ước tính giải thích cả mục đích mua/bán, cùng mô hình giá rao. Thang giá đặt giá mô hình, dải và giá bạn nhập cạnh nhau. Giá nhập không vào model. Căn đã lưu hiện ngay, không tự tạo B giống A; phải chạy căn tiếp theo để mở đối chiếu. Snapshot giữ qua điều hướng; có thay/xóa.
- Trang độ chính xác dùng mẫu test thật: biểu đồ và panel chi tiết gần nhau, chọn tin bằng bàn phím, bảng/error cases mở rộng. R² thiếu hiển thị “—”, không giả số 0.
- Trang phương pháp dùng manifest thật và phân tích tin bằng bộ quy tắc Spark thật; bốn quyết định giải thích giao dịch, giá tổng, diện tích, phạm vi. Thuật ngữ/rule codes nằm trong phần mở rộng; không lưu nội dung vào train.

## Kiểm thử và bằng chứng

| Kiểm tra | Kết quả / bằng chứng |
|---|---|
| Next production build / TypeScript | Đạt; build cuối với workspace-v4.css |
| API gốc | 35 calls đạt, số lượng/trung vị khớp Parquet, invalid input và model đã lưu |
| API chức năng / quy tắc frozen | 41 calls đạt, gồm search/reference/pipeline/error examples/check-listing |
| Sáu trang, filter, CSV, click polygon, model | scripts/check_web.cjs đạt, artifacts/verification/web/checks.json |
| Luồng V4 | scripts/check_ui_ux_v4.cjs đạt, artifacts/verification/ui-ux-v4/checks.json |
| Nền bản đồ | PNG thật tải được; cố ý ngắt request → fallback và thử lại thành công |
| So sánh | Max3, bỏ/chọn, điều kiện mới giữ lựa chọn, modal trong viewport, ESC trả focus; lưu căn 70 → sửa 90 → kết quả khác, giữ snapshot khi điều hướng |
| Mobile | 390×844: cả sáu trang không tràn ngang; modal ba vùng đối chiếu cặp |
| Rỗng / lỗi | Không tin → comparison 0/—; search 503 → retry; predict 429 → thử lại → model thật |
| Chữ | 56 mẫu DOM đại diện trên sáu trang đạt ≥4,5:1; thấp nhất 5.58:1 |
| Gói nguồn | Xem fingerprint deliverables/GOI_BAN_GIAO_SHA256.json và kiểm tra giải nén artifacts/verification/handoff_checks.json |

Ảnh thực tế nằm ở artifacts/verification/ui-ux-v4 (desktop/mobile). Browser tích hợp không khởi tạo được vì lỗi import node:process; dùng Playwright Microsoft Edge thực tế làm fallback, không coi screenshot prototype hoặc DOM QA của công cụ là nghiệm thu app.

Đã phát hiện/sửa tràn ngang bảng độ chính xác trên mobile. Kiểm thử API chức năng có một lượt bị ngắt khi frontend được khởi động lại để build; đã chạy lại đủ 41 và đạt. Nền online trước đây lỗi DNS trực tiếp từ trình duyệt; tuyến qua API đã tải được trên máy này, không bảo đảm Internet luôn sẵn sàng.

## Giới hạn và những việc để sau

- Không phải chứng nhận WCAG toàn bộ hoặc nghiên cứu người dùng: contrast kiểm tra vị trí đại diện; kiểm tra keyboard/modal có phạm vi nêu trên. VS Code webview và thiết bị LAN vật lý chưa được thử trực tiếp trong đợt V4.
- Snapshot giữ trong phiên ứng dụng, chưa lưu qua refresh/đóng trình duyệt. Không đưa thông tin liên hệ cá nhân vào demo.
- Giữ core_v1/models/v1, train/validation/test và rules frozen; đợt này không huấn luyện lại. Có thể tái hiện huấn luyện riêng sau khi dừng API; không chạy hai Spark JVM cùng lúc trên máy này.
- 133.779 tin, dữ liệu 06/2025–03/2026, địa bàn TP.HCM trước hợp nhất, có cả trước/sau sáp nhập. Không có GPS từng căn, giá hiện tại hoặc giá giao dịch xác minh.
- Word/PPT chưa cập nhật. Hồ sơ nộp cần xác nhận tên đề tài, giảng viên/lớp và đóng góp thật; không suy đoán.

Đọc PLAN_TONG_HOP_UI_UX_V4.md cho hướng tổng hợp, KICH_BAN_DEMO_UI_UX_V4.md để demo, HUONG_DAN_CHAY.md để chạy máy/LAN.
