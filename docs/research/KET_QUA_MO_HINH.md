# Kết quả thực nghiệm mô hình v1

Nguồn: artifacts/models/v1/results.json và selection.json. Chọn theo MAE validation, không dùng test để chọn.

| Loại | Mô hình | MAE val (tỷ) | RMSE val (tỷ) | MAE test (tỷ) | RMSE test (tỷ) | R² test | MAPE test | Median APE |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| house | baseline | 4.749 | 14.487 | 4.662 | 21.929 | 0.008 | 42.78% | 27.15% |
| apartment | baseline | 3.430 | 43.747 | 3.359 | 8.781 | 0.047 | 45.46% | 31.82% |
| house | house_lr | 2.757 | 9.866 | 2.950 | 18.159 | 0.320 | 23.68% | 16.57% |
| house | house_rf | 3.542 | 12.745 | 3.615 | 20.584 | 0.126 | 29.48% | 20.38% |
| house | house_gbt | 3.085 | 11.764 | 3.198 | 19.442 | 0.220 | 25.27% | 16.69% |
| apartment | apartment_lr | 1.503 | 43.313 | 1.395 | 4.586 | 0.740 | 18.63% | 13.74% |
| apartment | apartment_rf | 2.414 | 43.436 | 2.198 | 6.053 | 0.547 | 29.21% | 22.52% |
| apartment | apartment_gbt | 2.132 | 43.420 | 1.958 | 5.644 | 0.606 | 25.38% | 19.14% |
| house | common_lr | 3.124 | 12.166 | 3.120 | 18.320 | 0.308 | 25.15% | 17.75% |
| apartment | common_lr | 1.534 | 43.319 | 1.419 | 4.643 | 0.733 | 18.89% | 13.82% |
| house | common_rf | 3.712 | 13.026 | 3.799 | 20.847 | 0.104 | 31.34% | 21.87% |
| apartment | common_rf | 2.480 | 43.437 | 2.290 | 6.167 | 0.530 | 30.65% | 23.21% |
| house | common_gbt | 3.348 | 11.123 | 3.537 | 18.320 | 0.308 | 29.13% | 20.41% |
| apartment | common_gbt | 2.117 | 43.409 | 1.946 | 5.541 | 0.620 | 25.86% | 19.11% |

Chọn house_lr và apartment_lr. Giảm MAE test so baseline 36,73% và 58,47%. Train 78.048, validation 17.886, test 37.845 tin. Chín pipeline huấn luyện, lưu/nạp và đánh giá trong 187,60 giây ở lần chạy local[4]/driver 4 GB.

Coverage test của dải validation: nhà 90,12%, căn hộ 86,00%; không bảo đảm 90% cho từng tài sản. RMSE validation căn hộ 43,313 tỷ và R² 0,021 chịu ảnh hưởng giá cực cao. Top 10 lỗi chiếm 92,20% SSE nhà và 42,47% SSE căn hộ. Không cắt target test hoặc chọn lại mô hình.

Các bảng theo quận/khoảng giá, scatter, domain train, kế hoạch, lựa chọn và pipeline lưu ở artifacts/models/v1. Review 800 nhãn AI chưa thay thế nhãn người độc lập; cohort chọn lọc và proxy trùng toàn văn có giới hạn.
