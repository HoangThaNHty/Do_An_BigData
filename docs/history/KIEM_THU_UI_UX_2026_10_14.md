# Kiểm thử trải nghiệm UI/UX — 14/10/2026

## Phạm vi và bằng chứng

Người dùng yêu cầu trải nghiệm/kiểm thử bản hiện tại, bổ sung hướng thiết kế vào plan rồi tiếp tục trao đổi. Đã khởi động bản production hiện có để audit; không sửa UI/API/model hoặc build lại, không chạy tạo thiết kế qua MCP, không đóng lại ZIP. Có thêm script QA và tài liệu.

- Desktop Edge headless 1440×1000; mobile viewport 390×844, cùng backend và model thật. Đây là mô phỏng viewport trên máy, không phải thiết bị điện thoại thật.
- Browser tích hợp không khởi tạo được vì môi trường chặn import node:process; dùng Playwright/Edge local theo phương án dự phòng. Chưa kiểm thử trực tiếp webview VS Code.
- Bằng chứng ở `artifacts/verification/ux-audit-2026-10-14/observations.json` và 14 ảnh. Script tái hiện: `scripts/audit_ux_v3.cjs`.
- Audit chính hoàn thành, không ghi nhận JavaScript pageerror. Điều này không chứng nhận mọi tương tác hoặc WCAG; chưa audit đầy đủ bàn phím, trình đọc màn hình, focus, zoom 200% hoặc mạng trên thiết bị khác.
- Các vị trí y bên dưới là tọa độ tương đối với viewport tại thời điểm thao tác, chịu ảnh hưởng scroll tự động của trình kiểm thử; chứng minh kết quả ngoài vùng nhìn trong tình huống đó, không phải tọa độ tuyệt đối cố định của trang.

## Phát hiện thực tế và mức ưu tiên

| ID | Mức | Đã quan sát | Ý nghĩa và hướng sửa đề xuất |
|---|---|---|---|
| UX01 | P0 | Chọn 1/3, chọn 3/3 và bỏ lựa chọn đều hoạt động. Bảng so sánh nằm ở y≈1813/1131 trong viewport cao 1000; không có status region | Chưa phải nút chết. Cần thanh chọn dễ thấy, phản hồi số lượng và nút mở kết quả tại chỗ |
| UX02 | P0 | Chọn khu vực rồi sang Tổng quan/quay lại Khám phá: 0 khu vực còn được chọn | State bị mất khi điều hướng; giữ lựa chọn và điều kiện ở cấp ứng dụng, thống nhất Khám phá/Bản đồ |
| UX03 | P0 | Bản đồ chọn 2 vùng tạo đúng 2 thẻ, nhưng bảng ở y≈1211, ngoài vùng nhìn | Đưa vùng đã chọn và đối chiếu vào panel cạnh bản đồ; mobile mở khung so sánh từ thanh dưới |
| UX04 | P0 | Lần online tự nhiên: 12 request tile lỗi ERR_NAME_NOT_RESOLVED, 0 tile tải được. Polygon vẫn có 22 vùng | Lỗi DNS tới tile.openstreetmap.org trong Edge audit; không kết luận nhà cung cấp ngừng hoạt động, lỗi API hoặc VS Code. Cần kiểm tra DNS/mạng riêng khi triển khai sửa |
| UX05 | P0 | Lỗi tile tự nhiên và mô phỏng mất Internet đều để checkbox online được chọn; không có nút Thử lại dành riêng cho nền | Tách đang tải/thành công/thất bại, fallback rõ, có retry. Không gọi nền đang hoạt động khi chỉ polygon hiển thị |
| UX06 | P0 | Bấm giữ A: nút vẫn tên cũ, không status region; khung A/B ở y≈1219. B hiển thị bản hiện tại giống A ngay lập tức | Lưu snapshot được, nhưng trạng thái “đã lưu” và “chưa có căn thứ hai” sai/khó hiểu. Hiện thẻ đã lưu ngay; B chờ đầu vào mới và dự đoán mới |
| UX07 | P0 | Sửa diện tích 70→90: kết quả hiện tại xóa, snapshot A giữ đúng; chạy B cho khoảng 4,59 tỷ so A 3,75 tỷ. Sang Tổng quan/quay lại: mất A, area trở về 70 | Phần tính A/B có hoạt động; phải giữ snapshot khi điều hướng và chỉ xóa theo hành động người dùng. Không tự diễn giải thay diện tích là tác động nhân quả |
| UX08 | P1 | Chọn điểm scatter hoạt động, ví dụ Quận 7 89 m², nguồn 7,5 tỷ, dự đoán 5,38 tỷ. Chi tiết ở y≈1071, ngoài vùng nhìn | Dùng popover/panel gần điểm đã chọn, có hỗ trợ bàn phím; phân biệt mẫu 300 điểm với toàn bộ test |
| UX09 | P1 | Tin thuê chạy Spark trả “Có ý định cho thuê”, chưa đạt ứng viên; kết quả hiện trong viewport ở lượt này | Logic làm việc đúng, nhưng mục đích/nhãn chưa nói rõ quyết định không dùng cho huấn luyện giá bán. Đặt câu hỏi dẫn đường và giải thích từng kiểm tra |
| UX10 | P1 | Các chú thích/nhãn đo được 9–12 px, contrast khoảng 2,48–3,27:1 | Chữ thường ở các mẫu đo không đạt ngưỡng 4,5:1. Tăng cỡ chữ/contrast, đừng dùng màu nhạt cho nội dung cần hiểu |
| UX11 | P1 | Sáu trang mobile không tràn ngang ở lượt audit; trang mô hình cao khoảng 3806 px. Nhiều nút cao 30,5–40 px; link phương pháp cao 13 px | Không tràn ngang chưa đủ dễ dùng. Thu gọn nội dung, mục mở rộng, nút chính đủ lớn; kiểm tra hit area/spacing theo WCAG thay vì chỉ nhìn kích thước chữ |
| UX12 | P1 | Đổi ngân sách form thành 1–2 tỷ nhưng chưa Apply vẫn hiển thị kết quả 3–4 tỷ; Apply trả 3685 tin phù hợp | Hành vi Apply hợp lệ nhưng chưa báo “điều kiện đã sửa, chưa áp dụng”. Phân biệt form nháp với điều kiện kết quả, tránh so sánh theo nhãn sai |

P0/P1 là mức ưu tiên sản phẩm của audit này, không phải mức độ bảo mật hoặc tuyên bố hỏng toàn hệ thống.

## Số đo tương phản đại diện

Tính từ foreground và background CSS solid của các phần tử thật ở trang Tổng quan, không tính trên ảnh chụp. Các lớp alpha/gradient khác chưa đánh giá đầy đủ.

| Phần tử | Cỡ chữ | Contrast đo được |
|---|---:|---:|
| Tiêu đề trang | 28 px | 11,48:1 |
| Mô tả trang | 12 px | 3,27:1 |
| Nhãn thống kê | 11 px | 3,17:1 |
| Chú thích thống kê | 9 px | 2,48:1 |
| Mô tả panel | 10 px | 2,77:1 |
| Giới hạn phạm vi ở footer | 9 px | 2,52:1 |
| Điều hướng đang chọn | 13 px | 5,65:1 |

Không suy ra toàn bộ website đạt/không đạt WCAG từ bảy mẫu này. Với các mẫu chữ thường có background solid đã đo, cần nâng tương phản.

## Giới hạn dữ liệu và nhận xét bổ sung

- Ngân sách 0–0,1 tỷ/diện tích 60–80 m² còn 4 tin nguồn, giá trung vị 39 triệu. Không dùng điều kiện này làm giả định “chắc chắn không có kết quả”. Chưa đọc nội dung bốn tin để xác minh; không kết luận giá đó có thật hoặc tự loại khỏi cohort. Đây là tín hiệu chất lượng nguồn cần xem xét riêng, không sửa pipeline/test để làm demo đẹp.
- Trạng thái rỗng được kiểm tra bằng điều kiện diện tích 9999–10000 m² và ngân sách thấp; thông báo gợi ý mở rộng điều kiện hoạt động.
- Nhóm tham khảo chỉ lọc loại hình/khu vực/diện tích ±15%. Nó có thể có trung vị khác xa model do trộn dự án, thời gian và đặc điểm khác; phải giải thích rằng đây không phải nhóm tài sản tương đương đã xác minh.
- Kỳ tin 06/2025–03/2026, địa bàn TP.HCM trước hợp nhất, chưa có GPS và crosswalk đầy đủ mới/cũ vẫn là phạm vi hiện hành.

## Chuẩn tham chiếu

- WCAG 2.2: chữ thường tối thiểu 4,5:1; chữ lớn đủ điều kiện tối thiểu 3:1. [W3C — Contrast Minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).
- Mục tiêu kích thước tối thiểu 24×24 CSS px có các ngoại lệ/điều kiện spacing; cần kiểm tra hit area thật. Đề xuất nội bộ cho thao tác chính/mobile là 44×44 px, không gán đó là yêu cầu AA 2.5.8. [W3C — Target Size Minimum](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html).
- Status sau lưu/chọn/tải cần truy cập được bằng công nghệ hỗ trợ mà không yêu cầu chuyển focus chỉ để đọc thông báo. Chưa có role=status không tự chứng minh mọi trạng thái đều vi phạm, nhưng luồng mới cần thiết kế live region phù hợp. [W3C — Status Messages](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html).
