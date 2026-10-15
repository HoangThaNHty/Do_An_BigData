# Mục03 ETL và lớp kiểm tra chất lượng

Cập nhật 12/10/2026. Chưa coi đầu ra ETL là tập huấn luyện đã được xác nhận. Kết quả thực tế từng lần chạy ở data/processed/<run>/manifest.json và artifacts/etl/<run>/summary.json.

## Kết quả chạy thực tế

Lượt thành công: data/processed/etl_v1_retry1, thời gian 321,76 giây. Đọc 1.122.870 dòng; loại 2 bản ghi nguồn trùng hoàn toàn; ghi và đọc lại đủ 1.122.868 dòng.

| Trạng thái | Nhà | Căn hộ | Tổng |
|---|---:|---:|---:|
| Ứng viên tạm | 53.101 | 134.862 | 187.963 |
| Cần xem lại | 749.621 | 139.133 | 888.754 |
| Xác định thuê | 40.198 | 5.953 | 46.151 |

Các mã lý do thường gặp: chưa xác nhận diện tích đất nhà 717.257, giao dịch chưa rõ 297.358, chưa đọc được tổng giá 195.134, giá văn bản khác cột nguồn 175.199. Một tin có thể có nhiều lý do; không cộng các mã lý do thành số tin. Quy tắc giá giữ riêng cả tình huống có giá cũ/mới hoặc nhiều tài sản; số mâu thuẫn không đồng nghĩa tất cả nguồn sai.

Lượt etl_v1 trước đó lỗi commit thư mục phân vùng trên Windows và không được dùng; artifacts/etl/etl_v1/failure.json lưu chẩn đoán. Đã sửa adapter Hadoop local và kiểm tra phân vùng tiếng Việt/null/ghi đè. Manifest thành công và các bảng số liệu thuộc lượt retry1.

## Lý do bổ sung

Evaluation v1 đối chiếu 34 ứng viên có6 tin còn vấn đề giá/diện tích. Precision nhận diện tin bán không thay thế kiểm tra nhãn giá và loại diện tích. Xem KET_QUA_EVALUATION_V1.md.

Giữ nguyên src/etl/rules.py phiên bản đã đánh giá. Thêm src/etl/quality.py riêng, phiên bản cross-field-v1-provisional. Lớp mới được xây sau khi xem v1; cần mẫu kiểm tra mới, không công bố kết quả chẩn đoán trên v1 là độ chính xác độc lập.

## Những gì mã ETL thực hiện

1. Đọc10shard nguồn đã kiểm tra checksum; giới hạn province_name HồChíMinh và property_type_name Nhà/Căn hộ chung cư.
2. Tạo source_record_id từ toàn bộ trường nguồn. Chỉ loại bản ghi nguồn trùng hoàn toàn. Giữ dữ liệu gốc.
3. Chạy quy tắc giao dịch/diện tích đã cố định và lớp chất lượng mới. Không impute hoặc sửa price/area.
4. Kiểm tra nhóm row_id có nhiều bản ghi nguồn khác nhau: giữ riêng để tránh chọn ngẫu nhiên đặc trưng bất đồng.
5. Ghi Parquet phân vùng disposition, loại tài sản, tháng; giữ văn bản nguồn và danh sách lý do.
6. Đếm lại artifact đã ghi; số dòng phải bằng số bản ghi nguồn duy nhất. Lưu số trước/sau, lý do, phiên bản/hash mã và revision dataset.

| Disposition | Ý nghĩa |
|---|---|
| provisional_training | Ứng viên đạt các kiểm tra hiện tại; chưa có xác nhận đủ để huấn luyện |
| quarantine | Tin cần xem lại giao dịch, giá, diện tích, phạm vi, thiếu/trùng hoặc nhận diện |
| excluded_rent | Quy tắc xác định thuê; vẫn giữ dòng và bằng chứng để kiểm tra |

Chưa gộp tin đăng lại cùng tài sản. Đây là yêu cầu cần làm trước chia train/test theo thời gian. Chưa ghép ranh giới địa lý; có tên quận không có nghĩa địa chỉ đã xác minh.

## Lớp đối chiếu sơ bộ

- Tổng giá: trích số tiền rõ từ tiêu đề và cụm giá trong mô tả; so với cộtprice theo ngưỡng đối chiếu1%. Tách tiền/tháng hoặc tiền/m². Số mâu thuẫn, thiếu biểu thức có thể đọc hoặc dạng viết tắt không chắc được giữ riêng.
- Căn hộ: cần sốm² trong văn bản phù hợp area, không chỉ dựa cột loại hình. Nhà: vẫn yêu cầu bằng chứng đất/công nhận rõ từ lớp đã cố định.
- Phạm vi: giữ riêng dấu hiệuofficetel/villa/shophouse/dãytrọ/nhàtrọ bên cạnh cờ phạm vi từ bộ quy tắc ban đầu.
- Kiểm tra giá/diện tích dương hữu hạn, timestamp, quận và giao dịch. Không lọc IQR hoặc đặt trần giá toàn cục.

Đối chiếu số không chứng minh đó là đúng căn chính nếu tin có giỏ hàng/nhiều tài sản. Biểu thức có thể không đọc được cách viết VND đầy đủ, dấu phân cách hàng nghìn, sốtiền cũ/mới hoặc viết tắt hiếm; chọn giữ riêng thay vì suy đoán. Sốm² có thể nằm trong thông tin dựán/tiệních. Cần đánh giá mẫu mới, báo cáo tỷ lệ giữ và lỗi; không gọi đây là dữ liệu sạch hoàn toàn.

## Chạy và bảo toàn kết quả

```powershell
./scripts/run.ps1 src.etl.quality_smoke
./scripts/run.ps1 src.etl.build
```

Mặc định ghi data/processed/etl_v1. Nếu thư mục đã tồn tại, lệnh từ chối ghi đè; dùng --output=data/processed/etl_v2 cho lượt tiếp theo. Đường dẫn đầu ra phải nằm trong data/processed của dự án; không xóa raw hoặc kết quả cũ tự động.

11tình huống kiểm tra chéo đã chạy qua: giá tỷ/triệu sai đơn vị, giá khác cột, giá/diện tích thiếu bằng chứng, trả góp/dòng tiền không được nhầm và phạm viofficetel. Đây là kiểm tra hồi quy, không phải kết quả đánh giá thị trường.

## Mẫu đánh giá bổ sung

```powershell
./scripts/run.ps1 src.etl.review prepare --output=artifacts/review/v2 --size=200 --seed=20261012 --quality-checks --evaluation-only
```

Mẫu mới loại row_id trong mẫu profile và tất cả review đã có. Phiếu đọc chỉ có trường nguồn; dự đoán kiểm tra chất lượng lưu riêng; manifest lưu hashquality/rules và các nguồn mẫu đã loại. 200dòng đều dùng đánh giá; không dùng để sửa lớp chất lượng rồi gọi là đánh giá độc lập của cùng phiên bản. Nếu sửa tiếp, cần lượt mới.

Đã chạy lệnh và xác nhận 200 row_id duy nhất, không giao với 1.980 row_id mẫu trước; không có nhãn tự động trong CSV. Snapshot mã ở artifacts/review/v2/frozen_code; freeze.json lưu hash mã/dự đoán trước gán nhãn. Quality SHA256 c2487cef8313f3ff988f84d85e1567bab4e50cd57e18ffc298350c74ac20382a. Hiện 0/200 nhãn; công cụ score trả metrics=null đúng yêu cầu.

Bước kế tiếp là đọc đủ văn bản v2, ghi bằng chứng theo QUY_UOC_GAN_NHAN.md trước khi mở predictions.json. Dùng scripts/apply_review_labels.py với --review-dir=artifacts/review/v2 --split=evaluation; index là vị trí 0–199 trong phiếu evaluation. Chỉ gán nhãn từ nội dung nguồn, không từ cờ protected_candidate. Sau đó chạy:

```powershell
.venv/Scripts/python.exe -m src.etl.review score --output=artifacts/review/v2
```

Báo cáo thêm quality_candidates: số ứng viên giữ tạm, số được cả ba nhãn nguồn hỗ trợ và row_id còn vấn đề. Tỷ lệ này chưa kiểm chứng phạm vi, tài sản thật, địa giới hoặc tin đăng lại; phải báo cáo cùng cỡ mẫu ứng viên và phương thức AI/người.
