import requests

def registerReq():
    res = requests.post('http://127.0.0.1:3000/api/register/1/',
                        json={'login': 'ser', 'password': 123, 'role': 'u', 'email': '21@ma.ru'})
    res = requests.post('http://127.0.0.1:3000/api/b/register/2/',
                        json={'login': 'ser_business', 'password': 321, 'role': 'b', 'email': '213@ma.ru'})
    print(res.json())

def loginReq():
    res = requests.post('http://127.0.0.1:3000/api/login/1/', json={'login': 'ser', 'password': 123})
    res = requests.post('http://127.0.0.1:3000/api/b/login/2/', json={'login': 'res', 'password': 321})
    print(res.json())

loginReq()
