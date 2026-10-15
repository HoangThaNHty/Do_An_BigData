# Tiêu chí chốt tập nghiên cứu trước mẫu ứng viên v3

Ngày12/10/2026. Đây là tiêu chí vận hành đồ án, không phải chứng nhận dữ liệu thị trường sạch hay đảm bảo accuracy.

1. ETL đầy đủ phải ghi/đọc lại bảo toàn số dòng nguồn duy nhất, lưu phiên bản/hash và lý do giữ riêng. Chỉ dùng lượt có manifest thành công.
2. Lấy100 ứng viên mới không trùng các mẫu trước, mã quality được cố định trước gán nhãn. Đọc đủ nguồn, gồm nhãn giao dịch, giá, loại diện tích và phạm vi theo QUY_UOC_PHAM_VI_V3.md.
3. Tối thiểu80 nhãn đầy đủ và tỷ lệ ứng viên được cả bốn nhãn hỗ trợ trên mẫu ít nhất95% để tiếp tục thực nghiệm. Báo cáo tử số/mẫu số, khoảng Wilson95% và phương thức AI; ngưỡng điểm trên mẫu không đảm bảo toàn nguồn đạt95%. Nếu không đạt, xem lại phạm vi/nguyên nhân và trao đổi thay đổi cần thiết.
4. Giữ TP.HCM theo các khu vực quận/huyện trước sáp nhập2025 để có hệ tham chiếu thống nhất. Quận2/9 ghép về ThủĐức khi tổng hợp cấp quận; giữ địa danh nguyên bản. Địa danh ngoài bảng hoặc chưa giải quyết không vào mô hình; phường khác phiên bản ghi trạng thái rõ, không tự suy ra phường mới/cũ.
5. Loại tin đăng lại bằng nhóm văn bản đầy đủ đã chuẩn hóa, giữ bản xuất hiện đầu tiên. Kiểm tra không có cùng group giữa train/validation/test. Báo cáo giới hạn: đây là proxy, không có mã tài sản nên chưa chứng minh mọi tài sản độc lập.
6. Train06–11/2025, validation12/2025, test01–03/2026. Tiền xử lý học train; chọn cấu hình validation. Test cuối không dùng tuning. Không impute target, không dùng price_per_m2 làm feature.

Tập đủ điều kiện được gọi là tập nghiên cứu có kiểm chứng mẫu bằng AI; không gọi đã được người/chuyên gia kiểm chứng. Thống kê mô tả phần nguồn được chọn, có thiên lệch lựa chọn và không đại diện tất cả giao dịch.
