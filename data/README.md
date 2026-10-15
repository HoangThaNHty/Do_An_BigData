# Dữ liệu đi cùng Git và dữ liệu giữ local

**Clone chạy demo ngay sau setup** nhờ model ở artifacts/models/v1, serving ở artifacts/market, địa giới ở artifacts/geography và manifest ở data/demo_manifest.json. Serving chỉ có loại nhà, khu vực, tháng, diện tích, giá và đơn giá; không có mô tả/tên/liên hệ người đăng. Dự đoán test có row_id băm, không có mô tả/liên hệ.

Git giữ metadata nguồn pinned, dataset card, địa giới/giấy phép, manifest core và danh sách row_id loại review. Git không chứa raw 1,6 GB, các phiên bản ETL/core Parquet nhiều GB hoặc file review có nội dung tin. Chúng vẫn ở máy nghiên cứu, không bị xóa.

**Tái hiện ETL/cohort từ đầu** khác chạy demo: cần tải raw theo manifest pinned bằng scripts/bootstrap_data.py --dataset và có bộ review gốc/provenance tương ứng. src/etl/core.py kiểm tra review hash, ngưỡng hỗ trợ và loại các ID đã đọc; không bỏ kiểm tra này để cho qua. Nhóm trao đổi bộ review nghiên cứu riêng khi cần, không mặc định đưa nội dung tin lên GitHub. Huấn luyện cần cohort Parquet thật, không chỉ serving.

Model đã lưu và kết quả phục vụ môn học, dữ liệu gốc CC BY-NC 4.0. Giữ ghi công/giấy phép trong THIRD_PARTY_NOTICES.md. Không dùng gói demo như bằng chứng mô hình đã xác minh giá giao dịch hoặc địa giới hiện hành.
