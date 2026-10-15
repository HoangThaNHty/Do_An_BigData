> **Mốc hiện hành 14/10/2026 — UI/UX V4:** Người dùng đã chọn hướng B từ hai bản mẫu MCP. Đã tích hợp vào web/API thật và kiểm thử. Đọc [PLAN_TONG_HOP_UI_UX_V4.md](../plans/PLAN_TONG_HOP_UI_UX_V4.md), [NGHIEM_THU_UI_UX_V4.md](../guide/NGHIEM_THU_UI_UX_V4.md), [KICH_BAN_DEMO_UI_UX_V4.md](../guide/KICH_BAN_DEMO_UI_UX_V4.md). Các ghi chú “chỉ trao đổi/chưa triển khai” bên dưới là lịch sử đã được thay thế bằng yêu cầu tiếp tục hoàn thành.

> **Hướng thực hiện mới nhất 14/10/2026:** Người dùng đã yêu cầu dùng MCP để tiếp tục. Đọc [PLAN_TONG_HOP_UI_UX_V4.md](../plans/PLAN_TONG_HOP_UI_UX_V4.md) cho phạm vi, quy trình hai bản mẫu, tích hợp và nghiệm thu. Audit đã làm; brief MCP đang bắt đầu, chưa tạo thiết kế hoặc sửa app ở mốc lưu này.

> **Audit UI/UX 14/10/2026 đã hoàn thành, chưa sửa giao diện:** Đọc [KIEM_THU_UI_UX_2026_10_14.md](KIEM_THU_UI_UX_2026_10_14.md), [BRIEF_THIET_KE_UI_UX_V3.md](../plans/BRIEF_THIET_KE_UI_UX_V3.md) và phần bổ sung [PLAN_CAI_THIEN_TRAI_NGHIEM_V3.md](PLAN_CAI_THIEN_TRAI_NGHIEM_V3.md). Có bằng chứng về kết quả ngoài viewport, mất state và lỗi DNS tile; chưa chạy tạo thiết kế MCP.

> **Trao đổi mới 14/10/2026 — chưa triển khai:** Xem [PLAN_CAI_THIEN_TRAI_NGHIEM_V3.md](PLAN_CAI_THIEN_TRAI_NGHIEM_V3.md) cho đề xuất bỏ tra địa danh khỏi luồng chính, làm rõ so sánh/ước tính, xử lý bản đồ online và cải thiện giải thích mô hình/ETL. Người dùng hiện chỉ yêu cầu lưu plan rồi trao đổi tiếp; không sửa code hoặc chạy tester theo đề xuất này.

> **Sản phẩm v2 đã triển khai 13/10/2026:** Đọc [NANG_CAP_SAN_PHAM_V2.md](NANG_CAP_SAN_PHAM_V2.md), [KICH_BAN_DEMO_SAN_PHAM_V2.md](KICH_BAN_DEMO_SAN_PHAM_V2.md) và mốc mới nhất ở [BAN_GIAO_CHO_MODEL_KHAC.md](../guide/BAN_GIAO_CHO_MODEL_KHAC.md). Các đoạn bên dưới giữ lịch sử; không dùng làm trạng thái mới nhất.

> **Cập nhật 13/10/2026:** Trạng thái trao đổi và sửa lỗi mới nhất ở [BAN_GIAO_CHO_MODEL_KHAC.md](../guide/BAN_GIAO_CHO_MODEL_KHAC.md). ZIP 12/10 chưa chứa các sửa lỗi launcher/API mới; không dùng các mốc lịch sử bên dưới thay trạng thái hiện tại.

## Mốc bàn giao kỹ thuật 12/10/2026

Đã hoàn thành ETL v4, cohort core v1, thực nghiệm models/v1, API và giao diện web local/LAN. Tập nghiên cứu có 133.779 tin; chín pipeline cộng baseline đã đánh giá theo thời gian. Chọn LR riêng nhà/căn hộ theo validation trước test. MAE test: nhà 2,950 tỷ, căn hộ 1,395 tỷ VND; giảm so baseline 36,73% và 58,47%. Review 800 nhãn AI, v5 có 98/100 hỗ trợ cả phạm vi, Wilson 95% 93,00%–99,45%, chưa phải xác minh người.

Web có sáu màn hình, bộ lọc, xuất CSV, 22 polygon lịch sử và ước tính bằng mô hình thật. Production build và TypeScript đạt; 35 kiểm tra API đối chiếu Parquet đạt; kiểm tra sáu trang desktop/mobile, CSV, click bản đồ và dự đoán thật đạt, không có lỗi trình duyệt. Script start-local.ps1 khởi động hai dịch vụ đã được chạy kiểm tra.

Báo cáo Word 21 trang, PowerPoint 14 slide, hướng dẫn và nội dung Markdown ở deliverables và HUONG_DAN_CHAY.md. Gói bàn giao chứa mã nguồn, model, serving, địa giới, review và manifest; không chứa raw 1,6 GB hoặc môi trường cài đặt. Kết quả chi tiết ở KET_QUA_MO_HINH.md. Hướng dẫn hiện hành ở HUONG_DAN_CHAY.md trong mã nguồn.

Trước nộp, nhóm cần xác nhận tên đề tài với giảng viên và bổ sung lớp/giảng viên, nhật ký tuần, đóng góp thực tế theo NHAT_KY_VA_DONG_GOP_CAN_BO_SUNG.md. Chưa triển khai Internet. Dữ liệu chọn lọc, giá nguồn chưa xác minh, trùng tài sản khác nội dung và đuôi sai số lớn vẫn là giới hạn. Không gọi triển khai một máy là cluster hoặc dải tham khảo là bảo đảm 90%.

---

Các mốc dưới đây là lịch sử tại thời điểm viết, được giữ để truy vết. Mốc bàn giao phía trên thay thế trạng thái tiến độ cũ.

# Trạng thái triển khai

## Mốc tiếp tục mới nhất — 12/10/2026

**Lõi mục 02–06 hoàn tất và bắt đầu web:** Serving xuất133.779dòng vàcatalog đầu vào chỉtừtrain. Thực nghiệm9pipeline LR/RF/GBT riêng/chung vàbaseline hoàn tất187,60giây; selection.json lưu trước test, chọnhouse_lr/apartment_lr. Test nhà4705tin:MAE2,9496tỷ,RMSE18,1589tỷ,R²0,3200,MAPE23,676%,medianAPE16,568%; baselineMAE4,6622tỷ (giảm36,73%). Test căn hộ33140tin:MAE1,3949tỷ,RMSE4,5860tỷ,R²0,7399,MAPE18,629%,medianAPE13,738%; baselineMAE3,3586tỷ (giảm58,47%). Dải tham khảo90%fitvalidation coverage thựctest90,12%nhà/86,00%căn hộ, không bảo đảm90%.10sai sốlớn nhất chiếm92,20%SSEnhà và42,47%SSEcăn hộ. Dự đoánCLI từartifact đãnạp chạyđược (căn70m2 ThủĐức2PN2WC dự ánGrandPark khoảng3,7285tỷ, không dùnglàmgiáthẩm định).

Đã tạoartifacts/figures vàerror_tail_diagnostics. FastAPI0.143/Uvicorn0.54 đãcài, codeAPI trongsrc/api; đang khởi động/kiểmtra. KhungNext16.4/React19.3/TS7/Tailwind4.3/Recharts/Leaflet ởweb, npmđangcài; chưa viếtcomponents/dashboard hoặcgiao diệnchạy được. ĐãđọcskillSites, áp dụnglocal-only theo lựa chọnmáy/LANtrước, chưađăngký/deploySites. SkillBrowserđãđọcphầnđầu, chưabootstrap hoặcQAbrowser. Word/PPTchưa soạn; DocumentsSKILLđãđọc100dòngđầu, dependencyloadertoolkhôngcó; WindowsđãcóWord vàPowerPointCOM, chưa dùngtạoartifact. Không cóagentphụ, chỉ1SparkJVMmỗi lần.

**Core thực tế đã hoàn tất:** ETL v4 ghi/đọc lại1.122.868dòng,149.975ứng viên (22.789nhà,127.186căn hộ),503,59giây. Corev1 cùng qualityhashreviewv5: loại428ứng viên nằm trong2.480row_id từngreview;149.547tin ghép quận được. Loại15.768tinlặp/ngoàigiai đoạn, còn133.779tin. Có2.734nhóm toànvăn trước xử lý xuất hiện nhiều giai đoạn; sau xử lý không córepost_group trùng giữa cácsplit. Đây làproxytoànvăn, chưa loại hết cùng tài sản đổi nội dung.

Train:65.856căn hộ +12.192nhà =78.048. Validation:15.316căn hộ +2.570nhà =17.886. Test:33.140căn hộ +4.705nhà =37.845. Ghép quận100%trên ứng viên; ghép quận+phường123.516/149.975, thiếuphường26.020, khácphiênbản/chưakhớp439. Đã xuấtGeoJSON22nhóm địa bàn cũ và tổng hợpquận/tháng. Nguồn chínhdata/processed/core_v1/manifest.json, không dùng cácETLcũ để huấn luyện. Đang xuất bảngphụcvụ phân tích bằngserving.py, rồi chạy mô hình thật. Mô hình chưa cókếtquả ở mốc này.

**Sau evaluationv5:** Đã đọc100/100tin mới trước xem dự đoán;98/100được hỗ trợ cảgiá/diện tích/phạm vi, Wilson95%93,0%–99,45%. Theo loại14/14nhà,84/86căn hộ; sốnhà nhỏ không chứng minh100%toànnguồn. Đạt ngưỡngđiểm95%định trước, giữ qualityv4 SHA715b5b317087f9f347813d029f6114df7743dc3374dc158d46b9f5d58beb92d4. ETL v4 đang chạy, chờ đọc lại/manifest để chạy core với reviewv5. Không sửa quality nữa dựa trênv5. Core loại tấtcảrow_id từngreview khỏi thí nghiệmgiá, chuẩn hóa địa bàn, nhóm tinlặp toànvăn vàchia thời gian. MLsmoke đãđạt median chỉfittrain, cộttrainthiếuhoàn toàn, categorychưa thấy, lưu/nạp predictiongiốngnhau. MãML thực chưa chạy. Thiết kếđã cốđịnh tạiTHUC_NGHIEM_MO_HINH.md. Hai lỗi giỏhàng được công bố trongKET_QUA_EVALUATION_V5.md.

**Cập nhật sau v4:** ETL v3 hoàn tất trong469,28giây, đọc lại đủ1.122.868dòng; ứng viên25.517nhà +128.068căn hộ =153.585. Mẫu v4 đã đọc100/100nhãnAI, được hỗ trợ giá/diện tích97/100 và thêm phạm vi94/100, chưa đạt95%. Không dùng ETL v3 huấn luyện chính. Quality v4 đã đạt32kiểm tra hồi quy; đang chuẩn bị mẫu mới v5. Mã mô hình train/validation/test, baseline/LR/RF/GBT và inference đã viết trong src/models nhưng chưa chạy trên dữ liệu thực. Đây là trạng thái mới nhất, các đoạn dưới là lịch sử.

Evaluation v2 đã đọc đủ 200/200: 133 dự đoán bán đều phù hợp tham chiếu AI; 24/26 ứng viên được hỗ trợ giá/diện tích, còn vấn đề giá khởi điểm và vốn ban đầu. ETL v2 đã hoàn tất 1.122.868 dòng: 51.496 nhà và 130.575 căn hộ là ứng viên tạm (182.071 tổng), chưa dùng huấn luyện.

Evaluation v3 mới gồm 100 ứng viên, đã gán nhãn AI đủ 100 trước xem dự đoán. 96/100 hỗ trợ giá/diện tích, 83/100 đủ thêm phạm vi nhà ở; chưa đạt ngưỡng nghiên cứu 95% định trước. Xem KET_QUA_EVALUATION_V3.md. Quality v3 đang được kiểm tra hồi quy; sau đó cần mẫu mới v4. Giữ nguyên rules.py và các snapshot cũ.

Đã tải dữ liệu địa giới có revision/license/hash: mã hành chính trước hợp nhất 2025 và polygon quận/huyện 2020. Bản đồ 22 nhóm địa bàn TP.HCM cũ đã xuất; Quận 2/9/Thủ Đức hợp polygon vào mã 769. Không có GPS từng tài sản. geography.py và core.py đã viết; kiểm tra ghép địa danh, tách theo thời gian và loại tin lặp toàn văn đạt. Chưa chạy core thực tế vì chờ bộ lọc đạt tiêu chí trên mẫu mới.

Chưa huấn luyện mô hình giá thực, chưa viết web/API. Tiếp tục tự động mục 03–06 trước giao diện, sau đó tài liệu bàn giao. Các phần bên dưới là lịch sử và có thể chứa số liệu phiên bản cũ.

## Trạng thái hiện hành — 12/10/2026

Các phần ngày 11/10 bên dưới là nhật ký lịch sử. Trạng thái mới nhất:

- Đã đọc và gán nhãn AI đủ 300 tin v1: 150 calibration và 150 evaluation. Nhãn có bằng chứng, không phải ground truth do người xác nhận.
- Giữ nguyên rules.py đã cố định, SHA256 a2b7d760d9507f807edfbae6d414b575235ef399376581d018fda35b01a35b8e.
- Evaluation: 99/100 dự đoán bán phù hợp nhãn AI; nhận được 99/112 tin bán tham chiếu; đồng thuận loại diện tích 101/150. Chỉ có 1 nhãn thuê nên không suy rộng hiệu quả nhận diện thuê.
- 6/34 ứng viên evaluation còn vấn đề giá/diện tích. Precision bán không chứng minh dữ liệu huấn luyện sạch. Chi tiết KET_QUA_EVALUATION_V1.md.
- Thêm quality.py riêng để đối chiếu giá, diện tích, phạm vi; 11 kiểm tra hồi quy đạt. Lớp này hình thành sau evaluation v1 nên cần mẫu mới.
- build.py đã đếm 1.122.870 nhà/căn hộ TP.HCM, chỉ có 2 bản ghi nguồn trùng hoàn toàn. Lượt data/processed/etl_v1 lỗi commit phân vùng, chưa có manifest hoàn thành, không được dùng huấn luyện.
- Đã sửa adapter Java: dấu / cuối URI thư mục làm Hadoop đọc tên rỗng. Kiểm tra Parquet phân vùng tên tiếng Việt, tháng null và ghi đè đều đạt. Lượt data/processed/etl_v1_retry1 đã hoàn tất trong 321,76 giây, đọc lại đủ 1.122.868 dòng và có manifest.
- Ứng viên tạm: 53.101 nhà, 134.862 căn hộ. Quarantine: 749.621 nhà, 139.133 căn hộ. Xác định thuê: 40.198 nhà, 5.953 căn hộ. Tất cả vẫn giữ dữ liệu nguồn và mã lý do; chưa coi ứng viên tạm là sạch đã duyệt.
- Đã tạo và cố định mẫu evaluation v2: 200 row_id duy nhất, không trùng 1.980 row_id của các mẫu trước. Phiếu không hiển thị dự đoán; nhãn hiện 0/200 nên metrics=null. Snapshot rules/quality, manifest, freeze.json và fingerprint dự đoán đã lưu. Chưa đánh giá lớp chất lượng mới.

Mục 03 đang triển khai, chưa chuẩn hóa địa giới/ghép bản đồ, chưa xử lý tin đăng lại cùng tài sản hoặc chia train/test. Chưa huấn luyện mô hình giá nhà thật; chưa triển khai web/API. Giữ thứ tự cốt lõi mục 02–06 trước mục 07. Số ứng viên profile cũ thuộc quy tắc ban đầu, không phải số sạch của ETL mới. Đọc MUC_03_ETL_VA_CHAT_LUONG.md để tiếp nối.

## Nhật ký trước mốc 12/10

Cập nhật: 11/10/2026. Kế hoạch chính: PLAN_HUONG_DI_BIGDATA_V3.md.

## Đã hoàn thành

- Chốt tên, phạm vi và ba phương pháp xử lý với người dùng; đồng bộ bản plan vào docs.
- Tạo môi trường Python 3.11 riêng trên ổ D và cài PySpark 3.5.7.
- Tải JDK 17 portable, kiểm tra SHA256; không đổi Java hệ thống.
- Tải đủ 10 shard oceanNG theo revision 6f68fe87be7577afb03e38c535bd882d242ba26d, kiểm tra SHA256 từng file.
- Metadata Parquet xác nhận 3.500.744 dòng toàn bộ.
- Viết quy tắc Spark tạo nhãn giao dịch, loại diện tích, địa danh chuẩn hóa và mã lý do.
- Kiểm tra hồi quy đã mở rộng từ 8 lên 27 tình huống giao dịch/diện tích/phạm vi/giá hữu hạn, với cả giá số và giá chuỗi; đã pass.
- Viết adapter local filesystem Windows; kiểm tra ghi/đọc/ghi đè Parquet và MLlib fit/lưu/nạp mô hình nhỏ đã pass.

## Kết quả khảo sát hoàn thành

Spark xác nhận 1.357.526 tin TP.HCM, gồm 842.922 nhà và 279.948 căn hộ. Quy tắc ban đầu giữ 18,456 nhà và 153,198 căn hộ làm ứng viên. Chưa coi đây là dữ liệu sạch đã kiểm chứng.

Đã sửa kiểu price từ chuỗi sang double và chạy lại profile toàn bộ. Kết quả cuối ở artifacts/profile/profile.json, mẫu kiểm tra 1,680 dòng ở artifacts/profile/manual_review.csv, báo cáo tại docs/BAO_CAO_KHAO_SAT.md.

## Chưa hoàn thành

- Gán nhãn và đánh giá mẫu độc lập; hiệu chỉnh quy tắc.
- ETL chính, chuẩn hóa phiên bản địa giới và ghép bản đồ.
- Huấn luyện/so sánh mô hình giá nhà thật và đánh giá test cuối.
- Dashboard, tích hợp MongoDB nếu cần, báo cáo Word và slide.

Không coi candidate_eligible là nhãn sạch đã duyệt. Không có số liệu precision hoặc hiệu quả mô hình giá nhà tại thời điểm ghi nhật ký này.

## Phát hiện cần theo dõi

Schema thực tế lưu giá dưới dạng chuỗi. Không so sánh trực tiếp giá chuỗi với số nguyên 0 vì có thể ép sang int32 và gây null cho giá hàng tỷ đồng. Mã đã chuyển double rõ ràng; kiểm tra giá chuỗi hàng tỷ đã pass.

Quy tắc diện tích ban đầu ghi nhận 37.108 tin nhà có diện tích đất khớp area, còn phần lớn chưa rõ loại diện tích. Đây là bằng chứng theo quy tắc, chưa phải nhãn được xác nhận thủ công.

## Chia mục và triển khai mục 02

Lộ trình 8 mục ở docs/LO_TRINH_TRIEN_KHAI.md. Mục 01 hoàn thành; mục 02 đang triển khai.

Đã tạo bộ mẫu đọc riêng 300 tin nhà/căn hộ, không trùng row_id với 1.680 tin mẫu trước. Phiếu đọc không hiển thị nhãn tự động; 150 calibration và 150 evaluation. Dự đoán và manifest revision/seed/hash mã được lưu riêng ở artifacts/review/v1.

Đã viết và kiểm tra công cụ đánh giá: thiếu nhãn không xuất độ chính xác; nhãn sai bị từ chối; trường hợp dự đoán bán nhưng nhãn tham chiếu thuê tính precision 0 đúng. Kiểm tra dùng fixture riêng trong .runtime, không ghi nhãn giả vào bộ mẫu thực tế.

Trạng thái mẫu thực tế: 0/150 evaluation được gán nhãn, metrics=null. Tiếp theo đọc/gán nhãn có ghi nguồn người/model, hiệu chỉnh trên calibration, rồi đánh giá độc lập. Không coi mẫu đã chuẩn bị là mục 02 đã hoàn thành.

## Cập nhật phương án web

Đã khảo sát repo cloner/OpenDesign và viết đặc tả MUC_07_SAN_PHAM_WEB.md. Người dùng chọn local/LAN trước, Internet sau. Kiến trúc web đề xuất được ghi là Next.js/shadcn + FastAPI; giữ Spark/Parquet. Chưa clone template, cài OpenDesign, lập trình frontend/API hoặc triển khai hosting. Tại mốc trao đổi web, mục 02 chưa có nhãn; kết quả gán nhãn triển khai sau được cập nhật bên dưới.

## Thứ tự ưu tiên xác nhận lại

Người dùng xác nhận hoàn thiện cốt lõi mục 02–06 trước khi lập trình web/API mục 07. Web hiện chỉ đặc tả để trao đổi; chưa dựng khung giao diện hoặc cài công cụ thiết kế. Đã cập nhật V3, lộ trình, đặc tả web và DOC_TRUOC, đồng bộ sang docs. Điều kiện bắt đầu web: dữ liệu đã kiểm chứng, ETL tái chạy được, thống kê có phạm vi rõ, mô hình đã đánh giá và pipeline lưu/nạp/dự đoán bằng script được. Trạng thái triển khai dữ liệu/mô hình không thay đổi qua lần rà soát tài liệu này.

## Triển khai calibration mục 02

Đã đọc và gán nhãn AI đủ 150 calibration, ghi bằng chứng và giữ nguyên 300 dòng nguồn/split. Có 117 bán, 33 chưa xác định; không có nhãn thuê trong calibration nên mẫu này không chứng minh khả năng nhận diện mọi tin thuê. Evaluation vẫn 0/150 nhãn, metrics=null.

Đã hiệu chỉnh quy tắc; chẩn đoán calibration có bất đồng giao dịch giảm39 xuống12, diện tích giảm75 xuống61. Không coi đây là độ chính xác độc lập; phần diện tích còn khác vì nhãn AI có suy luận kích thước trong khi quy tắc giữ yêu cầu bằng chứng đất/công nhận rõ.

Đã cố định candidate-v2-frozen-for-evaluation, hash a2b7d760d9507f807edfbae6d414b575235ef399376581d018fda35b01a35b8e; lưu snapshot/freeze.json và dự đoán evaluation phiên bản mới riêng. Công cụ score hỗ trợ --predictions và kiểm tra provenance; thiếu nhãn vẫn không xuất metric; provenance sai bị từ chối trong fixture riêng.

Chi tiết KET_QUA_CALIBRATION_V1.md và QUY_UOC_GAN_NHAN.md. Tiếp theo đọc/gán nhãn evaluation theo quy ước cố định, đánh giá phiên bản mới. Mục 02 chưa hoàn thành; chưa chạy lại profile toàn bộ theo quy tắc mới, chưa ETL chính/huấn luyện giá nhà/web.
