# Kết quả đọc và hiệu chỉnh mẫu calibration v1

Ngày 11/10/2026. Đây là mốc triển khai mục 02, chưa hoàn thành kiểm chứng dữ liệu độc lập.

## Công việc thực tế

Đã đọc đủ tiêu đề/mô tả của 150 tin calibration, ghi nhãn giao dịch, loại diện tích và khả năng đối chiếu tổng giá; mỗi tin có ghi chú bằng chứng. Người đọc: Codex; `review_method=ai`. Đây là đánh giá từ nội dung tin do AI, không phải nhãn người hoặc chứng nhận tài sản.

Lưu nhãn ở `artifacts/review/v1/blind_review.csv`; giữ bản chưa gán nhãn `blind_review.unlabelled.csv`, bốn file annotation JSON theo đợt. Đã kiểm tra 300 dòng giữ nguyên trường nguồn, row_id và split; 150 dòng evaluation chưa được gán nhãn. `scripts/apply_review_labels.py` không ghi đè dòng đã có reviewer.

| Nhóm nhãn calibration | Số tin |
|---|---:|
| Bán / chưa xác định | 117 / 33 |
| Diện tích đất / căn hộ / chưa rõ | 74 / 32 / 44 |
| Tổng giá đối chiếu được / chưa chắc / không hợp lệ | 117 / 25 / 8 |

Không có nhãn thuê trong mẫu calibration này; không thể dùng nó để chứng minh khả năng nhận diện mọi loại tin thuê. Không diễn giải các tỷ lệ thành phân bố thị trường.

## Hiệu chỉnh quy tắc

- Nhận thêm các cách viết CH, tòa nhà, penthouse/penhouse, nhà bán, bán lại, bán gấp có dấu gạch nối và tổng giá bán trong mô tả.
- Giảm nhầm dòng tiền/hợp đồng thuê và công năng cho thuê thành giao dịch thuê; vẫn giữ tin bán hoặc thuê ở nhóm chưa xác định.
- Diện tích đất/công nhận hỗ trợ CN, DTCN, công nhận và định dạng markdown. Hai số đất/công nhận khác nhau được giữ riêng, không che bằng ngưỡng 5%.
- Chỉ gán thông thủy/tim tường vào cột area khi số đo tương ứng khớp; không gán theo từ khóa xuất hiện bất kỳ.
- Thêm cờ kiểm tra phạm vi cho dấu hiệu đất, biệt thự, officetel, tòa nhà, khách sạn/CHDV rõ trong tiêu đề.
- Giá và diện tích phải dương hữu hạn; không nhận infinity.

Quy tắc chưa xử lý hết cách viết, quảng cáo dự án/giỏ hàng, phủ định trong mọi ngữ cảnh, mâu thuẫn giá và phạm vi tài sản. Cờ ứng viên chưa phải dữ liệu sạch được phê duyệt. Nhà vẫn ưu tiên bằng chứng đất/công nhận rõ, chưa mở rộng tự động bằng phép nhân kích thước.

## Chẩn đoán trên calibration

| Bất đồng so với nhãn AI | Quy tắc ban đầu | Quy tắc sau hiệu chỉnh |
|---|---:|---:|
| Giao dịch | 39 | 12 |
| Loại diện tích | 75 | 61 |

Mẫu này đã dùng sửa mã, nên đây là chẩn đoán hiệu chỉnh, không phải độ chính xác độc lập. Bất đồng diện tích gồm cả trường hợp AI suy luận đất từ kích thước nhưng quy tắc tự động cố ý yêu cầu bằng chứng đất/công nhận rõ. Không quy đổi số này thành độ tin cậy của tập huấn luyện.

Quy ước chi tiết ở QUY_UOC_GAN_NHAN.md. So sánh giá dùng 1% để phát hiện mâu thuẫn/làm tròn ban đầu; đây không phải ngưỡng sai số dự đoán và không phải xác nhận giá thị trường.

## Phiên bản và kiểm tra

Phiên bản cố định: `candidate-v2-frozen-for-evaluation`.

SHA256 mã quy tắc: `a2b7d760d9507f807edfbae6d414b575235ef399376581d018fda35b01a35b8e`.

Diagnostic và dự đoán calibration ở `artifacts/review/v1/calibration_runs/a2b7d760d9507f80`; mã snapshot ở `frozen_rules`, hồ sơ ở `freeze.json`. Dự đoán evaluation của phiên bản cố định lưu riêng trong `evaluation_runs/a2b7d760d9507f80`, chưa phải kết quả đánh giá. Dự đoán ban đầu không bị ghi đè.

Đã chạy qua 27 tình huống hồi quy với cả giá số/chuỗi, Parquet đọc/ghi/ghi đè, MLlib fit/lưu/nạp mô hình nhỏ. Việc này không phải huấn luyện mô hình giá nhà thật. Replay kiểm tra row_id từ nguồn không bị đổi. Công cụ score đối chiếu fingerprint dự đoán và mã cố định; kiểm tra từ chối provenance sai đã chạy qua.

## Trạng thái và bước tiếp theo

Evaluation: 0/150 nhãn, `metrics=null`, trạng thái `needs_labels`. Đọc/gán nhãn phần evaluation theo quy ước cố định, ghi đúng phương thức; tính kết quả với dự đoán phiên bản đã cố định. Không sửa quy tắc theo mẫu evaluation rồi tiếp tục coi mẫu đó là đánh giá độc lập.

```powershell
./scripts/run.ps1 src.etl.review replay-calibration
./scripts/run.ps1 src.etl.review replay-evaluation
.venv/Scripts/python.exe -m src.etl.review score --predictions=artifacts/review/v1/evaluation_runs/a2b7d760d9507f80/predictions.json
```

Thống kê ứng viên trong profile trước vẫn thuộc quy tắc cũ. Sau đánh giá sẽ chạy lại profile/ETL và ghi số trước/sau phiên bản mới. Chưa triển khai giao diện web/API, chưa huấn luyện mô hình giá nhà thật.
