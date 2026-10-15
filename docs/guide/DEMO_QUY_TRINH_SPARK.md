> **Điều hướng V5:** Sau khi vào web, dùng Khám phá khu vực (Bản đồ/Danh sách chung); không tìm menu Bản đồ giá riêng. Sau ước tính chọn Lập kế hoạch với căn này, nhập dòng tiền và tính các mốc/ba mức giá. Bộ tính tài chính không phải model ML, không train lại. Mở Dữ liệu & phương pháp qua liên kết phụ, mở Minh họa kỹ thuật trước khi chạy ví dụ tin Spark. Các bước Terminal 0/1/2 không đổi.

# Demo từ dữ liệu nguồn đến web — hướng dẫn hai thành viên

Ngày 15/10/2026. **Chưa commit/push GitHub** theo yêu cầu mới; chỉ push khi cả hai thực hiện được quy trình. Phần demo nghiên cứu cần raw/ETL/cohort đầy đủ ở máy nghiên cứu, không chỉ clone demo gọn.

## 1. Hiểu ảnh Spark UI hiện tại

Ảnh người dùng gửi có application **HCM-web-inference** ở localhost:4040/jobs. Các job load/ReadWrite/StandardScaler/OneHotEncoder/LinearRegression là bằng chứng nạp metadata/pipeline đã lưu. Không dùng các dòng “load at LinearRegression” để nói đang huấn luyện.

Spark local không cần một server Spark/MongoDB khởi động riêng. Mỗi ứng dụng Python tạo SparkContext; API tạo context của nó và nạp model. Bài demo dữ liệu tạo context khác, nên chạy theo hai giai đoạn để tránh nhiều JVM và nhầm UI/cổng.

## 2. Chuẩn bị trên mỗi máy Windows

Mở folder repo trong VS Code, terminal PowerShell. Nếu đang ở folder tài liệu, chuyển sang `D:\slider\real-estate-bigdata` (máy thành viên dùng đường dẫn clone của mình). Đã setup thì không chạy setup lại mỗi buổi. Lần đầu làm theo SETUP.md.

Chuẩn bị raw 10 shard, `data/processed/etl_v4/listings`, `data/processed/core_v1/listings`, `artifacts/models/v1`, `.venv`, JDK theo `.runtime/java_home.txt`, `.runtime/project-local-fs.jar`, web build. Bản clone gọn chỉ đủ phục vụ web; muốn cả hai demo đoạn nghiên cứu thì chia sẻ bộ nghiên cứu đúng provenance qua kênh nhóm, hoặc cùng dùng máy nghiên cứu và diễn tập cả hai trên máy đó. Không bypass review/hash để tạo cohort cho qua.

Đóng API/launcher cũ bằng Ctrl+C ở terminal của nó trước buổi demo nghiên cứu. Không chạy start-local.ps1 đồng thời với API/web tách terminal: sẽ trùng cổng. Không tắt tất cả java.exe/node.exe vì có thể là ứng dụng khác.

## 3. Ba terminal — chạy theo thứ tự

### Terminal 0: Spark local cho phần dữ liệu/ETL/split

```powershell
cd D:\slider\real-estate-bigdata
.\scripts\run.ps1 -Module scripts.demo_spark -DriverMemory 1g
```

Lệnh này tạo Spark local[4], có các điểm dừng Enter. Mở **URL Spark UI mà terminal in ra**; thường http://localhost:4040. Cổng đã bận có thể thành 4041; tên application phải là HCM-demo-data-ETL-split. 1 GB đủ cho phần kiểm tra đọc/đếm này, khác cấu hình huấn luyện 4 GB. Script không ghi lại ETL/cohort/model.

### Terminal 1: API và nạp model

Sau khi phần nghiên cứu kết thúc, Terminal 0 in DEMO PASS và SparkContext dừng. Chạy:

```powershell
cd D:\slider\real-estate-bigdata
.\scripts\run.ps1 -Module src.api.serve -DriverMemory 2g --port 8000
```

Giữ terminal này mở. Chờ Application startup complete; health http://127.0.0.1:8000/api/v1/health phải trả status ready. Đây là load model đã huấn luyện, không train lại mỗi request. Spark UI mới thuộc application HCM-web-inference; refresh URL sau khi context cũ dừng, không đọc màn hình cũ còn cache.

### Terminal 2: web

Nếu chưa có build, chạy `npm ci` rồi `npm run build` tại folder web trước buổi demo. Khi đã build:

```powershell
cd D:\slider\real-estate-bigdata\web
$env:API_BASE_URL = 'http://127.0.0.1:8000'
npm.cmd run start
```

Mở http://127.0.0.1:3000. Để máy khác cùng LAN vào web, thay lệnh cuối bằng `npm.cmd exec -- next start --hostname 0.0.0.0 --port 3000`, truy cập IP LAN của máy này. API vẫn bind loopback vì web proxy API. Firewall/mạng LAN phải cho phép cổng web.

Nếu chỉ muốn mở sản phẩm hằng ngày, dùng `scripts/start-local.ps1` thay cả Terminal 1 và 2. Không chạy cả hai cách cùng lúc.

## 4. Kịch bản diễn giải từng bước

| Bước | Thao tác và hiện vật | Câu trình bày | Phân biệt quan trọng |
|---|---|---|---|
| Nguồn | Explorer mở data/raw/oceanng; manifest/card; Terminal 0 in schema và count | Nguồn toàn bộ 3.500.744 dòng/19 trường; bài toán chọn HCM nhà/căn hộ 1.122.870 tin | CSV là bản xuất để đọc, Parquet là nguồn xử lý |
| Xử lý Spark | Khi dừng 01-SOURCE: Jobs → job nhóm 01; SQL/DataFrame → truy vấn count/filter; bấm query xem plan | Spark đọc dữ liệu có cấu trúc, lọc phạm vi theo tỉnh/loại | count có thể tận dụng metadata/column pruning, không nói đã quét toàn bộ nội dung mô tả |
| ETL | Enter chạy 02-ETL-OUTPUT, xem bảng disposition; mở rules.py/quality.py và manifest etl_v4 | Chuẩn hóa giá/diện tích, nhận diện thuê/trả trước/không rõ, routing và lưu cả phần cách ly | Demo đang đọc/đếm output ETL đã tạo, không chạy lại toàn ETL |
| Chia tập | Enter chạy 03-TEMPORAL-SPLIT, xem tháng/số lượng từng split | Train 06–11/2025: 78.048; val 12/2025: 17.886; test 01–03/2026: 37.845 | Không random split; fit tiền xử lý trên train; proxy đăng lại chưa loại hết cùng tài sản |
| Train/đánh giá | Enter bước 04-SAVED-EXPERIMENT; mở train.py, experiment_plan.json, selection.json, results.json | Đã so sánh chín pipeline LR/RF/GBT và baseline, chọn LR riêng theo MAE validation rồi đánh giá test | Bước 04 trình bày thực nghiệm đã lưu, không tạo job train mới |
| Nạp model | Enter kết thúc; bật Terminal 1, kiểm tra health; Spark UI application HCM-web-inference | API tạo Spark và nạp pipeline đã fit từ đĩa; cùng tiền xử lý training | “load” là nạp, không phải fit |
| Sử dụng | Bật Terminal 2; mở web, nhập căn hộ, bấm ước tính, quay lại Spark UI refresh | Form gửi qua API, Spark pipeline suy luận thật, trả giá rao/dải tham khảo | Giá cân nhắc chỉ đối chiếu; không phải giá giao dịch hay thị trường hiện tại |

## 5. Nên bấm gì trên Spark UI?

- **Jobs:** chọn job nhóm 01-SOURCE/02-ETL-OUTPUT/03-TEMPORAL-SPLIT khi đang dừng; xem status, duration và succeeded/total. ID/job count thay đổi giữa lần chạy, không học thuộc “job 45”.
- **SQL / DataFrame:** chọn execution của count/groupBy; xem plan Scan Parquet, Filter, Aggregate/Exchange khi có, DAG và metrics thực tế. Giải thích truy vấn tạo các bước xử lý, không cần đọc mọi tên operator.
- **Stages:** từ một job bấm stage; xem task, input/shuffle nếu có. Job→stage→task là phân rã thực thi. Không phải mọi job đều có shuffle.
- **Executors:** local mode thường hiện driver/executor tại cùng máy; local[4] là bốn luồng, không phải bốn máy/cụm bốn node.
- **Environment:** tìm master/local[4], phiên bản/config nếu hiển thị; training 4 GB khác API 2 GB và demo đọc 1 GB.
- **Storage:** có thể trống vì phần demo không cache; trống không có nghĩa không có dữ liệu. File nằm trên filesystem, không phải tab Storage của UI.

Sau ước tính, Jobs/SQL có thêm execution suy luận; số lượng có thể khác phiên bản/đầu vào. Dashboard thống kê có phần đọc serving bằng PyArrow nên không hứa mọi lần đổi filter đều tạo job Spark.

## 6. Nếu cần show HUẤN LUYỆN TRỰC TIẾP

Đây là nhánh riêng, không trộn với trình bày kết quả đã lưu. Dừng Terminal 0 và API để chỉ chạy một Spark JVM. Dùng cohort chuẩn, đóng ứng dụng nặng, chuẩn bị đủ RAM/đĩa. Trong PowerShell:

```powershell
cd D:\slider\real-estate-bigdata
$experimentDir = 'artifacts/models/demo_' + (Get-Date -Format 'yyyyMMdd_HHmmss')
.\scripts\run.ps1 -Module src.models.train -DriverMemory 4g --core data/processed/core_v1 --output $experimentDir
```

Mở Spark UI trong lúc lệnh còn chạy, app HCM-price-model-comparison. Quan sát fit/model comparison, không chỉ load. Lệnh huấn luyện thật chín pipeline và đánh giá, ghi vào thư mục mới, **không ghi đè v1 và không tự chuyển model đang phục vụ**. Thời gian phụ thuộc máy, không đảm bảo giống 187,60 giây lần thực nghiệm cũ. Không chạy lệnh mặc định vào v1 vì code chủ động chặn ghi đè. Khi xong Spark UI tắt cùng context; đọc results/selection trong experimentDir, sau đó bật API v1 và web. Nếu chọn dùng model mới thì phải nghiệm thu riêng, không tự đổi trong lúc demo.

Để toàn chu trình có phần train trực tiếp, dùng nhánh này sau Terminal 0 và trước Terminal 1. Có thể quay video lần chạy thật dự phòng nếu thời lượng lớp/RAM không cho phép; nói rõ video/kết quả là lần chạy trước, không giả là đang chạy trực tiếp. Hỏi giảng viên về thời lượng cho phép, không tự cắt dữ liệu test để làm số đẹp.

Chạy lại ETL đầy đủ cũng là nhánh riêng, không bắt buộc mỗi lần mở sản phẩm:

```powershell
$etlDemoDir = 'data/processed/etl_demo_' + (Get-Date -Format 'yyyyMMdd_HHmmss')
.\scripts\run.ps1 -Module src.etl.build -DriverMemory 4g --output $etlDemoDir
```

ETL này ghi output mới, không thay etl_v4/core/model. Chưa tự chạy lại core chỉ để demo: core kiểm tra review/hash/provenance và có thể cập nhật serving khi chạy; giữ tập frozen đang dùng. Logic temporal đọc tại src/etl/core.py và groupBy trên cohort là bằng chứng split đang dùng.

## 7. HDFS và đề tài tự đề xuất

File môn học trong folder tài liệu ghi: dùng **ít nhất một công nghệ Big Data hoặc công nghệ lưu trữ/xử lý phân tán như Hadoop, HDFS, Spark, Flink, NoSQL hoặc tương đương**. HDFS trong cột gợi ý không đồng nghĩa mọi đề tài bắt buộc dùng HDFS. Spark hiện có đáp ứng điều kiện công nghệ trong văn bản đã đọc; nếu giảng viên có yêu cầu bổ sung riêng thì phải theo yêu cầu đó.

Không dùng HDFS thì phải giải thích chính xác: dữ liệu lưu Parquet trên filesystem local, Spark xử lý local nhiều luồng, chưa thực nghiệm fault tolerance/mở rộng nhiều máy. Không tuyên bố phân tán lưu trữ hay benchmark cụm. Có HDFS cũng không tự làm mô hình chính xác hơn. Với nhóm Windows, ưu tiên chu trình thật/tái hiện được; chỉ thêm HDFS nếu giảng viên yêu cầu hoặc mục tiêu thật sự là lưu trữ phân tán và có thời gian kiểm chứng.

File môn cũng cho phép sinh viên **chủ động đề xuất đề tài nhưng cần giảng viên xem xét/chấp thuận**. Việc các đề tài gợi ý đã có nhóm đăng ký là thông tin nhóm cung cấp, không suy ra từ văn bản quy định. Tên/phạm vi HCM giá rao và dùng Spark cần được xác nhận duyệt nếu chưa có.

## 8. Hai thành viên đều phải làm được trước GitHub

### Trả lời khi giảng viên hỏi nền tảng và Docker

“Nhóm triển khai trực tiếp trên Windows, không dùng Docker ở phiên bản hiện tại. Phần xử lý và mô hình dùng PySpark 3.5.7/Python 3.11/JDK 17, Spark local[4] trên một máy. Backend FastAPI và frontend Next.js chạy thành hai tiến trình, người dùng truy cập bằng trình duyệt localhost hoặc LAN. Dữ liệu lưu Parquet trên filesystem; chưa triển khai HDFS/cụm nhiều máy.”

Nếu hỏi tái hiện khi không Docker: trình bày dependency lock, setup.ps1/run.ps1, JDK portable có checksum và demo_manifest kiểm tra model/dữ liệu; đã có kiểm thử clone Windows, còn máy nhóm phải diễn tập. Không nói lockfile bảo đảm tái hiện giống hệt Docker hoặc đã hỗ trợ mọi OS.

Nếu hỏi “vậy có Big Data không”: chỉ ra nguồn 3,5 triệu dòng, ETL/SQL và Spark ML thật, UI job/stage/task; phân biệt công nghệ có khả năng phân tán với thực nghiệm đang chạy local. Không lấy nhiều cổng dịch vụ làm bằng chứng nhiều máy, không khẳng định benchmark mở rộng/fault tolerance.

Docker là cách đóng gói/chạy môi trường, không phải điều kiện để thuật toán là Spark. Hiện không có Dockerfile/Compose và chưa kiểm thử Docker; nếu muốn bổ sung thì là công việc tương lai. Báo cáo/sơ đồ deployment phải thể hiện Windows local/LAN đúng trạng thái.

Diễn tập lần 1: thành viên A trình bày nguồn→ETL→split→train; B load→web→giải thích kết quả. Lần 2 đổi vai. Không chỉ chia để mỗi người biết một nửa.

- Tự tìm raw, manifest, cohort, model, serving và giải thích khác nhau.
- Tự chạy đúng thứ tự, phân biệt app Spark nghiên cứu với API, kiểm tra health/cổng.
- Bấm Jobs→Stage và SQL plan, giải thích local[4]/Parquet và hạn chế không HDFS.
- Phân biệt training mới với xem results/nạp model cũ; hiểu train/val/test và chọn mô hình.
- Demo ước tính thật, so sánh vùng/căn, cảnh báo sai số và bộ kiểm tra tin Spark; xử lý API chưa ready/map offline.
- Trả lời giá rao khác giá giao dịch; dữ liệu 06/2025–03/2026/địa bàn lịch sử; R² không là accuracy.

Ghi kết quả từng người vào TEST_RESULT_TEMPLATE.md. Chỉ xem quy trình đã nghiệm thu đầy đủ khi cả hai làm được; hiện tài liệu là hướng dẫn, không thay thế việc hai thành viên đã diễn tập. Chưa push/commit theo chỉ dẫn người dùng.

Nguồn kỹ thuật: https://spark.apache.org/docs/3.5.7/monitoring.html ; giới hạn Excel: https://support.microsoft.com/en-gb/excel/excel-specifications-and-limits?nochrome=true ; yêu cầu môn là DOCX gốc trong tai_lieu_mon_hoc. Chỉ dùng chức năng thật; ảnh Spark UI người dùng là bằng chứng nạp model tại thời điểm ảnh, không chứng minh mọi giai đoạn cùng chạy.
