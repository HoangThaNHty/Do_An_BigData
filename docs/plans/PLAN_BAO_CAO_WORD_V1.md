# Plan báo cáo Word cuối kỳ — bản chốt cấu trúc v2

Ngày: 15/10/2026. **Đã hoàn thiện cấu trúc ba cấp theo yêu cầu mới; chưa soạn lại Word/PPT, chưa sửa/xóa chức năng web.** Giữ tên file V1 để các link bàn giao vẫn dùng được; nội dung hiện hành là v2.

Repo: `D:\slider\real-estate-bigdata`; tài liệu: `D:\slider\FolderDoAnBigData`.

## 1. Căn cứ yêu cầu

Đã đọc nội dung file `tai_lieu_mon_hoc/Ke hoach Do an mon hoc Nhap mon Big data_SV.docx` trong folder tài liệu. Môn yêu cầu source, Word, PPT và demo; ít nhất một công nghệ Big Data; mô tả dữ liệu, tiền xử lý, kiến trúc/luồng dữ liệu, cài đặt, thực nghiệm, đánh giá, trực quan hóa và hướng dẫn chạy.

Cấu trúc yêu cầu: **bìa → lịch làm việc nhóm hằng tuần → công việc từng thành viên → mục lục → giới thiệu đề tài → cơ sở lý thuyết → xây dựng ứng dụng/trực quan hóa dữ liệu → kết luận/định hướng → tài liệu tham khảo → phụ lục nếu có**.

File môn học chưa quy định font, cỡ chữ, lề, giãn dòng, số trang hoặc IEEE. Times New Roman và IEEE là yêu cầu người dùng; thông số dưới đây là đề xuất, thay bằng mẫu chính thức nếu nhóm cung cấp thêm. Không gọi đề xuất này là chuẩn trường đã xác nhận.

Tên đề tài đề xuất: “Phân tích dữ liệu tin đăng và xây dựng hệ thống ước tính giá rao bán nhà ở tại TP. Hồ Chí Minh bằng Apache Spark”. Chưa xác nhận giảng viên duyệt. Lớp, giảng viên, nhật ký thực tế và đóng góp do nhóm xác nhận trước khi hoàn thiện; không bịa lịch sử làm việc.

## 2. Plan kiểm tra toàn project trước khi soạn

| Phần | Kiểm tra | Bằng chứng |
|---|---|---|
| Yêu cầu môn | Từng yêu cầu có chương/sản phẩm/demo tương ứng | Ma trận yêu cầu–nội dung–bằng chứng |
| Dataset | Revision, giấy phép, schema, số dòng, phạm vi | Manifest, dataset card, metadata Parquet |
| ETL/cohort | Thiếu/trùng/ngoại lệ, tin thuê/trả trước, địa danh, loại ID review, chia thời gian | Code, manifest ETL/core, quality report |
| ML | Feature, fit train, baseline, tham số, chọn validation, đánh giá test | features.py, train.py, selection/results JSON |
| Inference | Pipeline thật, dải giá, validation input, giá cân nhắc chỉ đối chiếu | inference.py, fixture, kiểm thử API |
| Web | Sáu trang, lọc, so sánh vùng/căn, map, mobile, lỗi/rỗng | Checklist + ảnh ứng dụng thật |
| Bàn giao | Clone Windows/setup/dependencies/model/serving/ignore | Biên bản REPO_GITHUB_NGHIEM_THU.md và receipts |
| Hồ sơ cũ | Word/PPT là snapshot trước UI V4 | Danh sách nội dung/hình cần cập nhật |

Không cần huấn luyện lại chỉ để viết báo cáo; chỉ chạy lại khi có thay đổi hoặc thiếu bằng chứng, không đổi kết quả test đã khóa. Phân biệt những kiểm thử đã làm với các kiểm thử cần làm theo plan này.

## 3. Mục lục chốt ba cấp

Phần đầu: bìa; lịch làm việc hằng tuần; công việc/đóng góp từng thành viên; mục lục tự động; danh mục hình; danh mục bảng; danh mục ký hiệu/viết tắt. Chưa tự thêm lời cam đoan/nhận xét của giảng viên như yêu cầu bắt buộc nếu mẫu môn không có.

Các dòng dưới là outline, không phải những đoạn đã viết xong. Khi tạo Word, cấp chương = Heading 1, x.y = Heading 2, x.y.z = Heading 3. Các số trong plan là đặc tả; trong DOCX phải dùng numbering tự động. Mỗi mục cấp hai có ít nhất hai mục con có nội dung riêng, không tạo mục con duy nhất cho đủ hình thức; tối đa ba cấp trong mục lục.

### 1. Giới thiệu đề tài

**1.1 Bối cảnh và vấn đề nghiên cứu**

- 1.1.1 Đặc điểm dữ liệu tin đăng nhà ở và nhu cầu khai thác.
- 1.1.2 Vấn đề giá rao, chất lượng tin và hỗ trợ tra cứu/ước tính.

**1.2 Mục tiêu và giá trị của đề tài**

- 1.2.1 Mục tiêu xử lý dữ liệu và xây dựng mô hình.
- 1.2.2 Người dùng, đầu ra sản phẩm và tiêu chí đạt.

**1.3 Đối tượng và phạm vi nghiên cứu**

- 1.3.1 Loại bất động sản và phạm vi TP.HCM theo địa bàn lịch sử.
- 1.3.2 Thời gian dữ liệu, giá rao và giới hạn suy rộng.
- 1.3.3 Phạm vi công nghệ và triển khai local/LAN.

**1.4 Phương pháp thực hiện và bố cục**

- 1.4.1 Các bước nghiên cứu và phương pháp thực nghiệm.
- 1.4.2 Sản phẩm bàn giao và tổ chức báo cáo.

### 2. Cơ sở lý thuyết

**2.1 Dữ liệu lớn và lựa chọn công nghệ**

- 2.1.1 Khái niệm, đặc trưng dữ liệu lớn và liên hệ dataset thực tế.
- 2.1.2 Vai trò Apache Spark, local mode và phân biệt HDFS/Docker.

**2.2 Lưu trữ và xử lý dữ liệu có cấu trúc**

- 2.2.1 Parquet, schema, kiểu dữ liệu và tổ chức file/partition.
- 2.2.2 Spark SQL/DataFrame, lazy evaluation và transformations/actions.
- 2.2.3 Job, stage, task và quan sát bằng Spark UI.

**2.3 Tiền xử lý và pipeline học máy**

- 2.3.1 Dữ liệu thiếu, ngoại lệ, trùng lặp và chuẩn hóa.
- 2.3.2 Biến đổi log, imputation, encoding và scaling.
- 2.3.3 Chia thời gian, fit trên train và phòng tránh rò rỉ.

**2.4 Các phương pháp hồi quy được sử dụng**

- 2.4.1 Baseline trung vị theo nhóm.
- 2.4.2 Linear Regression và regularization.
- 2.4.3 Random Forest Regression.
- 2.4.4 Gradient-Boosted Tree Regression.

**2.5 Đánh giá và diễn giải kết quả**

- 2.5.1 MAE, RMSE và R².
- 2.5.2 MAPE, Median APE và phân tích sai số theo nhóm.
- 2.5.3 Dải tham khảo hiệu chỉnh trên validation và coverage.

**2.6 Nền tảng xây dựng ứng dụng web**

- 2.6.1 FastAPI, API/proxy và nạp mô hình để suy luận.
- 2.6.2 Next.js, thành phần giao diện, Recharts và Leaflet.

### 3. Xây dựng ứng dụng, thực nghiệm và trực quan hóa dữ liệu

**3.1 Phân tích yêu cầu và thiết kế hệ thống**

- 3.1.1 Người dùng, chức năng và các hành trình chính.
- 3.1.2 Kiến trúc, luồng dữ liệu, tầng lưu trữ và các sơ đồ thiết kế.
- 3.1.3 Môi trường thực nghiệm và triển khai Windows/local/LAN.

**3.2 Bộ dữ liệu và khảo sát ban đầu**

- 3.2.1 Nguồn, revision, giấy phép, quy mô và schema 19 trường.
- 3.2.2 Chọn phạm vi, đặc điểm thời gian/địa danh và dữ liệu thiếu.
- 3.2.3 Phân bố giá/diện tích, ngoại lệ và giới hạn nguồn.

**3.3 ETL và xây dựng tập nghiên cứu**

- 3.3.1 Nhận diện tin và chuẩn hóa, kiểm tra chéo giá/diện tích.
- 3.3.2 Routing/cách ly, review tham chiếu AI và loại ID đã đọc.
- 3.3.3 Proxy đăng lại, địa bàn và cohort cuối.
- 3.3.4 Chia tập theo thời gian và kiểm chứng số lượng.

**3.4 Huấn luyện và lựa chọn mô hình**

- 3.4.1 Chuẩn bị feature và fit tiền xử lý trên train.
- 3.4.2 Baseline, chín pipeline và bộ tham số thực nghiệm.
- 3.4.3 Chọn theo validation, khóa test và xây dựng dải giá.
- 3.4.4 Lưu/nạp pipeline và quy trình suy luận trong API.

**3.5 Kết quả thực nghiệm và phân tích**

- 3.5.1 Bảng so sánh baseline/LR/RF/GBT, riêng loại nhà và chung.
- 3.5.2 Kết quả test, scatter và phân tích sai số theo nhóm.
- 3.5.3 Ngoại lệ, coverage, thiên lệch chọn mẫu và giới hạn diễn giải.

**3.6 Sản phẩm web và trực quan hóa**

- 3.6.1 Tổng quan tập tin và bộ lọc.
- 3.6.2 Tìm khu vực theo nhu cầu và so sánh vùng.
- 3.6.3 Bản đồ, lớp màu và chi tiết địa bàn.
- 3.6.4 Ước tính giá rao, đối chiếu giá cân nhắc và so sánh hai căn.
- 3.6.5 Khám phá sai số mô hình.
- 3.6.6 Dữ liệu/phương pháp và kiểm tra một tin bằng Spark.

Tên/nội dung 3.6.3 khớp chức năng đã nghiệm thu khi viết. Không mô tả hướng nâng cấp bản đồ theo tháng như đã có nếu chưa triển khai; nếu gộp trang thì cập nhật outline tương ứng.

**3.7 Kiểm thử và tổ chức demo**

- 3.7.1 Kiểm thử API, đối chiếu dữ liệu và mô hình.
- 3.7.2 Kiểm thử hành trình UI/UX, mobile và trạng thái lỗi/offline.
- 3.7.3 Setup/clone Windows, giới hạn môi trường và bằng chứng nghiệm thu.
- 3.7.4 Demo nguồn → Spark → split → train/đánh giá → nạp model → web.

### 4. Kết luận và định hướng phát triển

**4.1 Kết quả đạt được**

- 4.1.1 Đối chiếu mục tiêu và yêu cầu môn học.
- 4.1.2 Giá trị của quy trình dữ liệu, mô hình và sản phẩm.

**4.2 Hạn chế**

- 4.2.1 Nguồn dữ liệu, nhãn tham chiếu, địa danh và thời gian.
- 4.2.2 Sai số mô hình, local mode và phạm vi kiểm thử.

**4.3 Hướng phát triển**

- 4.3.1 Nhãn người độc lập, cập nhật dữ liệu và cải thiện mô hình.
- 4.3.2 Hoàn thiện sản phẩm, triển khai Internet và mở rộng hạ tầng khi cần.

**Tài liệu tham khảo**: không đánh số thành chương 5; danh sách nguồn IEEE theo thứ tự trích dẫn.

**Phụ lục**: A — từ điển dữ liệu/quy tắc; B — tham số/bảng thực nghiệm; C — testcase/ảnh giao diện bổ sung; D — sơ đồ lớn/hướng dẫn tái hiện. Các mục phụ lục dùng A.1/A.2 nếu cần, không tiếp tục chuỗi số chương như nội dung chính.

Khung bốn chương bám yêu cầu gốc. Chương 2 giải thích nguyên lý và công thức; chương 3 trình bày cách áp dụng/tham số/kết quả thật, tránh chép lại lý thuyết. Chương 1 nêu phạm vi, chương 4 đánh giá giới hạn thay vì lặp nguyên văn. Không ép số trang hoặc kéo dài bằng ảnh; giữ sơ đồ chính trong chương phù hợp, chuyển bảng dài/ảnh bổ sung xuống phụ lục.

Trước khi soạn: mỗi mục cấp ba phải có nội dung/bằng chứng cụ thể; không để mục rỗng hoặc tách mục chỉ một câu. TOC, danh mục hình/bảng là các phần khác nhau; danh mục lấy từ caption chứ không tự gõ.

## 4. Định dạng đề xuất

| Thành phần | Phương án |
|---|---|
| Trang | A4; trái 3 cm, phải 2 cm, trên/dưới 2,5 cm |
| Văn bản | Times New Roman 13 pt, đen, căn đều, dòng 1,5; đầu dòng 1 cm; sau đoạn 6 pt |
| Heading 1 | 16 pt đậm, bắt đầu trang mới; số tự động 1, 2, 3 |
| Heading 2/3 | 14/13 pt đậm; số tự động 1.1 / 1.1.1; giữ với đoạn sau |
| Bảng | 11–12 pt nếu cần; lặp tiêu đề, có đơn vị; tránh tách hàng ngắn |
| Caption | 12 pt; tên bảng phía trên, tên hình phía dưới; số theo chương |
| Công thức | Equation Word có thể chỉnh sửa, số theo chương; ký hiệu/đơn vị rõ |
| Mã/lệnh | Consolas 10–11 pt trong đoạn mã |
| Trang | Bìa không hiện số; phần đầu La Mã; nội dung từ 1; tham khảo/phụ lục tiếp tục Ả Rập |

Font TNR cho văn bản, font toán của Word cho ký hiệu cần thiết. Liên kết Heading 1/2/3 với multilevel list, không gõ số mục tay. TOC tự động ba cấp; Caption/SEQ và cross-reference tự động; danh mục hình/bảng từ caption. Section break cho kiểu số trang/landscape khi cần. Cập nhật mọi field sau sửa cuối rồi kiểm tra trang thực, không để mục lục giả/số trang dự đoán.

## 5. Danh sách sơ đồ/biểu đồ

| Mã | Nội dung | Điều phải chính xác |
|---|---|---|
| S01 | Kiến trúc tổng thể | Parquet → Spark ETL/ML → artifact → FastAPI → Next.js; training khác inference |
| S02 | Luồng dữ liệu/tầng lưu trữ | Raw → ETL → cohort → model/serving → API, số dòng đúng bước |
| S03 | Quyết định kiểm tra tin | Tin bán/thuê/trả trước/không rõ và điều kiện chuẩn hóa thật |
| S04 | Timeline split | Train 06–11/2025, val 12/2025, test 01–03/2026; loại ID review/proxy đăng lại |
| S05 | Pipeline ML | Fit tiền xử lý trên train, transform val/test, chọn trên val, khóa test |
| S06 | Sequence ước tính | Web/proxy → API → pipeline nạp sẵn → giá/dải/cảnh báo; giá cân nhắc không làm feature |
| S07 | Triển khai local/LAN | Một máy chạy API/Next/Spark JVM, máy nhóm mở browser; cổng/tài nguyên đúng |
| B01 | Số lượng sau các bước | Manifest thật, không ghép mẫu số khác phạm vi |
| B02 | Phân bố giá/diện tích/vùng/tháng | Có đơn vị/cỡ mẫu, giải thích trục log nếu dùng |
| B03 | So sánh mô hình | Val/test tách rõ, baseline, đầy đủ chỉ số |
| B04 | Scatter/sai số/nhóm | Đường y=x, residual/APE, ngoại lệ và nhóm ít mẫu |
| B05 | Dải tham khảo | Calibration val và coverage test thật |

Không vẽ MongoDB/HDFS/cụm nhiều máy/mạng neural như thành phần đang chạy. Đây là ML hồi quy tabular, không phải deep learning. Lưu source sơ đồ Mermaid/SVG; biểu đồ từ artifact thật, vector hoặc PNG 300 dpi; kiểm tra chữ rõ khi in A4. Hình mượn nguồn phải trích dẫn; hình nhóm tự vẽ ghi nhóm thực hiện.

## 6. Công thức cần kiểm chứng

y: giá rao nguồn đã chuẩn hóa VND; y_hat: dự đoán VND; n: số mẫu; y>0. Khi soạn DOCX dùng Equation Word, các biểu thức sau chỉ là đặc tả plan:

- z=ln(y), feature có ln(area); LR: z_hat=b+beta^T x; y_hat=exp(z_hat). Regularization đối chiếu Spark 3.5.7 với regParam=0.05, elasticNetParam=0; không gọi exp(log-prediction) là kỳ vọng giá không chệch.
- Imputer median fit train; StandardScaler **withMean=False, withStd=True**. Không mô tả trừ trung bình khi code không làm.
- MAE=sum(|y_hat-y|)/n; RMSE=sqrt(sum((y_hat-y)^2)/n).
- R²=1-SSE/SST; SST=sum((y-mean(y))²); SST=0 không xác định; R² có thể âm và không phải “% chính xác”.
- APE_i=|y_hat_i-y_i|/y_i; MAPE=100×mean(APE); Median APE=100×median(APE). Code median dùng percentile_approx; JSON lưu tỉ lệ, bảng % nhân 100.
- Baseline trung vị theo loại nhà/khu vực trên train, nhóm tối thiểu 20 tin; fallback trung vị loại nhà.
- q=percentile_90(|ln(y)-ln(y_hat)|) trên validation; dải=[y_hat×exp(-q), y_hat×exp(q)]; coverage test là tỉ lệ y nằm trong dải. Không cam kết 90% cho từng căn.
- Giảm MAE=100×(MAE_baseline-MAE_model)/MAE_baseline.

RF/GBT giải thích ensemble/loss/tham số đúng regression implementation; dẫn nguồn chính thức/học thuật, không dùng công thức classification thay regression. Wilson review chỉ dùng khi giải thích kiểm tra mẫu và hạn chế nhãn AI; không diễn giải 98/100 là chất lượng toàn dataset. Mỗi công thức có ký hiệu/đơn vị/ý nghĩa/nguồn và vị trí áp dụng; nghiệm thu đối chiếu với code, không chỉ xem trình bày.

## 7. Số liệu và giới hạn khóa

- Raw 3.500.744 dòng/19 trường/10 shard; HCM nhà-căn hộ 1.122.870; cohort 133.779. Train 78.048, val 17.886, test 37.845.
- Chín pipeline LR/RF/GBT riêng nhà, riêng căn hộ và chung, thêm baseline; chọn house_lr/apartment_lr theo MAE val. Nguồn chuẩn results.json/selection.json trong artifacts/models/v1.
- MAE test nhà 2,950 tỷ/căn hộ 1,395 tỷ phải kèm RMSE/R²/APE/ngoại lệ; coverage 90,12%/86,00%, không khái quát đảm bảo cá thể.
- Review tham chiếu AI chưa là nhãn người độc lập; proxy toàn văn chưa loại hết tin cùng tài sản đổi nội dung; giá rao chưa xác minh giao dịch.
- Tin 06/2025–03/2026 có cả trước/sau sáp nhập; phân tích theo HCM trước hợp nhất/22 nhóm lịch sử, không bao phủ Bình Dương/Bà Rịa–Vũng Tàu cũ, không là giá hiện tại 10/2026.
- Spark 3.5.7/Python 3.11/JDK17. Thực nghiệm train local[4]/4 GB; demo API/inference mặc định 2 GB sau sửa bộ nhớ. API 1.2.1/UI V4.
- Web thống kê có phần đọc serving bằng PyArrow, inference/thử quy tắc dùng Spark thật. Không nói mọi request thống kê tạo Spark job.

## 8. Plan chụp ảnh và kiểm thử demo

Chụp ứng dụng thật **sau khi chốt chức năng**, không dùng prototype Open Design làm bằng chứng chạy được. Dùng MCP browser/desktop nếu khả dụng; nếu không có phiên công cụ phù hợp, dùng Playwright/Edge local, ghi đúng công cụ thực tế. Hiện chưa chụp lại theo plan này.

Ảnh cần có: tổng quan; tìm theo ngân sách/diện tích; so sánh 2–3 vùng; map/lớp/chi tiết; form và giá/dải; đối chiếu giá cân nhắc; lưu A rồi đổi input/dự đoán B; chọn điểm sai số; pipeline và ba ví dụ bán/thuê/trả trước; Spark UI sau action thật; map offline. Mobile/lỗi/rỗng để phụ lục nếu hữu ích.

Mỗi ảnh kèm case/bước/input/kỳ vọng/thực tế/ngày/phiên bản. Thực sự bấm và xác nhận chức năng; không chụp chỉ vì có nút. Chữ rõ, không cắt viewport/modal, không lộ thông tin riêng. Trước chụp kiểm tra health/một JVM/model frozen/mạng tile. Offline polygon là fallback thật khi mạng lỗi. Spark UI cổng 4040 chỉ là mặc định lúc SparkContext sống; kiểm tra URL thực.

## 9. Trích dẫn IEEE

Nguồn dùng [1], [2]… theo lần xuất hiện đầu; một nguồn giữ một số; dẫn gần phát biểu/công thức/hình. IEEE ở đây là kiểu trích dẫn, không yêu cầu báo cáo hai cột.

Lập sổ nguồn gồm tác giả/tổ chức, tên, năm/phiên bản, URL/DOI thật, ngày truy cập, phần được dùng và giấy phép. Ưu tiên nguồn chính thức và nghiên cứu gốc; không dựng DOI/tác giả/năm. Kết quả nhóm ghi artifact/lần chạy, không gán cho nguồn ngoài. Dataset/admin/boundary ghi công đúng THIRD_PARTY_NOTICES.md.

Nguồn đối chiếu ban đầu, kiểm tra ngày 15/10/2026 (chưa đánh số IEEE cuối vì chưa có bản thảo):

- https://spark.apache.org/docs/3.5.7/sql-programming-guide.html
- https://spark.apache.org/docs/3.5.7/ml-classification-regression.html
- https://spark.apache.org/docs/3.5.7/monitoring.html
- https://journals.ieeeauthorcenter.ieee.org/wp-content/uploads/sites/7/IEEE_Reference_Guide.pdf (có thể redirect sang tài liệu cập nhật)
- https://support.microsoft.com/en-gb/word/number-your-headings
- https://support.microsoft.com/en-gb/word/training/insert-a-table-of-contents?nochrome=true

## 10. Quy trình và nghiệm thu

1. Audit yêu cầu–repo–bằng chứng, chốt vai trò map.
2. Khóa outline, số liệu, nguồn, styles; metadata bìa/lịch nhóm xác nhận ở bước hoàn thiện.
3. Soạn nội dung/công thức; tạo sơ đồ/biểu đồ thật.
4. Test hành trình, chụp ảnh, lập danh mục bằng chứng.
5. Tạo DOCX có numbering/TOC/caption/cross-reference; cập nhật field trong Word, xuất PDF.
6. Render kiểm tra **tất cả trang**: font, mục lục/số trang, bảng tràn, hình mờ/cắt, công thức, đoạn cô lập, trang trắng và nguồn.
7. Đối chiếu Word–slide–README–demo cùng tên/số liệu/phiên bản/giới hạn rồi mới đóng gói.

Đầu ra: DOCX/PDF, nguồn sơ đồ, ảnh/biểu đồ, sổ nguồn, ma trận yêu cầu và checklist nghiệm thu. Build/raw ảnh giữ theo chính sách repo, không mặc định đưa mọi file lớn lên Git.

Đạt khi đủ mục môn, số liệu truy vết, công thức đúng code, không phóng đại công nghệ, TOC/danh mục cập nhật được, demo chức năng thật, hình/bảng đọc được A4, không bịa metadata/đóng góp.

## 11. Còn trao đổi

Vai trò map xem PLAN_VAI_TRO_BAN_DO_V1.md, chưa sửa. Format trên là mặc định nếu không có mẫu khác. Chưa cần hỏi bìa để dừng audit/phương pháp. Không thêm MongoDB/HDFS/deep learning chỉ để nhiều tên công nghệ; Spark đáp ứng ít nhất một công nghệ theo file môn.
