import requests

data = {
    "username": "newusername",
    "email": "user@example.com",
    "password": "userpassword"
}
r = requests.post('https://0.0.0.0:8001/register', data=data)

print(r.text)
print(r.json())