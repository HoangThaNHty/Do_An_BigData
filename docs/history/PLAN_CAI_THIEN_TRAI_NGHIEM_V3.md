> **Bổ sung sau audit 14/10/2026:** Người dùng đã yêu cầu trải nghiệm/kiểm thử bản hiện tại và bổ sung plan. Audit UI/UX đã hoàn thành; chỉ thêm script QA, bằng chứng và tài liệu, chưa triển khai sửa giao diện. Đọc [KIEM_THU_UI_UX_2026_10_14.md](KIEM_THU_UI_UX_2026_10_14.md) và [BRIEF_THIET_KE_UI_UX_V3.md](../plans/BRIEF_THIET_KE_UI_UX_V3.md). Các ghi chú “chưa chạy tester/khởi động dịch vụ” bên dưới mô tả trạng thái lúc lưu đề xuất trước yêu cầu audit mới.

# Plan cải thiện trải nghiệm sản phẩm — V3

Ngày lưu: 14/10/2026.

**Trạng thái: đề xuất đã trao đổi, chưa triển khai.** Người dùng yêu cầu lưu các hướng này vào plan rồi tiếp tục trao đổi. Chỉ cập nhật tài liệu trong lượt này; không sửa code, chạy tester, đổi dữ liệu/model, khởi động dịch vụ hoặc đóng lại ZIP. Việc lưu plan không đồng nghĩa duyệt mọi chi tiết để bắt đầu triển khai.

## 1. Căn cứ và điều cần làm rõ

Sản phẩm v2 đã có chức năng và kết quả QA theo kịch bản ở mốc 13/10. Phản hồi thực tế của người dùng ngày 14/10 cho thấy mục đích thao tác, phản hồi sau bấm nút và vị trí kết quả chưa dễ hiểu. Không dùng các checks v2 để khẳng định trải nghiệm đã đạt hoặc mọi tình huống so sánh đều hoạt động.

- Ảnh 1: ô chọn so sánh khu vực chưa được chọn; ảnh chưa chứng minh lỗi logic. Bảng kết quả phía dưới danh sách là vấn đề khả năng nhận biết cần xử lý.
- Ảnh 2: lớp nền online báo tải ô bản đồ thất bại; polygon vẫn hiển thị. Chưa xác định nguyên nhân mạng, nguồn tile hay trình duyệt tích hợp VS Code. QA trước chủ yếu offline, chưa chứng minh nền online hoạt động.
- Ảnh 3: nút giữ phương án A không làm rõ mục đích và kết quả ngay tại vị trí thao tác. Cần phân biệt lỗi xử lý với trạng thái/kết quả bị khuất màn hình, và kiểm tra mất trạng thái khi điều hướng.
- Ảnh 4: tên thao tác kiểm tra Spark giải thích công nghệ thay vì giải thích vì sao người xem cần dùng chức năng.

## 2. Địa danh: đề xuất bỏ khỏi luồng chính

- Bỏ khung tra cứu địa danh khỏi Tổng quan, Khám phá, Bản đồ và Ước tính.
- Giữ thông báo ngắn về phạm vi TP.HCM trước hợp nhất và thời gian tin 06/2025–03/2026.
- Chuyển giải thích địa giới lịch sử vào Dữ liệu & phương pháp.
- Chỉ cân nhắc đưa tra cứu trở lại khi có bảng đối chiếu địa chỉ mới/cũ đáng tin cậy. Không gọi danh mục lịch sử hiện tại là chuyển đổi địa chỉ sau sáp nhập.
- Chưa chốt xóa API tra cứu hoặc chỉ ẩn giao diện; quyết định này có thể trao đổi tiếp.

## 3. So sánh khu vực: phản hồi và kết quả ngay trước mắt

Mục đích: với cùng ngân sách/diện tích/loại hình/tháng, đối chiếu số tin phù hợp, giá trung vị, khoảng 50% giá và diện tích giữa các khu vực. Không kết luận khu vực tốt hơn hoặc đáng mua hơn từ số tin.

Luồng đề xuất:

1. Thẻ khu vực có hành động “Chọn để so sánh”.
2. Thanh lựa chọn dễ thấy hiển thị “Đã chọn 1/3 khu vực” và tên các khu vực, có nút bỏ từng mục.
3. Có ít nhất hai khu vực mới bật “Xem so sánh”; khi mới chọn một, giải thích cần chọn thêm khu vực.
4. Mở bảng tại chỗ hoặc khung riêng, không yêu cầu người dùng tự tìm phía cuối danh sách.
5. Thêm nhận xét bằng lời dựa trên số liệu thật và cùng điều kiện lọc. Giới hạn tối đa 3 khu vực, giải thích khi đã đủ.

Thống nhất cơ chế chọn với Bản đồ. V2 đang có giới hạn 3 khu vực ở Khám phá và 2 vùng ở Bản đồ; cần chốt có giữ giới hạn khác nhau hay dùng chung 2/3. Không tự coi lựa chọn này đã chốt.

## 4. Bản đồ: kiểm tra online và làm rõ so sánh

- Kiểm tra tải tile trong trình duyệt thường và trình duyệt tích hợp VS Code; đọc lỗi thực tế trước khi kết luận nguyên nhân.
- Thể hiện ba trạng thái: đang tải, đã bật nền đường phố, không tải được và trở về lớp địa bàn offline.
- Có thử lại; không giữ trạng thái “đã bật online” gây hiểu rằng nền đã tải thành công.
- Kiểm tra cả mất Internet và lỗi tải một phần. Không hứa có đường phố offline nếu chưa có dữ liệu nền được cấp phép phù hợp.
- Bên phải bản đồ hiển thị ngay các vùng đã chọn và kết quả đối chiếu. Có chọn, bỏ, thay vùng; không chỉ tô viền rồi đưa kết quả xuống dưới bản đồ.
- Dùng cùng cơ sở thống kê với tìm kiếm khi mang ngân sách/diện tích sang bản đồ. Đổi điều kiện không được để kết quả so sánh cũ mang nhãn mới.

## 5. Ước tính: mục đích mua/bán và so sánh căn rõ ràng

Tên đề xuất: **“Ước tính giá rao bán”**. Lời mở đầu: nhập thông tin để tham khảo giá đăng bán hoặc đối chiếu giá của căn đang xem; kết quả dựa trên dữ liệu 06/2025–03/2026, chưa phải giá hiện tại.

- Người mua: đối chiếu “Giá người bán đang rao”.
- Người bán: tham khảo và đối chiếu “Giá bạn dự định đăng”.
- Có thể thêm lựa chọn “Tôi đang tìm mua”/“Tôi đang muốn bán” để đổi hướng dẫn. Đây là tùy chọn UX còn cần chốt, không đòi hỏi hai mô hình mới; cả hai dùng cùng mô hình giá rao hiện tại.
- Không gọi kết quả là giá chốt giao dịch, chứng thư thẩm định hoặc kết luận tài sản rẻ/đắt.

Đổi “Giữ làm phương án A” thành **“Lưu căn này để so sánh”**:

1. Sau bấm, hiện ngay thẻ “Căn đã lưu”, thông tin đầu vào và giá đã tính.
2. Hướng dẫn thay thông tin căn tiếp theo rồi chạy ước tính để so sánh.
3. Đặt hai kết quả gần nhau; xóa/thay căn đã lưu có hành động rõ và phản hồi.
4. Giữ trạng thái khi chuyển trang trong ứng dụng. Chưa chốt lưu qua refresh/đóng trình duyệt; không tự mở rộng sang lưu tài khoản hoặc database.
5. Sửa đầu vào phải làm mất kết quả hiện tại đã lỗi thời, nhưng không thay snapshot căn đã lưu. Không dùng chênh lệch A/B để khẳng định tác động nhân quả của một yếu tố.

## 6. Đánh giá mô hình: giải thích trước, kỹ thuật sau

Tên hiển thị đề xuất: **“Độ chính xác dự đoán”**.

Ba câu hỏi dẫn nội dung:

- Mô hình sai lệch bao nhiêu? Giải thích bằng tiền/phần trăm và nêu rõ tập test, trung bình/trung vị.
- Trường hợp nào dễ sai? Nhóm giá, khu vực ít mẫu, tin nguồn cực cao chưa xác minh.
- Vì sao chọn mô hình này? So baseline và các phương án bằng validation trước test.

Khi chọn điểm biểu đồ, hiển thị: tin nguồn rao X, dự đoán Y, chênh Z. MAE/RMSE/R² giữ ở phần kỹ thuật có giải thích. Không biến sai số trung bình/trung vị thành lời hứa độ chính xác cho từng căn; không gọi giá nguồn là giá giao dịch thực tế.

## 7. Dữ liệu & phương pháp: minh họa quyết định giữ/loại tin

Tên phần đề xuất: **“Vì sao tin này được dùng hoặc loại khỏi dữ liệu?”**. Nút **“Phân tích tin mẫu”** thay tên thiên về công nghệ “Chạy bộ kiểm tra Spark”.

- Giải thích đây là demo kiểm tra chất lượng trước huấn luyện, chưa phải công cụ xác minh nhà/người bán cho người mua.
- Kết quả trình bày từng bước: bán/thuê/chưa rõ → giá tổng/trả trước → diện tích → đạt/chưa đạt điều kiện ứng viên.
- Tin thuê trả lời thẳng: không dùng để huấn luyện giá bán vì nội dung đang rao cho thuê.
- Giải thích giá/diện tích ở form là trường dữ liệu nguồn mô phỏng; mâu thuẫn với nội dung là điều bộ kiểm tra cần phát hiện.
- Công nghệ Spark và mã lý do nằm ở phần mở rộng cho demo môn học; vẫn dùng quy tắc ETL thật khi triển khai, không dựng kết quả cố định.
- Giữ cảnh báo ví dụ tổng hợp, trường địa bàn/ngày cố định phục vụ minh họa, input không tự thêm vào train. Đạt điều kiện ứng viên không chứng minh tin thật hoặc tài sản hợp pháp.

## 8. Đợt kiểm tra sau khi được yêu cầu triển khai

Không chỉ kiểm tra nút có chạy. Cần xác nhận người dùng thấy và hiểu phản hồi/kết quả:

| Nhóm | Tình huống cần kiểm tra |
|---|---|
| So sánh khu vực | Chưa chọn, chọn 1/2/đủ giới hạn, bỏ/thay, xem bảng, đổi điều kiện, chuyển Khám phá–Bản đồ, dữ liệu rỗng/ít mẫu |
| Bản đồ | Online tải thành công, đang tải, lỗi một phần, mất Internet, thử lại/fallback; desktop/mobile và trình duyệt thường/VS Code |
| So sánh căn | Chưa có dự đoán, lưu, sửa đầu vào, chạy căn thứ hai, xóa/thay, chuyển trang/quay lại, input lỗi/API bận, kết quả có dễ thấy không |
| Nội dung | Tên trang/nút/trường, vai trò mua/bán, lời giải thích giá và sai số, thông báo kết quả kỹ thuật bằng ngôn ngữ dễ hiểu |
| Pipeline | Các ví dụ bán/thuê/trả trước/mâu thuẫn, lời giải thích quyết định, quy tắc thật, không ghi input vào train |
| Hồi quy | Đối chiếu thống kê Parquet, dự đoán thật, scope/thời gian, bộ lọc/CSV, accessibility và không tràn ngang mobile |

## 9. Giới hạn phạm vi và những gì còn trao đổi

- Chưa thực hiện bất cứ sửa UX/code/test mới nào theo plan này.
- Chưa chốt dạng bảng so sánh tại chỗ hay drawer/modal, giới hạn dùng chung 2/3 khu vực, tùy chọn vai trò mua/bán, và thời gian lưu căn so sánh qua refresh.
- Giữ dataset/core/model, split và phương pháp đánh giá hiện hành; không tự thu thập dữ liệu mới, thêm MongoDB hoặc chỉnh model theo test trong đợt UX.
- Word/PPT tiếp tục để sau theo yêu cầu người dùng.
- ZIP sản phẩm v2 chưa chứa plan này; file Markdown tại thư mục mã nguồn và folder tài liệu là bản trao đổi hiện hành.

## 10. Bổ sung từ kiểm thử thực tế và định hướng thiết kế

Kiểm thử desktop/mobile đã xác nhận chọn/bỏ/giới hạn so sánh hoạt động, nhưng kết quả dễ nằm ngoài viewport và state mất khi điều hướng. Lưu căn A còn hiển thị B giống A ngay lập tức; việc sửa và tính căn thứ hai hoạt động nhưng snapshot mất khi chuyển trang. Đây là các vấn đề trạng thái và trình bày cần ưu tiên, không gọi toàn bộ chức năng là nút chết.

Nền online trong Edge audit lỗi ERR_NAME_NOT_RESOLVED, 12 request tự nhiên thất bại/0 tile tải được. Mô phỏng mất Internet cũng giữ checkbox online được chọn, không có retry nền. Chưa kiểm chứng webview VS Code hoặc mạng khác; chưa sửa DNS/nguồn tile. Khi triển khai cần tách lỗi mạng với trạng thái UI và kiểm tra đường thành công lẫn thất bại.

Các mẫu text 9–12 px có contrast khoảng 2,48–3,27:1 cần cải thiện; thiết kế nhắm chữ thường ít nhất 4,5:1 theo WCAG, CTA/mobile khoảng 44–48 px theo mục tiêu nội bộ. Sáu trang mobile không tràn ngang nhưng trang mô hình còn dài; bổ sung kiểm thử keyboard/focus/status/zoom chứ không coi audit này là chứng nhận accessibility.

Hướng bố cục đề xuất: desktop kết quả/bản đồ/panel so sánh cùng viewport; mobile tab kết quả/bản đồ và thanh mở so sánh. Giữ trạng thái chung của điều kiện/chọn khu vực và căn đã lưu khi điều hướng. Hiện rõ form chưa Apply, kết quả đang tính theo điều kiện nào, căn thứ hai chưa có dự đoán, và kết quả mẫu/tập test toàn bộ.

Chuẩn và trạng thái chi tiết, dữ liệu nền, nội dung mua/bán, cùng brief cho bản mẫu MCP đã lưu ở BRIEF_THIET_KE_UI_UX_V3.md. Chưa tạo hai bản mẫu, chưa chọn palette/bố cục cuối, chưa sửa app hoặc đóng lại ZIP. Tiếp tục trao đổi trước giai đoạn thiết kế/triển khai.
