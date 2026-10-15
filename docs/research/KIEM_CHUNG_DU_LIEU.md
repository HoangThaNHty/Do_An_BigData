# Kiểm chứng dữ liệu trước huấn luyện

Quy tắc trong `src/etl/rules.py` tạo nhãn ứng viên, không phải nhãn thật. Không công bố độ chính xác phân loại khi chưa có nhãn kiểm tra độc lập.

Sau khi chạy `src.etl.profile`, mở `artifacts/profile/manual_review.csv` để đọc tiêu đề/mô tả và điền:

- `manual_transaction`: `sale`, `rent`, `uncertain`.
- `manual_area_kind`: `apartment`, `land`, `floor`, `unknown`.
- `manual_price_valid`: `yes`, `no`, `uncertain` theo tổng giá rao bán.
- `review_notes`: bằng chứng hoặc lý do mâu thuẫn.

Các dòng có `review_split=calibration` dùng để hiệu chỉnh. Không dùng nhãn ở phần `evaluation` để sửa quy tắc trong cùng lượt đánh giá. Nếu đổi quy tắc sau khi xem evaluation, tạo lượt kiểm tra mới.

Mẫu hiện tại có hạn ngạch theo nhóm quy tắc/loại hình/bằng chứng diện tích, chọn bằng hash cố định. Đây là mẫu chẩn đoán có phân tầng, không phải mẫu ngẫu nhiên đơn giản của toàn thị trường. Không diễn giải tỷ lệ lỗi chưa có trọng số thành tỷ lệ lỗi của toàn bộ dữ liệu. Cần thêm mẫu ngẫu nhiên độc lập khi đánh giá độ chính xác toàn tập.

Với tin nhà đang cho thuê nhưng được quảng cáo bán, nhãn là bán nếu mục đích giao dịch rõ; tiền thuê không được nhầm với tổng giá. Không dùng mức giá tự quyết định bán/thuê.

Tin căn hộ hiện được suy ra loại diện tích từ loại tài sản, chưa chứng minh số liệu `area` là thông thủy/tim tường. Tin nhà chỉ đủ điều kiện ứng viên khi diện tích đất có số liệu rõ khớp `area` trong sai số kiểm tra 5% hoặc 1m²; đây là ngưỡng ban đầu, cần kiểm chứng, không phải kết luận về chất lượng.

`candidate_eligible` chỉ là điều kiện ứng viên, không có nghĩa đã được phê duyệt để huấn luyện hoặc tin sạch hoàn toàn. Bộ quy tắc chưa xử lý toàn bộ viết tắt, Unicode, các biểu thức diện tích và giá. Không điền nhãn thủ công từ chính dự đoán tự động.

Địa danh chuẩn hóa chưa được ghép với ranh giới hành chính; trạng thái chỉ nói có tên, không xác nhận tên hợp lệ. Không suy ra tọa độ hoặc độ chính xác vị trí từ trạng thái này.
