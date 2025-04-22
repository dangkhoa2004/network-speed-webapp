# ⚡️ SpeedTest by dangkh0a

Một ứng dụng web đơn giản được xây dựng bằng **Flask** kết hợp với **Tailwind CSS** và **Font Awesome**, cho phép bạn:

- Đo tốc độ mạng (ping, download, upload)
- Xem thông tin mạng nội bộ (IPv4, IPv6, Gateway, DNS...)
- Tra cứu IP công cộng, nhà mạng (ISP), tổ chức, vị trí địa lý...

## 🎯 Tính năng chính

- 🎯 Giao diện đẹp mắt, dễ dùng, hỗ trợ cả dark mode
- ⚡️ Kiểm tra tốc độ internet theo thời gian thực
- 🌐 Hiển thị IP công cộng, nhà mạng, ASN, vị trí
- 🧠 Phân tích mạng nội bộ: IPv4, IPv6, Gateway, DNS, Subnet Mask...
- 🔊 Có hiệu ứng âm thanh và confetti khi hoàn tất kiểm tra

## 💻 Công nghệ sử dụng

- **Backend**: Python + Flask
- **Frontend**: Tailwind CSS + Font Awesome + JavaScript
- **API sử dụng**: [ip-api.com](http://ip-api.com), `speedtest-cli`, `psutil`

## 🏗 Cấu trúc dự án

```

📁 project-root/
├── app.py # Flask App chính
├── templates/
│ └── index.html # Giao diện người dùng
├── static/
│ └── doneSound.mp3 # Âm thanh khi hoàn thành
├── requirements.txt # Danh sách thư viện cần cài
└── README.md # Tài liệu dự án

```

## 🚀 Cài đặt & chạy ứng dụng

1. **Clone project:**

```bash
git clone https://github.com/yourusername/speedtest-flask.git
cd speedtest-flask
```

2. **Tạo môi trường ảo (tuỳ chọn):**

```bash
python -m venv venv
source venv/bin/activate  # Hoặc venv\Scripts\activate trên Windows
```

3. **Cài đặt thư viện:**

```bash
pip install -r requirements.txt
```

4. **Chạy server:**

```bash
python app.py
```

5. **Truy cập trình duyệt:**

```
http://127.0.0.1:5000/
```

## 🔐 Lưu ý

- Nếu dùng trên **Linux/Mac**, thông tin DNS được đọc từ `/etc/resolv.conf`
- Một số hệ điều hành có thể không hiển thị đầy đủ IPv6 tạm thời
- API kiểm tra tốc độ có thể mất vài giây để phản hồi

## 📃 Giấy phép

Dự án được phát hành theo giấy phép **MIT** — Bạn có thể tự do sử dụng, chỉnh sửa và chia sẻ.

### 📦 `requirements.txt`

```txt
Flask
flask-cors
flask-compress
aiohttp
beautifulsoup4
lxml
python-whois
```
