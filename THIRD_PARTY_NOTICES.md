# Nguồn dữ liệu và thành phần sử dụng

## Dữ liệu tin đăng

Nguồn: **oceanNG/vietnam-real-estates**, Hugging Face, revision `6f68fe87be7577afb03e38c535bd882d242ba26d`.

Dataset card công bố giấy phép **CC BY-NC 4.0**. Giữ ghi công, thông tin giấy phép và điều kiện phi thương mại khi chia sẻ dữ liệu hoặc bảng dữ liệu đã biến đổi. Bản này phục vụ đồ án học tập. Dataset card gốc được giữ tại `data/raw/oceanng/DATASET_CARD.md`, cùng manifest revision/checksum. Mã nguồn dự án không thay đổi giấy phép của dữ liệu.

- Nguồn: https://huggingface.co/datasets/oceanNG/vietnam-real-estates
- Giấy phép: https://creativecommons.org/licenses/by-nc/4.0/
- Biến đổi đã thực hiện: chọn nhà/căn hộ TP.HCM, kiểm tra ngữ cảnh bán và hỗ trợ giá/diện tích/phạm vi, chuẩn hóa địa danh, loại mẫu từng kiểm tra, xử lý proxy đăng lại, chia tập thời gian, xuất bảng phục vụ và tổng hợp.
- Giá là giá rao từ nguồn, chưa xác minh giao dịch thực hoặc pháp lý.

## Địa danh và ranh giới

Vietnamese Provinces Database của **Thang Le Quoc**, v2.4.1, commit `fc33b7411ec4e3697817fab8118718a8d39ef090`, giấy phép MIT. Giữ bản LICENSE ở `data/raw/geography/admin_LICENSE.txt`.

Ranh giới **geoBoundaries VNM-ADM2-81297802**, dữ liệu thể hiện năm 2020, **OCHA ROAP / Government of Viet Nam**, **CC BY 3.0 IGO**. Biến đổi: chọn vùng HCM và hợp nhất Quận 2/Quận 9/Thủ Đức thành 22 nhóm địa bàn lịch sử. Không có GPS tài sản và không mô tả địa giới hiện hành 2026.

- https://github.com/ThangLeQuoc/vietnamese-provinces-database
- https://www.geoboundaries.org/
- https://creativecommons.org/licenses/by/3.0/igo/

## Thành phần giao diện và thư viện

Thông tin và bản MIT cho thành phần theo shadcn/ui ở `web/THIRD_PARTY_NOTICES.md`. Các thư viện Node/Python giữ giấy phép từ distribution khi cài qua npm/pip. Không nhúng node_modules, môi trường Python hoặc JDK vào gói mã nguồn; JDK portable tải từ nguồn xác minh bằng script bootstrap. Crawler cũ không dùng trong tập thực nghiệm này.

## Bản đồ nền online tùy chọn

Nền: © OpenStreetMap contributors, [ODbL / ghi công](https://www.openstreetmap.org/copyright). Dịch vụ tile tuân theo [Tile Usage Policy](https://operations.osmfoundation.org/policies/tiles/): tải theo viewport, User-Agent/Referer, cache và conditional validation; không prefetch/download toàn vùng. Cache .runtime/tile-cache chỉ phục vụ phiên demo, không đưa vào ZIP. Polygon nghiên cứu có nguồn/giấy phép riêng như phần trên.

## Bản mẫu UI/UX V4

Hai bản mẫu tạo qua MCP bằng Local Codex được lưu ở artifacts/design/v4. Người dùng chọn B; token/bố cục được thích ứng vào Next.js thật. Prototype giữ nhãn chưa nối API và fixture riêng; app chính dùng API/model thật. Bản mẫu không thay giấy phép dữ liệu/GeoJSON/thư viện.
