> **Bổ sung chuẩn bị GitHub 14/10/2026:** API1.2.1, demo driver2GB; thực nghiệm vẫn4GB. Xem docs/guide/REPO_GITHUB_NGHIEM_THU.md về clone check, dọn cấu trúc và phụ thuộc nền online hiện không truy cập được. Các kết quả V4 ban đầu bên dưới giữ đúng mốc lịch sử.

> **Cập nhật 14/10/2026:** Người dùng đã chọn **B — xanh than, bản đồ làm trung tâm**. Hai bản mẫu đã tạo qua MCP bằng Local Codex; hướng B đã tích hợp vào Next.js/FastAPI thật. Kiểm thử chức năng, lỗi/retry và mobile đã đạt; kết quả và bằng chứng ở `NGHIEM_THU_UI_UX_V4.md`.

# Plan tổng hợp nâng cấp UI/UX V4

Ngày chốt hướng triển khai: 14/10/2026. Người dùng yêu cầu dùng MCP để tiếp tục theo plan và xem bản tổng hợp cuối. Đây là hướng thực hiện hiện hành; các quyết định visual cụ thể sẽ đối chiếu trên bản mẫu.

## 1. Mục tiêu và nền tảng

Sản phẩm hỗ trợ tìm khu vực theo nhu cầu, tham khảo giá rao bán, đối chiếu và so sánh; có phần giải thích dữ liệu/mô hình cho đồ án Big Data. Người mua dùng để đối chiếu giá đang rao; người bán tham khảo giá đăng. Không tuyên bố xác minh giao dịch/pháp lý hoặc định giá thị trường hiện tại.

Giữ core_v1/models/v1: 133.779 tin nghiên cứu, train 78.048, validation 17.886, test 37.845. Spark 3.5.7 local[4], Parquet, Spark ML, FastAPI và Next.js/React hiện hữu. Không thay ML/split/ETL frozen theo phản hồi UX, không thêm MongoDB/cluster/Internet deployment trong đợt này. Word/PPT để sau.

Phạm vi địa lý là TP.HCM trước hợp nhất, tin từ 06/2025–03/2026 có cả trước/sau sáp nhập. Chưa có giá cập nhật tháng 10/2026, tọa độ tài sản hoặc crosswalk đầy đủ địa danh mới/cũ.

## 2. Các quyết định thực hiện

1. Bỏ ô tra cứu địa danh khỏi luồng chính; giữ scope ngắn và chuyển giải thích địa giới vào phương pháp. API tra cứu có thể giữ nội bộ cho tương thích, chưa cần xóa dữ liệu/API.
2. So sánh khu vực có thanh chọn và nút “Xem so sánh”; phải thấy phản hồi ngay. Thống nhất state điều kiện/khu vực giữa Khám phá và Bản đồ, giữ khi điều hướng. Mục tiêu tối đa 3 khu vực; mobile cho đối chiếu từng cặp nếu cần. Chi tiết trình bày 2/3 cột kiểm tra trên bản mẫu.
3. Sửa trạng thái nền bản đồ online, có loading/success/failure/retry và fallback offline. Audit cho thấy DNS lỗi ở máy hiện tại; phải kiểm tra mạng thực trước kết luận nguồn tile hỏng. Không hứa có đường phố offline khi chưa có dữ liệu phù hợp.
4. Giữ tên rõ “Ước tính giá rao bán”, giải thích mục đích mua/bán. Ưu tiên hướng dẫn rõ; lựa chọn vai trò chỉ thêm nếu bản mẫu giúp hiểu hơn, không sinh hai model.
5. Đổi “Giữ làm phương án A” thành “Lưu căn này để so sánh”. Hiện thẻ đã lưu ngay, căn thứ hai ở trạng thái chưa tính; giữ snapshot qua điều hướng, có xóa/thay rõ. Lưu qua refresh/đóng trình duyệt chưa phải yêu cầu bắt buộc.
6. Trang “Độ chính xác dự đoán” giải thích sai lệch bằng tiền/phần trăm trước bảng kỹ thuật; chi tiết điểm gần biểu đồ, không chìm cuối trang.
7. Trang phương pháp giải thích vì sao tin được giữ/loại. Nút “Phân tích tin mẫu”; kết quả theo bước và quyết định rõ, Spark/rule codes trong phần mở rộng. Vẫn dùng bộ quy tắc thật khi tích hợp.
8. Chuẩn hóa typography, contrast, đơn vị, spacing, hit area và các trạng thái thao tác trên desktop/mobile.

## 3. Vai trò từng trang

| Trang | Mục đích | Thay đổi chính |
|---|---|---|
| Tổng quan | Hiểu nguồn, kỳ dữ liệu và quy mô | Giảm chữ nhỏ, scope dễ đọc, dẫn sang hành động tìm/ước tính |
| Tìm khu vực | Tìm theo ngân sách/diện tích | Form nháp vs điều kiện áp dụng; list/map chia sẻ state; thanh chọn/so sánh |
| Bản đồ giá | Khám phá không gian và chọn khu vực | Panel chi tiết/so sánh trong viewport, lớp màu rõ đơn vị, online có trạng thái thật |
| Ước tính giá rao bán | Tham khảo và đối chiếu giá | Kết quả gần form; giá nhập/giá model/dải trực quan; căn đã lưu và căn tiếp theo |
| Độ chính xác dự đoán | Hiểu model tốt/yếu ở đâu | Ví dụ thật dễ đọc, điểm có chi tiết gần, bảng/MAE/RMSE mở rộng |
| Dữ liệu & phương pháp | Chứng minh chu trình Big Data | Pipeline/manifest, ví dụ giữ/loại, giải thích mục đích trước thuật ngữ |

Giữ sáu chức năng; dùng điều hướng ngang trên desktop và menu mở trên mobile. Không loại chức năng chỉ để làm giao diện ngắn hơn.

## 4. Quy trình thiết kế và triển khai qua MCP

### Bước 1 — Brief và nguồn tham chiếu

Đã có audit/bằng chứng, brief và plan. MCP đã kết nối, brief Web / Connected flows / Polished đã xác nhận. Local Codex đã tạo hai phương án A/B thành công; mã nguồn bản mẫu được giữ ở artifacts/design/v4.

Hướng phù hợp trong thẻ: Web app (desktop-first responsive), Connected flows, Polished product UI. Giao diện sản phẩm phải tiếng Việt; thẻ công cụ có thể dùng tiếng Anh vì chưa hỗ trợ locale tiếng Việt. Chế độ thực hiện OpenDesign Cloud/Local Codex cần theo khả năng có thật và lựa chọn người dùng; không tự đoán runtime hoặc trạng thái đăng nhập.

### Bước 2 — Hai phương án có thể bấm thử

Tạo trong workspace thiết kế riêng qua MCP, không ghi đè web hiện tại:

- Phương án A: xanh đậm/nền sáng, phát triển nhận diện hiện tại, tăng độ rõ và tương phản.
- Phương án B: xanh than/nền sáng/điểm nhấn màu ấm, bố cục bản đồ và panel hành động nổi bật hơn.

Cả hai phải minh họa cùng luồng Tìm khu vực → Bản đồ → So sánh, Ước tính → Lưu căn → Tính căn tiếp theo → So sánh. Có trạng thái rỗng/lỗi/loading/ít mẫu/chưa có căn thứ hai. Không tạo hai landing page chỉ đổi màu.

Nếu bản mẫu dùng fixture, ghi rõ là bản mẫu chưa nối API; số liệu lấy từ nguồn đã kiểm chứng, không bịa live prediction. Dữ liệu thật và ảnh audit là nguồn tham chiếu; không gửi toàn bộ raw 1,6 GB hoặc thông tin liên hệ tin đăng.

### Bước 3 — Đối chiếu và chọn hướng

Xem preview hai phương án, đánh giá khả năng hiểu chức năng và phát hiện kết quả, state sau điều hướng, mobile, đơn vị/contrast. Người dùng đã chọn hướng B: xanh than, nền sáng, điểm nhấn ấm, ưu tiên bản đồ. Điểm cần xem lại: panel/drawer, so sánh 2/3 cột, vai trò mua/bán.

### Bước 4 — Tích hợp vào ứng dụng hiện tại

Lấy bundle mã nguồn thiết kế phù hợp, đưa component/tokens vào Next.js hiện hữu. Nối API/model thật, giữ nguồn dữ liệu/scope. State so sánh ở cấp ứng dụng; tách state form nháp, kết quả đã áp dụng và snapshot đã lưu. Không tuyên bố prototype đã thành sản phẩm trước tích hợp.

### Bước 5 — Hoàn thiện cả sáu trang

Áp dụng cùng quy ước chữ/màu/nút; cải thiện biểu đồ sai số/pipeline/minh họa tin. Sửa tải nền online sau xác định lỗi mạng và trạng thái; giữ chế độ offline cho demo.

### Bước 6 — Kiểm thử chức năng và trải nghiệm

Chạy checks thích hợp, đối chiếu API/Parquet/model. Thử desktop/mobile, bàn phím/focus, trạng thái rỗng/lỗi/retry, chuyển trang/giữ state, chọn/bỏ/thay so sánh, kết quả trong viewport. Kiểm tra online thành công lẫn lỗi; VS Code webview cần thử riêng, không lấy Edge headless làm bằng chứng thay thế.

### Bước 7 — Bàn giao

Cập nhật plan, hướng dẫn demo, screenshots/receipts và ZIP sau khi tích hợp/QA đạt. Word/PPT cập nhật ở giai đoạn người dùng yêu cầu. Tiếp tục local/LAN; chưa publish Internet.

## 5. Tiêu chí nghiệm thu

- Chọn một đối tượng phải thấy phản hồi số lượng/tên; chọn đủ hai thì có hành động xem so sánh rõ; bỏ/thay/đạt giới hạn được giải thích.
- Khám phá/Bản đồ dùng cùng điều kiện; đổi form chưa Apply có trạng thái “chưa áp dụng”; không gắn số liệu cũ với nhãn mới.
- Lưu căn phải hiện “Căn đã lưu”, không tạo B giống A ngay; đổi input không sửa snapshot; quay lại trang vẫn giữ; xóa chỉ do người dùng chủ động.
- Sau submit/click, kết quả nằm gần vị trí thao tác hoặc có mở panel/scroll/focus phù hợp, không yêu cầu tự tìm cuối trang.
- Online tải lỗi phải có failure/fallback/retry chính xác, polygon offline vẫn thao tác được; không bypass xác thực TLS hoặc bịa nền thành công.
- Chữ thường đạt contrast tối thiểu 4,5:1; body/form 15–16 px, chú thích quan trọng 13–14 px là mục tiêu thiết kế nội bộ. CTA/mobile nhắm 44–48 px; kiểm tra target/spacing WCAG với ngoại lệ đúng.
- Có labels, focus visible, status/live region thích hợp; các khung mở đóng hỗ trợ keyboard/focus; biểu đồ có cách đọc thông tin tương đương.
- Không tràn ngang mobile; thông tin chính không chìm dưới bảng dài. Các thuật ngữ thống kê/model có giải thích dễ hiểu và không hứa độ chính xác từng căn.
- Bộ kiểm tra dùng Spark/rules thật, ghi rõ ví dụ và trường cố định; không gọi là phát hiện tin giả hoặc tự đưa input vào train.

## 6. Trạng thái hiện hành và bàn giao

| Hạng mục | Trạng thái |
|---|---|
| Audit, brief, MCP và hai prototype | Hoàn thành; Local Codex tạo A/B; người dùng chọn B |
| Tích hợp hướng B vào web thật | Hoàn thành; 6 chức năng, dữ liệu/API thật |
| So sánh khu vực và căn nhà | Hoàn thành; state giữ qua điều hướng, modal, mobile đối chiếu cặp |
| Bản đồ nền | Đã thử tải PNG thật, lỗi có fallback/retry; nền cần Internet |
| Mô hình / ví dụ Spark | Chỉ cải thiện cách trình bày; dùng model và bộ quy tắc frozen thật |
| Kiểm thử | Build/TypeScript, 35 + 41 API calls, luồng desktop/mobile và 56 mẫu contrast đạt |
| Gói bàn giao | Xem GOI_BAN_GIAO_SHA256.json và artifacts/verification/handoff_checks.json của bản V4 |
| Word/PPT, Internet và thông tin nộp môn | Để sau theo yêu cầu người dùng |

Snapshot/điều kiện giữ khi chuyển trang trong phiên ứng dụng, chưa giữ qua refresh/đóng trình duyệt. VS Code webview và thiết bị LAN vật lý chưa được thử trực tiếp trong đợt V4; không suy diễn từ Edge headless. Contrast là kiểm tra 56 vị trí đại diện, không chứng nhận WCAG toàn bộ.

Nguồn: KIEM_THU_UI_UX_2026_10_14.md (audit trước sửa), BRIEF_THIET_KE_UI_UX_V3.md, PLAN_CAI_THIEN_TRAI_NGHIEM_V3.md. Đọc NGHIEM_THU_UI_UX_V4.md, KICH_BAN_DEMO_UI_UX_V4.md và BAN_GIAO_CHO_MODEL_KHAC.md cho trạng thái thực tế. Các plan cũ giữ để truy vết, không dùng làm trạng thái hiện hành.
