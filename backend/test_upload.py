import requests

url = "http://127.0.0.1:5000/upload"
file_path = "C:\Users\user\Pictures\test-image.png"  # Change this to your image path

with open(file_path, "rb") as file:
    files = {"file": file}
    response = requests.post(url, files=files)

print(response.json())  # Output server response
