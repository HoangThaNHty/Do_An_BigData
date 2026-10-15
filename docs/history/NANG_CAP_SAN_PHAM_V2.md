# Nâng cấp sản phẩm v2 — 13/10/2026

Người dùng đã duyệt triển khai sau trao đổi về địa giới và nâng cấp các trang. API version 1.1.0; dữ liệu/model vẫn core_v1/models/v1. Không thay quy tắc ETL, split, pipeline đã huấn luyện hoặc lựa chọn theo validation.

## Chức năng đã triển khai

| Trang | Hành động và dữ liệu thật |
|---|---|
| Toàn sản phẩm | Ghi rõ phạm vi TP.HCM trước hợp nhất, kỳ tin 06/2025–03/2026 có cả trước/sau sáp nhập, chưa phải giá hiện tại |
| Khám phá thị trường | Nhập khoảng ngân sách/diện tích; tìm các khu vực có tin lịch sử phù hợp; số tin, trung vị và tứ phân vị; so sánh tối đa 3 khu vực; chuyển sang bản đồ/ước tính |
| Bản đồ giá | Chọn giá/m², tổng giá hoặc số tin; nhận điều kiện tìm kiếm; bấm vùng xem chi tiết; so sánh 2 khu vực; chuyển sang ước tính; tùy chọn nền OpenStreetMap online, mặc định offline |
| Ước tính | Đối chiếu giá rao người dùng nhập với model và dải tham khảo; giữ snapshot A, sửa thông tin chạy B; nhóm tham khảo cùng loại/khu vực, diện tích ±15% |
| Đánh giá mô hình | Biểu đồ 300 dự đoán test thật, chọn điểm để xem sai lệch; thang log/tuyến tính; lọc mẫu theo khu vực/giá; bảng toàn test theo khu vực/giá; 10 lỗi tuyệt đối lớn nhất; giải thích MAE/RMSE/baseline; bảng kỹ thuật mở rộng |
| Dữ liệu & phương pháp | Bấm 6 bước nguồn → ETL → cohort → split → ML → API/web; số liệu đọc manifest; nhập tin mẫu chạy bộ quy tắc Spark thực, xem bán/thuê/chưa rõ và dấu vết chất lượng |

Tìm kiếm hiển thị 6 khu vực trước, có nút xem thêm; so sánh dùng đúng điều kiện đã áp dụng, không tự nới lọc. Số tin không phải số tài sản duy nhất và không xác nhận còn bán. Đối chiếu giá không kết luận tài sản rẻ/đắt; A/B không chứng minh tác động nhân quả.

## Địa giới: đã làm và chưa làm

Đã có tra cứu không dấu/tên lịch sử trong danh mục quận/phường, xử lý Quận 2/Quận 9 về nhóm Thủ Đức. Kết quả chỉ là địa danh lịch sử; tên có thể trùng phường mới. Không tự chuyển phường hiện hành thành phường lịch sử.

**Chưa có crosswalk đầy đủ địa chỉ mới/cũ**, chưa mở rộng cohort sang Bình Dương/Bà Rịa–Vũng Tàu cũ, chưa có GPS tài sản hoặc cập nhật giá tới tháng 10/2026. Các chức năng này cần nguồn địa giới/dữ liệu mới được kiểm chứng; không suy ra hệ số tăng giá từ sáp nhập. Nền OSM hiển thị đường phố online hiện tại; polygon phân tích vẫn theo địa bàn lịch sử, không phải địa giới hiện hành.

## Kỹ thuật và API mới

- `src/api/explore.py`: GET market/search, market/reference, map/explore, geography/lookup, models/error-examples, method/pipeline; POST method/check-listing. Tất cả dưới `/api/v1`.
- Search/reference/map tổng hợp bằng NumPy trên bảng serving 133.779 tin đã xuất từ Spark; không khẳng định mỗi lần bấm dashboard lại chạy Spark ETL.
- Demo check-listing dùng chính enrich/check của rules.py/quality.py với SparkSession resident và cùng lock suy luận. Giới hạn title 300, body 10.000 ký tự; không lưu input. Ngày 01/10/2025/địa bàn Thủ Đức là trường cố định minh họa, được ghi rõ trên UI/API.
- Error examples đọc selected-model test_predictions Parquet, không trả ID/mô tả/liên hệ nguồn. Scatter là mẫu cố định 300; bộ lọc scatter không thay các chỉ số tổng. Bảng giá/khu vực là hai phân nhóm độc lập, không giao bộ lọc.
- Kết nối backend local/LAN gửi `Connection: close` để tránh proxy Next/httpxy dùng lại socket idle đã hết hạn ở Uvicorn. Lỗi ECONNRESET ở reference khi chạy A/B được tái hiện, sửa và kiểm tra lại.
- Form khóa thay đầu vào khi đang tính; khi đổi thông tin xóa kết quả cũ, giữ snapshot A. Giá rao đối chiếu không đưa vào feature mô hình. Snapshot A chỉ giữ trong trang hiện tại, không lưu bền qua điều hướng/refresh.
- Không thêm dependency runtime hoặc đổi license. Tile OSM online có attribution, không tải trước/offline/cache bulk. Chế độ không bật tile vẫn chạy map địa bàn và tương tác.

## Kiểm chứng và hồ sơ

Các checks: `scripts/check_api.py` (35 calls cũ); `scripts/check_product_features.py` (41 calls mới, đối chiếu Parquet/manifest/top lỗi/input và hash frozen); `scripts/check_web.cjs` (6 trang desktop/mobile cũ); `scripts/check_product_web.cjs` (hành trình mới/A-B/ETL/mobile). Cần xem timestamp/base trong receipts để biết lần chạy mới nhất.

Browser plugin đã thử bootstrap nhưng import node:process bị môi trường chặn; QA dùng Playwright/Edge local đã cài. Không coi đây là kiểm tra trực tiếp terminal VS Code hoặc thiết bị LAN khác. Nền tile online cần Internet và còn phụ thuộc nhà cung cấp; đường chạy offline là kiểm tra chính.

Đọc `KICH_BAN_DEMO_SAN_PHAM_V2.md` để diễn tập. Word/PowerPoint vẫn là snapshot trước nâng cấp web; người dùng yêu cầu để xử lý sau. Không sửa hồ sơ Office trong đợt này.
