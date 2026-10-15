> **Mốc hiện hành 14/10/2026 — UI/UX V4:** Người dùng đã chọn hướng B từ hai bản mẫu MCP. Đã tích hợp vào web/API thật và kiểm thử. Đọc [PLAN_TONG_HOP_UI_UX_V4.md](../plans/PLAN_TONG_HOP_UI_UX_V4.md), [NGHIEM_THU_UI_UX_V4.md](NGHIEM_THU_UI_UX_V4.md), [KICH_BAN_DEMO_UI_UX_V4.md](KICH_BAN_DEMO_UI_UX_V4.md). Các ghi chú “chỉ trao đổi/chưa triển khai” bên dưới là lịch sử đã được thay thế bằng yêu cầu tiếp tục hoàn thành.

> **Hướng thực hiện mới nhất 14/10/2026:** Người dùng đã yêu cầu dùng MCP để tiếp tục. Đọc [PLAN_TONG_HOP_UI_UX_V4.md](../plans/PLAN_TONG_HOP_UI_UX_V4.md) cho phạm vi, quy trình hai bản mẫu, tích hợp và nghiệm thu. Audit đã làm; brief MCP đang bắt đầu, chưa tạo thiết kế hoặc sửa app ở mốc lưu này.

> **Audit UI/UX 14/10/2026 đã hoàn thành, chưa sửa giao diện:** Đọc [KIEM_THU_UI_UX_2026_10_14.md](../history/KIEM_THU_UI_UX_2026_10_14.md), [BRIEF_THIET_KE_UI_UX_V3.md](../plans/BRIEF_THIET_KE_UI_UX_V3.md) và phần bổ sung [PLAN_CAI_THIEN_TRAI_NGHIEM_V3.md](../history/PLAN_CAI_THIEN_TRAI_NGHIEM_V3.md). Có bằng chứng về kết quả ngoài viewport, mất state và lỗi DNS tile; chưa chạy tạo thiết kế MCP.

> **Trao đổi mới 14/10/2026 — chưa triển khai:** Xem [PLAN_CAI_THIEN_TRAI_NGHIEM_V3.md](../history/PLAN_CAI_THIEN_TRAI_NGHIEM_V3.md) cho đề xuất bỏ tra địa danh khỏi luồng chính, làm rõ so sánh/ước tính, xử lý bản đồ online và cải thiện giải thích mô hình/ETL. Người dùng hiện chỉ yêu cầu lưu plan rồi trao đổi tiếp; không sửa code hoặc chạy tester theo đề xuất này.

> **Sản phẩm v2 đã triển khai 13/10/2026:** Đọc [NANG_CAP_SAN_PHAM_V2.md](../history/NANG_CAP_SAN_PHAM_V2.md), [KICH_BAN_DEMO_SAN_PHAM_V2.md](../history/KICH_BAN_DEMO_SAN_PHAM_V2.md) và mốc mới nhất ở [BAN_GIAO_CHO_MODEL_KHAC.md](BAN_GIAO_CHO_MODEL_KHAC.md). Các đoạn bên dưới giữ lịch sử; không dùng làm trạng thái mới nhất.

> **Cập nhật 13/10/2026:** Đọc [BAN_GIAO_CHO_MODEL_KHAC.md](BAN_GIAO_CHO_MODEL_KHAC.md) trước. Tài liệu này cập nhật lỗi launcher PowerShell, lỗi API bị dừng, kiểm tra mới, yêu cầu để Word sau và phương án demo Spark. Các mốc dưới đây giữ để truy vết lịch sử.

## Mốc bàn giao kỹ thuật 12/10/2026

Đã hoàn thành ETL v4, cohort core v1, thực nghiệm models/v1, API và giao diện web local/LAN. Tập nghiên cứu có 133.779 tin; chín pipeline cộng baseline đã đánh giá theo thời gian. Chọn LR riêng nhà/căn hộ theo validation trước test. MAE test: nhà 2,950 tỷ, căn hộ 1,395 tỷ VND; giảm so baseline 36,73% và 58,47%. Review 800 nhãn AI, v5 có 98/100 hỗ trợ cả phạm vi, Wilson 95% 93,00%–99,45%, chưa phải xác minh người.

Web có sáu màn hình, bộ lọc, xuất CSV, 22 polygon lịch sử và ước tính bằng mô hình thật. Production build và TypeScript đạt; 35 kiểm tra API đối chiếu Parquet đạt; kiểm tra sáu trang desktop/mobile, CSV, click bản đồ và dự đoán thật đạt, không có lỗi trình duyệt. Script start-local.ps1 khởi động hai dịch vụ đã được chạy kiểm tra.

Báo cáo Word 21 trang, PowerPoint 14 slide, hướng dẫn và nội dung Markdown ở deliverables và HUONG_DAN_CHAY.md. Gói bàn giao chứa mã nguồn, model, serving, địa giới, review và manifest; không chứa raw 1,6 GB hoặc môi trường cài đặt. Kết quả chi tiết ở KET_QUA_MO_HINH.md. Hướng dẫn hiện hành ở HUONG_DAN_CHAY.md trong mã nguồn.

Trước nộp, nhóm cần xác nhận tên đề tài với giảng viên và bổ sung lớp/giảng viên, nhật ký tuần, đóng góp thực tế theo NHAT_KY_VA_DONG_GOP_CAN_BO_SUNG.md. Chưa triển khai Internet. Dữ liệu chọn lọc, giá nguồn chưa xác minh, trùng tài sản khác nội dung và đuôi sai số lớn vẫn là giới hạn. Không gọi triển khai một máy là cluster hoặc dải tham khảo là bảo đảm 90%.

---

Các mốc dưới đây là lịch sử tại thời điểm viết, được giữ để truy vết. Mốc bàn giao phía trên thay thế trạng thái tiến độ cũ.

# Hồ sơ hiện hành của đồ án

**Trạng thái mới hơn các mốc bên dưới:** review v5 đã đạt 98/100 theo tham chiếu AI, bộ lọc quality v4 được giữ nguyên. ETL v4/core v1 chạy xong; tập nghiên cứu 133.779 tin, bản đồ 22 nhóm địa bàn lịch sử, bảng phân tích gọn và catalog đầu vào chỉ từ train đã xuất. Thực nghiệm mô hình thật đang chạy tại artifacts/models/v1; chỉ đọc results.json sau khi hoàn tất, không gọi validation_results là kết quả test cuối. Xem THUC_NGHIEM_MO_HINH.md và nhật ký mới nhất.

Mốc mới nhất12/10: đọc KET_QUA_EVALUATION_V2/V3/V4.md và TRANG_THAI_TRIEN_KHAI.md. Các mẫu cũ đều đã đọc xong bằng AI, không phải xác minh người. V4 đạt94/100phạm vi nên chưa đủ ngưỡng95%; đang lấy mẫu mới v5 cho quality v4. ETL v3 chạy xong153.585ứng viên nhưng chưa dùng huấn luyện. Đã có bản đồ22nhóm địa bàn cũ, codecore và codemô hình; chưa chạy mô hình giá thực hoặc web. Các mốc cuối file là lịch sử.

Đọc theo thứ tự:

1. PLAN_HUONG_DI_BIGDATA_V3.md: tên, phạm vi và phương pháp đã chốt.
2. LO_TRINH_TRIEN_KHAI.md: các mục và tiêu chí hoàn thành.
3. TRANG_THAI_TRIEN_KHAI.md: những gì đã chạy, chưa hoàn thành và vấn đề cần theo dõi.
4. BAO_CAO_KHAO_SAT.md: số liệu thực tế từ Spark.
5. KIEM_CHUNG_DU_LIEU.md: cách đọc/gán nhãn mẫu và giới hạn đánh giá.
6. MUC_02_KIEM_CHUNG_DU_LIEU.md: bộ mẫu đọc độc lập và công cụ đánh giá đã tạo.
7. File Word yêu cầu môn học: nguồn chính xác định yêu cầu học phần.

V2, bản tổng quan và de_xuat_do_an.md giữ để tham chiếu lịch sử. Những quyết định đã được V3 thay thế không còn là đặc tả triển khai.

Người dùng đã cho phép triển khai từ đầu đến hoàn thành, không dùng deadline làm giới hạn. Không hỏi lại các quyết định đã chốt. Tên mới được chốt trong nhóm, chưa có xác nhận lại từ giảng viên.

Mã nguồn ở D:\slider\real-estate-bigdata. Không nhầm số mẫu ứng viên với số mẫu sạch đã được kiểm chứng. Tài liệu hồ sơ được sao chép theo mốc; xem nhật ký trong thư mục mã nguồn để biết trạng thái mới nhất khi tiếp tục chạy.

Bổ sung phần web: MUC_07_SAN_PHAM_WEB.md, thay phương án Streamlit bằng Next.js + FastAPI theo nhu cầu giao diện tùy chỉnh. Đã chọn local/LAN trước, Internet sau. Phần web hiện chỉ là kế hoạch; hoàn thiện cốt lõi mục 02–06 trước khi lập trình frontend/API mục 07. Không tự chuyển sang dựng giao diện sớm.

Mốc triển khai mục 02: đọc KET_QUA_CALIBRATION_V1.md và QUY_UOC_GAN_NHAN.md. Đã gán nhãn AI 150 calibration; 150 evaluation chưa gán nhãn. Mã quy tắc đã cố định để đánh giá; không diễn giải chẩn đoán calibration thành độ chính xác độc lập. Số ứng viên profile cũ chưa cập nhật theo quy tắc mới.

Cập nhật12/10/2026: đọc KET_QUA_EVALUATION_V1.md và MUC_03_ETL_VA_CHAT_LUONG.md. V1đã có đủ300nhãnAI,precisionbán99/100 trên mẫu,không phải độ sạch tập huấn luyện. Giữ nguyên mã rules cố định; thêm quality.py riêng và build.py để kiểm tra chéo/táchquarantine. Cần mẫu mới đánh giá lớp chất lượng sauv1; không dùng lại evaluationv1 để xác nhận cải tiến vừa làm. Trạng thái chạy và sốETL xem nhật ký mới nhất.

Mốc bàn giao tiếp: ETL thành công ở data/processed/etl_v1_retry1, đọc lại đủ 1.122.868 dòng; 187.963 ứng viên tạm. Không dùng lượt etl_v1 lỗi trước đó. Mẫu v2 đã tạo đủ 200 tin, không trùng các mẫu trước, đã cố định mã/dự đoán nhưng chưa gán nhãn. Việc tiếp theo: đọc/gán nhãn v2 theo bằng chứng nguồn, đánh giá quality_candidates rồi kiểm tra phạm vi/địa lý/tin đăng lại; chưa chuyển sang mô hình hoặc web khi chưa đủ điều kiện.
