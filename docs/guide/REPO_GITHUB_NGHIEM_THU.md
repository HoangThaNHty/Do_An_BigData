# Chuẩn bị repo GitHub và nghiệm thu clone Windows — 14/10/2026

## Cấu trúc và dọn dẹp

Repo mã nguồn: real-estate-bigdata. Đã tách docs/guide, plans, research, history; code/ETL/API/models/web giữ đường dẫn runtime. Crawler cũ và helper audit/prototype sang archive; bỏ writer finalize_docs.py cũ (ghi đè tài liệu hiện hành) và wrapper QA trùng. Bản sao trước loại được giữ local trong .runtime, không đưa lên Git.

Đã xóa 14 đường dẫn đầu ra kiểm thử cũ và ZIP JDK dư, giải phóng khoảng 313 MiB; giữ JDK đã cài, môi trường đang dùng, model/serving và raw/processed nghiên cứu gốc. Bản clone/env thử được dọn sau khi lấy biên nhận. Folder tài liệu môn học cũng đã gom lại; file yêu cầu môn/đăng ký gốc giữ trong tai_lieu_mon_hoc, Markdown cũ giữ ở snapshots-before-reorganization.

Gitignore loại raw/ETL nhiều GB, review có nội dung tin, môi trường, cache, builds, secrets/env thật, crash dumps và ZIP/Office local. Model, Parquet serving, metadata nguồn/core, địa giới/giấy phép và demo_manifest được giữ trong Git. Manifest xác minh 264 file demo; Git attributes giữ nguyên byte artifact qua clone Windows. Repo chỉ khoảng 17 MB trước nén, file lớn nhất khoảng 5,3 MB; số cuối xem audit JSON.

Git main đã khởi tạo và file đã stage để xem xét; chưa tạo commit thay danh tính thành viên, chưa tạo remote hoặc push. Người dùng tự commit/push bằng tài khoản thật theo GITHUB_TEAM.md.

## Kiểm tra actual clone

Tạo origin Git local dùng riêng kiểm thử từ index snapshot; clone sang thư mục mới không có .venv/node_modules/raw/cache của project. Chạy setup bằng Windows PowerShell 5.1: cài dependencies Python mới, npm ci mới, build production/TypeScript và kiểm tra 264 file. JDK 17 đã kiểm chứng trên máy được tái dùng bằng -JavaHome; không coi đây là kiểm thử máy vật lý khác hoặc tải JDK mới lần này.

Khởi động web/API từ clone ở port 3001, đã đạt:

- 35 API calls đối chiếu Parquet/model  + 41 API chức năng/rules frozen.
- Sáu trang, filter, CSV, polygon, dự đoán thật; luồng so sánh khu vực/căn, giữ snapshot, model diagnostics, ba ví dụ Spark; mobile 390×844.
- Rỗng 0/—, search 503/retry, predict 429/recovery; 56 vị trí contrast đại diện đạt 4,5:1.
- Sáu vòng lặp dự đoán fixture +phân tích tin bằng Spark, engine còn ready và giá đúng 3.728.469.791,73 VND.
- Bốn regression checks cho readiness: engine live, stopped, chưa khởi tạo và gateway đã mất.

## Vấn đề phát hiện khi thử và cách xử lý

**Bộ nhớ:** JVM 4 GB báo native memory allocation failure trên máy bận nhiều ứng dụng. Web và CLI suy luận mặc định 2 GB; ETL/huấn luyện vẫn 4 GB như thực nghiệm. Không đổi model, data, split hoặc bộ quy tắc. Có thể chọn -DriverMemory 4g cho start-local trên máy đủ tài nguyên. Health/API Spark trả 503 hướng dẫn restart khi engine mất kết nối, thay vì ready giả/500 khó hiểu. Browser QA được đóng khi test lỗi để tránh để tiến trình kiểm thử thừa.

**Nền Internet:** nguồn OSM trả kết nối bị từ chối trong lượt clone; không báo đã đạt tải online ở lượt này. Đã kiểm thử fallback/retry, 22 polygon vẫn dùng được. Bộ UI QA có cờ QA_SKIP_LIVE_TILES=1 và ghi rõ bỏ phần live, không giả kết quả thành công. Tải nền thật đã có kiểm tra ở mốc V4 trước; khả năng mạng không được suy diễn là luôn sẵn sàng.

## Bằng chứng và phạm vi

artifacts/verification/github-clone/clone_checks.json cùng các API/UI/contrast/soak receipts. Audit file Git: scripts/audit_github.py (token/private-key scan có phạm vi, không chứng nhận bảo mật toàn bộ). Gói ZIP/checksum local được làm lại sau dọn; runtime artifacts được kiểm tra từ bản giải nén.

Chỉ kiểm thử clone trên máy Windows hiện tại, không khẳng định mọi laptop/LAN/VS Code webview đã đạt. Nhóm tự thử các thiết bị của mình bằng TESTER_CHECKLIST.md. Dữ liệu/model lịch sử, không giá giao dịch/giá hiện tại/GPS từng căn. Word/PPT và publish Internet tiếp tục để sau.

Sau sửa runtime, bản clone đã fetch/reset từ origin Git local cuối, khởi động lại bằng launcher hiện hành và kiểm tra health, artifact, model fixture và quy tắc thuê; đều đạt. Bằng chứng được giữ sau khi dọn thư mục clone thử.
