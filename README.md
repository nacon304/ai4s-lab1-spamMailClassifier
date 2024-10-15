# Enron Spam Classifier

## Mô tả

Trong đồ án này, chúng tôi xây dựng một giao diện ứng dụng đơn giản phân loại email rác dựa trên bộ dữ liệu Enron. Ứng dụng sử dụng các mô hình học máy để xác định xem một email có phải là rác hay không. Giao diện người dùng (GUI) đơn giản cho phép người dùng nhập nội dung email hoặc file gồm các email và nhận phản hồi ngay lập tức.

## Cấu trúc dự án

- **enron_spam_data**: Chứa dữ liệu email Enron được sử dụng để huấn luyện và kiểm tra mô hình.
- **model**: Chứa trọng số cho pipeline mô hình học máy.
- **nltk_data/corpora**: Thư viện dữ liệu ngôn ngữ tự nhiên cần thiết cho quá trình xử lý văn bản.
- **enron_spam_app.py**: Tệp chính của ứng dụng, nơi chứa mã nguồn cho GUI và logic phân loại.
- **requirements.txt**: Danh sách các thư viện Python cần thiết để chạy ứng dụng.

## Cài đặt

Để chạy ứng dụng này, cần có Python và pip được cài đặt trên máy tính của mình. Thực hiện các bước sau để thiết lập môi trường:

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
