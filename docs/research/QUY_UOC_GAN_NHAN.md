# Quy ước đọc mẫu giao dịch, diện tích và giá

Cập nhật 11/10/2026. Mẫu calibration v1 được Codex đọc từ tiêu đề/mô tả và ghi nhãn `review_method=ai`. Đây là nhãn tham chiếu do AI, chưa phải xác nhận của người hoặc chuyên gia. Không dùng dự đoán của quy tắc để điền nhãn.

## Giao dịch

- `sale`: có ý định bán căn/tài sản chính, kể cả cách viết đảo "nhà bán", chuyển nhượng hoặc phát mãi. Lời mời khách mua rõ cũng là bằng chứng, nhưng có thể cần người kiểm tra lại.
- `rent`: mục đích chính rõ là cho thuê tài sản, không chỉ mô tả công năng hoặc hợp đồng hiện hữu.
- `uncertain`: không đủ bằng chứng, giao dịch kép hoặc mâu thuẫn chưa giải quyết được. Giá hàng tỷ không tự chứng minh bán.

Hợp đồng đang thuê, dòng tiền và công năng cho thuê không tự biến tin bán thành tin thuê. Dịch vụ môi giới và giỏ hàng khác không phải giao dịch căn chính.

## Diện tích của cột area

- `apartment`: nội dung xác nhận diện tích căn hộ chính tương ứng với cột area. Không chỉ dựa trên property_type_name nếu nội dung không có diện tích để đối chiếu.
- `land`: có diện tích đất/công nhận khớp, hoặc kích thước khuôn đất có cơ sở khớp với area; ghi rõ nếu là suy luận từ kích thước. Không coi nhãn này là chứng nhận pháp lý.
- `floor`: nội dung xác định diện tích sàn/sử dụng của nhà và số liệu tương ứng với area.
- `unknown`: thiếu loại đo, không xác nhận số liệu, hoặc có mâu thuẫn.

Trong lượt đọc calibration, kích thước gần khớp được đối chiếu với ngưỡng ban đầu 5% hoặc 1m², kế thừa kế hoạch. Mâu thuẫn số công nhận hoặc nở hậu/chênh lệch không giải thích được vẫn được ghi unknown. Quy tắc tự động hiện nghiêm hơn nhãn tham chiếu: chỉ dùng bằng chứng đất/công nhận rõ cho nhà; chưa đưa suy luận kích thước vào điều kiện huấn luyện. Vì vậy số bất đồng loại diện tích không đồng nghĩa toàn bộ là lỗi tin bán được giữ.

Thông thủy/tim tường được gắn vào area chỉ khi số đo tương ứng khớp. Có nhắc thông thủy67 trong tin area70 không đủ để gán area70 là thông thủy.

## Tổng giá

- `yes`: giá dương hữu hạn có tổng giá căn chính trong nội dung khớp; giá mới sau giảm được ưu tiên khi rõ. Sai lệch làm tròn nhỏ được ghi bằng chứng; dùng 1% làm ngưỡng đối chiếu ban đầu, không phải sai số mô hình.
- `no`: cột giá thiếu, bằng0, không hữu hạn, hoặc xác định rõ là giá thành phần/không phải tổng giá.
- `uncertain`: thiếu số tổng trong nội dung, chỉ có giá "nhỉnh/hơn/x", hoặc các tổng giá mâu thuẫn hơn ngưỡng đối chiếu.

Không tự sửa/điền giá từ nội dung trong lượt gán nhãn. `yes` chỉ xác nhận đối chiếu số liệu tin, không xác nhận giá thị trường, độ thật của tài sản hay khả năng giao dịch. Tiền trả trước/booking/thu nhập thuê tách khỏi tổng giá. Quy tắc có thể giữ riêng các tin trả trước dù người đọc tìm được tổng giá.

## Giới hạn và bước tiếp theo

Mẫu hiện tại chọn theo row_id, chưa đảm bảo độc lập theo tài sản. Mẫu calibration đã dùng để sửa mã; tuyệt đối không công bố số bất đồng trên calibration thành độ chính xác độc lập. Giữ nguyên 150 dòng evaluation chưa gán nhãn; cố định mã trước khi đọc evaluation. Nếu sửa mã dựa trên evaluation, cần lượt đánh giá mới và công bố lịch sử sử dụng mẫu.

Phân loại phạm vi nhà ở hiện là cờ kiểm tra ứng viên. Tin đất, biệt thự, officetel, tòa thương mại/khách sạn/CHDV có thể nằm trong cộtNhà hoặc căn hộ; các dấu hiệu rõ được giữ riêng. Cờ không phát hiện mâu thuẫn không chứng minh tin thuộc phạm vi hoàn toàn.
