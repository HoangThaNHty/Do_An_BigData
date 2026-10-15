> **Sản phẩm v2 đã triển khai 13/10/2026:** Đọc [NANG_CAP_SAN_PHAM_V2.md](NANG_CAP_SAN_PHAM_V2.md), [KICH_BAN_DEMO_SAN_PHAM_V2.md](KICH_BAN_DEMO_SAN_PHAM_V2.md) và mốc mới nhất ở [BAN_GIAO_CHO_MODEL_KHAC.md](../guide/BAN_GIAO_CHO_MODEL_KHAC.md). Các đoạn bên dưới giữ lịch sử; không dùng làm trạng thái mới nhất.

## Mốc bàn giao kỹ thuật 12/10/2026

Đã hoàn thành ETL v4, cohort core v1, thực nghiệm models/v1, API và giao diện web local/LAN. Tập nghiên cứu có 133.779 tin; chín pipeline cộng baseline đã đánh giá theo thời gian. Chọn LR riêng nhà/căn hộ theo validation trước test. MAE test: nhà 2,950 tỷ, căn hộ 1,395 tỷ VND; giảm so baseline 36,73% và 58,47%. Review 800 nhãn AI, v5 có 98/100 hỗ trợ cả phạm vi, Wilson 95% 93,00%–99,45%, chưa phải xác minh người.

Web có sáu màn hình, bộ lọc, xuất CSV, 22 polygon lịch sử và ước tính bằng mô hình thật. Production build và TypeScript đạt; 35 kiểm tra API đối chiếu Parquet đạt; kiểm tra sáu trang desktop/mobile, CSV, click bản đồ và dự đoán thật đạt, không có lỗi trình duyệt. Script start-local.ps1 khởi động hai dịch vụ đã được chạy kiểm tra.

Báo cáo Word 21 trang, PowerPoint 14 slide, hướng dẫn và nội dung Markdown ở deliverables và HUONG_DAN_CHAY.md. Gói bàn giao chứa mã nguồn, model, serving, địa giới, review và manifest; không chứa raw 1,6 GB hoặc môi trường cài đặt. Kết quả chi tiết ở KET_QUA_MO_HINH.md. Hướng dẫn hiện hành ở HUONG_DAN_CHAY.md trong mã nguồn.

Trước nộp, nhóm cần xác nhận tên đề tài với giảng viên và bổ sung lớp/giảng viên, nhật ký tuần, đóng góp thực tế theo NHAT_KY_VA_DONG_GOP_CAN_BO_SUNG.md. Chưa triển khai Internet. Dữ liệu chọn lọc, giá nguồn chưa xác minh, trùng tài sản khác nội dung và đuôi sai số lớn vẫn là giới hạn. Không gọi triển khai một máy là cluster hoặc dải tham khảo là bảo đảm 90%.

---

Các mốc dưới đây là lịch sử tại thời điểm viết, được giữ để truy vết. Mốc bàn giao phía trên thay thế trạng thái tiến độ cũ.

# Mục 07 Sản phẩm web phân tích nhà ở

Cập nhật: 11/10/2026. Bổ sung kế hoạch V3 theo yêu cầu phát triển giao diện web chi tiết.

Người dùng đã chọn chạy bằng trình duyệt trên máy/LAN trước, sau đó đưa lên Internet. Tài liệu này đặc tả phần web; chưa có frontend/API được cài đặt hoặc triển khai ở mốc lưu này. Mục 02 kiểm chứng dữ liệu vẫn đang thực hiện.

## 1. Quyết định công nghệ

Thay hướng dashboard Streamlit ban đầu bằng ứng dụng web tách giao diện và API để tùy chỉnh giao diện từ thư viện/component mã nguồn mở.

| Lớp | Công nghệ và trách nhiệm |
|---|---|
| Giao diện | Next.js + React + TypeScript |
| Component và style | shadcn/ui + Tailwind CSS; Lucide cho icon |
| Biểu đồ | Recharts; kiểm tra phiên bản tương thích khi cài |
| Bản đồ | Leaflet tích hợp React, GeoJSON đúng phiên bản địa giới |
| API | FastAPI, Pydantic, Uvicorn |
| ETL và ML | PySpark/Spark SQL/Spark MLlib, giữ kiến trúc đã chốt |
| Dữ liệu | Parquet là nguồn ETL/ML; bảng tổng hợp gọn cho API; MongoDB nếu cần truy vấn tin |
| Thiết kế hỗ trợ | OpenDesign để tạo prototype/design system khi xác định đúng repo và cách xuất mã |

Frontend không tải toàn bộ dataset và không chạy Spark trong trình duyệt. API không huấn luyện khi người dùng nhấn nút dự đoán. Dữ liệu nguồn và pipeline gốc vẫn giữ nguyên; chuyển web không yêu cầu làm lại ETL/ML.

## 2. OpenDesign và template cloner

Repo OpenDesign được khảo sát: https://github.com/nexu-io/open-design. Đây là cách hiểu hiện tại của tên OpenDesign người dùng nhắc đến, chưa có link cụ thể do người dùng cung cấp. Dự án là workspace/công cụ thiết kế, không phải thư viện React component. Nếu người dùng nói đến dự án khác thì cập nhật tài liệu.

Ưu tiên: thiết kế trải nghiệm bằng brief và DESIGN.md; dựng component bằng shadcn/ui; OpenDesign hỗ trợ khám phá bố cục, màu, typography và prototype. Mã prototype cần được chuyển thành component, nối API và kiểm tra hành vi thực tế.

Repo người dùng cung cấp: https://github.com/JCodesMore/ai-website-cloner-template. README hiện mô tả Next.js 16, React 19, TypeScript, Tailwind v4, shadcn/ui và Node >=24; giấy phép MIT. Máy đã có Node 26.5.0 khi kiểm tra, nhưng vẫn cần kiểm tra dependency/build khi tạo frontend.

Template cloner là phương án dựng khung hoặc tái hiện một bố cục tham chiếu khi đã có URL. Nó không tạo sẵn API, dữ liệu sạch hoặc mô hình định giá. Tham chiếu dashboard mã nguồn mở trước; điều chỉnh nội dung, thương hiệu và chức năng theo đồ án. Ghi nguồn và giữ thông báo license cho mã/assets tái sử dụng. Không nhập nguyên một bộ công cụ thiết kế vào runtime sản phẩm.

## 3. Kiến trúc vận hành

```text
Dataset -> Spark ETL -> Parquet sạch/ứng viên + bảng tổng hợp
                           |
                           -> Spark MLlib train/evaluate -> model + metadata

Trình duyệt -> Next.js web -> /api -> FastAPI
                                     |-> bảng tổng hợp nhỏ cho biểu đồ/bản đồ
                                     |-> pipeline Spark đã lưu cho dự đoán
                                     |-> chỉ số, phạm vi và phiên bản mô hình
```

Tách quá trình batch ETL/train khỏi API phục vụ. API có thể chạy thống kê khi chưa có mô hình; endpoint dự đoán trả trạng thái chưa sẵn sàng rõ ràng thay vì sinh giá giả.

Trong bản đầu, chạy một worker phục vụ inference Spark để tránh nhân bản JVM/mô hình trong RAM. Load Spark/pipeline một lần, kiểm soát số request dự đoán đồng thời và đo độ trễ. Nâng cấp hàng đợi/batch hoặc dịch vụ inference riêng khi có số liệu nhu cầu; không tự chuyển mô hình sang sklearn.

## 4. Cấu trúc giao diện

Tên hiển thị dự kiến: Nhà ở TP.HCM — Phân tích và ước tính giá rao bán. Sidebar điều hướng, thanh bộ lọc chung, nội dung phân tích rộng và typography tiếng Việt rõ. Ưu tiên desktop/laptop; menu và form dùng được trên điện thoại.

| Trang | Nội dung và tương tác |
|---|---|
| Tổng quan | Số tin đúng phạm vi lọc, trung vị giá, trung vị đơn giá theo loại tài sản, phân bố diện tích và thời gian |
| Khám phá thị trường | Biểu đồ theo loại nhà/quận/tháng, bảng thống kê sắp xếp, so sánh khu vực và xuất bảng tổng hợp |
| Bản đồ giá | Choropleth quận/huyện, chú giải, tooltip đơn giá/số mẫu/thời gian/loại nhà; click để xem phân tích khu vực |
| Ước tính giá | Form theo nhà/căn hộ; diện tích với loại đo đúng, quận/phường khi hỗ trợ, phòng/tầng và đặc trưng thuộc mô hình |
| Đánh giá mô hình | Baseline/LR/RF/GBT, MAE/RMSE/R², thời gian split, sai số phân khúc, phiên bản mô hình |
| Dữ liệu và phương pháp | Nguồn, thời gian, cách lọc và số mẫu, phạm vi địa giới, giới hạn và license |

Trang ước tính: chỉ yêu cầu đặc trưng đã được mô hình dùng và đã xác định ý nghĩa. Field tùy chọn phải sử dụng cùng cách xử lý thiếu như huấn luyện. Trả giá rao bán dự đoán, loại mô hình, thời gian dữ liệu và sai số kiểm tra tương ứng. Không gọi MAE là khoảng tin cậy cá nhân. Không hiển thị khoảng dự đoán nếu chưa kiểm chứng phương pháp.

Không thêm đăng nhập, rao tin, thanh toán, quản trị người dùng hay chatbot vào bản chính. Có thể lưu so sánh đầu vào trong phiên trình duyệt nếu hữu ích, chưa cần hệ tài khoản.

## 5. Dữ liệu và hợp đồng API dự kiến

API phiên bản `/api/v1`. Mọi thống kê trả cùng `scope`, `data_version`, `generated_at`, `sample_count`, trạng thái kiểm chứng để frontend không trộn thống kê thô với dữ liệu huấn luyện.

| Endpoint | Đầu ra |
|---|---|
| GET /health | API hoạt động, dữ liệu và mô hình có sẵn hay chưa |
| GET /metadata | Nguồn, phiên bản, loại tài sản, địa giới và phạm vi |
| GET /filters | Danh sách quận/phường/loại nhà/thời gian hỗ trợ |
| GET /overview | Thống kê theo bộ lọc |
| GET /market/trends | Tổng hợp theo tháng, kèm số tin |
| GET /market/districts | Thống kê khu vực, có phân trang khi cần |
| GET /map/districts | GeoJSON và chỉ số thống kê tương ứng; không tạo ranh giới giả |
| GET /models/metrics | Chỉ số thực nghiệm và phiên bản mô hình |
| POST /predict | Kiểm tra đầu vào, dự đoán bằng pipeline đã lưu, metadata kết quả |

Các tên cuối cùng được cố định lúc lập trình. Không nhận tên/path mô hình tùy ý từ client. Các quận/phường lạ hoặc loại nhà chưa được hỗ trợ phải được xử lý theo hợp đồng rõ, không âm thầm suy ra vị trí.

## 6. Quy tắc hiển thị

- Số liệu thật lấy từ API; dữ liệu demo nếu dùng phải tách chế độ và ghi rõ.
- Kết quả khảo sát hiện tại chưa phải thị trường tin bán đã làm sạch. Ghi rõ phạm vi khi hiển thị.
- Giá tổng hiển thị tỷ VND; đơn giá triệu VND/m², phân biệt nhà theo m² đất và căn hộ theo m² căn hộ.
- Trung vị là chỉ số chính; số mẫu luôn đi cùng số giá khu vực.
- Có trạng thái loading, rỗng, lỗi kết nối, ít mẫu và mô hình chưa sẵn sàng.
- Bộ lọc được đồng bộ giữa bảng, biểu đồ và bản đồ; có nút đặt lại.
- Điều hướng bàn phím, label form và độ tương phản đủ đọc; không dùng màu làm dấu hiệu duy nhất.
- Bản đồ nền trực tuyến có thể cần Internet ngay cả khi web chạy local; nếu không có mạng, vẫn có ranh giới và bảng khu vực, không để toàn trang hỏng. Dùng tile provider phù hợp và giữ attribution.

## 7. Chạy local/LAN và Internet

Giai đoạn đầu: dev frontend ở localhost:3000 và API ở localhost:8000, dùng proxy `/api` để trình duyệt không phải biết địa chỉ backend. Demo bản build production, không chỉ dựa trên dev server.

LAN: frontend lắng nghe địa chỉ mạng khi chạy demo; backend có thể chỉ lắng nghe loopback nếu proxy cùng máy. Dùng địa chỉ máy trong LAN thay localhost trên máy khác. Việc mở firewall chỉ làm khi thực tế cần và trong phạm vi demo. Không mặc định mở cổng router ra Internet.

Sau khi sản phẩm chạy xuyên suốt: chọn máy chủ có Python + Java + RAM đủ cho pipeline inference. Frontend có thể cùng server hoặc host riêng; API đặt sau HTTPS/reverse proxy, có kiểm soát đầu vào và tải. Frontend host tĩnh/serverless không tự chạy được Spark Java. Chọn nhà cung cấp và chi phí sau khi đo bộ nhớ/độ trễ, chưa thuê hay công bố URL ở giai đoạn này.

## 8. Các tiểu mục triển khai web

| Tiểu mục | Sản phẩm hoàn thành |
|---|---|
| 07.1 | Brief, DESIGN.md, layout các trang, component và API contract |
| 07.2 | Khung Next.js, điều hướng, responsive, trạng thái dữ liệu; trang tổng quan dùng thống kê thật |
| 07.3 | FastAPI nối bảng tổng hợp; bộ lọc và biểu đồ cùng phạm vi |
| 07.4 | Bản đồ ranh giới và popup giá/số mẫu đúng dữ liệu |
| 07.5 | Form dự đoán nối pipeline đã lưu; validation và xử lý lỗi |
| 07.6 | Trang kết quả mô hình và dữ liệu/phương pháp |
| 07.7 | Build production, kiểm tra máy/LAN, hướng dẫn khởi chạy |
| 07.8 | Đánh giá triển khai Internet sau khi bản local hoàn chỉnh |

Ưu tiên đã chốt lại: hoàn thiện phần cốt lõi ở mục 02–06 trước khi triển khai 07.1 hoặc khung giao diện/API. Tài liệu này hiện chỉ là đặc tả trao đổi. Điều kiện bắt đầu web: dữ liệu đã kiểm chứng, ETL tái chạy được, thống kê có phạm vi rõ, mô hình đã đánh giá và pipeline lưu/nạp/dự đoán bằng script được. Các tính năng chưa sẵn sàng phải hiển thị đúng trạng thái. Chưa coi mục 07 hoàn thành chỉ vì có prototype đẹp.

## 9. Nguồn tham khảo đã đọc

- Template cloner: https://github.com/JCodesMore/ai-website-cloner-template
- OpenDesign đang được hiểu trong tài liệu: https://github.com/nexu-io/open-design
- Component: https://ui.shadcn.com/docs
- FastAPI workers: https://fastapi.tiangolo.com/deployment/server-workers/

Các phiên bản/thông tin repo cần được khóa lại theo commit khi sử dụng mã thực tế.
