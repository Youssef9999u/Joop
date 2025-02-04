import requests
import json

# بيانات تسجيل الدخول
login_data = {
    'username': '1281811280',
    'password': '123456',
    'lang': 'eg',
}

# المتغيرات
progress = 0  # تقدم المحاولات
is_running = True  # حالة المحاولة

# التوكن الخاص بجيتهاب
github_token = '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'
repo_owner = 'your-github-username'
repo_name = 'your-repo-name'
file_path = 'progress.txt'  # الملف الذي يحتوي على التقدم
branch = 'main'

# التوكن المستخدم في الطلبات
token = "02c8znoKfqx8sfRg0C0p1mQ64VVuoa7vMu+wgn1rttGH04eVulqXpX0SM9mF"

# رأس الطلبات (Headers)
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'PythonRequests',
    'Authorization': f'Bearer {token}',
}

# قراءة التقدم من GitHub
def read_progress_from_github():
    global progress
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'
    response = requests.get(url, headers={'Authorization': f'token {github_token}'})
    
    if response.status_code == 200:
        file_content = response.json()
        file_data = requests.get(file_content['download_url']).text
        progress = int(file_data.strip())  # تحويل النص إلى رقم
        print(f"✅ تم استرجاع التقدم الحالي من GitHub: {progress}")
    else:
        print("⚠️ لم يتم العثور على الملف أو فشل الاتصال بـ GitHub.")

# تحديث التقدم في GitHub
def update_progress_on_github():
    global progress
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'
    response = requests.get(url, headers={'Authorization': f'token {github_token}'})
    
    if response.status_code == 200:
        file_info = response.json()
        sha = file_info['sha']
        update_content = {
            "message": "Updating progress",
            "content": json.dumps(str(progress)).encode('utf-8').decode('utf-8'),
            "sha": sha,
            "branch": branch
        }
        update_response = requests.put(url, headers={'Authorization': f'token {github_token}'}, json=update_content)
        if update_response.status_code == 200:
            print(f"✅ تم تحديث التقدم إلى: {progress}")
        else:
            print(f"⚠️ حدث خطأ أثناء تحديث التقدم: {update_response.content}")
    else:
        print("⚠️ لم يتم العثور على الملف لتحديثه.")

# هنا تقوم باستدعاء `read_progress_from_github` في بداية الكود لاسترجاع التقدم من GitHub
read_progress_from_github()

# وفي كل مرة يتغير التقدم (بعد كل محاولة ناجحة أو فاشلة) تقوم باستدعاء `update_progress_on_github` لحفظ التقدم
progress += 1  # عند نجاح أو فشل المحاولة
update_progress_on_github()
