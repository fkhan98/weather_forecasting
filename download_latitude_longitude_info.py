import requests

url = "https://raw.githubusercontent.com/strativ-dev/technical-screening-test/main/bd-districts.json"

response = requests.get(url)

if response.status_code == 200:
    with open("lat_long_info.json", "wb") as file:
        file.write(response.content)
    print("File downloaded successfully.")
else:
    print(f"Failed to download the file. Status code: {response.status_code}")
