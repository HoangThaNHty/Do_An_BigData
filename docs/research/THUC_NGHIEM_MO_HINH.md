# Thiết kế thực nghiệm mô hình giá rao bán

Thiết kế này được viết trước khi chạy và xem kết quả mô hình trên tập thực. Kết quả cuối phải lấy từ artifacts/models/v1/results.json sau khi chạy thành công; đã hoàn thành. Xem KET_QUA_MO_HINH.md và results.json; thiết kế dưới đây được giữ nguyên để đối chiếu quyết định trước kết quả.

## Dữ liệu và chia tập

Tập nghiên cứu: ứng viên được quality v4 giữ; review v5 đạt98/100 với tham chiếu AI. Chỉ22nhóm quận/huyện TP.HCM trước hợp nhất có mã tham chiếu được giữ. Các row_id mọi mẫu review được loại khỏi thực nghiệm giá; snapshot mã và nguồn loại lưu trong manifest. Điều kiện này tạo tập có chọn lọc, không đại diện tất cả thị trường.

Tin đăng lại được nhóm theo toàn văn tiêu đề/mô tả chuẩn hóa, bỏ giá/điện thoại, kèm địa bàn, loại hình và diện tích. Giữ bản sớm nhất. Đây là proxy trùng toàn văn, không chứng minh tài sản duy nhất; môi giới đổi nội dung có thể còn trùng giữa tập. Chia train06–11/2025, validation12/2025, test01–03/2026. Không random split.

## Đầu vào

Diện tích (log), số phòng ngủ/toilet/tầng, ngang/sâu/đường; district_code, ward_code, project_name. Mô hình chung thêm loại hình. Không dùng giá/m2, giá gốc, tiêu đề/mô tả chứa giá, thời điểm đăng hoặc nhãn target dẫn xuất làm đặc trưng.

Biến số tùy chọn không hữu hạn, âm/0, vượt giới hạn kiểm tra cú pháp (50phòng,100tầng,1000m chiều dài) chuyển thiếu riêng features và có chỉ báo thiếu; giữ nguyên trường nguồn ở core. Không điền giá target. Median imputation chỉfit train. Cột thiếu hoàn toàn trong train không làm biến giá trị; giữ chỉ báo thiếu. StringIndexer/OneHotEncoder/StandardScaler fittrain, có nhóm chưa thấy khi suy luận. Không suy địa chỉ từ GPS giả hoặc gán mã phường không ghép được.

## Các phương án cố định

- Baseline: trung vị tổng giá train theo loại hình+quận, tối thiểu20tin; nhóm ít tin dùng trung vị theo loại hình.
- LinearRegression: loggiá, regParam0,05, maxIter80.
- RandomForest:30cây, sâu7, minInstances10, seed20261012.
- GBT:30vòng, sâu5, stepSize0,1, minInstances10, seed20261012.

Mỗi thuật toán thử mô hình nhà riêng, căn hộ riêng và chung:9pipeline, thêmbaseline. Đây là thực nghiệm giới hạn tài nguyên, không exhaustive hyperparameter tuning. Spark chạy local4cores/driver4GB, không gọi là cluster nhiều máy.

Chọn cho từng loại hình bằng MAE(VND) trênvalidation, gồm cảbaseline vàmô hình chung. Lưu selection.json trước khi đánh giá test. Test chỉ dùng sau chọn, không dùng thay cấu hình. So sánh MAE/RMSE/R² trên giá tiền, MAPE=mean(abs(pred-price)/price), medianAPE. Giá nguồn đã phải hữu hạn dương nên MAPE không chia0, nhưng nhạy khi giá thấp.

exp(logprediction) ước tính giá điển hình, không tự coi là trung bình không chệch. Không sửa retransformation bằng targettest. Dải tham khảo nhân dùng phân vị90% củaabs(log(price/pred)) trênvalidation, công bố coverage thực đo trêntest; không gọi là khoảng tin cậy90%bảo đảm trong thị trường biến động.

Lưu toàn bộpipeline và nạp lại chínhartifact trước tínhvalidation. Script dự đoán phải chỉ cần đầu vào tài sản, không cần giá thật. Báo cáo test theo quận và khoảnggiá cố định (<3,3–6,6–12,>=12tỷ), kèm số mẫu; mẫu scatter lấyhash row_id ổn định. Không loại outlier trên targettest để tăng thành tích.

## Giới hạn phải công bố

Giá rao, không giá giao dịch; nhãn kiểm traAI; khác biệt thôngthủy/timtường/sânvườn còn chưa đồng nhất ở một số tin; nhóm nhà ưu tiên bằng chứng ở rõ làm thiên lệch mẫu; địa danh theo phiên bản cũ; thiếu dự án/phường và mứcgiá cao có thể gây sai số lớn. Mô hình thắng phải do thực đo, có thể làbaseline.
