> **Kịch bản đã cập nhật theo sản phẩm V5:** Menu còn năm mục chính. Phần 5.2 và 5.3 là hai cách xem trong Khám phá khu vực, không chuyển sang menu map riêng. Sau 5.4 dùng Lập kế hoạch với căn này và lời dẫn mới dưới đây. Dữ liệu & phương pháp là liên kết phụ; mở Minh họa kỹ thuật trước các ví dụ. Phần dưới giữ bố cục nghiên cứu để không mất nội dung Spark.

### Lời dẫn bổ sung: Kế hoạch mua nhà (1–2 phút)

Sau dự đoán, bấm **Lập kế hoạch với căn này**. Chỉ vào giá/dải đã lấy từ kết quả vừa tính; nhập tiền hiện có, dự phòng, thu nhập và chi tiêu, giả định vay rồi bấm tính.

> Từ giá tham chiếu, nhóm bổ sung bộ tính để người dùng thấy tác động của ngân sách và mức giá tới thời gian tích lũy. Đây là công thức theo giả định, không huấn luyện thêm model và không dự báo giá tương lai. Kết quả tách đủ tiền mua không vay, đủ vốn ban đầu và mốc có vốn kèm dòng tiền tháng đầu không âm. Có thể đủ vốn nhưng khoản trả nợ vẫn vượt phần thu nhập còn lại.

Chỉ bảng ba mức giá, biểu đồ tích lũy và dòng kiểm tra tăng lãi. Nêu rõ lãi/chi phí mặc định là minh họa, không báo giá ngân hàng; 0 phí là chưa tính phí. Nếu đủ thời gian đổi lãi và tính lại để thấy dòng tiền thay đổi. Ví dụ độc lập: vốn khả dụng 500 triệu, 20 triệu/tháng, giá không đổi/0 lãi/0 phí → 2,8/3,5/4,2 tỷ cần 115/150/185 tháng. Không biến dải lịch sử thành xác suất thời gian mua.

Bản 10–12 phút rút bớt phần đọc map/scatter chi tiết để dành một phút cho chức năng này, không kéo dài ngầm hoặc bỏ phần giới hạn.

# Kế hoạch và lời dẫn thuyết trình cuối kỳ — toàn bộ project

Ngày 15/10/2026. Tài liệu diễn tập cho cả hai thành viên; không phải slide đã tạo hoặc xác nhận nhóm đã trình bày thành công. Mã nguồn thực: `D:\slider\real-estate-bigdata`; có bản sao tài liệu trong `D:\slider\FolderDoAnBigData`.

## 1. Mục tiêu và thông điệp cần nhớ

Người nghe phải hiểu: bài toán là gì; dữ liệu từ đâu; Spark làm gì; model đã được huấn luyện thế nào; kết quả tốt/chưa tốt ở đâu; sản phẩm giúp người dùng làm gì; nhóm triển khai trên môi trường nào.

Tên đề tài đề xuất: **Phân tích dữ liệu tin đăng và xây dựng hệ thống ước tính giá rao bán nhà ở tại TP. Hồ Chí Minh bằng Apache Spark**. Khi đưa lên bìa/slide cuối cùng phải khớp tên được giảng viên duyệt, không tự nói tên đề xuất đã được duyệt.

Câu xương sống:

> Nguồn Parquet → Spark xử lý và kiểm tra chất lượng → tập nghiên cứu và chia thời gian → huấn luyện/chọn/đánh giá → pipeline đã lưu → API nạp model → người dùng tra cứu và ước tính trên web.

Ba ý phải nói đúng từ đầu: **giá rao bán**; **dữ liệu 06/2025–03/2026**; **TP.HCM theo địa bàn lịch sử trước hợp nhất**. Không giới thiệu như hệ thống định giá giao dịch hiện tại cho toàn TP.HCM mới.

## 2. Thời lượng và phân vai đề xuất

Bản đầy đủ: **18–22 phút, chưa gồm hỏi đáp và huấn luyện lại trực tiếp**. Đây là đề xuất luyện tập, không phải thời gian chính thức của lớp. Nếu lớp giới hạn 10–12 phút, dùng mục 12 để rút gọn.

| Chặng | Thời gian tham khảo | Người dẫn | Hiện vật chính |
|---|---|---|---|
| Mở đầu/bài toán | 0–1 phút | A | Slide 1–2 |
| Kiến trúc/công nghệ | 1–2,5 | A | Slide 3/sơ đồ |
| Nguồn dữ liệu | 2,5–3,5 | A | Folder nguồn, schema/count |
| Spark/ETL | 3,5–5 | A | Spark UI và output ETL |
| Chia tập/tiền xử lý | 5–6,5 | A | Split theo tháng, pipeline |
| Mô hình/lựa chọn | 6,5–8 | A | Code/tham số/selection |
| Kết quả và chuyển API | 8–10,5 | B | Bảng metrics; API đang nạp |
| Sản phẩm web | 10,5–18 | B | Sáu màn hình theo hành trình |
| Giới hạn/kết luận | 18–20 | A hoặc B | Slide 12 |

Hai người phải diễn tập đổi vai. Phân công trình bày không phải bảng đóng góp nghiên cứu thực tế. Khi chuyển người, nói một câu kết nối thay vì dừng im lặng.

12 slide lõi dự kiến: (1) tên/nhóm; (2) bài toán/mục tiêu/phạm vi; (3) kiến trúc/công nghệ; (4) dữ liệu; (5) ETL; (6) chia tập/pipeline; (7) mô hình/tham số/lựa chọn; (8) kết quả; (9) triển khai Windows/local/LAN; (10) tình huống người dùng và chuyển demo; (11) minh bạch sai số/phương pháp; (12) hạn chế/kết luận. Live demo xen giữa, không cần tạo một slide riêng cho mọi nút. Phụ lục slide có bảng mô hình đầy đủ, công thức, screenshot/ảnh dự phòng và câu hỏi kỹ thuật.

## 3. Chuẩn bị trước khi nói

- Mở đúng repo, cắm sạc, đóng ứng dụng nặng. Không cài package, tải nguồn, build Next hoặc mở CSV 3,27 GB lần đầu trước mặt lớp.
- Chạy setup/build và checklist từ trước. Máy nghiên cứu phải có đủ raw/ETL/cohort; clone gọn chỉ đủ demo sản phẩm bằng model/serving. Xem `../guide/SETUP.md` và `../guide/DEMO_QUY_TRINH_SPARK.md`.
- Chuẩn bị terminal T0 Spark demo, T1 API, T2 web. Không chạy launcher đồng thời với API/web tách terminal; chỉ một Spark JVM cho phần diễn tập chính.
- VS Code mở trước: DATASET_CARD, manifest nguồn, manifest core, experiment_plan, selection, results và features/train.py. Chỉ mở vùng code cần giải thích, không cuộn tìm file giữa buổi.
- Chuẩn bị tab Spark UI, web, API health; API docs là tab dự phòng. Kiểm tra đúng tên Spark application, không dùng trang của context đã tắt.
- Khi mở đầu có thể cho T0 chạy đến điểm dừng đầu tiên, rồi trình bày slide bài toán/kiến trúc. Đến phần nguồn mới chuyển màn hình.
- Có screenshot/video của lần chạy thật dự phòng; ghi rõ đó là bằng chứng đã lưu nếu sử dụng. Không dùng prototype Open Design như ảnh app hoạt động.
- Chọn trước nhánh **kết quả huấn luyện đã lưu** hay **huấn luyện trực tiếp**. Nhánh chính dưới đây dùng kết quả đã lưu và live suy luận; không đánh tráo hai việc.

## 4. Lời dẫn chi tiết theo chu trình nghiên cứu

### Chặng 1 — Mở đầu và bài toán

**Hiển thị:** slide tên và mục tiêu. **Mục đích:** người nghe biết nhóm giải quyết việc gì trước khi thấy công nghệ.

**Nói mẫu:**

> Em chào thầy/cô và các bạn. Nhóm chúng em thực hiện đề tài phân tích dữ liệu tin đăng và ước tính giá rao bán nhà ở tại TP.HCM bằng Apache Spark. Bài toán đặt ra là tin đăng có nhiều cách ghi giá, thông tin thiếu và cả tin thuê hoặc giá trả trước. Nếu đưa tất cả vào thống kê và mô hình thì kết quả dễ gây hiểu nhầm. Vì vậy nhóm xây dựng một quy trình từ kiểm tra dữ liệu, huấn luyện mô hình đến ứng dụng web để tra cứu và đối chiếu giá rao.

> Người mua có thể tìm khu vực theo ngân sách và tham khảo một mức giá đang được rao. Người bán có thể tham khảo mức giá đăng. Kết quả là thông tin hỗ trợ, không phải chứng thư thẩm định hoặc khuyến nghị mua bán.

**Nối:** “Để thực hiện, nhóm tổ chức hệ thống thành các bước sau.”

### Chặng 2 — Kiến trúc và vai trò công nghệ

**Hiển thị:** sơ đồ Parquet → Spark ETL → cohort/split → Spark ML → model/serving → FastAPI → Next.js. Phân biệt luồng huấn luyện trước và luồng sử dụng sau.

**Nói mẫu:**

> Dữ liệu nguồn lưu dạng Parquet trên filesystem. Spark SQL và DataFrame xử lý, kiểm tra và tổng hợp dữ liệu. Spark ML dùng để fit tiền xử lý và huấn luyện các mô hình hồi quy. Kết quả được lưu thành pipeline và các artifact phục vụ. FastAPI nạp model để nhận yêu cầu ước tính. Next.js là phần web người dùng thao tác, Recharts thể hiện biểu đồ và Leaflet thể hiện địa bàn.

> Phiên bản hiện tại chạy trực tiếp trên Windows, Spark local[4] trên một máy, chưa dùng Docker hoặc HDFS. local[4] là bốn luồng, không phải bốn máy. Nhóm dùng Spark thật nhưng chưa có thực nghiệm mở rộng cụm nhiều máy.

**Không đọc tất cả version trên slide.** Nếu được hỏi: Spark 3.5.7, Python 3.11, JDK17; training thực nghiệm driver 4 GB, API demo 2 GB, script đọc/đếm demo 1 GB. Đây là ba cấu hình cho ba nhiệm vụ khác nhau.

**Nối:** “Trước khi xem sản phẩm, em minh họa dữ liệu mà hệ thống thực sự xử lý.”

### Chặng 3 — Nguồn dữ liệu

**Thao tác:** mở folder `data/raw/oceanng`, DATASET_CARD và manifest. Trong T0 chạy:

```powershell
cd D:\slider\real-estate-bigdata
.\scripts\run.ps1 -Module scripts.demo_spark -DriverMemory 1g
```

Chờ dừng sau `01-SOURCE`. Terminal in schema, count toàn nguồn/phạm vi, 5 dòng các trường chọn để xem. Không mở mô tả dài hoặc liên hệ người đăng trên màn hình trình chiếu.

**Nói mẫu:**

> Nhóm lựa chọn bộ dữ liệu oceanNG/vietnam-real-estates và cố định revision trong manifest. Toàn nguồn có 3.500.744 bản ghi, 19 trường, chia thành 10 file Parquet. Các trường gồm loại nhà, tỉnh/khu vực, diện tích, giá nguồn, thời gian đăng và một số thuộc tính nhà ở. Giá nguồn ban đầu là chuỗi nên cần kiểm tra và chuyển đổi, không coi mọi giá đều đã là giá bán tổng hợp lệ.

> Sau khi chọn nhà và căn hộ tại TP.HCM, phạm vi đầu vào còn 1.122.870 tin. Đây vẫn chưa phải tập huấn luyện cuối cùng. CSV toàn nguồn đã xuất chỉ để đọc/trao đổi; pipeline chính đọc Parquet.

**Nếu hỏi nguồn:** đây là bộ dữ liệu công khai nhóm chọn dùng, không nói nhóm tự crawl toàn bộ nguồn này. Crawler Chợ Tốt trong archive không phải nguồn hiện hành. Giấy phép nguồn CC BY-NC 4.0, giữ ghi công và giới hạn sử dụng phi thương mại.

**Nối:** “Bước quan trọng tiếp theo là kiểm tra các tin có thực sự phù hợp bài toán giá rao bán hay không.”

### Chặng 4 — Spark xử lý và ETL

**Thao tác:** ở điểm dừng 01, mở Spark UI đúng URL terminal. Jobs → một job → stage; SQL/DataFrame → count/filter execution. Không học thuộc job ID. Quay T0 nhấn Enter, xem `02-ETL-OUTPUT` và bảng disposition.

**Nói mẫu:**

> Trên Spark UI, một yêu cầu xử lý được tổ chức thành job, stage và task. Tab SQL/DataFrame cho thấy kế hoạch đọc Parquet, lọc và tổng hợp tương ứng với truy vấn. Count có thể tận dụng metadata hoặc chỉ đọc cột cần thiết; không có nghĩa mọi thao tác đều đọc toàn bộ mô tả tin.

> Về nghiệp vụ, nhóm nhận diện dấu hiệu bán/thuê, kiểm tra giá tổng, đối chiếu diện tích và phạm vi nhà ở. Tin chưa rõ hoặc có mâu thuẫn được cách ly thay vì ép thành dữ liệu hợp lệ. Đây là bộ quy tắc kiểm tra, không phải mô hình AI xác minh tin thật hoặc tài sản có thật.

**Số liệu để đối chiếu:** sau bỏ hai bản ghi nguồn trùng hệt, ETL lưu 1.122.868 bản ghi: thuê 46.151; ứng viên tạm 149.975; cách ly 926.742. “Tạm phù hợp” chưa đồng nghĩa đã được xác minh hoặc đều vào train. Cách ly nhiều phản ánh phạm vi/quy tắc thận trọng, không có nghĩa toàn bộ phần đó là tin giả.

**Nói rõ trạng thái demo:**

> Đoạn này đang dùng Spark để đọc và thống kê đầu ra ETL đã tạo; không thực thi lại toàn bộ ETL trong buổi trình bày. Mã thực hiện và manifest được giữ để tái hiện.

**Nối:** “Từ các ứng viên, nhóm xây dựng tập nghiên cứu và tách dữ liệu theo thời gian.”

### Chặng 5 — Cohort, chia tập và tránh rò rỉ

**Thao tác:** Enter sang `03-TEMPORAL-SPLIT`; chỉ vào bảng tháng/split và manifest core.

**Nói mẫu:**

> Tập nghiên cứu cuối cùng có 133.779 tin. Nhóm loại ID đã từng đọc hoặc review khỏi thí nghiệm và xử lý đăng lại theo proxy toàn văn chuẩn hóa. Train gồm tháng 6 đến tháng 11/2025 với 78.048 tin; validation là tháng 12/2025 với 17.886 tin; test là tháng 1 đến tháng 3/2026 với 37.845 tin.

> Train dùng học tham số; validation dùng chọn mô hình; test dùng đánh giá sau khi đã chọn. Chia theo thời gian phù hợp cách sử dụng dữ liệu quá khứ cho giai đoạn sau. Cách chia này không tự loại hết rò rỉ: cùng tài sản có thể được đăng lại với nội dung khác, đây vẫn là hạn chế.

**Giải thích pipeline:** diện tích biến đổi log; số phòng/kích thước có kiểm tra hợp lệ và cờ thiếu; median imputation học từ train; địa bàn/phường/dự án được mã hóa; vector được scale độ lệch chuẩn, không trừ trung bình (`withMean=False`). Giá rao nguồn là target, không đưa giá/m² hoặc giá người dùng đang cân nhắc vào feature để đoán chính giá đó.

**Nối:** “Sau khi khóa cách chia và tiền xử lý, nhóm so sánh những mô hình nào?”

### Chặng 6 — Huấn luyện và chọn mô hình

**Thao tác:** Enter sang `04-SAVED-EXPERIMENT`; mở experiment_plan, selection và vài dòng train.py/features.py nếu cần.

**Nói mẫu:**

> Nhóm thử ba thuật toán hồi quy: Linear Regression, Random Forest và Gradient-Boosted Trees. Mỗi thuật toán chạy cho nhà riêng, căn hộ và mô hình chung, tổng cộng chín pipeline. Nhóm bổ sung baseline trung vị theo loại nhà và khu vực để kiểm tra mô hình có cải thiện so với một cách dự đoán đơn giản hay không.

> Model học log của giá, rồi chuyển dự đoán về VND bằng hàm mũ. Tiền xử lý chỉ fit trên train và được lưu cùng pipeline. Nhóm chọn model theo MAE validation, không chọn theo test. Kết quả chọn Linear Regression riêng cho nhà và căn hộ; mô hình phức tạp hơn không mặc nhiên tốt hơn trên dữ liệu này.

**Nếu hỏi tham số:** LR maxIter=80, regParam=0.05, elasticNetParam=0; RF 30 cây/maxDepth7; GBT 30 vòng/maxDepth5/stepSize0.1. Bộ so sánh có ngân sách cố định, chưa phải tìm kiếm siêu tham số toàn diện.

**Nói trạng thái:**

> Đây là kết quả của lần huấn luyện đã lưu, không phải model đang fit ngay lúc em mở JSON. Phần web tiếp theo sẽ nạp pipeline và suy luận trực tiếp.

**Chuyển người:** “Em đã trình bày quá trình dữ liệu và lựa chọn mô hình. Sau đây bạn … trình bày chất lượng kết quả và ứng dụng của mô hình.”

### Chặng 7 — Đánh giá và chuyển sang nạp model

**Thao tác:** Enter kết thúc T0. Bật T1 API, trong lúc nạp chuyển về slide kết quả để không im lặng chờ máy:

```powershell
cd D:\slider\real-estate-bigdata
.\scripts\run.ps1 -Module src.api.serve -DriverMemory 2g --port 8000
```

**Bảng cần nhớ, đơn vị tiền là tỷ VND:**

| Test | Nhà riêng | Căn hộ |
|---|---:|---:|
| Số mẫu | 4.705 | 33.140 |
| MAE baseline | 4,662 | 3,359 |
| MAE model chọn | 2,950 | 1,395 |
| Giảm MAE so baseline | 36,73% | 58,47% |
| RMSE model | 18,159 | 4,586 |
| R² | 0,320 | 0,740 |
| Median APE | 16,57% | 13,74% |
| Coverage test của dải tham khảo | 90,12% | 86,00% |

**Nói mẫu:**

> Trên test, MAE giảm khoảng 36,73% với nhà và 58,47% với căn hộ so baseline. Tuy nhiên sai số tuyệt đối vẫn lớn: khoảng 2,95 tỷ và 1,395 tỷ. Vì vậy nhóm không khẳng định đây là công cụ thẩm định chính xác từng căn. RMSE nhà rất cao vì một số sai lệch lớn; nhóm giữ và công bố kết quả này thay vì loại test sau khi thấy sai số.

> Median APE cho thấy mức sai lệch tương đối ở giữa phân bố, không phải cam kết mọi căn đều sai dưới con số đó. R² cũng không phải phần trăm dự đoán đúng. Dải giá hiệu chỉnh trên validation có coverage test thực tế khác nhau giữa hai loại nhà và không bảo đảm cho từng tài sản.

**Chỉ công thức khi hỏi:** MAE = trung bình |giá dự đoán − giá nguồn|; RMSE = căn trung bình bình phương sai số, nhạy với lỗi lớn; APE = sai số tuyệt đối/giá nguồn; R² so sai số với biến thiên giá. Giá nguồn chưa là giá giao dịch được xác minh.

**Nối:** “Nhóm đưa model đã lưu vào API để người dùng trải nghiệm mà không phải huấn luyện lại.”

### Chặng 8 — Nạp model và mở web

**Thao tác:** T1 báo startup complete; mở http://127.0.0.1:8000/api/v1/health, thấy ready/core_v1/v1. Spark UI mới phải có tên HCM-web-inference. T2:

```powershell
cd D:\slider\real-estate-bigdata\web
$env:API_BASE_URL = 'http://127.0.0.1:8000'
npm.cmd run start
```

**Nói mẫu:**

> Backend khởi tạo Spark và nạp pipeline đã fit từ đĩa. Các dòng load trong Spark UI là đọc model, không phải train. Web gửi yêu cầu qua API, pipeline transform đầu vào rồi trả dự đoán. Đây là sự khác nhau giữa huấn luyện trước và suy luận khi sử dụng.

Mở http://127.0.0.1:3000. Nếu API chưa ready, tiếp tục giải thích bảng kết quả hoặc sơ đồ; không bấm gửi liên tục và không mở thêm Spark JVM. API docs ở http://127.0.0.1:8000/docs là dự phòng nếu cần giải thích hợp đồng đầu vào/đầu ra.

## 5. Kịch bản demo web theo một câu chuyện

**Tình huống xuyên suốt:** người dùng tìm căn hộ 60–80 m², ngân sách 3–4 tỷ; muốn xem khu vực, đối chiếu một căn 70 m² đang rao 4,2 tỷ, rồi so với một phương án khác. Không kết luận nên mua/bán từ kết quả model.

### 5.1 Tổng quan — 40–60 giây

**Làm:** mở Tổng quan; chỉ kỳ dữ liệu và loại căn hộ; thay một bộ lọc nếu đủ thời gian; có thể xuất CSV tổng hợp.

**Nói:**

> Trang này mô tả tập tin đã được chọn theo điều kiện hiện tại: số tin, mức giá và phân bố. Đây là thống kê dữ liệu nguồn, không đại diện mọi giao dịch hoặc số tài sản duy nhất đang bán. CSV trên web là bảng tổng hợp theo bộ lọc, khác CSV toàn nguồn 3,5 triệu dòng.

**Chứng minh:** filter phản ánh vào số liệu, không chỉ một ảnh dashboard cố định.

### 5.2 Khám phá khu vực và so sánh — 1–1,5 phút

**Làm:** chọn căn hộ; ngân sách 3–4 tỷ; diện tích 60–80 m² → áp dụng tìm kiếm; chọn Tân Phú, Quận 7 và Thủ Đức nếu có trong kết quả → mở so sánh. Nếu tên/điều kiện không cho ba vùng đó thì chọn các vùng thực có; không sửa dữ liệu để có kết quả mong muốn.

**Nói:**

> Người dùng bắt đầu bằng nhu cầu thay vì tự đọc hàng loạt biểu đồ. Hệ thống tìm các khu vực có tin phù hợp và cho so sánh trong cùng điều kiện về số tin, giá và diện tích. Số tin cao không có nghĩa khu vực đó tốt nhất, có nhiều căn duy nhất hơn hoặc đang còn bán.

**Chứng minh:** ít nhất hai vùng được chọn và bảng so sánh hiện ra. Nếu thay draft điều kiện, nhấn áp dụng trước khi diễn giải kết quả mới. Không học thuộc 14.110 tin nếu bộ lọc đã thay đổi.

### 5.3 Bản đồ — 40–60 giây

**Làm:** trong Khám phá khu vực chọn cách xem Bản đồ; bấm một vùng; đổi lớp giá/m² sang số tin; quan sát vùng so sánh được giữ.

**Nói:**

> Bản đồ bổ sung góc nhìn không gian cho các thống kê. Màu và chú giải thay đổi theo chỉ tiêu đang chọn. Số tin giúp nhận biết vùng có ít dữ liệu để đọc mức giá thận trọng hơn. Các polygon là địa bàn lịch sử; không có tọa độ từng căn và chưa tự ánh xạ hoàn chỉnh sang địa giới mới.

**Giới hạn chức năng:** bản đồ hiện có giao thoa với Tìm khu vực. Hướng phân tích theo hai tháng là đề xuất, chưa demo như chức năng đã làm. Không mở Google Maps hoặc nói đã có bản đồ từng nhà. Nền online tùy mạng; polygon offline vẫn là chức năng thật.

### 5.4 Ước tính và so sánh hai căn — 2–2,5 phút

**Làm đúng thứ tự:** chọn căn hộ, 70 m², Thủ Đức, 2 phòng ngủ, 2 WC; phường/dự án chỉ chọn khi biết; nhập giá cân nhắc 4,2 tỷ. Chạy ước tính; đọc kết quả thực tế. Lưu căn để so sánh → đổi diện tích 90 m² → **chạy lại ước tính** → mở so sánh hai căn. Không chỉ đổi input rồi gọi đó là dự đoán mới.

**Nói:**

> Giá 4,2 tỷ là giá người dùng muốn đối chiếu, không đưa vào feature để mô hình đoán lại chính nó. Kết quả gồm giá rao ước tính theo dữ liệu lịch sử, dải tham khảo và các cảnh báo. Người mua dùng để có thêm thông tin đối chiếu; người bán tham khảo mức đăng, không coi đây là giá giao dịch chắc chắn.

> Em lưu kết quả căn đầu để giữ snapshot. Sau khi đổi thuộc tính và chạy lại, hệ thống có phương án thứ hai để so. Chênh lệch là phản ứng của mô hình với hai đầu vào; không chứng minh quan hệ nhân quả rằng thêm 20 m² sẽ luôn làm giá tăng đúng mức đó.

**Chứng minh:** kết quả A không đổi khi sửa B; B được tính thật. Có thể quay Spark UI refresh để chỉ execution suy luận nếu thời gian đủ. Không đòi mọi filter dashboard phải tạo job: một phần thống kê đọc serving bằng PyArrow.

### 5.5 Độ chính xác dự đoán — 50–70 giây

**Làm:** chọn loại nhà; bấm một điểm scatter hoặc chọn tin trong danh sách; xem giá nguồn/dự đoán/chênh lệch. Mở bảng kỹ thuật hoặc lỗi lớn nếu được hỏi.

**Nói:**

> Trang này giúp người dùng nhìn thấy mô hình có sai số như thế nào thay vì chỉ thấy một giá dự đoán. Một điểm minh họa một mẫu trong phần biểu đồ. Chỉ số tổng hợp tính trên toàn tập test; scatter chỉ là mẫu 300 điểm cho mỗi loại, không phải toàn bộ test hoặc toàn bộ dataset. Giá nguồn ở đây cũng là giá rao, chưa là giao dịch xác minh.

**Chứng minh:** chọn điểm thực sự đổi phần chi tiết; nêu cả lỗi lớn, không chỉ chọn một điểm gần đường y=x.

### 5.6 Dữ liệu/phương pháp và thử tin bằng Spark — 1–1,5 phút

**Làm:** mở Dữ liệu & phương pháp qua liên kết phụ, xem quy trình sáu bước và mở Minh họa kỹ thuật; chọn lần lượt ví dụ bán rõ, thuê, trả trước; với mỗi ví dụ bấm phân tích rồi đọc kết quả trước khi chuyển ví dụ khác. Nếu thiếu thời gian, chạy bán và một ví dụ không phù hợp.

**Nói:**

> Người dùng nhìn được vì sao dữ liệu được giữ hay cần kiểm tra: ý định giao dịch, giá tổng, diện tích và phạm vi. Tin thuê hoặc giá trả trước không được trộn như giá bán tổng. Chức năng này gọi bộ quy tắc Spark thật, nhưng ví dụ là nội dung minh họa, không phải tin nguồn và không được thêm vào train. Vượt kiểm tra chỉ là ứng viên, vẫn còn bước review, trùng lặp và chia tập.

**Chứng minh:** kết quả khác nhau theo nội dung, lý do có thể giải thích. Không gọi đây là phát hiện tin giả hoặc chatbot AI.

## 6. Kết luận và câu chốt

**Hiển thị:** slide kết luận/giới hạn, ngừng thao tác web để tập trung vào người nghe.

**Nói mẫu:**

> Nhóm đã xây dựng quy trình dữ liệu từ nguồn triệu dòng, xử lý bằng Spark, tạo tập nghiên cứu có chia thời gian, huấn luyện và so sánh mô hình, rồi tích hợp suy luận vào web. Kết quả cải thiện so baseline nhưng vẫn có sai số đáng kể. Giá rao chưa được xác minh, review tham chiếu AI chưa thay thế nhãn người độc lập, địa bàn và thời gian còn giới hạn, chưa thực nghiệm cụm nhiều máy.

> Hướng tiếp theo là bổ sung kiểm chứng của con người, cập nhật dữ liệu và mapping địa danh, cải thiện mô hình rồi mới mở rộng triển khai. Nhóm xin kết thúc và sẵn sàng trả lời câu hỏi.

Không nêu những hướng tương lai như cam kết chắc chắn hoàn thành hoặc tính năng đã tồn tại.

## 7. Từ điển công nghệ để nói bằng lời của mình

| Thành phần | Nói ngắn gọn | Chỗ chứng minh trong project |
|---|---|---|
| Parquet | Định dạng lưu theo cột, giữ schema; dùng làm nguồn/lớp đã xử lý | raw shards, ETL/core/serving |
| Spark SQL/DataFrame | Bộ máy biến đổi và truy vấn dữ liệu có cấu trúc | src/etl, job/query trong Spark UI |
| Spark ML/MLlib | Học tiền xử lý và các mô hình hồi quy | features.py/train.py và pipeline lưu |
| Pipeline | Chuỗi bước tiền xử lý và model, lưu để dùng nhất quán | stages/metadata trong model |
| FastAPI | Backend nhận/kiểm tra input và gọi suy luận | src/api, health/docs |
| Next.js/React | Giao diện và luồng thao tác trình duyệt | web/app và components |
| shadcn/ui/Tailwind | Thành phần giao diện và styling | web/components, cấu hình CSS |
| Recharts | Biểu đồ tương tác | overview/scatter và biểu đồ web |
| Leaflet/GeoJSON | Hiển thị lớp bản đồ và polygon địa bàn | map, artifacts/geography |
| PyArrow | Đọc serving gọn và xuất dữ liệu; không phải model khác thay Spark | thống kê API/script CSV |
| JDK/Python/Node | Runtime cho Spark, backend/script và frontend | setup/run, requirements, package lock |
| Docker | Công cụ đóng gói môi trường; hiện chưa dùng | Không có Dockerfile/Compose đã nghiệm thu |
| HDFS | Hệ thống lưu trữ phân tán; hiện chưa dùng | Đang dùng filesystem local |

Không đọc danh sách framework như thành tích. Với mỗi công nghệ, nói **vai trò → dữ liệu đi qua → bằng chứng**. UI Open Design là hỗ trợ thiết kế đã dùng trước đó, không phải engine xử lý dữ liệu hoặc model định giá.

## 8. Hai nhánh khi cần chạy lại thật

### 8.1 Huấn luyện trực tiếp

Đây là phần thêm thời gian ngoài kịch bản chính. Dừng API và Spark demo, chỉ giữ một JVM. Đã có cohort đúng provenance, đủ RAM; chạy:

```powershell
cd D:\slider\real-estate-bigdata
$experimentDir = 'artifacts/models/demo_' + (Get-Date -Format 'yyyyMMdd_HHmmss')
.\scripts\run.ps1 -Module src.models.train -DriverMemory 4g --core data/processed/core_v1 --output $experimentDir
```

Nói “em đang chạy một thực nghiệm mới trên cohort đã chuẩn bị”. UI phải là HCM-price-model-comparison, quan sát trong khi lệnh còn sống. Lưu output mới, không đè v1; API sau đó vẫn dùng v1 nếu chưa có thay đổi được nghiệm thu. Lần thực nghiệm cũ khoảng 187,60 giây không bảo đảm máy hôm nay cũng vậy. Không đổi siêu tham số dựa vào kết quả test vừa thấy.

Nếu không đủ thời gian: dùng video thật/kết quả đã lưu và nói rõ, không tuyên bố train live. Đọc JSON không thay thế bằng chứng đang fit. Phần trình bày chính chứng minh train bằng code/config/artifact/metrics, live chứng minh suy luận.

### 8.2 Chạy ETL lại

Dừng API/JVM khác; dùng output mới theo DEMO_QUY_TRINH_SPARK.md. ETL lớn cần thời gian và đĩa, không làm mặc định trước lớp. Không tự chạy core và cập nhật serving trong buổi demo vì core kiểm tra review/hash/provenance. Giữ dữ liệu thí nghiệm đã khóa; ghi nhận lần chạy mới tách biệt.

## 9. Phản biện và câu trả lời mẫu

| Giảng viên hỏi | Cách trả lời |
|---|---|
| Big Data ở đâu khi chạy một laptop? | Nguồn triệu dòng, ETL/SQL/ML dùng Spark thật. Đây là thực nghiệm local nhiều luồng; nhóm chưa đo mở rộng cluster. Quy mô dữ liệu không tự chứng minh phải có cluster, nhóm trình bày cả nhu cầu và giới hạn. |
| Có Docker không? | Chưa. Chạy native Windows; có script setup, dependency lock, JDK kiểm tra checksum và demo manifest. Chưa nhận đã portable như Docker hoặc hỗ trợ mọi OS. |
| Vì sao không HDFS/MongoDB? | Lưu Parquet local đáp ứng phạm vi thử nghiệm; Spark là công nghệ Big Data đang dùng. Văn bản môn yêu cầu ít nhất một công nghệ, không bắt buộc mọi dự án có HDFS. Nếu có yêu cầu riêng của giảng viên thì nhóm cần bổ sung. |
| Dataset do nhóm crawl? | Nguồn hiện hành là bộ công khai oceanNG, cố định revision và ghi giấy phép; không nhận tự crawl toàn bộ. |
| Có phải train trên 3,5 triệu dòng? | Không. Đó là toàn nguồn; HCM nhà/căn hộ 1.122.870, cohort 133.779 và train 78.048. |
| Có deep learning/LLM không? | Không dùng neural network cho giá. Đây là hồi quy tabular Spark ML; bộ kiểm tra tin là quy tắc. Review tham chiếu AI là hỗ trợ nghiên cứu, không phải nhãn chuyên gia. |
| Vì sao tin bị loại nhiều? | Quy tắc tập trung tính phù hợp/nhất quán, nhiều tin phải cách ly chứ không kết luận giả. Cohort có thiên lệch chọn mẫu cần công bố. |
| Loại trùng hết chưa? | Có loại trùng hệt và proxy đăng lại theo toàn văn chuẩn hóa, chưa đảm bảo cùng tài sản đổi nội dung không lọt qua. |
| Vì sao chia thời gian? | Mô phỏng dùng quá khứ cho giai đoạn sau; tránh trộn ngẫu nhiên giữa các kỳ. Còn các nguồn leakage khác nên phải xử lý riêng. |
| Vì sao LR thắng RF/GBT? | Trên bộ feature/cấu hình và validation hiện tại, LR riêng có MAE tốt hơn. Không kết luận LR luôn hơn; ngân sách tuning còn hạn chế. |
| Baseline là gì? | Trung vị giá train theo loại nhà/khu vực, nhóm đủ ít nhất 20 tin; thiếu nhóm thì về trung vị loại nhà. |
| R² 0,74 có phải đúng 74%? | Không. Là độ đo so sai số bình phương với biến thiên giá test; không là tỷ lệ căn đoán đúng hay độ chắc chắn mỗi dự đoán. |
| Sai số tiền lớn vậy dùng được không? | Có giá trị minh họa phân tích/đối chiếu, chưa đủ cho thẩm định hay quyết định tài chính. Báo cáo cả MAE, RMSE, APE, nhóm và ngoại lệ thay vì chỉ nêu cải thiện. |
| Dải có chắc chứa đúng giá không? | Không. Hiệu chỉnh trên validation; coverage test nhà 90,12%, căn hộ 86,00%; không bảo đảm từng căn hay tương lai. |
| 98/100 là chính xác 98% toàn dữ liệu? | Không. Đó là kết quả hỗ trợ trên một mẫu review tham chiếu AI; không chứng nhận toàn nguồn hoặc thay nhãn người độc lập. |
| Dữ liệu sau sáp nhập xử lý sao? | Tin có trước và sau, nhưng chuẩn phân tích dùng địa bàn HCM lịch sử; chưa cover toàn TP.HCM mới hoặc crosswalk phường đầy đủ. |
| Có giá hiện tại không? | Chưa. Dữ liệu đến 03/2026, không nói giá tháng 10/2026 hoặc giá giao dịch xác thực. |
| Người dùng nhập giá thì model học từ đó? | Giá cân nhắc chỉ để so kết quả, không làm feature, không fit lại trên input demo. |
| Tăng diện tích làm giá tăng đúng chênh lệch? | Chỉ là so hai đầu vào theo model, không khẳng định tác động nhân quả hoặc quy luật cho mọi nhà. |
| API bật có phải đang train? | Không. Nạp model đã lưu rồi suy luận. Spark UI load/read không chứng minh fit. |
| Spark Storage trống có lỗi không? | Không nhất thiết; tab đó phản ánh dữ liệu cache/persist, không phải toàn bộ file Parquet trên đĩa. |
| Clone có phải tải raw/train lại? | Không cho web demo vì model/serving gọn đi cùng repo; tái hiện nghiên cứu cần raw/cohort/review đúng provenance. |
| Nền bản đồ lỗi thì dự đoán có lỗi? | Nền online là phụ trợ; polygon offline và model/API độc lập với tile Internet. |
| Chức năng mới theo tháng có chưa? | Đó là đề xuất nâng cấp bản đồ, chưa trình bày như đã triển khai. |

## 10. Xử lý sự cố khi trình bày

| Tình huống | Làm gì | Nói gì |
|---|---|---|
| Cổng đã bận | Dùng phiên đang chạy hoặc dừng đúng terminal cũ; kiểm tra app name | Không mở thêm nhiều server để chữa lỗi |
| Spark UI chuyển cổng | Dùng URL localhost terminal in, refresh đúng application | Mỗi context có UI, không phải một CSDL chung |
| API đang load | Xem health/log, tiếp tục bảng kết quả trong lúc chờ | Model cần được nạp trước khi suy luận |
| JVM/API hỏng | Dừng đúng tiến trình, khởi động lại nếu có thời gian | Chuyển ảnh/video đã lưu và nói rõ phần live chưa thực hiện được |
| Tile online lỗi | Tắt nền online, giữ polygon | Bản đồ dữ liệu địa bàn vẫn dùng được |
| Không có vùng phù hợp | Kiểm tra loại/tháng, mở rộng ngân sách/diện tích có giải thích | Tập dữ liệu không có tin thỏa điều kiện, không có nghĩa thị trường không tồn tại |
| Kết quả giá bất thường | Kiểm tra input/đơn vị/dự án/cảnh báo | Công bố giới hạn, không sửa dữ liệu/model cho đẹp ngay lúc demo |
| Thời gian thiếu | Bỏ lớp online, bảng kỹ thuật, ví dụ tin thứ ba; giữ dự đoán và sai số | Ưu tiên chu trình và bằng chứng chính |

## 11. Phiếu nhớ nhanh trước buổi nói

**Nhớ theo 8 từ:** Bài toán → Nguồn → Làm sạch → Chia tập → Học → Đánh giá → Sử dụng → Giới hạn.

**Nhớ 5 số:** toàn nguồn 3,5 triệu; phạm vi 1,12 triệu; cohort 133.779; train/val/test khoảng 78 nghìn/18 nghìn/38 nghìn; chín pipeline. Khi cần số chính xác đọc bảng, không đọc nhầm toàn nguồn thành train.

**Nhớ 3 khác biệt:** giá rao ≠ giao dịch; train ≠ load/predict; local[4] ≠ bốn máy.

**Nhớ bộ công nghệ theo vai trò:** Parquet lưu → Spark xử lý/học → FastAPI phục vụ → Next.js hiển thị → Recharts/Leaflet trực quan. Không Docker/HDFS ở bản hiện tại.

**Câu kết quả ngắn:** “Cải thiện MAE so baseline, nhưng sai số còn lớn; dùng tham khảo và công bố hạn chế.”

**Câu chuyển sang demo:** “Sau đây em dùng một nhu cầu cụ thể để đi từ tìm khu vực đến ước tính và kiểm tra độ tin cậy của kết quả.”

Không cần học thuộc toàn văn. Mỗi chặng nhớ ba điểm: đang mở gì, muốn chứng minh gì, giới hạn nào phải nói đúng.

## 12. Bản rút gọn nếu chỉ có 10–12 phút

| Phần | Phút |
|---|---:|
| Bài toán/phạm vi/kiến trúc | 1,5 |
| Nguồn và một job/query Spark | 1,5 |
| Split, model và metrics đã lưu | 2 |
| API load và chuyển sang web | 0,5–1 |
| Tìm vùng/so sánh + ước tính A/B | 3 |
| Một điểm sai số + một kiểm tra tin | 1 |
| Giới hạn/kết luận | 0,5–1 |

Không live train toàn bộ ở bản rút gọn. Có thể nói ngắn phần bản đồ vì đã xuất hiện trong Tìm khu vực; vẫn giải thích được vai trò nếu hỏi. Giữ slide/bằng chứng dự phòng cho toàn bộ phần chưa bấm.

## 13. Checklist luyện tập và hoàn thiện

1. Chạy trước toàn hành trình và đo thời gian, không chỉ đọc kịch bản.
2. A và B đổi vai, tự giải thích được nguồn, Spark UI, split, training/load, metrics và web.
3. Với mỗi chức năng: thao tác thành công → đọc kết quả → nêu ý nghĩa → nêu một giới hạn nếu cần. Không đọc nút thay nội dung.
4. Luyện các câu hỏi Docker/HDFS/local, vì sao LR, R²/MAE và dữ liệu sáp nhập.
5. Ghi lỗi/thời gian vào TEST_RESULT_TEMPLATE.md, sửa lời dẫn hoặc điều kiện demo cho nhất quán. Không ghi nhóm đã đạt nếu chưa diễn tập.
6. Khi tạo slide sau này: dùng sơ đồ/code/ảnh thật, font đọc được trên máy chiếu, số liệu từ artifacts; tên và phạm vi khớp plan Word. Không biến mọi lời dẫn trong file này thành chữ trên slide.
7. Chưa push GitHub cho đến khi cả hai trình bày được theo yêu cầu người dùng; không tự coi việc có tài liệu là nghiệm thu xong.

## 14. Tài liệu đối chiếu

- [Chạy từng terminal, thao tác Spark UI, nhánh ETL/train](../guide/DEMO_QUY_TRINH_SPARK.md).
- [Test theo chức năng](../guide/TESTER_CHECKLIST.md) và [mẫu ghi kết quả](../guide/TEST_RESULT_TEMPLATE.md).
- [Metrics đầy đủ](../research/KET_QUA_MO_HINH.md); JSON chuẩn nằm ở `artifacts/models/v1/results.json` tính từ root repo.
- [Plan Word ba cấp](PLAN_BAO_CAO_WORD_V1.md) và [vai trò map còn đề xuất](PLAN_VAI_TRO_BAN_DO_V1.md).
- Nội dung kỹ thuật đối chiếu code `src/etl`, `src/models`, `src/api`, `web` và manifest nguồn/core. Đây là kịch bản bám trạng thái hiện hành, chưa tạo thêm chức năng/slide hay huấn luyện lại.
