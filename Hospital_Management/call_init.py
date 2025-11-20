import requests

try:
    r = requests.post('http://127.0.0.1:8000/init_db', timeout=20)
    print('init_db:', r.status_code, r.text)
except Exception as e:
    print('init_db error:', e)
