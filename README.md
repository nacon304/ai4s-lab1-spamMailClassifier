# Enron Spam Classifier

## Mô tả

Dự án này là một ứng dụng phân loại email rác dựa trên bộ dữ liệu Enron. Ứng dụng sử dụng các mô hình học máy để xác định xem một email có phải là rác hay không. Giao diện người dùng (GUI) đơn giản cho phép người dùng nhập nội dung email và nhận phản hồi ngay lập tức.

## Cấu trúc dự án

- **enron_spam_data/**: Chứa dữ liệu email Enron được sử dụng để huấn luyện và kiểm tra mô hình.
- **model/**: Chứa mã nguồn cho mô hình học máy và các thông tin liên quan.
- **nltk_data/corpora/**: Thư viện dữ liệu ngôn ngữ tự nhiên cần thiết cho quá trình xử lý văn bản.
- **pdf/**: Chứa các tài liệu PDF liên quan đến dự án.
- **.gitignore**: Các tệp và thư mục sẽ bị bỏ qua khi commit.
- **README.md**: Tài liệu này.
- **enron_spam_app.py**: Tệp chính của ứng dụng, nơi chứa mã nguồn cho GUI và logic phân loại.
- **requirements.txt**: Danh sách các thư viện Python cần thiết để chạy ứng dụng.

## Cài đặt

Để chạy ứng dụng này, bạn cần có Python và pip được cài đặt trên máy tính của mình. Thực hiện các bước sau để thiết lập môi trường:

1. **Clone repository**:
    ```bash
    git clone https://github.com/<username>/enron_spam_classifier.git
    cd enron_spam_classifier
    ```

2. **Cài đặt các thư viện cần thiết**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Chạy ứng dụng**:
    ```bash
    python enron_spam_app.py
    ```

## Cách sử dụng

1. Mở ứng dụng.
2. Nhập nội dung email vào ô văn bản.
3. Nhấn nút "Phân loại" để nhận phản hồi về email đó (rác hoặc không rác).

## Đóng góp

Nếu bạn muốn đóng góp cho dự án này, vui lòng tạo một pull request hoặc mở một issue để thảo luận về những thay đổi bạn muốn thực hiện.

## Liên hệ

- **Nguyễn Duy** - [ndtduy](https://github.com/ndtduy)
- Email: ndtduy@example.com

## Giấy phép

Dự án này được cấp phép theo [Giấy phép MIT](LICENSE).
