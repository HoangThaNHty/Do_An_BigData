# Mục 02 Kiểm chứng giao dịch và diện tích

Trạng thái cập nhật 12/10/2026: đã đọc/gán nhãn AI đủ 150 calibration và150 evaluation. Phiên bản cố định dự đoán bán100tin,99khớp nhãn bán AI; mẫu chỉ có1tin thuê. 34ứng viên còn6tin có vấn đề giá/diện tích, chưa coi là dữ liệu sạch. Xem KET_QUA_EVALUATION_V1.md; cần mẫu mới đánh giá lớp chất lượng bổ sung. Kết quả dựa nhãn AI, chưa có kiểm tra chéo của người.

## Sản phẩm đã tạo

- 1.680 tin mẫu phân tầng từ khảo sát trước, phục vụ tìm các trường hợp khó.
- 300 tin mẫu bổ sung trong phạm vi nhà/căn hộ TP.HCM, không trùng row_id với mẫu trước.
- Phiếu đọc 300 tin không hiển thị nhãn tự động; 150 tin hiệu chỉnh và 150 tin đánh giá.
- File dự đoán riêng và manifest lưu seed, revision dataset, fingerprint mã quy tắc.
- Công cụ kiểm tra nhãn và tính precision tin bán, ma trận nhầm lẫn, mức đồng thuận loại diện tích trên mẫu.

Mẫu 300 tin được lấy Bernoulli với cùng xác suất ban đầu, sau đó chọn bằng hash và bỏ row_id trùng. Mẫu được đóng băng để tái kiểm tra. Mẫu này không chứng minh các tài sản độc lập: hai tin khác row_id vẫn có thể nói về cùng tài sản.

## Đọc và ghi nhãn

File: `D:\slider\real-estate-bigdata\artifacts\review\v1\blind_review.csv`.

Điền theo nội dung tin, không sao chép dự đoán:

| Cột | Giá trị |
|---|---|
| manual_transaction | sale / rent / uncertain |
| manual_area_kind | apartment / land / floor / unknown |
| manual_price_valid | yes / no / uncertain |
| reviewer | Tên hoặc định danh người/model đọc |
| review_method | human / ai_assisted / ai |
| review_notes | Bằng chứng, mâu thuẫn hoặc lý do không xác định |

Đọc phần calibration để hiệu chỉnh. Chỉ đánh giá phần evaluation sau khi cố định quy tắc tương ứng; nếu quy tắc đổi, chạy dự đoán lại có phiên bản và ghi rõ lượt đánh giá. Không sử dụng evaluation để hiệu chỉnh rồi công bố là tập kiểm tra độc lập.

## Chạy công cụ

Tại D:\slider\real-estate-bigdata:

```powershell
./scripts/run.ps1 src.etl.review prepare
./scripts/run.ps1 src.etl.review replay-evaluation
.venv/Scripts/python.exe -m src.etl.review score --predictions=artifacts/review/v1/evaluation_runs/a2b7d760d9507f80/predictions.json
```

Lệnh prepare không ghi đè bộ mẫu đã có nhãn. Muốn lượt mới dùng `--output artifacts/review/v2`.

Lệnh score ghi evaluation.json. Nếu phần evaluation chưa đủ nhãn hoặc chưa có tên/phương thức người đọc, trạng thái là needs_labels, metrics là null. Công cụ không tự biến dự đoán thành ground truth. Nếu nhãn sai danh mục, row_id trùng hoặc thiếu dự đoán, công cụ báo lỗi.

Lệnh replay-evaluation yêu cầu hash mã trùng freeze.json; score với --predictions kiểm tra fingerprint dự đoán và phiên bản cố định. Không bỏ --predictions khi đánh giá phiên bản mới: mặc định cũ dùng predictions.json của quy tắc ban đầu để bảo toàn lịch sử.

## Điều kiện hoàn thành mục 02

Đã đọc mẫu hiệu chỉnh, ghi các quy tắc sửa và lý do; có nhãn tham chiếu cho mẫu đánh giá; báo cáo độ phủ và lỗi theo phương thức gán nhãn thực tế. Nhãn AI chỉ là đánh giá dựa trên AI, không trình bày như nhãn người hay chuyên gia xác nhận. Chưa đặt ngưỡng precision giả định trước khảo sát mẫu. Dữ liệu chưa xác định được giữ riêng.

Các phần chưa có nhãn không chặn việc xây cấu trúc ETL, nhưng chặn tuyên bố dữ liệu sạch đã kiểm chứng.
