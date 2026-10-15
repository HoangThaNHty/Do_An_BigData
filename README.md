# Nhà & Dữ liệu — đồ án Nhập môn Big Data

Phân tích tin đăng và ước tính **giá rao bán** nhà riêng/căn hộ tại TP.HCM. Nhóm 18, HUIT. Web sử dụng dữ liệu thật, mô hình Spark đã huấn luyện và bộ quy tắc kiểm tra tin.

Repo nhóm: [HoangThaNHty/Do_An_BigData](https://github.com/HoangThaNHty/Do_An_BigData).

> **Đường chạy:** clone và setup ở mục 2. Chỉ mở sản phẩm thì chạy **Terminal 1 → Terminal 2**, hoặc launcher gộp ở mục 6. Demo toàn chu trình thì cần đủ dữ liệu nghiên cứu, chạy **Terminal 0 → kết thúc → Terminal 1 → Terminal 2**. Không cần bật một dịch vụ Spark riêng trước API.

## 1. Luồng dữ liệu và công nghệ

### Chuẩn bị dữ liệu và huấn luyện

```text
Parquet nguồn
 → Spark SQL/DataFrame: chọn phạm vi, chuẩn hóa và kiểm tra
 → ETL: ứng viên phù hợp / tin thuê / dữ liệu cách ly
 → Review tham chiếu, loại ID đã đọc, proxy đăng lại và địa bàn
 → Cohort có train/validation/test theo thời gian
 → Spark ML: fit tiền xử lý, huấn luyện, chọn trên validation, đánh giá test
 → Lưu pipeline, kết quả thực nghiệm và dữ liệu serving
```

### Khi dùng ứng dụng

```text
Trình duyệt → Next.js :3000 → proxy /api → FastAPI :8000
 ├─ Thống kê/tra cứu: serving và artifact gọn
 ├─ Ước tính: pipeline Spark đã nạp → giá/dải tham khảo/cảnh báo
 └─ Thử tin mẫu: bộ quy tắc kiểm tra bằng Spark
```

Web **suy luận**, không huấn luyện lại theo từng request. Giá người dùng đang cân nhắc chỉ để đối chiếu, không đưa vào feature dự đoán. Một phần thống kê đọc bằng PyArrow; không phải mọi lần đổi filter đều tạo job Spark.

| Công nghệ | Vai trò |
|---|---|
| Python 3.11, PySpark/Spark 3.5.7, JDK 17 | Runtime xử lý và mô hình |
| Spark SQL/DataFrame | Lọc, biến đổi, kiểm tra chất lượng và tổng hợp |
| Spark ML/MLlib | Pipeline tiền xử lý và hồi quy LR, RF, GBT |
| Parquet trên filesystem | Lưu nguồn, ETL, cohort và serving |
| FastAPI/Uvicorn | Backend, kiểm tra input, nạp model và phục vụ API |
| Next.js/React/TypeScript | Giao diện và luồng thao tác trình duyệt |
| Tailwind CSS/shadcn/ui | Styling và thành phần giao diện |
| Recharts | Biểu đồ, khám phá sai số |
| Leaflet/GeoJSON | Polygon 22 nhóm địa bàn lịch sử; nền online tùy chọn |
| PyArrow | Đọc serving gọn, xuất CSV |

Hiện chạy **trực tiếp trên Windows, local/LAN**, chưa dùng Docker, MongoDB, Redis, Neo4j hoặc HDFS. Spark mặc định `local[4]` nghĩa là **bốn luồng trên một máy**, không phải bốn máy. Chưa thực nghiệm cụm nhiều máy; Spark SQL là bộ máy xử lý, không phải màn quản trị CSDL.

## 2. Clone và setup lần đầu trên Windows / VS Code

### Phần mềm cần có

Git, **Python 3.11**, Node.js/npm, VS Code và trình duyệt. Cần Internet để cài dependencies/JDK lần đầu. Môi trường đã kiểm thử: Python 3.11.15, Node 26.5.0, npm 12.0.1, JDK17, Spark 3.5.7; không khẳng định mọi phiên bản Node khác đã đạt.

Không cần cài Spark riêng toàn máy. Setup cài PySpark, tải JDK portable có checksum và build adapter filesystem Windows. Cần RAM cho Windows/Node/native JVM ngoài heap Spark; chỉ chạy một Spark JVM cho quy trình demo chính.

### Clone và mở folder

Trong PowerShell, ở thư mục muốn lưu project:

```powershell
git clone https://github.com/HoangThaNHty/Do_An_BigData.git
cd Do_An_BigData
```

VS Code → **File → Open Folder** → chọn folder vừa clone. **Terminal → New Terminal → PowerShell**. Root repo phải có `README.md`, `scripts`, `src`, `web`.

Trên máy nghiên cứu repo có thể nằm ở `D:\slider\real-estate-bigdata`; không cần đổi tên folder. Scripts lấy root theo vị trí repo. `FolderDoAnBigData` là folder tài liệu, không phải root chạy ứng dụng. Không copy phần dấu nhắc `PS ...>` vào lệnh.

### Setup tại root repo

```powershell
python --version
node --version
npm.cmd --version
.\scripts\setup.ps1
```

Python phải là **3.11**. Nếu lệnh `python` trỏ sai và có Python Launcher, dùng môi trường mới:

```powershell
py -3.11 -m venv .venv
.\scripts\setup.ps1 -Python .\.venv\Scripts\python.exe
```

Không coi đây là cách nâng cấp `.venv` cũ sai phiên bản; dùng clone sạch hoặc xử lý môi trường cũ riêng. Setup sẽ từ chối Python không đúng 3.11.

Nếu Windows chặn chạy `.ps1`, đặt cho terminal hiện tại rồi chạy lại; không cần đổi policy toàn máy:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\setup.ps1
```

Setup: tạo `.venv` → cài dependency theo lock → chuẩn bị JDK17 → build adapter Java → kiểm 264 file demo → `npm ci`/build web. Có JDK17 sẵn thì dùng `-JavaHome` trỏ đường dẫn thật theo [SETUP](docs/guide/SETUP.md).

**Đạt khi:** hiện `Setup complete`. Setup không tải raw, không train model. Không cần activate `.venv` bằng tay khi dùng các lệnh hướng dẫn.

### Clone có dữ liệu nào?

| Mục tiêu | Clone có đủ không? |
|---|---|
| Web, dự đoán thật, kiểm tra tin mẫu | Có sau setup: có model/serving/địa giới |
| Terminal 0 nguồn → output ETL → split | Chưa: cần raw + ETL + cohort đầy đủ ở máy nghiên cứu |
| Huấn luyện lại | Chưa: cần cohort Parquet có đủ feature/split, không chỉ serving |

Không tải raw hoặc train lại chỉ để mở sản phẩm. Nếu vừa clone, có thể bỏ qua Terminal 0 và chạy Terminal 1/2 ngay.

## 3. Terminal 0 — dữ liệu nguồn và Spark

### Điều kiện

Phải có dữ liệu thật tại các đường dẫn sau, không chỉ metadata:

```text
data/raw/oceanng/shard_0000.parquet ... shard_0009.parquet
data/processed/etl_v4/listings/
data/processed/core_v1/listings/
artifacts/models/v1/
```

Tải raw thôi **chưa đủ**: script còn đọc ETL/cohort đã chuẩn bị. Xem mục 9 để biết nguồn dữ liệu. Dừng API/launcher cũ bằng Ctrl+C ở terminal của nó trước; không dừng tất cả java.exe/node.exe của máy.

### Lệnh chạy và điểm dừng

Tại root repo, đặt tên terminal **Terminal 0 — Spark demo**:

```powershell
.\scripts\run.ps1 -Module scripts.demo_spark -DriverMemory 1g
```

Tạo application `HCM-demo-data-ETL-split`, heap 1 GB. Script dừng chờ **Enter** sau từng bước để người trình bày xem kết quả và chuyển sang UI.

| Chặng | Làm gì? | Kết quả/ý nghĩa |
|---|---|---|
| `01-SOURCE` | Đọc schema, count raw/phạm vi, xem vài dòng chọn lọc | Toàn nguồn 3.500.744 dòng/19 trường; nhà-căn hộ HCM 1.122.870 tin |
| `02-ETL-OUTPUT` | Đọc **output ETL đã lưu**, groupBy disposition | Thuê 46.151; ứng viên tạm 149.975; cách ly 926.742 |
| `03-TEMPORAL-SPLIT` | Đọc cohort, count theo tháng/loại/split | Train 78.048, validation 17.886, test 37.845; tổng 133.779 |
| `04-SAVED-EXPERIMENT` | Đọc selection/results đã lưu | Chọn house_lr/apartment_lr theo MAE validation; **không train mới** |

ETL lưu 1.122.868 bản ghi sau loại hai bản ghi nguồn trùng hệt. Cách ly không có nghĩa toàn bộ là tin giả. Train 06–11/2025, validation 12/2025, test 01–03/2026.

**Thao tác:** xem terminal → mở Spark UI giải thích → quay lại Enter. Sau bước 04, Enter để hiện `DEMO PASS`, dừng SparkContext và trả dấu nhắc PowerShell. **Lúc đó mới chạy Terminal 1.** Terminal 0 không chạy lại toàn ETL hoặc fit model; muốn train thật xem mục 8.

Kiểm tra tự động không dừng:

```powershell
.\scripts\run.ps1 -Module scripts.demo_spark -DriverMemory 1g --no-pause
```

### Xem gì trên Spark UI?

Dùng URL terminal in, thường [127.0.0.1:4040](http://127.0.0.1:4040). Cổng bận có thể chuyển 4041 hoặc tiếp theo; kiểm tra đúng tên application.

| Tab | Nên xem/giải thích |
|---|---|
| Jobs | Trạng thái, group, duration; mở một job |
| Stages | Stage/task và input/shuffle nếu có |
| SQL / DataFrame | Execution/plan count/filter/groupBy; Scan Parquet, Filter, Aggregate/Exchange khi xuất hiện |
| Executors | Tiến trình local trên cùng máy; không gọi là bốn node |
| Environment | Thông tin cấu hình/môi trường |
| Storage | Dữ liệu cache/persist nếu có; trống không có nghĩa không có file Parquet |

UI theo vòng đời SparkContext; script kết thúc thì UI đó dừng. Job ID/số job thay đổi giữa lượt chạy. Count có thể tận dụng metadata/column pruning, không nói mọi job đọc toàn bộ mô tả tin.

## 4. Terminal 1 — API và nạp mô hình Spark

Mở terminal mới **Terminal 1 — API**, tại root repo. Nếu chạy Terminal 0 thì đợi nó kết thúc; clone chỉ mở web có thể bắt đầu ở đây.

```powershell
.\scripts\run.ps1 -Module src.api.serve -DriverMemory 2g --port 8000
```

Lệnh khởi tạo Spark, nạp model v1 và chạy Uvicorn **một worker** ở `127.0.0.1:8000`. Demo dùng heap 2 GB. Chờ nạp model, có thể khoảng một phút hoặc hơn tùy máy; **giữ terminal mở**.

Mở [API health](http://127.0.0.1:8000/api/v1/health), hoặc kiểm tra ở terminal khác:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/v1/health
```

Kết quả mong đợi:

```json
{"status":"ready","data_version":"core_v1","model_version":"v1","analysis_rows":133779}
```

[API docs](http://127.0.0.1:8000/docs) cho xem endpoint/schema. Chỉ gửi dự đoán khi API ready.

Spark UI mới thuộc **`HCM-web-inference`**. Các dòng load/ReadWrite/StandardScaler/LinearRegression lúc khởi động là **nạp pipeline đã học**, không phải fit. Refresh đúng context sau khi Terminal 0 đã tắt. Không dùng nhiều worker/reload hoặc mở launcher song song vì có thể tạo nhiều Spark/trùng cổng.

## 5. Terminal 2 — web

Mở terminal mới **Terminal 2 — Web**, bắt đầu từ root repo rồi vào `web`:

```powershell
cd .\web
$env:API_BASE_URL = 'http://127.0.0.1:8000'
npm.cmd run start
```

Đây là **production build đã được setup tạo**, không chạy lệnh npm ở root Python. Mở [127.0.0.1:3000](http://127.0.0.1:3000). Kiểm tra [health qua proxy web](http://127.0.0.1:3000/api/v1/health) phải cùng ready với API trực tiếp. Mở được giao diện chưa chứng minh backend hoạt động.

Đường chuẩn dùng API 8000. Proxy rewrites lấy từ cấu hình build: nếu đổi cổng API thì đặt `API_BASE_URL` đúng **khi build lại**, không chỉ đổi biến sau khi đã build.

Giữ **Terminal 1 và 2** mở. Dừng bằng Ctrl+C ở Terminal 2 rồi Terminal 1. Muốn quay lại ETL/train, dừng API trước để chỉ chạy một Spark JVM.

## 6. Những lần sau: một lệnh mở sản phẩm

Nếu không cần tách log hoặc demo nguồn, tại root:

```powershell
.\scripts\start-local.ps1
```

Launcher tự bật API 2 GB, chờ ready, rồi chạy Next.js 3000. Nó **thay Terminal 1 và 2**; không chạy đồng thời hai cách. Chờ `Open http://localhost:3000/`, giữ terminal; Ctrl+C dừng launcher và phiên API đi cùng.

LAN hoặc đổi cổng frontend:

```powershell
.\scripts\start-local.ps1 -Lan
```

```powershell
.\scripts\start-local.ps1 -Port 3001
```

`-Port` chỉ đổi **frontend**, API vẫn 8000. Có thể chọn `-DriverMemory 4g` khi đủ tài nguyên, nhưng 2 GB là mặc định demo; tăng heap không khắc phục máy thiếu RAM.

## 7. LAN và hành trình demo web

### LAN

Dùng launcher `-Lan`, hoặc nếu chạy tách thì giữ Terminal 1 và ở Terminal 2/folder web thay start bằng:

```powershell
npm.cmd exec -- next start --hostname 0.0.0.0 --port 3000
```

Thiết bị cùng mạng mở `http://IP-LAN-CUA-MAY-CHAY:3000`; xem IPv4 bằng `ipconfig`. `127.0.0.1` trên máy thứ hai trỏ chính máy thứ hai. Firewall/mạng phải cho phép cổng web trên mạng Private. API vẫn ở loopback qua proxy; LAN không phải publish Internet.

### Demo sáu màn hình

| Trang | Thao tác | Giải thích |
|---|---|---|
| Tổng quan | Đổi loại/tháng, xem chỉ số, xuất CSV | Tập tin được chọn; CSV web là tổng hợp, khác raw toàn nguồn |
| Tìm khu vực | Căn hộ 3–4 tỷ, 60–80 m²; áp dụng; chọn 2–3 vùng so sánh | Cùng điều kiện; số tin không là số tài sản duy nhất đang còn bán |
| Bản đồ giá | Bấm vùng, đổi lớp giá/m²/giá tổng/số tin | Polygon lịch sử; nền online phụ trợ, không có GPS từng căn |
| Ước tính | Căn hộ 70 m², Thủ Đức, 2 PN/2 WC, giá cân nhắc 4,2 tỷ; chạy/lưu A; đổi 90 m², chạy lại B, so | Giá cân nhắc chỉ đối chiếu; A/B không chứng minh quan hệ nhân quả |
| Độ chính xác | Chọn điểm/tin, đọc giá nguồn/dự đoán/chênh lệch | Chỉ số toàn test khác mẫu scatter 300 điểm; công bố cả lỗi lớn |
| Dữ liệu & phương pháp | Xem sáu bước, thử bán/thuê/trả trước | Bộ quy tắc Spark thật; ví dụ không thêm vào train, không xác minh tin thật |

[Lời dẫn thuyết trình đầy đủ](docs/plans/PLAN_THUYET_TRINH_CUOI_KY.md) · [Spark từng bước](docs/guide/DEMO_QUY_TRINH_SPARK.md) · [Tester](docs/guide/TESTER_CHECKLIST.md).

## 8. Huấn luyện lại trực tiếp — tùy chọn

Không cần train lại để mở web. Cần `data/processed/core_v1/listings` đủ feature/split và manifest; serving bảy trường không thay cohort. Dừng Terminal 0/API trước. Tại root:

```powershell
$experimentDir = 'artifacts/models/demo_' + (Get-Date -Format 'yyyyMMdd_HHmmss')
.\scripts\run.ps1 -Module src.models.train -DriverMemory 4g --core data/processed/core_v1 --output $experimentDir
```

Đây là **train thật**, app `HCM-price-model-comparison`, chín pipeline và đánh giá, output mới. Xem UI lúc lệnh còn chạy; thời gian phụ thuộc máy. Không ghi đè v1; code chặn output đã tồn tại. API vẫn dùng v1, không tự chuyển model mới.

Phân biệt rõ: bước 04 Terminal 0 đọc kết quả cũ; lệnh này chạy thí nghiệm mới. Không sửa test/loại lỗi sau đánh giá để làm số đẹp.

## 9. Dataset, CSV và tái hiện nghiên cứu

| Tầng | Vị trí | Trong Git? |
|---|---|---|
| Nguồn 3.500.744 dòng/19 trường | `data/raw/oceanng/shard_*.parquet` | Không; có manifest/card |
| CSV toàn nguồn khoảng 3,27 GB | `data/raw/oceanng/vietnam_real_estates_full.csv` | Không |
| ETL đầy đủ | `data/processed/etl_v4/listings` | Không; có summary |
| Cohort 133.779 tin | `data/processed/core_v1/listings` | Không; có manifest/ID loại |
| Serving/catalog | `artifacts/market` | Có |
| Model/kết quả/test predictions | `artifacts/models/v1` | Có |
| Địa giới/giấy phép | `artifacts/geography`, `data/raw/geography` | Có |

Sau setup, tải raw đúng revision pinned, tại root:

```powershell
.\.venv\Scripts\python.exe scripts/bootstrap_data.py --dataset
```

Chỉ tải raw, **không tạo ETL/core hoặc thay model**. ETL lại dùng output mới khi API đã dừng:

```powershell
$etlDir = 'data/processed/etl_demo_' + (Get-Date -Format 'yyyyMMdd_HHmmss')
.\scripts\run.ps1 -Module src.etl.build -DriverMemory 4g --output $etlDir
```

Tái hiện cohort còn cần review/provenance đúng phiên bản; không bypass kiểm tra hash/review trong `src/etl/core.py`. Nhóm dùng máy nghiên cứu hoặc chia sẻ bộ nghiên cứu riêng; tải raw thôi không làm Terminal 0 chạy đủ.

Xuất CSV đầy đủ từ 10 shard, khi file mặc định chưa có:

```powershell
.\.venv\Scripts\python.exe -m scripts.export_source_csv
```

Script không ghi đè; dùng `--output data/raw/oceanng/ten_moi.csv` nếu cần. CSV UTF-8 BOM kèm manifest số bản ghi/cột/SHA-256; văn bản có xuống dòng nên số dòng vật lý khác số bản ghi. Parquet giữ kiểu/null đầy đủ hơn và vẫn là nguồn chính.

Excel tối đa 1.048.576 dòng/sheet nên không hiện hết 3,5 triệu bản ghi. Dùng mẫu nhỏ hoặc Power Query lọc trước; nhập trường văn bản như Text. [Dataset/CSV](docs/guide/XEM_DATASET.md) · [Dữ liệu đi cùng Git](data/README.md). CSV crawler Chợ Tốt cũ không phải dataset hiện hành.

## 10. Kiểm tra và xử lý lỗi

### Kiểm tra không cần web

Tại root:

```powershell
.\.venv\Scripts\python.exe -m scripts.check_repo
.\.venv\Scripts\python.exe -m scripts.audit_github
```

`check_repo` kiểm SHA-256 của 264 artifact demo. `audit_github` rà file Git và một số dấu hiệu token/private key; không phải kiểm toán bảo mật toàn diện.

| Triệu chứng | Xử lý |
|---|---|
| PowerShell chặn ps1 | Đặt ExecutionPolicy Scope Process như mục 2 cho terminal bị chặn |
| Python sai phiên bản | Chọn 3.11 rõ khi setup; kiểm tra môi trường cũ |
| Thiếu java_home/adapter | Chạy setup để chuẩn bị JDK và adapter Windows |
| Terminal 0 thiếu raw/ETL/core | Clone không có bộ nghiên cứu; chuẩn bị riêng hoặc chỉ chạy Terminal 1/2 |
| FileExistsError train/ETL/CSV | Chọn output mới, không xóa/ghi đè nghiên cứu gốc để chạy qua |
| Cổng 3000/8000 bận | Dừng đúng phiên cũ; không chạy launcher và terminal tách cùng lúc |
| Không vào được 4040 | Context đã tắt/UI đổi cổng; xem URL và app name hiện tại |
| Web không gọi API | Kiểm health trực tiếp 8000 rồi proxy 3000; giữ cả hai tiến trình |
| Health 503/JVM mất kết nối/native memory error | Dừng phiên cũ, giảm ứng dụng nặng, restart API 2 GB; không mở thêm JVM |
| Next thiếu production build | Dừng frontend, vào web: `npm.cmd run build`, sau đó `npm.cmd run start` |
| WARN winutils/native Hadoop | Có thể xuất hiện trong phiên thành công; xem exception và health |
| Nền bản đồ lỗi | Tắt nền online hoặc thử lại; polygon/model không cần tile Internet |
| Checksum sai | Đối chiếu artifact đúng phiên bản, không sửa model JSON để qua kiểm tra |

Sau pull frontend phải build lại trước start; lock/setup đổi thì chạy setup theo hướng dẫn. Không push `.next`/`node_modules`. QA nâng cao ở [SETUP](docs/guide/SETUP.md) và [nghiệm thu clone](docs/guide/REPO_GITHUB_NGHIEM_THU.md); không cần Playwright chỉ để chạy sản phẩm. Sửa README không đồng nghĩa đã diễn tập trên mọi laptop.

## 11. Kết quả và giới hạn

Chín pipeline LR/RF/GBT + baseline; chọn LR riêng nhà/căn hộ theo validation trước test. Train 78.048, validation 17.886, test 37.845.

| Test | Nhà riêng | Căn hộ |
|---|---:|---:|
| MAE (tỷ VND) | 2,950 | 1,395 |
| RMSE (tỷ VND) | 18,159 | 4,586 |
| R² | 0,320 | 0,740 |
| Giảm MAE so baseline | 36,73% | 58,47% |

Sai số vẫn lớn; R² không là phần trăm đoán đúng. Dải hiệu chỉnh trên validation không bảo đảm từng căn. Xem [kết quả/ngoại lệ đầy đủ](docs/research/KET_QUA_MO_HINH.md).

Tin 06/2025–03/2026 gồm trước/sau sáp nhập, phân tích theo **TP.HCM trước hợp nhất**, 22 nhóm lịch sử; chưa bao phủ Bình Dương/Bà Rịa–Vũng Tàu cũ hoặc mapping phường mới đầy đủ. Giá rao chưa xác minh giao dịch/pháp lý, không là giá hiện tại. Không có GPS từng căn. Review AI chưa là nhãn người độc lập; proxy đăng lại chưa loại hết cùng tài sản đổi nội dung. Chưa là công cụ thẩm định hay quyết định tài chính.

## 12. Cấu trúc repo và tài liệu

```text
src/                      API, ETL, model, cấu hình, Java adapter
web/                      Next.js/React, proxy, giao diện
scripts/                  Setup, run, demo, QA, tải nguồn, xuất CSV
artifacts/models/v1/      Pipeline thật, selection/results, test predictions
artifacts/market/         Serving Parquet và catalog/thống kê
artifacts/geography/      Polygon địa bàn nghiên cứu
artifacts/etl/            Summary, không phải ETL Parquet đầy đủ
artifacts/verification/   Bằng chứng kiểm thử đã lưu
data/                     Manifest/metadata; raw/cohort đầy đủ ở máy nghiên cứu
docs/guide/               Setup, tester, demo, GitHub, bàn giao
docs/plans/               Word, thuyết trình, hướng sản phẩm
docs/research/            Phương pháp, dữ liệu, kết quả
docs/history/             Mốc cũ để truy vết, không là hướng dẫn hiện hành
archive/                  Crawler/audit cũ, không tham gia runtime
```

Không xóa `stages`, `metadata`, `_SUCCESS`, `part-*` như rác: đó là cấu trúc model Spark. Môi trường, cache, `.next`, raw/CSV lớn, review và Office/ZIP local được ignore Git.

- [Danh mục tài liệu](docs/README.md), [scripts](scripts/README.md).
- [Kịch bản toàn bộ đồ án](docs/plans/PLAN_THUYET_TRINH_CUOI_KY.md).
- [Spark từng bước và lời giải thích](docs/guide/DEMO_QUY_TRINH_SPARK.md).
- [Tester](docs/guide/TESTER_CHECKLIST.md), [mẫu ghi kết quả](docs/guide/TEST_RESULT_TEMPLATE.md).
- [GitHub cho nhóm](docs/guide/GITHUB_TEAM.md).
- [Plan Word ba cấp](docs/plans/PLAN_BAO_CAO_WORD_V1.md).

## 13. Giấy phép và phạm vi bàn giao

Mã nguồn theo [MIT LICENSE](LICENSE). Dữ liệu/thành phần bên thứ ba theo [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES.md): nguồn tin CC BY-NC 4.0, địa giới/admin giữ điều kiện riêng. MIT của code không thay giấy phép dữ liệu hoặc cho phép thương mại mọi artifact đi kèm.

Windows/local/LAN là đường chạy đã kiểm thử; macOS/Linux/Docker/Internet chưa được nghiệm thu. Word/PPT local là snapshot cần cập nhật theo plan. Model/data giữ v1/core_v1; sửa UI/tài liệu không tự đổi kết quả nghiên cứu.
