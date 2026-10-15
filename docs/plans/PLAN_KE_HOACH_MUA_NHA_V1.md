# Kế hoạch mua nhà và điều hướng hợp nhất — bản triển khai 15/10/2026

Người dùng đã chốt triển khai và cập nhật GitHub. Giữ lõi Spark/ETL/ML của môn học, không thêm mô hình tài chính được huấn luyện hay giả dự báo thị trường.

## Phạm vi đã chọn

- Một mục **Khám phá khu vực**, Bản đồ/Danh sách chung loại nhà/tháng/ngân sách/diện tích. Mặc định toàn địa bàn, bỏ giới hạn không xóa lựa chọn so sánh. Giữ lớp màu, zoom/focus, offline, 2–3 vùng và liên kết ước tính.
- Menu chính năm mục: Tổng quan, Khám phá khu vực, Kế hoạch mua nhà, Ước tính giá rao bán, Độ chính xác dự đoán. Dữ liệu & phương pháp là liên kết phụ, truy cập cả desktop/mobile.
- Minh họa quy tắc tin Spark nằm trong details mặc định đóng. Pipeline, provenance và giới hạn vẫn giữ để thuyết trình Big Data.
- Kế hoạch mua nhà: tích lũy mua không vay, vốn ban đầu khi vay, mốc đồng thời có vốn và dòng tiền không âm; lịch trả nợ, tăng lãi kiểm tra, ba mức giá và biểu đồ.

## Cách tính và ranh giới kỹ thuật

Engine thuần TypeScript `web/lib/home-plan.ts`, chạy local trong trình duyệt; không gửi thu nhập/chi tiêu lên API, không lưu dữ liệu tài chính vào train. Draft và lần tính đã áp dụng giữ khi điều hướng trong phiên, refresh trang khởi tạo lại.

- Tách tiền dự phòng khỏi vốn mua trước khi mô phỏng. Tiền đầu tháng tăng theo lãi hiệu dụng tháng, sau đó cộng dòng tiền thu nhập trừ chi tiêu/nợ vào cuối tháng. Âm dòng tiền làm giảm số dư, sàn số dư 0.
- Tốc độ lãi tích lũy/tăng giá/thu nhập/chi phí là giả định tự nhập, chuyển hệ số năm thành tháng bằng lũy thừa. Không coi là dự báo hoặc mức thị trường hiện tại.
- Mục tiêu mua không vay = giá nhà theo tháng + chi phí mua tự nhập. Vốn ban đầu = giá nhà × tỷ lệ vốn tối thiểu + chi phí mua.
- Khoản vay là phần còn thiếu sau dùng toàn vốn khả dụng; do đó vốn vượt ngưỡng sẽ giảm vay. Chỉ ghi mốc mua có vay nếu đáp ứng cả vốn và dòng tiền còn lại tháng đầu không âm. Không có xác nhận ngân hàng phê duyệt và không mặc định đây là mức chi trả an toàn.
- Trả đều: A=Lr/[1−(1+r)^(-n)], r=lãi danh nghĩa năm/12; lãi 0 thì L/n. Trả gốc đều: gốc=L/n, lãi theo dư nợ đầu kỳ; cuối kỳ thanh toán phần dư do số thực.
- Dòng tiền sau mua giả định giữ chi tiêu/nợ hiện tại và cộng chi phí nhà phát sinh; không tự xóa tiền thuê cũ hoặc nợ cũ. Kiểm tra tại tháng đầu mua, không mô phỏng thu nhập toàn bộ thời hạn vay.
- Kịch bản tăng lãi tính lại toàn kỳ ở lãi cao hơn; không giả một lịch ưu đãi/thả nổi ngân hàng. Lịch nợ minh họa không gồm chi phí ngoài những giả định đã nhập.
- Ba giá thấp/tham chiếu/cao tự nhập hoặc lấy snapshot giá/dải từ căn đã ước tính; không lấy MAE hoặc R² tạo xác suất thời gian mua. Giá từ Spark là tham chiếu lịch sử, không là giá nhà hiện tại/tương lai.
- Không có khuyến nghị đầu tư, lướt sóng, dự báo lợi nhuận hay thuế/phí tự suy diễn. Chỉ so sánh các kịch bản do người dùng chịu trách nhiệm giả định.

## Đầu vào và kết quả

Giá ba mức, tiền hiện có/dự phòng, thu nhập/chi tiêu/nợ/chi phí nhà sau mua, vốn ban đầu, phí mua tự nhập, kỳ hạn, lãi vay, mức tăng kiểm tra, cách trả nợ, tốc độ tích lũy/tăng giá/thu nhập/chi phí, thời hạn xét.

Kết quả luôn gắn lần giả định đã áp dụng; sửa form hiện trạng thái chưa tính lại. Chặn số không hữu hạn, âm sai phạm vi, dự phòng vượt vốn, giá không đúng thứ tự, kỳ hạn không nguyên. Không đạt phải ghi “Chưa đạt trong thời hạn xét”, không gán một mốc vô hạn hoặc khẳng định không bao giờ mua được.

## Nghiệm thu

- Oracle tích lũy không lãi, giá cố định: vốn khả dụng 500 triệu, 20 triệu/tháng, giá 2,8/3,5/4,2 tỷ → 115/150/185 tháng.
- Kiểm tra lãi 0, annuity mẫu 1 tỷ/12%/12 tháng, gốc đều, bảo toàn tổng gốc, dư nợ cuối 0, tăng lãi làm tăng trả tháng đầu, dòng tiền âm, đủ tiền ngay, giá tăng vượt tích lũy, compound một năm, validation lỗi.
- UI: năm mục chính + phương pháp phụ; map/list thống kê khớp API; giữ selection/lớp màu; 0 tin; A/B dự đoán Spark thật; chuyển đúng giá/dải sang kế hoạch; nhập/sửa/tính lại; method collapsed và ba tin mẫu Spark; mobile không tràn.
- Kiểm thử API core hiện có và manifest 264 artifact không đổi. Không retrain hoặc thay rules/data để phục vụ thay UI.

Nguồn đối chiếu nguyên tắc: [CFPB — chi phí/dòng tiền nhà ở](https://www.consumerfinance.gov/owning-a-home/prepare/decide-how-much-you-want-spend/) và [Investor.gov — tích lũy](https://www.investor.gov/financial-tools-calculators/calculators/compound-interest-calculator), truy cập 15/10/2026. Không áp dụng quy định vay Mỹ cho Việt Nam.

Đọc biên bản nghiệm thu V5 để phân biệt những kiểm thử đã chạy và giới hạn mạng tile. Word/PPT chỉ cập nhật plan/lời dẫn, chưa tạo Office hoàn chỉnh.
