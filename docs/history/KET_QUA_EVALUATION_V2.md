# Kết quả evaluation v2 và xử lý các lỗi còn lại

Ngày 12/10/2026. Đã đọc đủ văn bản 200 tin mới trước khi mở dự đoán; 10 file evaluation_001.json–010.json lưu nhãn và bằng chứng. Nhãn đều do AI, chưa có người xác nhận. Giữ nguyên nguồn và split so bản chưa gán nhãn.

Phiên bản được đánh giá: rules candidate-v2-frozen-for-evaluation và quality cross-field-v1-provisional (SHA256 c2487cef8313f3ff988f84d85e1567bab4e50cd57e18ffc298350c74ac20382a). Snapshot giữ trong artifacts/review/v2/frozen_code; kết quả không bị thay khi mã hiện hành được sửa tiếp.

## Kết quả thực tế

- Nhãn AI: 196 bán, 4 chưa xác định, không có thuê. Không đánh giá được nhận diện thuê trên mẫu này.
- Dự đoán bán133 tin, đều khớp nhãn bán AI; recall133/196≈67,9%. Đây là kết quả trên mẫu, không phải bảo đảm thị trường.
- Đồng thuận loại diện tích102/200=51%; phần lớn bất đồng nhà do AI suy luận khuôn đất còn quy tắc yêu cầu đất/CN rõ.
- 26 protected_candidate:24 được đồng thời nhãn giao dịch/giá/loại diện tích hỗ trợ.2 tin còn vấn đề: index53giá từ6,5 tỷ và index17920,8 tỷ vốn ban đầu so tổng26 tỷ.
- Ngoài ba nhãn trên, index2 là tòa building vẫn được giữ dù ngoài phạm vi nhà ở chính. Vì vậy24/26 không đồng nghĩa24tin đủ mọi điều kiện huấn luyện.

Mẫu không trùng1.980row_id đã đọc trước, nhưng chưa bảo đảm tài sản độc lập. Cùng AI đọc các lượt nên không gọi đây là đánh giá của người độc lập. Nguồn có thể chứa quảng cáo giỏ hàng, condo-villa hoặc địa danh mới; ghép giá/diện tích cần căn chính, không dựa số khớp đơn lẻ.

## Quyết định sau đánh giá

Giữ kết quả v2 nguyên trạng. Mã quality hiện hành chuyển cross-field-v2-provisional để giữ riêng giá từ/giá khoảng, vốn ban đầu/booking, tòa building và một số dấu hiệu thương mại rõ. Không sửa rules.py đã cố định, không sửa giá/diện tích nguồn.

Cần mẫu ứng viên mới để đánh giá phiên bản quality này; mẫu v2 trở thành dữ liệu chẩn đoán cho các thay đổi vừa làm. Mẫu mới đánh giá chất lượng có điều kiện trong nhóm được giữ, không đánh giá recall toàn bộ hoặc chất lượng tin thuê. Thống kê độ phủ lấy từ ETL đầy đủ, báo cáo cùng cỡ mẫu và giới hạn AI.
