# Nhà & Dữ liệu — đồ án Nhập môn Big Data

Phân tích tin đăng và ước tính **giá rao bán** nhà riêng/căn hộ tại TP.HCM. Nhóm 18, HUIT. Web dùng dữ liệu thật và mô hình Spark đã huấn luyện; chạy trên máy hoặc LAN.

## Clone và chạy trên Windows / VS Code

Repo nhóm: [HoangThaNHty/Do_An_BigData](https://github.com/HoangThaNHty/Do_An_BigData).

```powershell
git clone https://github.com/HoangThaNHty/Do_An_BigData.git
cd Do_An_BigData
```

Cần Git, **Python 3.11**, Node.js/npm (đã kiểm thử Node 26.5.0, npm 12.0.1), Internet để cài dependencies lần đầu. JDK 17 portable được setup tải và kiểm tra checksum. Clone repo bằng URL GitHub của nhóm, mở folder vừa clone trong VS Code, Terminal → New Terminal → PowerShell:

```powershell
./scripts/setup.ps1
./scripts/start-local.ps1
```

Mở **http://localhost:3000/** khi terminal báo Ready. Giữ terminal mở; Ctrl+C để dừng. Không copy phần `PS ...>` từ terminal vào lệnh. Nếu PowerShell chặn script, dùng `Set-ExecutionPolicy -Scope Process Bypass` cho terminal hiện tại rồi chạy lại.

Clone đã chứa model và dữ liệu phục vụ gọn, **không cần tải raw 1,6 GB hoặc huấn luyện lại để demo**. Chỉ chạy một tiến trình Spark: dừng web/API trước khi chạy ETL/huấn luyện. Thêm `-Lan` cho start-local để thiết bị cùng mạng truy cập frontend; API vẫn bind localhost.

[Hướng dẫn setup và sửa lỗi](docs/guide/SETUP.md) · [Tester theo từng chức năng](docs/guide/TESTER_CHECKLIST.md) · [Kịch bản thuyết trình demo](docs/guide/DEMO_THUYET_TRINH.md).

## Cấu trúc repo

```text
src/                  Python: API, ETL, mô hình, cấu hình; Java adapter Windows
web/                  Next.js/React: giao diện, gọi API qua proxy
scripts/              Setup, chạy, kiểm thử, tái hiện và đóng gói
archive/              Crawler/audit cũ, không tham gia runtime hiện hành
artifacts/models/v1/  Model thật, kết quả thực nghiệm và dự đoán test
artifacts/market/     Parquet serving + catalog gọn cho web
artifacts/geography/  22 nhóm địa bàn lịch sử
artifacts/etl/        Tổng kết quy trình, không phải toàn bộ ETL Parquet
artifacts/verification/ Bằng chứng kiểm thử hiện hành
data/                Manifest demo, metadata nguồn và địa giới có giấy phép
docs/guide/          Chạy máy, tester, demo và bàn giao cho model khác
docs/plans/          Phương án hiện hành và phạm vi
docs/research/       Phương pháp, chất lượng dữ liệu, kết quả mô hình
docs/history/        Các mốc cũ để truy vết; không phải hướng dẫn chạy hiện hành
```

[Danh mục tài liệu](docs/README.md) · [Danh mục scripts](scripts/README.md) · [Quy trình làm việc GitHub](docs/guide/GITHUB_TEAM.md).

## Sản phẩm và công nghệ

Sáu chức năng: Tổng quan; Tìm khu vực theo ngân sách/diện tích; Bản đồ giá; Ước tính giá rao bán và so sánh hai căn; Độ chính xác dự đoán; Dữ liệu & phương pháp với ví dụ Spark thật. Giao diện UI/UX V4 hướng B đã được nhóm chọn.

Chu trình: **Parquet nguồn → Spark SQL/ETL → chia train/validation/test theo thời gian → Spark ML → model đã lưu → FastAPI → Next.js**. Spark 3.5.7 chạy `local[4]`, driver 4 GB cho thực nghiệm trên một máy; demo API dùng 2 GB; không có MongoDB/HDFS hoặc cluster nhiều máy. Mỗi lần nhập trên web là suy luận, không huấn luyện lại.

Tập nghiên cứu 133.779 tin; train 78.048, validation 17.886, test 37.845. Đã thử 9 pipeline LR/RF/GBT + baseline, chọn LR riêng nhà/căn hộ theo validation trước test. MAE test nhà khoảng 2,950 tỷ, căn hộ 1,395 tỷ; đọc cùng RMSE/R² và sai lệch theo nhóm trong [kết quả mô hình](docs/research/KET_QUA_MO_HINH.md).

## Giới hạn và chia sẻ

Mã nguồn dự án theo LICENSE (MIT). Dataset và các thành phần bên thứ ba giữ giấy phép riêng trong THIRD_PARTY_NOTICES.md; MIT của mã nguồn không thay thế điều kiện CC BY-NC của dữ liệu hoặc cho phép sử dụng thương mại mọi artifact đi kèm.

Dữ liệu 06/2025–03/2026 có cả trước/sau sáp nhập; phạm vi TP.HCM trước hợp nhất, chưa bao phủ Bình Dương/Bà Rịa–Vũng Tàu cũ. Giá rao chưa xác minh giao dịch; không phải giá hiện tại, không có GPS từng căn. Nhãn review là tham chiếu AI, chưa phải ground truth chuyên gia. Không bảo đảm dải giá cho từng tài sản.

Model/serving nhỏ được giữ trong Git để clone chạy; raw, ETL Parquet nhiều GB, review có nội dung tin, `.venv`, `node_modules`, `.runtime`, cache, ZIP/Office local bị loại. Tái hiện ETL đầy đủ cần nguyên liệu nghiên cứu riêng; xem [phạm vi dữ liệu trong Git](data/README.md). Không xóa dữ liệu nghiên cứu gốc để làm repo nhỏ.

[Thông tin nguồn và giấy phép](THIRD_PARTY_NOTICES.md): dataset CC BY-NC 4.0; ghi công và giữ điều kiện phi thương mại. Không tự gán MIT cho dữ liệu hoặc toàn bộ model. Word/PPT hiện là snapshot cũ, để cập nhật sau; chưa publish Internet.

Demo mặc định dùng Spark driver 2 GB để giảm áp lực bộ nhớ. Thực nghiệm ETL/huấn luyện giữ 4 GB, không thay data/model. Nếu máy đủ tài nguyên có thể chạy start-local.ps1 -DriverMemory 4g; không chạy nhiều Spark. Khi health báo Spark đã dừng, dừng phiên cũ rồi khởi động lại.

[Xem nghiệm thu repo/clone Windows](docs/guide/REPO_GITHUB_NGHIEM_THU.md).
