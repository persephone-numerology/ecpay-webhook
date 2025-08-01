from flask import Flask, request

app = Flask(__name__)

@app.route('/ecpay_callback', methods=['POST'])
def ecpay_callback():
    data = request.form.to_dict()
    print("ECPay callback received:", data)
    return '1|OK'

if __name__ == '__main__':
    app.run()