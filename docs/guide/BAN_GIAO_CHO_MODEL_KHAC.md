> **15/10/2026 — Yêu cầu mới nhất cho phép push:** Người dùng đã chỉ định https://github.com/HoangThaNHty/Do_An_BigData và yêu cầu kiểm tra rồi push đúng project, loại file không cần thiết. Điều này thay yêu cầu tạm hoãn trong các mốc trước; lịch sử ghi “chưa push” không còn là lệnh chặn. Giữ LICENSE/commit remote ban đầu, kiểm tra file và checksum trước commit; không force-push. Xem [GITHUB_TEAM.md](GITHUB_TEAM.md) cho lệnh clone thật. Việc push không đồng nghĩa hai thành viên đã diễn tập hoặc Word/PPT đã hoàn thiện.

> **15/10/2026 — Kịch bản thuyết trình toàn đồ án:** Đã lưu [PLAN_THUYET_TRINH_CUOI_KY.md](../plans/PLAN_THUYET_TRINH_CUOI_KY.md): bản 18–22 phút và bản rút gọn 10–12 phút, lời dẫn từng chặng, phân vai, sáu màn hình web, công nghệ, metrics, nhánh train thật, phản biện và xử lý sự cố. Đây là plan/lời dẫn, chưa tạo PPT, chưa xác nhận nhóm diễn tập xong. Plan Word cùng đường dẫn V1 hiện là cấu trúc v2 ba cấp.

> **15/10/2026 — Chuẩn bị demo, chưa push GitHub:** Người dùng yêu cầu cả hai thành viên trình bày được toàn chu trình rồi mới push. Đã xuất CSV toàn nguồn 3.500.744 dòng/19 trường trong data/raw/oceanng (ignored Git), có manifest kiểm chứng. Đọc DEMO_QUY_TRINH_SPARK.md và ../plans/PLAN_DEMO_NGHIEM_THU_V1.md. Script demo_spark read-only đã chạy PASS với driver 1g; chỉ đọc ETL/kết quả train đã lưu, không train/ETL lại. Plan Word và vai trò bản đồ vẫn đang trao đổi, chưa sửa web. Không nhầm ảnh HCM-web-inference/load model với training trực tiếp.

> **Chuẩn bị GitHub / nhóm Windows — 14/10/2026:** Mã nguồn nằm ở repo real-estate-bigdata. Tài liệu đã tách guide/plans/research/history; README là điểm vào hiện hành. Setup lần đầu: scripts/setup.ps1; chạy: scripts/start-local.ps1. Git giữ model/serving/metadata demo; raw, ETL đầy đủ và review có nội dung tin ở local. Không bỏ kiểm tra review/split frozen để tái hiện nghiên cứu. Xem SETUP.md, TESTER_CHECKLIST.md, DEMO_THUYET_TRINH.md và GITHUB_TEAM.md trong cùng thư mục. Kết quả clone check và dọn repo sẽ ghi ở REPO_GITHUB_NGHIEM_THU.md.

> **Mốc hiện hành 14/10/2026 — UI/UX V4:** Người dùng đã chọn hướng B từ hai bản mẫu MCP. Đã tích hợp vào web/API thật và kiểm thử. Đọc [PLAN_TONG_HOP_UI_UX_V4.md](../plans/PLAN_TONG_HOP_UI_UX_V4.md), [NGHIEM_THU_UI_UX_V4.md](NGHIEM_THU_UI_UX_V4.md), [KICH_BAN_DEMO_UI_UX_V4.md](KICH_BAN_DEMO_UI_UX_V4.md). Các ghi chú “chỉ trao đổi/chưa triển khai” bên dưới là lịch sử đã được thay thế bằng yêu cầu tiếp tục hoàn thành.

API 1.2.0; model/data giữ core_v1/models/v1. Các file mới: workspace-state, region-comparison, property-comparison, price-scale và workspace-v4.css; src/api/tiles.py relay OSM có cache tạm. Lựa chọn khu vực, draft/criteria và căn đã lưu giữ qua điều hướng trong phiên. Đã kiểm thử tải nền thật, lỗi/retry, 2–3 vùng, 70→90 m², 3 tin mẫu Spark, sáu trang mobile và 56 mẫu contrast. Bundle MCP ở artifacts/design/v4; không lấy fixture prototype làm logic ứng dụng. Gói V4 không có raw/môi trường/tile cache, Office vẫn snapshot cũ. Đọc nghiệm thu trước khi đổi code hoặc chạy Spark mới.


> **Hướng thực hiện mới nhất 14/10/2026:** Người dùng đã yêu cầu dùng MCP để tiếp tục. Đọc [PLAN_TONG_HOP_UI_UX_V4.md](../plans/PLAN_TONG_HOP_UI_UX_V4.md) cho phạm vi, quy trình hai bản mẫu, tích hợp và nghiệm thu. Audit đã làm; brief MCP đang bắt đầu, chưa tạo thiết kế hoặc sửa app ở mốc lưu này.

> **Audit UI/UX 14/10/2026 đã hoàn thành, chưa sửa giao diện:** Đọc [KIEM_THU_UI_UX_2026_10_14.md](../history/KIEM_THU_UI_UX_2026_10_14.md), [BRIEF_THIET_KE_UI_UX_V3.md](../plans/BRIEF_THIET_KE_UI_UX_V3.md) và phần bổ sung [PLAN_CAI_THIEN_TRAI_NGHIEM_V3.md](../history/PLAN_CAI_THIEN_TRAI_NGHIEM_V3.md). Có bằng chứng về kết quả ngoài viewport, mất state và lỗi DNS tile; chưa chạy tạo thiết kế MCP.

> **Trao đổi mới 14/10/2026 — chưa triển khai:** Xem [PLAN_CAI_THIEN_TRAI_NGHIEM_V3.md](../history/PLAN_CAI_THIEN_TRAI_NGHIEM_V3.md) cho đề xuất bỏ tra địa danh khỏi luồng chính, làm rõ so sánh/ước tính, xử lý bản đồ online và cải thiện giải thích mô hình/ETL. Người dùng hiện chỉ yêu cầu lưu plan rồi trao đổi tiếp; không sửa code hoặc chạy tester theo đề xuất này.

## Mốc mới nhất: sản phẩm v2 đã triển khai — 13/10/2026

Người dùng đã duyệt và đã triển khai nâng cấp sản phẩm: tìm khu vực theo ngân sách/diện tích và so sánh 3 vùng; bản đồ nhiều lớp/so sánh 2 vùng/liên kết ước tính; đối chiếu giá rao và so sánh A/B; nhóm tin tham khảo ±15% diện tích; khám phá sai số test; pipeline tương tác và kiểm tra tin bằng bộ quy tắc Spark thực. Dữ liệu/model giữ core_v1/models/v1, API 1.1.0.

Build và TypeScript đạt. API cũ 35 calls và mới 41 calls đạt qua proxy. QA giao diện cũ và hành trình mới đạt trên desktop/mobile, không lỗi trình duyệt; kiểm tra giá trị theo Parquet và giữ snapshot A khi sửa B. Đã xử lý lỗi proxy ECONNRESET do kết nối idle bằng Connection: close ở backend local/LAN.

Chi tiết ở [NANG_CAP_SAN_PHAM_V2.md](../history/NANG_CAP_SAN_PHAM_V2.md); hướng dẫn demo ở [KICH_BAN_DEMO_SAN_PHAM_V2.md](../history/KICH_BAN_DEMO_SAN_PHAM_V2.md). Tra địa danh hiện chỉ là danh mục lịch sử/alias Quận 2, Quận 9 về nhóm Thủ Đức; chưa có crosswalk đầy đủ phường hiện hành, GPS tài sản hoặc cập nhật giá đến 10/2026. Nền OSM online tùy chọn, chế độ offline là đường chạy QA chính.

Word/PPT giữ snapshot trước nâng cấp theo yêu cầu người dùng, chưa cập nhật hình/nội dung mới. Gói nguồn được đóng lại theo phiên bản handoff-2026-10-13-product-v2 và kiểm tra độc lập sau đóng gói; xem GOI_BAN_GIAO_SHA256.json cùng artifacts/verification/handoff_checks.json để đối chiếu ZIP và kết quả. Không dùng hash ZIP 12/10 cho phiên bản mới.

Các phần bên dưới là lịch sử trước nâng cấp này và được giữ để truy vết.

---

# Bàn giao trao đổi và triển khai — cập nhật 13/10/2026

Đọc tài liệu này trước các mốc lịch sử trong DOC_TRUOC.md và TRANG_THAI_TRIEN_KHAI.md. Mã nguồn thực nằm tại `D:\slider\real-estate-bigdata`; folder tài liệu của người dùng là `D:\slider\FolderDoAnBigData`. Các bản Markdown được sao chép sang folder tài liệu để trao đổi với model khác.

## Yêu cầu và quyết định của người dùng

- Tiếp tục hoàn thiện đồ án môn Nhập môn Big Data, ưu tiên lõi kỹ thuật và sản phẩm. Người dùng đã yêu cầu để Word tính sau; không tiếp tục hỏi thông tin bìa trong giai đoạn này.
- Chạy trình duyệt trên máy/LAN trước, Internet sau. Chưa có triển khai Internet.
- Đề tài đề xuất: “Phân tích dữ liệu tin đăng và xây dựng hệ thống ước tính giá rao bán nhà ở tại TP. Hồ Chí Minh bằng Apache Spark”. Chưa xác nhận giảng viên duyệt tên này.
- Cần trao đổi và xây dựng demo cho thấy công nghệ Big Data thực tế, không chỉ dashboard. Không thêm MongoDB chỉ để có một màn hình cơ sở dữ liệu.

## Kiến trúc và trạng thái đã làm

Luồng: Parquet nguồn → PySpark ETL → Parquet cohort có split thời gian → Spark ML → pipeline lưu trên đĩa → FastAPI → Next.js/React.

- Lưu trữ là **Parquet trên filesystem**, không dùng MongoDB, HDFS hay cụm nhiều máy. Spark 3.5.7 chạy `local[4]`, driver 4 GB, Java 17/Python 3.11. Chỉ nên chạy một Spark JVM mỗi lần trên máy hiện tại.
- Phạm vi nguồn nhà/căn hộ TP.HCM: 1.122.870 tin. ETL hiện hành `data/processed/etl_v4`; tập nghiên cứu `data/processed/core_v1` có 133.779 tin.
- Train 78.048, validation 17.886, test 37.845; chia theo thời gian. Đã loại toàn bộ ID từng đọc/review khỏi thí nghiệm và xử lý proxy tin đăng lại theo toàn văn. Không khẳng định loại hết tin cùng tài sản đổi nội dung.
- Đã huấn luyện 9 pipeline LR/RF/GBT riêng nhà, riêng căn hộ và chung, cùng baseline. Chọn LR riêng mỗi loại theo MAE validation trước khi đánh giá test; model hiện hành `artifacts/models/v1`.
- MAE test nhà khoảng 2,950 tỷ; căn hộ 1,395 tỷ VND, giảm so baseline 36,73%/58,47%. Đọc `KET_QUA_MO_HINH.md` để có đủ RMSE/R²/MAPE/ngoại lệ; không chỉ nêu MAE.
- API `src/api`, web `web` có 6 màn hình, bộ lọc, CSV tổng hợp, 22 polygon địa bàn lịch sử, form dự đoán bằng model thật.
- Chất lượng: 800 nhãn tham chiếu AI, chưa phải nhãn người độc lập. V5 hỗ trợ phạm vi cùng giá/diện tích 98/100; Wilson 95% khoảng 93,00%–99,45%, chỉ 14 mẫu nhà. Giá rao bán chưa xác minh giao dịch; không có GPS tài sản. Dataset CC BY-NC 4.0.

## Các sửa lỗi chạy trên Windows mới nhất

### 1. Script khởi động dừng ngay sau thông báo nạp model

Tái hiện bằng Windows PowerShell 5.1: stderr chứa log bình thường của Python/Uvicorn bị chuyển thành error record trong Start-Job, trong khi ErrorActionPreference là Stop.

- `scripts/run.ps1`: dùng Continue quanh lệnh native Python, rồi trở lại Stop và kiểm tra LASTEXITCODE để vẫn phát hiện module thất bại.
- `scripts/start-local.ps1`: Receive-Job trong nhánh thất bại dùng ErrorAction Continue để không che thông báo API thoát bằng dòng log đầu tiên.
- Đã chạy lại launcher bằng powershell.exe; API ready và Next.js trả HTTP 200.

### 2. Web mở được nhưng không lấy được API

Log người dùng ngày 13/10 có Application startup complete, sau đó KeyboardInterrupt, lỗi accumulator/JVM và cleanup. Kiểm tra tại thời điểm sửa: frontend 3000 vẫn lắng nghe, backend 8000 đã dừng. Kết luận chắc chắn là thiếu backend; log có tín hiệu ngắt, không khẳng định người dùng chủ động nhấn Ctrl+C.

- Khởi động lại API; các endpoint qua proxy frontend hoạt động.
- `src/api/main.py`: giữ/restores SIGINT handler của Uvicorn sau tạo SparkSession, vì Spark cài handler riêng; tránh KeyboardInterrupt làm ngắt event loop trực tiếp.
- Cleanup Spark chỉ bắt Py4JError/OSError khi JVM đã ngắt và ghi cảnh báo; không che lỗi khởi động hoặc lỗi dự đoán.
- Đã chạy **35 kiểm tra API qua http://127.0.0.1:3000**, gồm đối chiếu count/median Parquet, map, bộ lọc, dự đoán thật và input lỗi: PASS. Đã dừng/khởi động lại API và xác nhận health trực tiếp và qua proxy đều ready, overview căn hộ 114.312 tin.
- Chưa kiểm thử trực tiếp thao tác Ctrl+C trong terminal VS Code sau sửa; công cụ dừng process không chứng minh đầy đủ shutdown mềm của terminal tương tác. Không tuyên bố đã loại mọi thông báo khi đóng cưỡng bức terminal Windows.
- Bổ sung mục xử lý lỗi trong `HUONG_DAN_CHAY.md`, sao chép sang folder tài liệu. WARN winutils/native Hadoop không làm API khởi động thất bại trên cấu hình hiện tại.

## Lệnh chạy và chẩn đoán

Trong PowerShell của VS Code, mở folder mã nguồn:

```powershell
cd D:\slider\real-estate-bigdata
.\scripts\start-local.ps1
```

Giữ terminal hoạt động; chờ API nạp xong rồi Next.js Ready, mở http://localhost:3000. Có thể dùng `-Lan`. Không chạy launcher nếu hai dịch vụ đã hoạt động riêng.

Hoặc hai terminal, giữ cả hai tiến trình chạy:

```powershell
# Terminal API, thư mục gốc
.\scripts\run.ps1 src.api.serve
```

```powershell
# Terminal web
cd D:\slider\real-estate-bigdata\web
npm run start
```

Health trực tiếp: http://127.0.0.1:8000/api/v1/health; qua web: http://localhost:3000/api/v1/health; phải có status ready. Nếu chỉ web chạy thì khởi động API rồi tải lại trang. Proxy production được build với localhost:8000; đổi backend cần rebuild.

Trạng thái dịch vụ là tạm thời, không suy ra còn chạy từ tài liệu này. Kiểm tra cổng/health trước khi khởi động thêm. Không tự dừng tiến trình lạ để giải phóng cổng.

## Phương án demo môn Big Data đã trao đổi, chưa hoàn thiện thành công cụ demo riêng

Đề xuất 12–15 phút: nguồn/Parquet/schema → ETL Spark và các nhóm chất lượng → cohort/split → huấn luyện Spark ML, Spark UI → bảng đánh giá → API và sản phẩm web. Full ETL trước đó khoảng 504 giây; huấn luyện 9 pipeline khoảng 188 giây trên máy hiện tại, không bảo đảm thời gian ở buổi trình bày.

Lệnh huấn luyện thật đã hướng dẫn (dừng API trước):

```powershell
.\scripts\run.ps1 src.models.train --core data/processed/core_v1 --output artifacts/models/demo_01
```

Thư mục output phải mới; demo lần sau đổi tên. Model mới không tự thay model v1 của web. Spark UI thường ở http://localhost:4040 trong lúc Spark còn sống, có thể chuyển cổng nếu bị chiếm; cần diễn tập để xác nhận địa chỉ và những tab thật có nội dung. Chưa diễn tập riêng một buổi demo end-to-end cùng người dùng.

### Việc tiếp theo nên trao đổi/làm

1. Chốt thời lượng demo và phần chạy live: đề xuất live huấn luyện, phần ETL dùng đầu ra đã kiểm chứng + giải thích code, hoặc live ETL nếu đủ thời gian. Nếu dùng mẫu nhỏ phải ghi rõ quy mô demo khác thí nghiệm chính.
2. Tạo kịch bản/demo runbook có lệnh an toàn, output mới, điểm cần mở trong Spark UI, schema/count/manifest và file kết quả cần đối chiếu. Hiện chỉ có hướng dẫn tổng quát và đề xuất trong chat, chưa có runner demo chuyên dụng.
3. Diễn tập thao tác bằng VS Code, khởi động/dừng cả hai dịch vụ, kiểm tra giao diện và trường hợp backend chưa chạy. Không đổi pipeline/split theo kết quả test để làm chỉ số đẹp hơn.
4. Word/slide đã có bản kỹ thuật nhưng người dùng yêu cầu để sau. Thông tin giảng viên/lớp/duyệt đề tài/nhật ký/đóng góp cần người thật xác nhận, không tự bịa.

## Cách đọc hồ sơ và gói bàn giao

- Đọc tài liệu này → DOC_TRUOC.md → PLAN_HUONG_DI_BIGDATA_V3.md → KET_QUA_MO_HINH.md → HUONG_DAN_CHAY.md → mã nguồn liên quan.
- DOC_TRUOC/TRANG_THAI/plan có nhiều mốc lịch sử. Các đoạn “chưa chạy mô hình/chưa làm web” là trạng thái cũ, không thay thế bàn giao hiện tại.
- ZIP bàn giao ngày 12/10 là snapshot trước các sửa launcher/API gần đây. **Chưa đóng gói lại ZIP sau các sửa lỗi này**; nếu bàn giao cho máy khác cần cập nhật và kiểm chứng lại archive. Không dùng receipt kiểm tra ZIP cũ làm bằng chứng cho source hiện hành.
- API check hiện tại: `artifacts/verification/api_checks.json`. Build web/QA browser đã đạt ở mốc 12/10; sau sửa 13/10 chỉ chạy lại API checks, compile Python và health, chưa chạy lại toàn bộ browser QA.
