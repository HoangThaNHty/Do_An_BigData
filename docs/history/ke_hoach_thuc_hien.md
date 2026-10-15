> Tài liệu lịch sử: kế hoạch hiện hành là PLAN_HUONG_DI_BIGDATA_V3.md, chốt ngày 11/10/2026. Giữ nội dung dưới đây để tham chiếu; không dùng các quyết định đã bị V3 thay thế làm đặc tả triển khai.

# KẾ HOẠCH CHI TIẾT THỰC HIỆN ĐỒ ÁN MÔN HỌC: NHẬP MÔN BIG DATA

## ĐỀ TÀI CHÍNH THỨC
**Phân tích dữ liệu lớn thị trường nhà ở và Xây dựng mô hình định giá bất động sản tự động tại TP. Hồ Chí Minh bằng Apache Spark**

* **Nhóm sinh viên thực hiện**:
  1. **Lê Minh Hoài** – MSSV: **2001230256**
  2. **Nguyễn Hoàng Thành Tỷ** – MSSV: **2001230872**
* **Trường**: Đại học Công Thương TP. Hồ Chí Minh (HUIT)
* **Thời gian thực hiện**: 10 tuần (theo kế hoạch đề cương học phần)

---

## 1. MỤC TIÊU VÀ SẢN PHẨM CẦN ĐẠT THEO BAREM HUIT (10 ĐIỂM)

| Tiêu chí Rubric | Điểm tối đa | Nhiệm vụ & Sản phẩm cụ thể cần đạt |
|:---|:---:|:---|
| **CLO1: Tính ứng dụng kỹ thuật** | **1.0đ** | Xác định bài toán thực tế nhức nhối về giá nhà đất tại TP.HCM. Giải pháp định giá tự động hỗ trợ người mua, người bán và ngân hàng thẩm định tài sản. |
| **CLO2: Lưu trữ & Xử lý dữ liệu phân tán** | **2.0đ** | - Thu thập 300.000 – 500.000 bản ghi tin đăng BĐS (Chợ Tốt REST API + Hugging Face).<br>- Lưu trữ trên MongoDB / HDFS / Parquet.<br>- Dùng PySpark DataFrame xử lý ngoại lệ (outlier), chuẩn hóa giá VND/m², mã hóa `StringIndexer` + `OneHotEncoder`. |
| **CLO3: Mô hình xử lý bài toán** | **2.5đ** | Tận dụng thư viện học máy phân tán **Spark MLlib**:<br>1. *Hồi quy định giá (Price Prediction)*: So sánh `LinearRegression`, `RandomForestRegressor`, `GBTRegressor` qua các độ đo RMSE, MAE, $R^2$.<br>2. *Phân cụm thị trường (Market Segmentation)*: Dùng `KMeans` phân nhóm phân khúc BĐS (nhà phố, chung cư, biệt thự, vùng ven). |
| **CLO3: Trực quan hóa & Ứng dụng** | **2.5đ** | Xây dựng Dashboard **Streamlit** trực quan:<br>- Bản đồ nhiệt GPS (Heatmap Folium/PyDeck) hiển thị phân bố giá nhà đất theo tọa độ thực tế tại các quận huyện TP.HCM.<br>- Form nhập thông số (Quận, Phường, Diện tích, Hướng, Số phòng) $\rightarrow$ Spark Model dự đoán khoảng giá hợp lý. |
| **CLO4: Trình bày báo cáo** | **1.0đ** | Soạn thảo Báo cáo Word đúng cấu trúc đề cương HUIT, văn phong khoa học, hình ảnh trích xuất rõ nét, đầy đủ tài liệu tham khảo. |
| **CLO5: Phối hợp làm việc nhóm** | **1.0đ** | Bảng phân công chi tiết công việc hàng tuần, nhật ký làm việc nhóm, mức độ đóng góp cân bằng 50% - 50%. |

---

## 2. PHÂN CÔNG VAI TRÒ GIỮA 2 THÀNH VIÊN

| Thành viên | Trách nhiệm chính (Lead) | Công việc phối hợp (Support) |
|:---|:---|:---|
| **Lê Minh Hoài**<br>(MSSV: 2001230256) | **Lead Data Engineering & Storage (CLO2)**:<br>- Thu thập dữ liệu API & Tích hợp dataset Hugging Face.<br>- Thiết kế cơ sở dữ liệu MongoDB / HDFS.<br>- Viết pipeline PySpark ETL (làm sạch, chuẩn hóa, lọc outlier). | Hỗ trợ đánh giá mô hình học máy và kiểm thử độ đo RMSE/MAE. |
| **Nguyễn Hoàng Thành Tỷ**<br>(MSSV: 2001230872) | **Lead Machine Learning & Dashboard (CLO3)**:<br>- Xây dựng và huấn luyện mô hình Spark MLlib (`RandomForestRegressor`, `GBTRegressor`, `KMeans`).<br>- Phát triển giao diện Web Dashboard Streamlit (Bản đồ GPS Heatmap + Form định giá). | Hỗ trợ kiểm thử pipeline tiền xử lý và tích hợp model vào web. |
| **Cả 2 thành viên** | - Viết báo cáo Word Giai đoạn 1 và Giai đoạn 2.<br>- Thiết kế Slide thuyết trình PPT và chuẩn bị kịch bản thuyết trình tuần 10. |

---

## 3. LỘ TRÌNH THỰC HIỆN 10 TUẦN (THEO MỐC ĐỀ CƯƠNG HUIT)

```text
Tuần 1-3          Tuần 4-5          Tuần 6-7          Tuần 8-9          Tuần 10
[ĐĂNG KÝ ĐỀ TÀI] ──> [CƠ SỞ LÝ THUYẾT] ──> [NỘP BÁO CÁO GĐ1] ──> [NỘP HOÀN CHỈNH GĐ2] ──> [THUYẾT TRÌNH]
- Chốt tên đề tài  - Nghiên cứu Spark  - Baseline model   - Hoàn thiện Spark MLlib  - Báo cáo trước lớp
- Crawl thử data   - Thiết kế MongoDB  - Viết Word GĐ1    - Xây dựng Dashboard      - Q&A Hội đồng
- Lập kế hoạch     - Pipeline PySpark                     - Hoàn thiện Word & PPT
```

### 📍 Giai đoạn 1: Chuẩn bị, Thu thập dữ liệu & Báo cáo tiến độ (Tuần 1 – 6)
* **Tuần 1 – 3: Khởi tạo & Đăng ký**
  * Nộp mẫu đăng ký đề tài gửi giảng viên duyệt.
  * Thiết lập môi trường: Python 3.11, PySpark 3.5, MongoDB.
  * Chạy crawler Chợ Tốt API mở rộng ra toàn bộ các quận huyện TP.HCM và các tỉnh lân cận.
* **Tuần 4 – 5: Kiến trúc & Tiền xử lý dữ liệu (CLO2)**
  * Nghiên cứu cơ sở lý thuyết: Kiến trúc Apache Spark, RDD, DataFrame, Spark MLlib, MongoDB.
  * Xây dựng script PySpark ETL:
    - Xử lý giá tiền (chuyển đổi đơn vị, chuẩn hóa về triệu VND/m²).
    - Xử lý giá trị khuyết (Imputation: điền giá trị thiếu cho hướng nhà, số tầng).
    - Lọc bỏ tin rác/ngoại lệ bằng phương pháp phân vị (IQR) trên Spark.
  * Nạp dữ liệu đã làm sạch vào MongoDB / Parquet.
* **Tuần 6 – 7: Xây dựng mô hình Baseline & NỘP BÁO CÁO TIẾN ĐỘ GIAI ĐOẠN 1 (Mốc chấm điểm 1)**
  * Huấn luyện mô hình thử nghiệm ban đầu (Linear Regression baseline).
  * Viết báo cáo tiến độ Giai đoạn 1 theo mẫu Word của HUIT.
  * Nộp bài Giai đoạn 1 trên Google Classroom đúng hạn.

---

### 📍 Giai đoạn 2: Hoàn thiện Học máy, Trực quan hóa & Đóng gói (Tuần 7 – 9)
* **Tuần 8: Huấn luyện mô hình tối ưu & Đánh giá (CLO3 - ML)**
  * Huấn luyện các mô hình nâng cao: `RandomForestRegressor` và `GBTRegressor` (Gradient Boosted Trees).
  * Tinh chỉnh siêu tham số (*Hyperparameter Tuning*) bằng `CrossValidator` và `ParamGridBuilder` trong Spark MLlib.
  * Phân cụm `KMeans`: Phân nhóm thị trường bất động sản thành các cụm (Cao cấp, Trung cấp, Bình dân, Đất nền vùng ven).
  * Đánh giá và so sánh kết quả bằng các chỉ số: RMSE, MAE, $R^2$, Silhouette Score.
* **Tuần 9: Phát triển Dashboard Web & NỘP BÁO CÁO HOÀN CHỈNH GIAI ĐOẠN 2 (Mốc chấm điểm 2)**
  * Lập trình ứng dụng Streamlit:
    - Tab 1: Bản đồ nhiệt bất động sản TP.HCM theo tọa độ GPS thực tế.
    - Tab 2: Phân tích xu hướng giá nhà đất theo quận/huyện, loại hẻm và diện tích.
    - Tab 3: Công cụ định giá nhà đất thông minh (nhập thông số $\rightarrow$ trả về giá ước tính và độ tin cậy).
  * Hoàn thiện toàn bộ: Mã nguồn sạch, File Word báo cáo hoàn chỉnh (đầy đủ các chương theo barem HUIT), File Slide thuyết trình PPT.
  * Nộp bài Giai đoạn 2 trên Google Classroom.

---

### 📍 Giai đoạn 3: Thuyết trình & Bảo vệ đồ án (Tuần 10)
* **Tuần 10: Thuyết trình cuối kỳ**
  * Thuyết trình trước lớp và giảng viên (thời lượng 10 – 15 phút).
  * Phân chia người nói: Hoài trình bày Phần 1 (Bối cảnh, Lưu trữ & Pipeline PySpark); Tỷ trình bày Phần 2 (Mô hình Spark MLlib & Demo trực tiếp Dashboard).
  * Trả lời các câu hỏi vấn đáp phản biện từ giảng viên.
