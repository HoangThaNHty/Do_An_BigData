> Tài liệu lịch sử: kế hoạch hiện hành là PLAN_HUONG_DI_BIGDATA_V3.md, chốt ngày 11/10/2026. Giữ nội dung dưới đây để tham chiếu; không dùng các quyết định đã bị V3 thay thế làm đặc tả triển khai.

# HỒ SƠ TỔNG QUAN DỰ ÁN ĐỒ ÁN CUỐI KỲ: NHẬP MÔN BIG DATA (HUIT)
> **Tài liệu bàn giao & Context chuẩn dành cho các AI Models / Thành viên nhóm**
> *Phiên bản: 1.0 (Cập nhật: 10/2026)*

---

## 📌 PHẦN 1: THÔNG TIN HÀNH CHÍNH & BỐI CẢNH HỌC PHẦN

* **Cơ sở đào tạo**: Trường Đại học Công Thương TP. Hồ Chí Minh (**HUIT**).
* **Khoa**: Công nghệ Thông tin.
* **Học phần**: **Nhập môn Big Data** (Đồ án môn học chiếm 50% tổng điểm).
* **Giảng viên hướng dẫn (GVHD)**: Thầy/Cô phụ trách học phần (Ví dụ: Thầy Ngô Dương Hà theo lịch phân công).
* **Nhóm sinh viên thực hiện (Nhóm 18)**:
  1. **Lê Minh Hoài** – MSSV: **2001230256** *(Trưởng nhóm - Lead Data Engineering & Storage)*
  2. **Nguyễn Hoàng Thành Tỷ** – MSSV: **2001230872** *(Thành viên - Lead Machine Learning & Visualization)*

---

## 🎯 PHẦN 2: ĐỀ TÀI ĐỒ ÁN CHÍNH THỨC & LỊCH SỬ RA QUYẾT ĐỊNH

### 1. Tên đề tài chính thức (Chuẩn học thuật HUIT)
> **"Phân tích dữ liệu lớn thị trường nhà ở và Xây dựng mô hình định giá bất động sản tự động tại TP. Hồ Chí Minh bằng Apache Spark"**

### 2. Lịch sử ra quyết định & Lý do chọn đề tài (RẤT QUAN TRỌNG)
1. **Tách biệt với bài thuyết trình trên lớp**: Ban đầu nhóm đăng ký chủ đề lý thuyết *"Apache Mahout"* (buổi thứ 5). Bộ slide 25 slide và demo MovieLens 100K đã hoàn thành tại `mahout-demo/`. Tuy nhiên, Mahout chỉ là bài thuyết trình lý thuyết công nghệ thông thường, **không dùng làm đồ án cuối kỳ**. Đồ án cuối kỳ đòi hỏi một bài toán kỹ thuật ứng dụng thực tế hoàn chỉnh (*End-to-End Pipeline*).
2. **Tránh 15 đề tài gợi ý có sẵn trong đề cương**: Tránh trùng lặp với các nhóm khác trong lớp (mua sắm FP-Growth, chậm chuyến bay, phân tích log, cảm xúc review...).
3. **Phân định rõ ràng với các nhóm tự đề xuất**:
   * *Nhóm Lê Thiên Phú & Nguyễn Ngọc Quý*: Đề xuất "giá phòng & đề xuất mức giá tối ưu cho dịch vụ lưu trú" $\rightarrow$ Đây là bài toán **Homestay / Khách sạn thuê theo đêm (Airbnb)**.
   * *Nhóm chúng ta*: Bài toán **Mua bán Bất động sản Nhà ở dân sinh & Căn hộ thương phẩm dài hạn** tại TP.HCM. Đối tượng tài sản, cấu trúc dữ liệu và bài toán hoàn toàn khác biệt.
4. **Tính thời sự & Ý nghĩa thực tiễn**: Giá nhà đất và căn hộ tại TP.HCM là vấn đề kinh tế - xã hội nhức nhối bậc nhất. Việc xây dựng mô hình định giá tự động và bản đồ nhiệt giá đất có giá trị thực tế cao, được hội đồng HUIT đánh giá rất cao.
5. **Tránh bẫy kỹ thuật**: Không sa đà vào việc cào dữ liệu từ các trang chống bot nặng như Batdongsan.com.vn (dính Cloudflare 403 Forbidden). Dự án tận dụng **REST API Gateway mở của Chợ Tốt Nhà** và dataset 1.000.000 tin trên Hugging Face.

---

## 🏆 PHẦN 3: BAREM ĐÁNH GIÁ 10 ĐIỂM THEO CHUẨN ĐẦU RA (CLO) CỦA HUIT

Đồ án được chấm điểm theo Rubric 6 tiêu chí (Thang điểm 10) trong file quy định của trường:

| Chuẩn đầu ra (CLO) | Tiêu chí đánh giá | Trọng số | Yêu cầu đạt mức Tối đa (8.5 – 10.0 điểm) trong dự án này |
|:---|:---|:---:|:---|
| **CLO1** | **Tính ứng dụng của kỹ thuật** | **1.0 đ** | Bài toán định giá nhà đất và phân tích thị trường giải quyết trực tiếp nhu cầu minh bạch hóa giá nhà tại TP.HCM, hỗ trợ người mua, môi giới và thẩm định tài sản. |
| **CLO2** | **Lưu trữ & Xử lý dữ liệu phân tán** | **2.0 đ** | - Bộ dữ liệu lớn: **300.000 – 500.000 bản ghi** BĐS TP.HCM.<br>- Lưu trữ trên **MongoDB / HDFS / Parquet**.<br>- Pipeline **PySpark DataFrame**: Xử lý dữ liệu khuyết, lọc outlier bằng IQR/Z-Score, mã hóa đặc trưng (`StringIndexer`, `OneHotEncoder`, `VectorAssembler`). |
| **CLO3** | **Mô hình / Công nghệ xử lý bài toán** | **2.5 đ** | Ứng dụng thư viện học máy phân tán **Spark MLlib**:<br>1. *Hồi quy định giá (Regression)*: Huấn luyện và so sánh `LinearRegression`, `RandomForestRegressor`, `GBTRegressor` qua RMSE, MAE, $R^2$.<br>2. *Phân cụm thị trường (Clustering)*: Dùng `KMeans` phân nhóm các phân khúc BĐS (nhà phố, biệt thự, căn hộ, đất nền vùng ven). |
| **CLO3** | **Trực quan hóa / Xây dựng ứng dụng** | **2.5 đ** | Xây dựng Dashboard **Streamlit** hoàn chỉnh:<br>- Bản đồ nhiệt GPS (Heatmap Folium/PyDeck) trực quan hóa giá nhà đất theo tọa độ thực tế tại các quận huyện TP.HCM.<br>- Form định giá tự động tương tác (nhập thông số $\rightarrow$ trả về giá dự đoán). |
| **CLO4** | **Trình bày báo cáo** | **1.0 đ** | File Word báo cáo theo đúng cấu trúc đề cương HUIT, văn phong học thuật, bảng biểu rõ ràng, đầy đủ tài liệu tham khảo. |
| **CLO5** | **Phân công & Phối hợp nhóm** | **1.0 đ** | Có nhật ký phân công chi tiết, khối lượng công việc cân bằng giữa 2 thành viên (50% - 50%). |

---

## ⚙️ PHẦN 4: KIẾN TRÚC KỸ THUẬT & LUỒNG DỮ LIỆU (DATA PIPELINE)

```text
[ NGUỒN DỮ LIỆU ]
  ├── Chợ Tốt REST API Gateway (100K - 200K tin mới có GPS thực tế)
  └── Hugging Face Parquet (binleevn/vietnam-real-estates: ~1M tin lịch sử)
         │
         ▼
[ BƯỚC 1: DATA INGESTION & STORAGE ]
  ├── Script: src/crawler/chotot_crawler.py (Thuần Python urllib/json/csv, chạy mượt 100%)
  └── Lưu trữ thô: data/raw/ + Nạp vào MongoDB / HDFS
         │
         ▼
[ BƯỚC 2: DISTRIBUTED ETL VỚI PYSPARK ]
  ├── Chuẩn hóa giá: Tính unit price (triệu VND/m2), total price (tỷ VND)
  ├── Làm sạch: Loại bỏ tin rác, xử lý null (Imputation)
  ├── Lọc ngoại lệ: Áp dụng phân vị IQR phân tán loại bỏ tin ảo
  └── Trích xuất đặc trưng: StringIndexer + OneHotEncoder cho Quận, Phường, Hướng, Pháp lý
         │
         ▼
[ BƯỚC 3: DISTRIBUTED MACHINE LEARNING (SPARK MLLIB) ]
  ├── Regression: RandomForestRegressor & GBTRegressor dự đoán giá
  ├── Clustering: KMeans phân cụm phân khúc thị trường
  └── Tuning & Evaluation: CrossValidator đánh giá RMSE, MAE, R2
         │
         ▼
[ BƯỚC 4: INTERACTIVE DASHBOARD (STREAMLIT) ]
  ├── Tab 1: Bản đồ nhiệt (GPS Heatmap) phân bố giá nhà đất toàn TP.HCM
  ├── Tab 2: Phân tích tương quan giá theo quận huyện, loại hẻm, diện tích
  └── Tab 3: Bộ công cụ định giá tự động thông minh theo thông số người dùng nhập
```

---

## 📅 PHẦN 5: LỘ TRÌNH 10 TUẦN & MỐC NỘP BÀI (DEADLINES)

* **Tuần 1 – 3 (Khởi tạo & Đăng ký)**:
  * Nộp bản đăng ký đề tài tự đề xuất cho GVHD.
  * Thiết lập cấu trúc thư mục dự án và chạy thử nghiệm crawler Chợ Tốt API.
* **Tuần 4 – 5 (Cơ sở lý thuyết & Xử lý dữ liệu - CLO2)**:
  * Thu thập dữ liệu quy mô lớn (300.000+ bản ghi).
  * Viết pipeline PySpark ETL làm sạch, chuẩn hóa và lưu trữ MongoDB/Parquet.
* **Tuần 6 – 7 (Mô hình Baseline & NỘP TIẾN ĐỘ GIAI ĐOẠN 1)**:
  * Xây dựng mô hình hồi quy Baseline đầu tiên trên Spark MLlib.
  * Hoàn thành và nộp **Báo cáo tiến độ Giai đoạn 1 (Tuần 5-6)** trên Google Classroom.
* **Tuần 8 – 9 (Hoàn thiện ML, Dashboard & NỘP HOÀN CHỈNH GIAI ĐOẠN 2)**:
  * Tinh chỉnh mô hình `GBTRegressor` và `KMeans`.
  * Xây dựng giao diện Streamlit Dashboard hoàn chỉnh.
  * Viết Báo cáo Word hoàn chỉnh, thiết kế Slide PPT.
  * Nộp trọn bộ mã nguồn, File Word và File PPT (Giai đoạn 2 - Tuần 9).
* **Tuần 10 (Thuyết trình & Vấn đáp cuối kỳ)**:
  * Thuyết trình trước lớp (10–15 phút) và demo ứng dụng trực tiếp.
  * Trả lời các câu hỏi phản biện từ giảng viên.

---

## 👥 PHẦN 6: PHÂN CÔNG VAI TRÒ GIỮA 2 THÀNH VIÊN

| Thành viên | Vai trò chính | Nhiệm vụ cụ thể |
|:---|:---|:---|
| **Lê Minh Hoài**<br>(2001230256) | **Lead Data Engineering & Storage (CLO2)** | - Quản lý crawler API Chợ Tốt và tích hợp dataset Hugging Face.<br>- Thiết kế kiến trúc lưu trữ MongoDB / HDFS.<br>- Lập trình pipeline PySpark ETL (làm sạch, lọc outlier, Feature Engineering).<br>- Đồng tác giả Báo cáo Word & Slide PPT. |
| **Nguyễn Hoàng Thành Tỷ**<br>(2001230872) | **Lead Machine Learning & Visualization (CLO3)** | - Xây dựng và tối ưu mô hình Spark MLlib (`RandomForest`, `GBTRegressor`, `KMeans`).<br>- Đánh giá và đối chiếu các độ đo RMSE, MAE, $R^2$, Silhouette.<br>- Phát triển ứng dụng Web Dashboard Streamlit (Bản đồ GPS Heatmap + Form định giá).<br>- Đồng tác giả Báo cáo Word & Slide PPT. |

---

## 📂 PHẦN 7: HIỆN TRẠNG MÃ NGUỒN ĐÃ TRIỂN KHAI

Toàn bộ dự án được tổ chức tại thư mục: `d:\slider\real-estate-bigdata\`

```text
d:\slider\real-estate-bigdata\
├── data\
│   ├── raw\                     # Đã chạy thử nghiệm thành công file: chotot_raw_13000_1020.csv (100 tin mẫu)
│   └── processed\               # Chứa dữ liệu sạch sau PySpark ETL
├── src\
│   ├── crawler\                 # Đã hoàn thiện script: chotot_crawler.py (Thuần Python urllib/json/csv)
│   ├── etl\                     # Pipeline làm sạch PySpark (sắp triển khai)
│   ├── models\                  # Huấn luyện Spark MLlib (sắp triển khai)
│   └── dashboard\               # Ứng dụng Streamlit (sắp triển khai)
├── docs\
│   ├── ke_hoach_thuc_hien.md    # Kế hoạch chi tiết 10 tuần
│   └── TONG_QUAN_DO_AN_BIGDATA.md # Bản sao lưu hồ sơ tổng quan này
├── requirements.txt             # Danh sách thư viện Python cần thiết
└── README.md                    # Tài liệu hướng dẫn dự án
```

---

## 🤖 PHẦN 8: HƯỚNG DẪN DÀNH CHO CÁC AI MODEL (SYSTEM PROMPT INJECTION)

Khi người dùng chuyển sang trò chuyện với bất kỳ AI Model nào khác, hãy cấp tài liệu này làm ngữ cảnh. AI Model cần tuân thủ nghiêm ngặt các nguyên tắc sau:
1. **Tuyệt đối không nhầm lẫn với Apache Mahout**: Mahout chỉ là bài thuyết trình lý thuyết cũ. Đồ án chính thức là **Bất động sản TP.HCM bằng Apache Spark**.
2. **Tuyệt đối không nhầm lẫn với đề tài lưu trú**: Đề tài này giải quyết mua bán nhà đất lâu dài, không phải homestay/khách sạn thuê theo đêm (Airbnb) của nhóm khác.
3. **Mọi giải pháp xử lý dữ liệu và học máy BẮT BUỘC phải dùng Apache Spark (PySpark DataFrame / Spark SQL / Spark MLlib)**, không dùng Pandas thuần hoặc Scikit-Learn để huấn luyện chính vì sẽ vi phạm tiêu chí Big Data (CLO2).
4. **Dashboard trực quan hóa bắt buộc dùng Streamlit + Folium/PyDeck** để thể hiện bản đồ nhiệt GPS.
5. **Giữ vững văn phong học thuật HUIT**, bám sát 6 tiêu chí Rubric để đảm bảo nhóm đạt điểm tối đa (9.0 - 10.0 điểm).
