import requests


url = "http://127.0.0.1:8000/api/datasets/upload/"

file_path = "datasets/sample/validation_test.csv"


with open(file_path, "rb") as file:

    response = requests.post(
        url,
        files={
            "file": file
        }
    )


print("Status code:", response.status_code)
print("Response:")
print(response.json())