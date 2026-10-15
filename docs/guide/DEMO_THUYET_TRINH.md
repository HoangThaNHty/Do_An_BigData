# Kế hoạch mô phỏng và lời dẫn thuyết trình demo

**Bản đầy đủ mới 15/10/2026:** đọc [PLAN_THUYET_TRINH_CUOI_KY.md](../plans/PLAN_THUYET_TRINH_CUOI_KY.md) để có lời nói mẫu từ bài toán/dữ liệu/Spark/ML đến sáu màn hình, phân vai, bảng công nghệ, phản biện và phiếu nhớ. Nội dung dưới đây là bản rút gọn 8–10 phút tập trung sản phẩm; không thay thế kịch bản đầy đủ.

Thời lượng gợi ý **8–10 phút**. Đây là kịch bản rehearsal, không phải lời khẳng định nhóm đã kiểm thử trên mọi máy. Người trình bày tự phân công; Word/PPT chưa cập nhật đợt này.

## Chuẩn bị trước buổi trình bày

- Setup và chạy trước 5–10 phút; health ready, model nạp xong. Sạc máy, tắt tác vụ RAM nặng; không train lại khi API đang chạy.
- Mở ba tab: web 3000, API health, API docs. VS Code mở manifest core, kết quả models và terminal. Dùng polygon offline làm nền demo chính; OSM chỉ thêm khi mạng tốt.
- Reset web trước rehearsal. Căn hộ 3–4 tỷ/60–80 m²; form 70 m² / Thủ Đức / 2 PN / 2 WC; giá cân nhắc 4,2 tỷ. Tin mẫu bán/thuê/trả trước đã có nút chọn.
- Chạy checklist T01, T04, T06, T12 hoặc T13, T15–T18, T21, T25–T27 trước. Có ảnh QA dự phòng nhưng phải nói rõ là ảnh lượt kiểm thử đã lưu, không giả live.

## Luồng trình bày và lời dẫn

| Phút | Màn hình / thao tác | Lời dẫn gợi ý / điều muốn chứng minh |
|---|---|---|
|0–1| Tổng quan, kỳ dữ liệu |“Đồ án phân tích tin rao và ước tính giá rao bán. Dữ liệu 06/2025–03/2026, địa bàn TP.HCM trước hợp nhất; chưa phải giá giao dịch hoặc giá hiện tại.”|
|1–2,5| Tìm khu vực 3–4 tỷ, 60–80 m²; chọn Tân Phú, Quận 7, Thủ Đức→so sánh |“Người dùng bắt đầu từ ngân sách và diện tích. Chúng em trả các khu vực có dữ liệu phù hợp và đối chiếu theo cùng điều kiện, không chỉ show dashboard.”|
|2,5–3,5| Bản đồ: giá/m²→số tin; bấm vùng |“Bản đồ giúp đọc khác biệt không gian. Lớp màu theo phân vị, viền vàng là vùng so sánh; polygon lịch sử, không có GPS từng căn.”|
|3,5–5,5| Ước tính 70 m²; nhập 4,2 tỷ; lưu; sửa 90 m²; chạy; so sánh |“Model đã học trước. Người mua đối chiếu giá rao, người bán tham khảo giá đăng. Giá nhập chỉ đối chiếu, không đưa vào model. Căn đã lưu giữ nguyên, ước tính căn tiếp theo có kết quả riêng.”|
|5,5–6,5| Độ chính xác: bấm/chọn một tin; giải thích MAE |“Mô hình có sai số. Mẫu test này cho thấy giá nguồn, giá dự đoán và chênh lệch. Chọn model bằng validation trước test; không sửa test để tăng thành tích.”|
|6,5–8| Pipeline; phân tích mẫu bán/thuê/trả trước |“Spark không chỉ dùng để đặt tên công nghệ. Bộ quy tắc thật tách giao dịch, kiểm tra giá tổng, diện tích và phạm vi; tránh trộn giá thuê tháng/trả trước vào giá bán.”|
|8–9| VS Code manifest/results, health/docs |“Nguồn Parquet → Spark SQL/ETL → cohort/split thời gian → Spark ML → artifact → FastAPI → Next.js. Thực nghiệm trên một máy local[4], không có MongoDB/HDFS/cluster.”|
|9–10| Giới hạn và câu hỏi |“Mẫu có chọn lọc, nhãn review AI, giá chưa xác minh, còn tin đăng lại khác nội dung. Dải tham khảo không bảo đảm từng căn. Đợt sau có thể bổ sung dữ liệu/địa giới và triển khai Internet.”|

## Mô phỏng hai tình huống sử dụng

**Người mua:** có 3–4 tỷ, cần căn hộ 60–80 m² → tìm vùng → so hai vùng → tham khảo căn 70 m² đang rao 4,2 tỷ → đọc model, dải và cảnh báo. Không kết luận “nên mua” từ kết quả.

**Người bán:** có căn 70 m² tại Thủ Đức → nhập thuộc tính → tham khảo giá đăng → lưu → đổi sang phương án 90 m²/dự án khác → chạy lại và so sánh. Chênh lệch không chứng minh tác động nhân quả của một đặc trưng.

## Khi có sự cố

- Nền Internet lỗi: chuyển offline, tiếp tục 22 polygon; giải thích nền là phụ trợ, không ảnh hưởng Spark/model.
- API chưa sẵn sàng: kiểm tra health/terminal, chờ load. Không mở phiên Spark thứ hai. Nếu lỗi chặn demo, dùng ảnh/kết quả đã lưu và nói rõ chưa live được phần này.
- Ít/không tin: cho thấy thông báo 0/— và mở rộng điều kiện, không gán giá 0 hoặc bịa tin.
- Model trả giá lạ: kiểm tra input/đơn vị/dự án và cảnh báo; công bố giới hạn, không chỉnh artifact ngay lúc demo.

## Câu hỏi thường gặp và cách trả lời

| Câu hỏi | Trả lời trung thực |
|---|---|
| Có huấn luyện không? |Có,9 pipeline + baseline; model được lưu. Web suy luận bằng model, không train từng request.|
| Big Data nằm ở đâu? |Nguồn triệu dòng, Parquet/Spark SQL/ETL, chia thời gian và Spark ML. local[4] một máy; chưa benchmark cluster.|
| MongoDB đâu? |Dự án dùng Parquet filesystem; không dùng MongoDB và không mở màn hình CSDL chỉ để minh họa.|
| Đã sáp nhập thì phạm vi sao? |Tin có cả trước/sau nhưng phân nhóm theo địa bàn lịch sử; chưa bao phủ tỉnh mới/địa giới hiện hành hoặc GPS tài sản.|
| Giá chính xác từng nhà không? |Không. Có MAE/RMSE/test; giá rao chưa xác minh, thiếu pháp lý/chất lượng/vị trí chi tiết.|
| Nhập tin mẫu có thêm vào train? |Không. Chạy rule thật cho minh họa, không lưu nội dung vào tập nghiên cứu.|
| Clone có phải train lại? |Không cho demo:model và serving gọn có trong Git; tái hiện nghiên cứu từ raw là quy trình riêng.|

Sau mỗi rehearsal: ghi Test ID/lỗi và thời gian từng bước, điều chỉnh lời dẫn để không vượt 10 phút.
