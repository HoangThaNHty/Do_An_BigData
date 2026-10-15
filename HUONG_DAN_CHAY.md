# Hướng dẫn chạy hiện hành

Đọc [SETUP.md](docs/guide/SETUP.md) cho cài từ clone và xử lý lỗi; [tester](docs/guide/TESTER_CHECKLIST.md) để kiểm tra chức năng; [demo](docs/guide/DEMO_THUYET_TRINH.md) để thuyết trình.

```powershell
./scripts/setup.ps1
./scripts/start-local.ps1
```

Setup chạy lần đầu. Những lần sau chỉ start-local. Mở http://localhost:3000/ sau Ready, giữ terminal hoạt động; thêm -Lan nếu demo cùng mạng. Chỉ một Spark JVM mỗi lần.
