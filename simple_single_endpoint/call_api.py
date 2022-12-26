import requests

if __name__ == "__main__":
    request = requests.get("http://127.0.0.1:8000/home")
    print(request.status_code)
    print(request.text)
