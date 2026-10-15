# Đưa repo lên GitHub và phối hợp nhóm

Repo mã nguồn: [HoangThaNHty/Do_An_BigData](https://github.com/HoangThaNHty/Do_An_BigData), nhánh `main`. Folder local trên máy nghiên cứu là **real-estate-bigdata**, không phải folder chứa tài liệu môn học. Ngày 15/10/2026 người dùng đã yêu cầu kiểm tra và push lên repo này, thay cho yêu cầu tạm hoãn trước đó. Giữ commit khởi tạo/LICENSE hiện có, không force-push.

## Người sở hữu repo

Remote `origin` đã cấu hình tới repo nhóm. Trước mỗi lần chia sẻ thay đổi tiếp theo, trong terminal repo:

```powershell
python scripts/check_repo.py
python scripts/audit_github.py
git status --short
git add .
git diff --cached --stat
git diff --cached --check
git commit -m "Prepare runnable Big Data project and team guides"
git remote -v
git push -u origin main
```

Nếu Git yêu cầu danh tính, cấu hình user.name và user.email thật của bạn; không dùng tên/email của AI. Remote đã có, không add origin lần nữa. Nếu push báo nhánh remote đi trước thì fetch/review và tích hợp lịch sử, không dùng force để vượt lỗi.

Không force-add .venv/.runtime/node_modules/raw/processed/ZIP. Model v1 và serving được track có chủ đích để clone chạy. `.env.example` chứa cấu hình mẫu, không credentials; không push file .env thật. Dataset/model giữ ghi công và điều kiện phi thương mại, không gán MIT cho toàn bộ dữ liệu.

## Thành viên

Clone, mở folder và theo SETUP.md:

```powershell
git clone https://github.com/HoangThaNHty/Do_An_BigData.git
cd Do_An_BigData
.\scripts\setup.ps1
.\scripts\start-local.ps1
```

Máy cần Python 3.11, Node/npm, Git và Internet lần đầu theo SETUP.md. Clone có model/serving để chạy web, không có raw/CSV toàn nguồn hay review/cohort đầy đủ để nghiên cứu lại. Các thành viên đổi tên folder clone cũng được vì scripts lấy root theo vị trí repo.

Mỗi thay đổi dùng branch riêng:

```powershell
git switch main
git pull --ff-only
git switch -c feature/ten-chuc-nang
```

Làm xong: test phần bị ảnh hưởng, commit/push branch, tạo pull request và ghi rõ thay đổi + kiểm thử. Thống nhất người review trước merge. Không sửa artifact model chỉ để đổi kết quả trên web, không thay train/test hoặc rules frozen khi xử lý UI.

## Đầu việc gợi ý để nhóm tự phân công

- Frontend/UI: web/, tester luồng và mobile.
- API/ML: src/api, src/models, kiểm tra input và kết quả artifact.
- Dữ liệu/phương pháp: src/etl, docs/research, truy vết manifest và giới hạn.
- Demo/tài liệu: guide, ghi lỗi, rehearsal.

Đây là đề xuất phân công, không phải nhật ký đóng góp thực tế. Nhóm tự xác nhận công việc đã làm. Quyền truy cập repo do chủ tài khoản GitHub quản lý.
