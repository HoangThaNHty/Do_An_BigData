# Khảo sát dữ liệu thực tế bằng Apache Spark

Ngày: 11/10/2026. Nguồn: oceanNG/vietnam-real-estates, revision 6f68fe87be7577afb03e38c535bd882d242ba26d.

Đã tải và kiểm tra SHA256 10 shard. Spark đã đọc toàn bộ 3.500.744 dòng và lọc chính xác province_name = Hồ Chí Minh, được 1.357.526 dòng. Phạm vi hiện tại là nhãn địa phương trong nguồn, chưa ghép ranh giới hành chính.

| Loại hình | Tin TP.HCM |
|---|---:|
| Nhà | 842,922 |
| Căn hộ chung cư | 279,948 |
| Đất | 162,110 |
| Biệt thự/Nhà liền kề | 62,666 |
| Shophouse | 9,880 |

## Điều kiện ứng viên ban đầu

Các điều kiện là quy tắc kỹ thuật chưa được xác nhận bằng nhãn kiểm tra thủ công. Chưa loại hết giá bất thường, chưa xử lý trùng để huấn luyện, chưa xác nhận toàn bộ diện tích căn hộ hoặc địa chỉ.

- Căn hộ chung cư: 153,198 tin qua điều kiện ứng viên.
- Nhà: 18,456 tin qua điều kiện ứng viên.

Mẫu chẩn đoán: 1,680 dòng, chưa gán nhãn thủ công. Mẫu phân tầng theo nhóm quy tắc, không đại diện trực tiếp cho tỷ lệ toàn thị trường. File: artifacts/profile/manual_review.csv. Quy trình: docs/KIEM_CHUNG_DU_LIEU.md.

## Phát hiện quan trọng

- Schema price thực tế là string, khác metadata float64. Đã chuyển kiểu double rõ ràng và kiểm tra giá trên giới hạn int32. Kết quả ứng viên lượt đầu trước sửa kiểu giá không được sử dụng.
- Nhà riêng: 37.108 tin có biểu thức diện tích đất với số khớp area theo quy tắc ban đầu. Phần lớn nhà chưa rõ loại diện tích; không mặc định area là diện tích đất.
- Thiếu district_name: 83,627 tin. Thiếu ward_name: 212,945 tin.
- Thiếu price nguyên bản: 65,706 tin. Còn phải kiểm tra chuỗi không chuyển kiểu được, NaN, giá không hợp lệ và giá trả trước.
- Nhãn sale/rent là dự đoán quy tắc, không phải kết luận về cơ cấu giao dịch thực tế.
- Thời gian xử lý profile cuối: 177.84 giây trong môi trường thực nghiệm local[4], driver 4 GB. Không diễn giải một lần chạy thành benchmark tổng quát.

## Kiểm tra môi trường

Đã pass 8 tình huống ngữ cảnh với cả giá số/chuỗi, đọc/ghi/ghi đè Parquet, huấn luyện và lưu/nạp mô hình LinearRegression nhỏ bằng MLlib. Không phải kết quả mô hình giá nhà.

## Bước tiếp theo

Đọc và gán nhãn mẫu hiệu chỉnh; chuẩn bị mẫu ngẫu nhiên đánh giá độc lập; hiệu chỉnh quy tắc; hoàn thiện ETL, kiểm tra ngoại lệ và trùng lặp; ghép địa lý; chia tập theo thời gian rồi mới huấn luyện/đánh giá giá nhà.
