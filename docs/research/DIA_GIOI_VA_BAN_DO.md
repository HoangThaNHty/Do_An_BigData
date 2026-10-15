# Địa giới và bản đồ của tập nghiên cứu

Phạm vi sản phẩm là khu vực TP.HCM trước hợp nhất2025, gồm22nhóm quận/huyện sau gộp Quận2, Quận9 và ThủĐức vào ThànhphốThủĐức (mã769). Không tự nhận các địa bàn BìnhDương/BàRịa–VũngTàu vào mô hình dù tên tỉnhnguồn đã thànhHồChíMinh. Không gọi các nhóm quận cũ là đơn vị hành chính hiện hành2026.

Tham chiếu tên/mã lấy từ vietnamese-provinces-database v2.4.1, commitfc33b7411ec4e3697817fab8118718a8d39ef090, licenseMIT. Tải JSON và license trongdata/raw/geography, manifest có URL/hash. Ghép tên chuẩn hóa (UnicodeNFC, bỏ tiền tố, số0đầu), giữ tên nguồn. Phường ghép bằngquận+phường, không ghép tên phường đơn lẻ. Không ghép được hoặc thuộc phiên bản khác giữ trạng thái riêng, không dựng crosswalk thiếu bằng chứng.

Polygon lấy từ geoBoundaries gbOpen VNM ADM2, boundaryIDVNM-ADM2-81297802, năm2020; nguồnOCHA ROAP/Government of Vietnam, licenseCCBY3.0IGO. Dữ liệu pinned revision9469f09 vàSHA256. Xử lý GitLFS bằng xác minhOID trước dùng. Mã hóa tên riêng tách từtênđa ngôn ngữ; kiểm tra phạm vi địa lý để tránh đơn vị trùng tên; gộp3polygoncũ vàoThủĐức. Output22polygonhợp lệ ởartifacts/geography/hcm_districts.geojson. Mỗi feature giữ boundaryyear/sourceIDs vàmã địa bàn tương ứng.

Bản đồ là nền lịch sử2020 tổng hợp theo22nhóm địa bàn nghiên cứu, không mô tả ranh giới chính xác2026 hoặc địa giới từng căn. Không cóGPS tài sản; không tạo marker căn hộ tại tâmquận. Các thay đổi địa giới giữa2020và2025 không được ngầm coi là đã xác minh. Mãphường2025 vàtên tin có thể không cùngvintage; báo cáo tỷ lệghép thực tế từmanifestcore.

Attribution cần hiển thị: geoBoundaries / OCHA ROAP / Government of Vietnam, CC BY3.0IGO; Vietnamese Provinces Database, MIT. Nền map dùngGeoJSON tự có nên không phụ thuộc dịchvụtile bênngoài khi demoLAN. Sốtin/mứcgiá bản đồ là tập nguồn đượcchọn, không toàn thị trường hay giao dịchđãchốt.

Nguồn:

- https://www.geoboundaries.org/api/current/gbOpen/VNM/ADM2/
- https://github.com/ThangLeQuoc/vietnamese-provinces-database/tree/v2.4.1
- https://github.com/wmgeolab/geoBoundaries
