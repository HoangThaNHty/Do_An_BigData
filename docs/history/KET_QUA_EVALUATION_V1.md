# Đánh giá mẫu evaluation v1 và quyết định triển khai

Ngày 12/10/2026. Đã đọc đủ 150 tin evaluation theo quy ước đã lưu, sau khi cố định phiên bản giao dịch/diện tích candidate-v2-frozen-for-evaluation. Tất cả nhãn ghi review_method=ai, reviewer=Codex-source-text-review; có ghi chú bằng chứng. Đây là nhãn tham chiếu AI, chưa có người kiểm tra chéo.

## Tính toàn vẹn

Đã xác nhận 300 dòng calibration/evaluation giữ nguyên trường nguồn, row_id và split so với bản chưa gán nhãn. Mã src/etl/rules.py vẫn giữ SHA256 a2b7d760d9507f807edfbae6d414b575235ef399376581d018fda35b01a35b8e. Dự đoán evaluation đã được tạo trước khi gán nhãn; kiểm tra fingerprint qua công cụ score. Không sửa quy tắc này trong lượt đánh giá.

Sáu file evaluation_001.json đến evaluation_006.json lưu các đợt ghi nhãn; blind_review.csv có nhãn và evidence; evaluation.json lưu kết quả. Chưa bảo đảm các tin nói về các tài sản độc lập; cùng AI đọc calibration và evaluation nên không coi là đánh giá của người kiểm tra độc lập. Một dòng evaluation đã hiển thị trong lệnh xem đầu CSV ở giai đoạn chuẩn bị; không tuyên bố toàn bộ nội dung evaluation chưa từng xuất hiện trước khi cố định.

## Kết quả giao dịch trên mẫu

| Nhãn tham chiếu AI / Dự đoán | Bán | Thuê | Chưa xác định |
|---|---:|---:|---:|
| Bán | 99 | 2 | 11 |
| Thuê | 0 | 1 | 0 |
| Chưa xác định | 1 | 3 | 33 |

- 100 tin được quy tắc dự đoán bán; 99 khớp nhãn bán AI: precision tin bán 99/100 = 99% trên mẫu.
- 112 tin có nhãn bán AI; nhận diện đúng 99: recall tin bán 99/112, khoảng 88,4% trên mẫu.
- Đồng thuận loại diện tích: 101/150, khoảng 67,3%. Bất đồng gồm cả trường hợp nhãn AI suy luận đất từ kích thước nhưng quy tắc cố ý yêu cầu bằng chứng đất/công nhận rõ.
- Mẫu chỉ có 1 nhãn thuê, không đủ kết luận khả năng nhận diện thuê trong toàn dữ liệu.

Không diễn giải 99% thành độ sạch của dữ liệu huấn luyện, độ chính xác dự đoán giá hoặc độ tin cậy toàn thị trường. Các tỷ lệ phụ thuộc nhãn AI và mẫu nhỏ; chưa có đánh giá bằng người.

## Kiểm tra riêng nhóm ứng viên

Trong 150 tin, quy tắc giữ 34 candidate_eligible:

- Cả34 có nhãn giao dịch bán theo AI.
- Giá: 29 đối chiếu được, 5 chưa xác định; không có giá được gán no trong nhóm này.
- Diện tích: 24 căn hộ, 8 đất, 2 chưa rõ theo nhãn AI.
- Có6 tin có ít nhất một vấn đề giá/diện tích;28 tin còn lại phù hợp cả ba nhãn. Đây vẫn chưa xác nhận phạm vi địa lý, tài sản thật hoặc độc lập theo tài sản.

Ví dụ: TropicGarden ghi9.75tỷ nhưng cộtprice9.4tỷ; PhúHoàngAnh ghi3.85triệu nhưng cộtprice3.85tỷ; D-Homme chỉ quảng cáo dự án không có diện tích/giá căn cụ thể; căn900triệu không có diện tích38 để đối chiếu. Hai trường hợp khác thiếu tổng giá trong nội dung.

Vì vậy chưa cho phép dùng candidate_eligible v2 như nhãn dữ liệu sạch. Không điền/sửa price hay area từ suy đoán. Bổ sung lớp chất lượng riêng cho ETL; giữ nguyên bộ quy tắc giao dịch đã được đánh giá.

## Hướng xử lý tiếp theo

src/etl/quality.py thực hiện lớp cross-field-v1-provisional: đối chiếu số tổng giá giữa cột dữ liệu và văn bản, cần bằng chứng số diện tích căn hộ, giữ riêng thêm dấu hiệu lệch phạm vi. Đây là cải tiến sau khi xem evaluation v1; kết quả kiểm tra trên v1 chỉ dùng chẩn đoán, không phải đánh giá độc lập của lớp mới.

src/etl/build.py tạo Parquet có disposition provisional_training, quarantine hoặc excluded_rent; lưu lý do và phiên bản. Chỉ loại nguồn trùng hoàn toàn; không tùy ý chọn một dòng trong nhóm row_id cùng định danh nội dung nhưng đặc trưng nguồn khác nhau. Tin đăng lại cùng tài sản chưa được giải quyết ở bước này.

Cần tạo mẫu mới không trùng row_id với mẫu đã đọc và kiểm chứng lớp chất lượng mới. Chỉ sau khi đánh giá mới và kiểm tra phạm vi, địa lý, thiếu/trùng phù hợp mới chốt tập huấn luyện. Không dùng kết quả v1 để tự xác nhận lớp chất lượng vừa sửa.

Mục02 hoàn thành lượt đọc/đánh giá v1; còn kiểm chứng chất lượng bổ sung. Mục03 đã bắt đầu; chưa huấn luyện mô hình giá nhà hoặc triển khai web/API.
