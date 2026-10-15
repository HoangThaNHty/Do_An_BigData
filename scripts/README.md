# Scripts theo công việc

| Mục đích | Lệnh / file |
|---|---|
| Cài lần đầu | setup.ps1 |
| Chạy local/LAN | start-local.ps1 / -Lan |
| Chạy một module Python cùng cấu hình Spark | run.ps1 <module> |
| Kiểm tra artifact trong clone | python scripts/check_repo.py |
| Regression health khi Spark dừng | .venv/Scripts/python.exe -m scripts.check_health |
| Rà file đưa vào Git | python scripts/audit_github.py |
| API đối chiếu dữ liệu/model | check_api.py, check_product_features.py |
| UI V5 / lỗi và độ tương phản | check_product_v5.cjs, check_ui_ux_v4_errors.cjs; check_web/check_ui_ux_v4 là alias, không chạy lặp |
| Công thức tài chính độc lập | node scripts/check_home_plan.mjs |
| Tải JDK/nguồn pinned/địa giới | bootstrap_data.py, bootstrap_geo.py |
| Java adapter Windows | build_local_fs.ps1 (setup tự gọi) |
| Phân tích model / khóa dependencies | model_diagnostics.py, lock_python.py |
| Đóng và kiểm tra ZIP local | package_handoff.py, verify_handoff.py |
| Soạn/xuất Office, chưa chạy đợt này | prepare_deliverables.py, export_office.ps1 |
| Lịch sử audit/prototype, không dùng để chạy app | archive/ui-audits/audit_ux_v3.cjs, archive/ui-audits/review_mcp_prototypes.cjs |

Các script Python/Powershell lấy root theo vị trí repo, không yêu cầu ổ D: của máy gốc. Script audit prototype dùng preview MCP riêng, không phải kiểm thử ứng dụng đã tích hợp. Không chạy finalize_docs.py cũ: đã loại vì ghi đè tài liệu hiện hành bằng snapshot trước V4.
