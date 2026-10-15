# Plan nghiệm thu quy trình demo trước GitHub

Ngày 15/10/2026. Người dùng yêu cầu **khoan push GitHub cho đến khi quy trình đủ và cả hai thành viên trình bày được**. Không tự commit/push trong lúc chuẩn bị.

Yêu cầu mới: diễn tập từng bước cùng người dùng, bắt đầu ở nguồn. Khi chưa có phản hồi thao tác thì không ghi người dùng đã hoàn thành bước hoặc tự chuyển sang train. Câu trả lời Windows/local/Docker đã bổ sung trong hướng dẫn demo; plan Word cùng đường dẫn cũ hiện là bản cấu trúc v2 có ba cấp ở tất cả chương.

## Đã chuẩn bị và xác minh

- CSV toàn nguồn: `data/raw/oceanng/vietnam_real_estates_full.csv`; đọc lại bằng Arrow CSV parser: 3.500.744 records, 19 trường; 3.266.488.214 byte; SHA-256 `7c8f1d87105c5114e3b54c37492b0a3108d6774c407b2105e422c66c0123d3fe`. Có manifest cạnh file, raw Parquet giữ nguyên. CSV không đưa vào Git.
- Script xuất streaming: `scripts/export_source_csv.py`; không nạp toàn bộ dataset vào RAM. Lần kiểm tra hoàn tất dùng `--verify-partial` để tiếp tục xác minh/đổi tên sau lỗi giữ file Windows; đã khắc phục đóng stream và thêm retry rename.
- Script read-only `scripts/demo_spark.py` chạy qua `scripts/run.ps1 -Module scripts.demo_spark -DriverMemory 1g --no-pause`: PASS, Spark 3.5.7/local[4]. Test tạm dùng UI 4041 vì API hiện hữu đang ở 4040; context demo đã dừng, không dừng API của người dùng.
- Đếm nguồn thực 3.500.744; HCM nhà/căn hộ 1.122.870. ETL đã lưu: excluded_rent 46.151, provisional_training 149.975, quarantine 926.742; tổng 1.122.868 vì đã bỏ hai bản ghi nguồn trùng hệt. Đây là đọc output ETL, không thực thi ETL lại.
- Split thực: train 78.048, validation 17.886, test 37.845; đối chiếu tháng và loại nhà. Kết quả model đọc artifact đã khóa, không train mới.
- Hướng dẫn ba terminal, thao tác Jobs/Stages/SQL/Executors/Environment/Storage, nhánh train mới và ETL mới, yêu cầu HDFS tại `docs/guide/DEMO_QUY_TRINH_SPARK.md`.
- Kiểm tra cuối lượt: health API 8000 và health qua proxy web 3000 đều HTTP 200/status ready, data core_v1/model v1/133.779 tin. CSV và manifest xuất đều được git check-ignore xác nhận loại khỏi Git.

## Còn phải nghiệm thu với nhóm

1. Cả hai đọc và tự chạy hướng dẫn; kiểm tra môi trường/dữ liệu mỗi máy. Clone demo gọn không có raw/cohort/review đầy đủ; thống nhất máy nghiên cứu để demo hoặc chia sẻ bộ nghiên cứu riêng đúng provenance.
2. Diễn tập có điểm dừng Enter và thao tác UI, không chỉ chạy --no-pause. Cả hai biết phân biệt Spark app hiện hành, nạp model và huấn luyện.
3. Chọn trình bày kết quả train trước đó hay train trực tiếp; nếu trực tiếp, dùng thư mục output mới, đóng API/Spark khác và diễn tập thời lượng/RAM. Chưa thực thi train/ETL lại trong lần chuẩn bị này.
4. Tự chạy API/web, xem health rồi ước tính thật; thực hành so sánh và kiểm tra tin. Tham khảo TESTER_CHECKLIST.md và DEMO_THUYET_TRINH.md.
5. Đổi vai để cả hai thực hiện được toàn chu trình; ghi kết quả từng người, giới hạn dữ liệu và trả lời HDFS.
6. Khi nhóm xác nhận đạt, audit repo mới, kiểm tra tài liệu/ảnh/ZIP đúng phiên bản rồi mới tính commit/push. Không coi việc tạo tài liệu là cả hai đã nghiệm thu.

Các thay đổi trang bản đồ và báo cáo Word vẫn theo plan riêng, chưa được triển khai trong lượt này.
