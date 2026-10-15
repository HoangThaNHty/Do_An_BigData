# Hồ sơ và gói bàn giao local

Word/PPT, ZIP và checksum được tạo local, không cần để clone chạy web và không đưa vào Git mặc định. Word/PPT là snapshot trước V4, cập nhật sau theo yêu cầu nhóm. Tạo ZIP bằng python scripts/package_handoff.py; kiểm tra giải nén bằng python scripts/verify_handoff.py sau khi dừng API để chỉ có một Spark JVM.
