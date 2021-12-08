import requests

host = "http://localhost:5000"
secret_key = input("Enter secret key: ")
total_request = input("Enter total requests: ")
time = input("Enter request time: ")
request = int(total_request)
i = 1
while i <= request:
  headers = {
    'x_secret_key': secret_key,
    'time_req': time
  }
  response_code = requests.get(host+"/ping", headers=headers)
  response_json = response_code.json()
  print(response_json)
  i += 1