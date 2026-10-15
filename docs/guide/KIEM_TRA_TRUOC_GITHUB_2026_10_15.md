# Kiểm tra trước GitHub — 15/10/2026

Trạng thái: đã kiểm tra file dự kiến đưa lên Git và tính toàn vẹn bundle. **Chưa commit/push**; người dùng muốn cả hai thành viên diễn tập đầy đủ trước.

## Đã kiểm tra

- `python -m scripts.audit_github`: PASS; danh sách gồm staged và untracked chưa bị ignore, không chỉ xem index cũ. Khoảng 16,8 MB; con số chính xác ở `.runtime/github_audit.json` sau mỗi lần chạy.
- Không có `.venv`, `.runtime`, `node_modules`, `.next`, cache, `.env` riêng, raw/CSV toàn nguồn, review có nội dung tin hoặc file vượt chính sách 45 MiB trong danh sách Git. CSV 3,27 GB và manifest export được `git check-ignore` xác nhận bị loại.
- Rà tên file Git: không có clipboard, pasted text, backup/copy, file tạm `.bak`/`.tmp`, lock Word hoặc JVM dump theo nhóm tên kiểm tra.
- `python -m scripts.check_repo`: PASS; 264 file model/serving/metadata trong demo manifest còn đúng SHA-256.
- API health 8000 và health qua web proxy 3000: HTTP 200, ready, core_v1/model v1/133.779 tin tại thời điểm kiểm tra.
- Các link Markdown tương đối trong README, hướng dẫn chạy, danh mục scripts, guide và plan: không có link file thiếu trong lượt rà. Tài liệu history không được dùng như hướng dẫn hiện hành.
- Môi trường hiện tại không có Dockerfile/Compose; triển khai là Windows local/LAN, không mô tả Docker như tính năng đã làm.

## File giữ có chủ đích

- `archive/`: bốn file README/crawler/audit lịch sử; không tham gia runtime, không phải mã chính để thành viên chạy.
- `docs/history/` và summary ETL cũ: truy vết các quyết định/thực nghiệm; giữ thay vì xóa bằng chứng nghiên cứu.
- Các thư mục `metadata`, `stages`, file `_SUCCESS`/`part-*` trong Spark pipeline: cấu trúc model do Spark ghi; không dọn như file rác.
- `.venv`, raw/ETL lớn, CSV và cache ở máy nghiên cứu vẫn cần cho chạy/nghiên cứu; “không đưa lên Git” khác “xóa khỏi máy”.

## Giới hạn kết luận

Scan token/private-key và file inclusion có phạm vi, không là kiểm toán bảo mật toàn diện. Không tìm thấy file thừa theo các nhóm đã rà, không khẳng định hiểu mọi byte trong mọi dependency local. Kiểm thử clone Windows từ mốc trước nằm ở REPO_GITHUB_NGHIEM_THU.md; lượt này không tạo lại một clone mới hoặc kiểm thử UI toàn bộ vì không sửa ứng dụng/model/dependency.

Repo chia sẻ là `real-estate-bigdata`, không push nguyên folder tài liệu `FolderDoAnBigData` hoặc nguyên ổ đĩa. Trước commit phải thêm cả các guide/plan/demo scripts mới, xem `git status`, chạy lại audit nếu danh sách file thay đổi. Gói ZIP local cũ không tự đồng bộ với các tài liệu mới; không gọi ZIP cũ là bản cuối hôm nay.

## Điều kiện còn lại trước push

Hai thành viên tự diễn tập, đổi vai, ghi kết quả vào mẫu kiểm thử. Đọc DEMO_QUY_TRINH_SPARK.md và PLAN_DEMO_NGHIEM_THU_V1.md. Bằng chứng kỹ thuật trên không thay thế việc nhóm đã diễn tập thành công.
