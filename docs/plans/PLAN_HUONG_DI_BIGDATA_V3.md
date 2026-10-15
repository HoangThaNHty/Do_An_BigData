> **Hướng thực hiện mới nhất 14/10/2026:** Người dùng đã yêu cầu dùng MCP để tiếp tục. Đọc [PLAN_TONG_HOP_UI_UX_V4.md](PLAN_TONG_HOP_UI_UX_V4.md) cho phạm vi, quy trình hai bản mẫu, tích hợp và nghiệm thu. Audit đã làm; brief MCP đang bắt đầu, chưa tạo thiết kế hoặc sửa app ở mốc lưu này.

> **Audit UI/UX 14/10/2026 đã hoàn thành, chưa sửa giao diện:** Đọc [KIEM_THU_UI_UX_2026_10_14.md](../history/KIEM_THU_UI_UX_2026_10_14.md), [BRIEF_THIET_KE_UI_UX_V3.md](BRIEF_THIET_KE_UI_UX_V3.md) và phần bổ sung [PLAN_CAI_THIEN_TRAI_NGHIEM_V3.md](../history/PLAN_CAI_THIEN_TRAI_NGHIEM_V3.md). Có bằng chứng về kết quả ngoài viewport, mất state và lỗi DNS tile; chưa chạy tạo thiết kế MCP.

> **Trao đổi mới 14/10/2026 — chưa triển khai:** Xem [PLAN_CAI_THIEN_TRAI_NGHIEM_V3.md](../history/PLAN_CAI_THIEN_TRAI_NGHIEM_V3.md) cho đề xuất bỏ tra địa danh khỏi luồng chính, làm rõ so sánh/ước tính, xử lý bản đồ online và cải thiện giải thích mô hình/ETL. Người dùng hiện chỉ yêu cầu lưu plan rồi trao đổi tiếp; không sửa code hoặc chạy tester theo đề xuất này.

> **Sản phẩm v2 đã triển khai 13/10/2026:** Đọc [NANG_CAP_SAN_PHAM_V2.md](../history/NANG_CAP_SAN_PHAM_V2.md), [KICH_BAN_DEMO_SAN_PHAM_V2.md](../history/KICH_BAN_DEMO_SAN_PHAM_V2.md) và mốc mới nhất ở [BAN_GIAO_CHO_MODEL_KHAC.md](../guide/BAN_GIAO_CHO_MODEL_KHAC.md). Các đoạn bên dưới giữ lịch sử; không dùng làm trạng thái mới nhất.

> **Bổ sung 13/10/2026:** Đọc [BAN_GIAO_CHO_MODEL_KHAC.md](../guide/BAN_GIAO_CHO_MODEL_KHAC.md) cho trạng thái thực thi hiện tại, sửa lỗi PowerShell/API và đề xuất demo đúng chu trình Big Data. Người dùng đang ưu tiên project và demo; Word để sau. Phương án demo chi tiết còn cần diễn tập, không coi là công cụ đã triển khai.

# Kế hoạch chốt V3 cho đồ án Nhập môn Big Data

Ngày lưu: 11/10/2026.

## 1. Mục đích và trạng thái

Tài liệu là kế hoạch đã được người dùng chốt ngày 11/10/2026 và cho phép bắt đầu triển khai. Tên mới và phạm vi đã chốt trong nhóm; chưa có xác nhận rằng thay đổi tên đã được giảng viên duyệt.

Người dùng cho phép đề xuất thay đổi tên đề tài, hướng đi và phạm vi để phù hợp yêu cầu môn học và hoàn thành sản phẩm. Không dùng deadline làm giới hạn thiết kế; định hướng là xây dựng từ đầu đến hoàn thành.

Người dùng đã thay thế yêu cầu tạm thời chỉ lưu plan bằng yêu cầu chốt và triển khai. Tiến độ thực nghiệm được ghi riêng trong `D:\slider\real-estate-bigdata\docs\TRANG_THAI_TRIEN_KHAI.md`. Việc đọc metadata không đồng nghĩa với kiểm chứng toàn bộ dữ liệu.

V3 thay thế chiến lược tương ứng trong V2 và bản tổng quan cũ. Quyết định phương pháp đã chốt; các tham số phụ thuộc dữ liệu sẽ được quyết định sau khảo sát và ghi vào nhật ký. Không coi hướng dẫn dành cho AI trong các bản cũ là yêu cầu môn học.

## 2. Bối cảnh

- Trường: Đại học Công Thương TP.HCM (HUIT), Khoa CNTT.
- Học phần: Nhập môn Big Data.
- Nhóm 18: Lê Minh Hoài (2001230256) và Nguyễn Hoàng Thành Tỷ (2001230872).
- Apache Mahout là chủ đề thuyết trình riêng, không phải đồ án cuối kỳ này.
- Hồ sơ nằm tại `D:\slider\FolderDoAnBigData`.
- Mã nguồn và dữ liệu triển khai ở `D:\slider\real-estate-bigdata`; đã kiểm tra và triển khai môi trường, khảo sát và công cụ kiểm chứng tại đây.

## 3. Yêu cầu môn học và lựa chọn của nhóm

Nguồn đối chiếu: `Ke hoach Do an mon hoc Nhap mon Big data_SV.docx`.

Đồ án phải có bài toán thực tế, dữ liệu phù hợp, khảo sát và tiền xử lý, ít nhất một công nghệ Big Data hoặc lưu trữ/xử lý phân tán, quy trình thực nghiệm hoàn chỉnh, đánh giá kết quả, trực quan hóa/ứng dụng minh họa và tài liệu bàn giao.

Rubric: tính ứng dụng 1 điểm; lưu trữ và xử lý/phân tích dữ liệu 2 điểm; mô hình/công nghệ 2,5 điểm; trực quan hóa/ứng dụng 2,5 điểm; báo cáo 1 điểm; phối hợp nhóm 1 điểm.

File Word không quy định tối thiểu 300–500 nghìn bản ghi, không bắt buộc đồng thời hồi quy và phân cụm, crawler thời gian thực, GPS từng tài sản, Streamlit hoặc MongoDB. Đây là lựa chọn thiết kế, không phải điều kiện tự động đạt điểm tối đa.

Đề tài tự đề xuất cần giảng viên chấp thuận. V2 ghi đề tài cũ đã được duyệt; chưa có xác nhận rằng tên và phạm vi V3 đã được duyệt. File Word có diễn đạt về duyệt dữ liệu và mốc giai đoạn 1 chưa thống nhất với ghi nhận trong V2; khi cần xác định yêu cầu nộp, đối chiếu chỉ dẫn thực tế của giảng viên.

## 4. Tên đề tài và mục tiêu đã chốt

Tên đã chốt để triển khai trong nhóm:

> Phân tích dữ liệu tin đăng và xây dựng hệ thống ước tính giá rao bán nhà ở tại TP. Hồ Chí Minh bằng Apache Spark

Lý do: nguồn là tin đăng; nhãn là giá rao bán, chưa phải giá giao dịch hay giá thẩm định. Nhà ở trong phạm vi mô hình chính gồm nhà riêng và căn hộ.

Ba câu hỏi nghiên cứu:

1. Giá rao bán và đơn giá khác nhau thế nào theo khu vực, loại nhà, diện tích và thời gian?
2. Mô hình dự đoán tốt hơn baseline giá trung vị bao nhiêu, ở những phân khúc nào?
3. Pipeline xử lý và ứng dụng cung cấp kết quả cho người dùng như thế nào?

Không đặt trước mức R² hoặc cam kết sai số khi chưa chạy thực nghiệm.

## 5. Phạm vi và dữ liệu

| Nội dung | Quyết định |
|---|---|
| Địa lý | TP.HCM theo địa danh thực tế trong dataset; ghi rõ phiên bản địa giới |
| Tài sản mô hình chính | Nhà riêng và căn hộ |
| Giao dịch | Tin rao bán nhận diện được; loại tin thuê và tin chưa đủ cơ sở phân loại |
| Nguồn chính | `oceanNG/vietnam-real-estates` |
| Nhãn | Tổng giá rao bán; thử biến đổi log khi huấn luyện |
| Đơn giá/m² | Phân tích, kiểm tra chất lượng và phương án đối chiếu |

Đất, biệt thự và shophouse chưa thuộc phạm vi mô hình chính. Khảo sát ban đầu có thể thống kê tất cả loại hình để xác định phạm vi, nhưng không mở rộng mô hình mặc định.

Metadata oceanNG đã đọc trực tuyến trong phiên trao đổi: 3.500.744 dòng, dung lượng tải 1.669.244.898 byte, 19 cột, `price` kiểu `float64`. Dataset card công bố 1.357.526 tin TP.HCM, thời gian 06/2025–03/2026 và giấy phép CC-BY-NC-4.0. Cập nhật triển khai: Spark đã đếm toàn bộ và xác nhận 1.357.526 tin TP.HCM, 842.922 tin nhà và 279.948 tin căn hộ. Schema Parquet thực tế có `price` là chuỗi, khác metadata float64; phải chuyển kiểu số rõ ràng trước so sánh và thống kê. Các số liệu được lưu tại artifacts/profile/profile.json trong dự án.

Dataset card ghi tin bán/cho thuê và có mô tả loại hình chưa nhất quán. Không tiếp tục khẳng định nguồn chỉ chứa tin bán. Schema đã đọc không có cột loại giao dịch riêng; cần khảo sát tiêu đề/mô tả và quy tắc phân loại, kiểm tra mẫu, ghi rõ phần không xác định được. Không suy ra tin bán chỉ từ giá lớn.

Các kiểm tra nền tảng:

- Giá tổng, giá theo m², tiền trả trước và tin giá thương lượng.
- Diện tích đất, diện tích sàn, diện tích sử dụng căn hộ; không coi chúng tương đương.
- Tỷ lệ thiếu, trùng và giá trị bất thường theo loại hình.
- Số mẫu sử dụng được theo thời gian và khu vực.
- Địa danh cũ/mới và tỷ lệ ghép với bảng địa lý.

Không dự báo trước số dòng sạch hoặc cố lọc để đạt một số lượng nhất định. Lưu số lượng và lý do loại sau từng bước. Không điền nhãn giá thiếu bằng trung vị để tạo dữ liệu huấn luyện.

## 6. Vai trò nguồn bổ sung

| Nguồn | Vai trò |
|---|---|
| Dữ liệu hành chính/ranh giới | Chuẩn hóa địa danh, bản đồ, đặc trưng vị trí khi phù hợp |
| Dataset GPS bổ sung | Minh họa vị trí; chỉ đối chiếu khi có căn cứ tương thích |
| Chợ Tốt | Minh họa ingestion và phân tích dữ liệu thu thập bổ sung |

Pipeline chính phải hoàn thành được bằng nguồn chính và dữ liệu địa lý phù hợp. Không trộn nguồn bổ sung vào huấn luyện trước khi đối chiếu đơn vị, thời gian, loại giao dịch, địa giới, diện tích và trùng lặp.

Không gọi dữ liệu crawler là thời gian thực nếu chỉ là ảnh chụp tại thời điểm thu thập. Demo phải dùng được dữ liệu đã lưu.

## 7. Kiến trúc

```text
Dữ liệu gốc
  -> Khảo sát, chuẩn hóa và kiểm tra chất lượng bằng PySpark/Spark SQL
  -> Dữ liệu sạch Parquet
  -> Chia train/validation/test theo thời gian
  -> Fit tiền xử lý và huấn luyện bằng Spark MLlib
  -> Đánh giá, lưu pipeline/mô hình và bảng tổng hợp
  -> Web Next.js + FastAPI + pipeline Spark đã lưu
```

Parquet là lớp lưu trữ chính cho ETL/ML. MongoDB phục vụ truy vấn ứng dụng nếu có nhu cầu cụ thể, không thêm chỉ để tăng số công nghệ. Nếu dùng, ưu tiên một collection có index phù hợp thay vì mặc định một collection mỗi quận.

Dashboard đọc bảng tổng hợp và pipeline đã lưu; không huấn luyện khi người dùng thao tác. Không đưa toàn bộ dữ liệu lớn vào bộ nhớ dashboard.

## 8. Tiền xử lý và đánh giá

Chuẩn hóa định dạng, kiểm tra hợp lệ và xử lý trùng trước; chia tập trước khi fit các bước học từ dữ liệu. Imputer, StringIndexer, OneHotEncoder và ngưỡng thống kê dùng cho mô hình phải học từ train. Áp dụng thống nhất cho validation/test và khi dự đoán.

Chia thời gian dự kiến, chỉ chốt sau khi kiểm tra phân bố dữ liệu:

- Train: 06–11/2025.
- Validation: 12/2025.
- Test: 01–03/2026.

Kiểm tra tin đăng lại/cùng tài sản giữa các tập. Nếu không có mã tài sản, dùng quy tắc nhận diện phù hợp và ghi rõ giới hạn. Không dùng giá thật của test để tạo features hoặc tối ưu mô hình. Không dùng `price_per_m2` làm feature khi nhãn là `price`.

Không dùng IQR chung cho mọi tài sản như một quy tắc loại tự động. Kết hợp kiểm tra hợp lệ, phân tích theo loại hình/khu vực và đánh giá tỷ lệ loại. Không loại tài sản hợp lệ chỉ vì giá cao. Tập test hợp lệ cần được giữ để phản ánh phạm vi ứng dụng; mọi tập đánh giá giới hạn thêm phải được mô tả riêng.

Giữ dữ liệu gốc, dữ liệu phục vụ phân tích và dữ liệu huấn luyện có định nghĩa rõ; thống kê thị trường không nên bị hiểu nhầm là thống kê chỉ trên phần dữ liệu đã cắt đuôi cho mô hình.

## 9. Mô hình

1. Baseline giá trung vị theo loại hình/khu vực, chỉ tính từ train, có phương án dự phòng nhóm ít mẫu.
2. Linear Regression.
3. Random Forest và GBT.
4. So sánh mô hình chung có loại hình với mô hình riêng cho nhà/căn hộ.

Thử nhãn `log(price)`; đánh giá sau quy đổi về giá tiền. Đối chiếu phương án dự đoán đơn giá nếu có lý do thực nghiệm, không mặc định tốt hơn.

Chọn mô hình bằng validation, sai số từng phân khúc, độ ổn định và chi phí chạy. Không mặc định GBT thắng. Bản đầu thử một số cấu hình nhỏ trên validation theo thời gian; không dùng k-fold thông thường như bằng chứng tự động chống rò rỉ thời gian.

Độ đo: MAE, RMSE, R² trên giá tiền; bổ sung sai số phần trăm với định nghĩa và xử lý giá nhỏ rõ ràng. Báo cáo theo loại nhà, khu vực và khoảng giá, kèm số mẫu. Test cuối chỉ dùng sau khi chọn phương án.

## 10. Địa lý và đặc trưng

Không join chỉ theo `ward_name`; dùng mã hoặc tổ hợp địa phương đã chuẩn hóa. Xác định phiên bản địa giới phù hợp với dataset; không cố định 168 phường ngay từ đầu.

Bản đồ quận/huyện làm trước; phường làm sau nếu ghép đáng tin cậy. Hiển thị trung vị đơn giá, loại hình, số tin và thông tin khu vực ít mẫu.

Tọa độ trọng tâm là vị trí đại diện, không phải GPS tài sản. Đặc trưng khoảng cách cần được thử bằng so sánh mô hình có/không có; không khẳng định trước chúng tăng hoặc không tăng độ chính xác.

Nếu chia độ rộng đường theo quartile, đặt tên nhóm Q1–Q4 hoặc nhóm độ rộng tương ứng. Không suy ra số làn xe/hẻm chỉ từ quartile. Chỉ sử dụng sau khi kiểm tra độ phủ và chất lượng `road_width`.

## 11. Sản phẩm web

| Màn hình | Nội dung |
|---|---|
| Tổng quan | Số tin, cơ cấu nhà/căn hộ, phân bố giá và diện tích |
| Khám phá thị trường | Biểu đồ, bảng so sánh theo loại nhà/khu vực/tháng và xuất bảng tổng hợp |
| Phân tích khu vực | Bản đồ trung vị đơn giá, số mẫu, bộ lọc địa phương/loại hình/thời gian |
| Ước tính giá | Nhập đặc điểm tài sản, trả giá dự đoán, phạm vi áp dụng và sai số đánh giá |
| Kết quả mô hình | So sánh baseline và mô hình, sai số theo phân khúc |
| Dữ liệu và phương pháp | Nguồn, thời gian, chất lượng, địa giới, phạm vi và giới hạn |

Sai số trên tập đánh giá không tự động là khoảng tin cậy cho một tài sản. Chỉ hiển thị khoảng dự đoán nếu đã xây dựng và kiểm chứng phương pháp tương ứng.

## 12. Môi trường

Cấu hình xử lý: PySpark 3.5.x + Java 17, Python tương thích và Parquet; MongoDB khi cần. Cập nhật phần web theo yêu cầu người dùng: Next.js + React + TypeScript + shadcn/ui/Tailwind; FastAPI nối dữ liệu và inference Spark; Leaflet cho bản đồ. OpenDesign hỗ trợ thiết kế. Chi tiết tại MUC_07_SAN_PHAM_WEB.md. Hướng này thay dashboard Streamlit + Folium ban đầu. Khóa phiên bản cụ thể sau kiểm tra chạy tối thiểu.

V2 ghi Spark 3.5 hỗ trợ Java 21 là không phù hợp danh sách hỗ trợ chính thức của Spark 3.5.7 (Java 8/11/17).

Spark local chạy song song trên một máy, không phải cụm nhiều máy. Báo cáo mô tả đúng môi trường thực nghiệm và khả năng mở rộng kiến trúc; không khẳng định không thể dùng Pandas chỉ dựa trên số dòng.

Giữ temp/shuffle/cache tải dataset trên ổ D khi thích hợp; đặt bộ nhớ driver từ lúc khởi chạy và kiểm tra cấu hình có hiệu lực. RAM, số core và dung lượng trống trong V2 là số liệu lịch sử, phải đo lại khi triển khai. Không bảo đảm hiệu năng chỉ dựa trên cấu hình máy.

Không cần Docker, Hadoop cluster hoặc Databricks cho bản chính theo hướng hiện tại.

## 13. Thứ tự thực hiện và tiêu chí hoàn thành

| Giai đoạn | Điều kiện hoàn thành |
|---|---|
| Khảo sát | Nhận diện tin bán, số mẫu, thiếu/trùng, ý nghĩa cột và phạm vi địa lý |
| ETL | Dữ liệu sạch, thống kê trước/sau, lý do loại, quy trình tái chạy |
| Mô hình đầu | Baseline và một mô hình Spark chạy bằng script, pipeline lưu/nạp và dự đoán được |
| Thực nghiệm | So sánh mô hình, đánh giá theo thời gian, phân tích sai số |
| Sản phẩm | Bản đồ, bộ lọc, pipeline lưu sẵn, hướng dẫn, demo bằng dữ liệu lưu sẵn |
| Bàn giao | Source, Word, PPT, nguồn dữ liệu, kết quả và phân công nhóm |

Ghi phương pháp, quyết định và kết quả ngay trong quá trình làm; hoàn thiện báo cáo/slide sau khi kết quả ổn định. Ghi nhật ký đóng góp thực tế, không gán tỷ lệ 50–50 nếu chưa có căn cứ.

Ưu tiên đã được người dùng xác nhận: hoàn thiện phần cốt lõi (kiểm chứng dữ liệu, ETL, địa lý/thống kê, baseline, huấn luyện, đánh giá và pipeline tái chạy) trước khi lập trình frontend/API. Phần web hiện chỉ đặc tả để thống nhất hướng sản phẩm; không dựng giao diện sớm hoặc cài công cụ thiết kế trong giai đoạn cốt lõi. Bắt đầu mục 07 khi có dữ liệu đã kiểm chứng, bảng tổng hợp có phạm vi rõ và mô hình đã đánh giá, lưu/nạp, dự đoán bằng script được. Nếu chất lượng chưa đạt, xử lý nguyên nhân hoặc áp dụng phương án thu hẹp phạm vi, không dùng web để che phần chưa hoàn thiện.

Vai trò dự kiến kế thừa: Hoài phụ trách dữ liệu/ETL/lưu trữ; Tỷ phụ trách ML/dashboard; cả hai làm tài liệu và phản biện. Cùng hiểu pipeline tổng thể để demo và trả lời câu hỏi.

## 14. Mở rộng và phương án dự phòng

Không bắt buộc trong sản phẩm chính: crawler Chợ Tốt, dataset GPS thứ hai, KMeans, bản đồ phường, tuning quy mô lớn. Chỉ bổ sung khi có đóng góp rõ và bản chính ổn định.

Nếu làm KMeans: chuẩn hóa đặc trưng phù hợp, thử số cụm, phân tích rồi mới đặt tên; không gán trước bốn phân khúc.

Phương án dự phòng:

- Nhà riêng không đủ chất lượng: chuyển mô hình chính sang căn hộ, chỉnh tên và báo cáo tương ứng.
- Ghép phường không tin cậy: giữ cấp khu vực phù hợp và công bố độ phủ.
- Mô hình phức tạp không vượt baseline: báo cáo trung thực, phân tích nguyên nhân và chọn phương án tốt nhất đã đo.
- Tài nguyên hạn chế: ETL toàn bộ dữ liệu phù hợp, huấn luyện mẫu có chiến lược và công bố cách lấy mẫu; mở rộng sau khi đo tài nguyên.
- Không nhận diện được tin bán đủ tin cậy: phải xem lại nguồn hoặc phạm vi trước khi tiếp tục mô hình giá bán.

## 15. Ba giải pháp đã chốt và điểm kiểm chứng

### 15.1. Nhận diện giao dịch

Dùng quy tắc ngữ cảnh trên tiêu đề/mô tả, ba nhãn `sale`, `rent`, `uncertain`, kèm mã lý do. Phân biệt bán tài sản đang cho thuê với tin cho thuê; tin bán hoặc thuê và giá trả trước chưa rõ tổng giá vào nhóm chưa xác định. Mức giá không tự quyết định loại giao dịch.

Tạo mẫu ngẫu nhiên và mẫu theo nhóm khó để gán nhãn thủ công. Tách mẫu hiệu chỉnh và mẫu đánh giá; đánh giá precision nhóm bán và tỷ lệ chưa xác định. Quy tắc ban đầu là bản ứng viên, không coi nhãn tự động là ground truth. Giữ mô tả tới khi phân loại/kiểm tra xong; chỉ loại khỏi features và dữ liệu tổng hợp nhẹ sau đó.

### 15.2. Diện tích

Ghi loại diện tích (`apartment`, `land`, `floor`, `unknown`), bằng chứng và độ tin cậy. Đối chiếu `area` với tiêu đề/mô tả khi có số liệu rõ. Không nhân diện tích với số tầng để tạo diện tích sàn. Không tự đồng nhất thông thủy với tim tường.

Nhà riêng ưu tiên diện tích đất xác định được; căn hộ sử dụng diện tích căn hộ. Giá trên m² đất của nhà bao gồm công trình, không gọi là giá đất thuần. Bản mô hình chính tách nhà/căn hộ; mô hình chung là thực nghiệm đối chiếu. Tin mâu thuẫn hoặc không xác định được diện tích chưa vào tập huấn luyện chính.

### 15.3. Địa lý

Giữ địa danh nguyên bản và chuẩn hóa riêng; chọn phiên bản tham chiếu phù hợp dataset. Ghép tỉnh + quận + phường hoặc mã đã xác minh; lưu trạng thái ghép. Không mở rộng phạm vi sang địa giới mới ngầm. Bản đồ quận làm trước; bản đồ phường sau khi kiểm chứng. Không tạo GPS giả; tọa độ đại diện được ghi rõ.

### 15.4. Những điều chưa được xác nhận bằng thực nghiệm

Số mẫu sạch, precision bộ quy tắc, loại diện tích thực tế, tỷ lệ ghép địa lý, ngưỡng xử lý, mô hình tốt nhất và độ chính xác phải đo khi triển khai. Không hỏi lại deadline. Không cần dừng để xin phép các bước cài đặt/tải dữ liệu/lập trình cần thiết đã được người dùng cho phép.

## 16. Nguồn kiểm chứng kỹ thuật

- Dataset card: https://huggingface.co/datasets/oceanNG/vietnam-real-estates/raw/main/README.md
- Metadata: https://datasets-server.huggingface.co/info?dataset=oceanNG/vietnam-real-estates
- Spark 3.5.7 và Java: https://spark.apache.org/docs/3.5.7/
- Tuning: https://spark.apache.org/docs/3.5.7/ml-tuning.html
- Cấu hình: https://spark.apache.org/docs/3.5.7/configuration.html

Đây là các nguồn đã đọc trong phiên trao đổi; metadata và dataset card không thay thế kiểm tra dữ liệu thực tế.

## 17. Hướng dẫn tiếp nhận ngữ cảnh

Đọc V3 trước để nắm phương án hiện tại, file Word để xác định yêu cầu môn học, bản tổng quan để hiểu bối cảnh nhóm. V2 và `de_xuat_do_an.md` giữ vai trò lịch sử ở các phần đã thay đổi.

Người dùng đã yêu cầu triển khai. Tiếp tục công việc theo V3 và nhật ký trạng thái, không quay về chiến lược V2. Không diễn đạt số liệu chưa đo lại hoặc tên mới như quyết định đã được giảng viên xác nhận. Báo cáo trung thực bước đã chạy, phần còn thiếu và hạn chế; không dùng nhãn tự động thay cho kiểm chứng thủ công.

## 18. Cập nhật hướng sản phẩm web

Người dùng muốn thiết kế giao diện web chi tiết, có thể sử dụng OpenDesign và template JCodesMore/ai-website-cloner-template. Đã chọn chạy trên máy/LAN trước, sau đó đưa lên Internet. Phương án kỹ thuật: Next.js/shadcn + FastAPI; giữ Spark cho ETL và mô hình. Phần web được đặc tả tại MUC_07_SAN_PHAM_WEB.md; chưa cài/frontend/API hoặc triển khai URL ở mốc cập nhật này.

Trao đổi về web là chuẩn bị phương án, không thay đổi thứ tự ưu tiên. Hoàn thiện mục 02–06 trước khi triển khai mục 07; tài liệu và nhật ký được cập nhật trong suốt quá trình.


## Bàn giao kỹ thuật 12/10/2026

Các mục core, mô hình và web local/LAN đã triển khai. Dùng HUONG_DAN_CHAY.md, KET_QUA_MO_HINH.md và mốc bàn giao đầu TRANG_THAI_TRIEN_KHAI.md để xem trạng thái hiện hành. Quyết định phương pháp trong kế hoạch giữ làm đối chiếu, không đổi sau khi xem test. Hồ sơ kỹ thuật ở deliverables; nhóm còn xác nhận tên với giảng viên và ghi công việc thực tế.
