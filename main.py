from flask import Flask, request
import hashlib
import urllib.parse

app = Flask(__name__)

# 綠界提供的 HashKey 與 HashIV（請勿外流）
HASH_KEY = 'ePIXXcPwtc62OSCs'
HASH_IV = 'sUOJZ8dmTEuZaYxn'


# 檢查碼生成函式
def generate_check_mac_value(params: dict) -> str:
    # 移除 CheckMacValue 本身
    sorted_items = sorted((k, v) for k, v in params.items() if k != 'CheckMacValue')
    query = f"HashKey={HASH_KEY}&" + '&'.join([f"{k}={v}" for k, v in sorted_items]) + f"&HashIV={HASH_IV}"
    # URL encode + 轉小寫
    encoded_str = urllib.parse.quote_plus(query).lower()
    # 做 MD5 並轉成大寫十六進位
    checksum = hashlib.md5(encoded_str.encode('utf-8')).hexdigest().upper()
    return checksum


# 接收綠界付款結果通知的 webhook
@app.route('/payment/notify', methods=['POST'])
def payment_notify():
    data = request.form.to_dict()
    print("[Webhook 收到通知]", data)

    # 驗證 CheckMacValue
    received_mac = data.get('CheckMacValue')
    generated_mac = generate_check_mac_value(data)

    if received_mac != generated_mac:
        print("[錯誤] 檢查碼不一致！")
        return '0|CheckMacValue Mismatch'

    print("[成功] 檢查碼驗證通過！")
    # ⚠️：這裡未來可以加上寄送 email、產生 CloudFront 連結的邏輯

    return '1|OK'


if __name__ == '__main__':
    app.run()
