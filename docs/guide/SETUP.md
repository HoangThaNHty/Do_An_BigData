> **QA V5:** check_product_v5.cjs là suite hiện hành cho khám phá hợp nhất, kế hoạch tài chính và phương pháp phụ. Các entry check_web/check_ui_ux_v4 chuyển tiếp tới suite này; không cần chạy lặp. Tải tile Internet thật không thuộc suite V5, chỉ có kiểm tra fallback.

# Clone, cài và chạy trên Windows / VS Code

## Chuẩn bị

Git, Python **3.11**, Node.js/npm. Môi trường đã kiểm thử: Python 3.11.15, Node 26.5.0, npm 12.0.1, JDK 17, Spark 3.5.7; thực nghiệm dùng driver 4 GB; API demo mặc định 2 GB, vẫn cần RAM cho Windows/Node. Không cần MongoDB, Docker, tài khoản map hoặc JDK hệ thống. Internet cần cho lần cài đầu; bản đồ polygon và model chạy được offline sau cài.

## Lần đầu từ clone

Clone bằng URL GitHub thật của nhóm, mở folder repo trong VS Code (File → Open Folder), Terminal → New Terminal → PowerShell. Chạy từng lệnh, không copy phần PS ...>:

```powershell
./scripts/setup.ps1
./scripts/start-local.ps1
```

Nếu lệnh python đang trỏ phiên bản khác, chọn Python3.11 qua launcher:

```powershell
py -3.11 -m venv .venv
./scripts/setup.ps1 -Python ./.venv/Scripts/python.exe
```

Setup cài dependencies theo lock, tải JDK portable với checksum, build adapter Java Windows, kiểm tra264 file demo và npm ci/build. Không huấn luyện hoặc tải raw. Có JDK 17 sẵn thì dùng `./scripts/setup.ps1 -JavaHome 'C:\duong-dan-jdk-17'`; thay đường dẫn bằng vị trí thật. Không sửa JAVA_HOME/PATH toàn máy.

Nếu Windows chặn thực thi ps1, chạy `Set-ExecutionPolicy -Scope Process Bypass` trong terminal đó rồi chạy lại. Không cần đổi policy toàn máy. Setup có thể chạy lại nếu cài bị ngắt.

## Những lần sau

```powershell
./scripts/start-local.ps1
```

Chờ dòng Loading saved Spark models, tiếp đến API sẵn sàng và frontend Ready. Mở http://localhost:3000/. Giữ terminal mở; Ctrl+C dừng. Lần chạy này nạp model rồi suy luận, không train lại.

LAN: `./scripts/start-local.ps1 -Lan`; máy cùng mạng mở http://IP-LAN-CUA-MAY:3000/. Nếu firewall chặn thì cho phép frontend 3000 trên mạng Private theo quyền quản trị máy. API 8000 chỉ ở localhost và được frontend proxy. Chưa deploy Internet.

## Chạy riêng để xem log

Terminal 1: `./scripts/run.ps1 src.api.serve`. Terminal 2: `cd web`, `npm run start`. Không dùng cùng lúc với start-local vì trùng API/port. Sau sửa frontend: dừng frontend, `cd web`, `npm run build`, chạy lại. Sau pull: chạy lại setup nếu lock hoặc code/build đổi; không push .next.

## Lỗi thường gặp

| Triệu chứng | Kiểm tra / cách xử lý |
|---|---|
| Port 3000/8000 occupied | Dừng phiên đang chạy của repo bằng Ctrl+C; không khởi động Spark thứ hai. Có thể đổi frontend `-Port 3001`, API vẫn 8000. |
| Web mở nhưng API lỗi | Mở http://localhost:3000/api/v1/health, phải status ready/analysis_rows 133779. Kiểm tra terminal API và http://127.0.0.1:8000/api/v1/health. Giữ cả hai tiến trình hoạt động. |
| Thiếu model/serving | `python scripts/check_repo.py`; kiểm tra clone đủ các file artifacts, không dùng ZIP chỉ chứa src/web. |
| Java adapter missing | Chạy setup hoặc build_local_fs.ps1 sau khi có .venv/JDK. |
| Python không đúng 3.11 | Dùng py -3.11 tạo .venv, rồi setup với -Python như trên. |
| WARN winutils/native Hadoop | Trên Windows đã dùng adapter riêng; WARN có thể xuất hiện trong phiên thành công. Xem API status/exception/tiến trình, không coi mọi WARN là lỗi. |
| Nền online không tải | Dùng lớp địa bàn offline hoặc bấm thử lại; model/thống kê không cần OSM. |
| File Git/model changed | Không sửa model JSON/metadata thủ công. Khôi phục artifact từ Git và chạy check_repo. |

## Kiểm tra tự động (tùy chọn)

Cả web/API cần đang chạy; chạy lần lượt để Spark không bị gọi chồng nhiều test:

```powershell
.venv/Scripts/python.exe scripts/check_api.py
.venv/Scripts/python.exe scripts/check_product_features.py
npm install --prefix .runtime/qa playwright
node scripts/check_home_plan.mjs
node scripts/check_product_v5.cjs
node scripts/check_ui_ux_v4_errors.cjs
```

Node QA dùng Microsoft Edge đã cài, Playwright chỉ là công cụ kiểm thử; không cần khi chạy sản phẩm. Xem [tester thủ công](TESTER_CHECKLIST.md) để nhóm trực tiếp kiểm tra và ghi lỗi. Windows là đường chạy đã xác minh; macOS/Linux chưa có setup script đã nghiệm thu.

## Chạy từ menu VS Code

Mở đúng folder repo, chọn Terminal → Run Task. Có các task **Project: setup lan dau**, **Project: chay web local**, **Project: chay web LAN** và **Project: kiem tra model va du lieu**. Chạy setup lần đầu, sau đó chọn một task chạy web; không chạy local/LAN đồng thời.

Bộ UI QA mặc định kiểm tra nền OSM thật và cần nguồn bên ngoài truy cập được. Nếu nguồn đang lỗi, có thể dùng `$env:QA_SKIP_LIVE_TILES='1'` trước check_ui_ux_v4.cjs: kiểm thử fallback/retry và các chức năng còn lại, biên nhận ghi rõ live tiles bị bỏ qua; không tính là đã nghiệm thu tải nền online. Sau thử xóa biến bằng `Remove-Item Env:QA_SKIP_LIVE_TILES`. Chức năng demo mặc định vẫn là polygon offline.

Demo mặc định dùng Spark driver 2 GB để giảm áp lực bộ nhớ. Thực nghiệm ETL/huấn luyện giữ 4 GB, không thay data/model. Nếu máy đủ tài nguyên có thể chạy start-local.ps1 -DriverMemory 4g; không chạy nhiều Spark. Khi health báo Spark đã dừng, dừng phiên cũ rồi khởi động lại.
