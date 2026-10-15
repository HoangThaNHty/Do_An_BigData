# Các mục triển khai đồ án

Ngày chốt: 11/10/2026. Kế hoạch chính: PLAN_HUONG_DI_BIGDATA_V3.md.

Tên: Phân tích dữ liệu tin đăng và xây dựng hệ thống ước tính giá rao bán nhà ở tại TP. Hồ Chí Minh bằng Apache Spark.

## Thứ tự và đầu ra

| Mục | Công việc | Đầu ra và điều kiện hoàn thành | Trạng thái |
|---|---|---|---|
| 01 | Môi trường, nguồn dữ liệu, khảo sát | Dataset có revision/checksum; Spark đọc/ghi và MLlib lưu/nạp chạy được; thống kê toàn bộ | Hoàn thành |
| 02 | Kiểm chứng giao dịch và diện tích | Mẫu hiệu chỉnh, mẫu ngẫu nhiên độc lập, nhãn đọc thực tế, báo cáo độ phủ/lỗi; quy tắc có phiên bản | Đã đọc 800 nhãn AI qua v1–v5; v5 đạt 98/100 phạm vi theo tiêu chí nghiên cứu, công bố giới hạn |
| 03 | ETL chính và chất lượng dữ liệu | Parquet ứng viên/loại/không rõ tách riêng; mã lý do; kiểm tra hữu hạn, đơn vị, trùng và địa chỉ; thống kê từng bước | ETL v4 đủ 1.122.868 dòng, 149.975 ứng viên; core v1 còn 133.779 tin sau loại mẫu review/tin lặp, có manifest |
| 04 | Địa lý và thống kê thị trường | Bảng địa danh theo phiên bản; tỷ lệ ghép; tổng hợp quận/loại nhà/tháng; bản đồ cấp quận | Đã ghép địa bàn, xuất 22 polygon lịch sử, tổng hợp và bảng phục vụ 133.779 dòng; không có GPS tài sản |
| 05 | Baseline, chia tập và mô hình đầu | Split thời gian, hạn chế tin đăng lại giữa tập; tiền xử lý fit train; baseline và LR riêng nhà/căn hộ | Hoàn thành trên toàn train; baseline và pipeline lưu/nạp đã kiểm tra |
| 06 | So sánh và chọn mô hình | RF/GBT, validation theo thời gian, bảng sai số phân khúc, mô hình/pipeline lưu được; test cuối sau chọn cấu hình | Hoàn thành 9 pipeline + baseline; chọn LR riêng theo validation trước test; có bảng phân khúc |
| 07 | Sản phẩm web và API | Next.js/shadcn + FastAPI; tổng quan, bản đồ, dự đoán và đánh giá; local/LAN trước, Internet sau | Hoàn thành sáu trang, API và script chạy local/LAN; kiểm tra desktop/mobile và dự đoán thật đạt |
| 08 | Hoàn thiện và bàn giao | Chạy xuyên suốt, hướng dẫn tái chạy, báo cáo Word, PPT, tài liệu nguồn và nhật ký nhóm | Hoàn thành hồ sơ kỹ thuật, Word/PPT và gói demo; nhóm còn bổ sung xác nhận/nhật ký/đóng góp thực tế |

## Cách làm

Hoàn thành một mục và ghi kết quả thực tế trước khi chuyển sang bước phụ thuộc. Hoàn thiện mục 02–06 trước khi lập trình frontend/API ở mục 07. Bản baseline và mô hình đầu chạy bằng script, chưa cần giao diện. Ghi phương pháp và kết quả trong lúc làm; không viết kết quả dự kiến như đã thực nghiệm.

Mục 02: nhãn tự động không phải nhãn tham chiếu. Người đọc có thể là thành viên nhóm hoặc AI, nhưng phải ghi rõ tác giả/phương thức; nhãn AI không được trình bày như nhãn người hoặc kiểm chứng độc lập của chuyên gia. Phần đánh giá không được dùng hiệu chỉnh cùng phiên bản quy tắc.

Mục 03 có thể xây cấu trúc trong lúc chuẩn bị mục 02; chưa gắn nhãn dữ liệu sạch đã kiểm chứng nếu chưa hoàn thành đánh giá. Crawler, GPS bổ sung, KMeans và bản đồ phường không chặn việc hoàn thành bản chính.

## Nơi lưu

- Hồ sơ để trao đổi: D:\slider\FolderDoAnBigData.
- Mã nguồn và dữ liệu: D:\slider\real-estate-bigdata.
- Kết quả máy đọc: artifacts/profile và artifacts/review trong dự án.
- Nhật ký cập nhật: docs/TRANG_THAI_TRIEN_KHAI.md trong dự án; sao chép về hồ sơ tại các mốc bàn giao.
- Không sao chép dataset hoặc môi trường vào hồ sơ. Các bản tài liệu ở hồ sơ là ảnh chụp tại mốc cập nhật, không tự đồng bộ sau mỗi lần chạy code.

Chi tiết mục 07 và thay đổi hướng giao diện: MUC_07_SAN_PHAM_WEB.md. Đã triển khai giao diện/API sau khi core và mô hình đạt điều kiện. Hướng dẫn chạy ở HUONG_DAN_CHAY.md; trạng thái mới nhất ở đầu nhật ký. Điều kiện bắt đầu mục 07: dữ liệu đã kiểm chứng, ETL tái chạy được, bảng tổng hợp có phạm vi rõ, mô hình đã đánh giá và pipeline lưu/nạp/dự đoán bằng script được. Nếu chưa đủ chất lượng thì hiệu chỉnh hoặc thu hẹp phạm vi trước.
