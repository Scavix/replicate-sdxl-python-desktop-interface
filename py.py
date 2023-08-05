import requests
import shutil
import time
# https://replicate.com/stability-ai/sdxl

prompt = input("Enter the prompt: ")
url = "https://api.replicate.com/v1/predictions"
data = {
    "version": "2b017d9b67edd2ee1401238df49d75da53c523f36e363881e057f5dc3ed3c5b2",
    "input": {"prompt": prompt, "seed": 42, "num_outputs": 4}
}
headers = {
    "Authorization": "Token r8_YXpUpYn13jRFr5JXYktCIyaiMyLfMtP4OTOnr",
    "Content-Type": "application/json"
}
response = requests.post(url, json=data, headers=headers)

print(response.status_code)
print(response.json())
print()

if response.status_code == 201:
    reqId = response.json()['id']
    url = "https://api.replicate.com/v1/predictions/"+reqId
    headers = {
        "Authorization": "Token r8_YXpUpYn13jRFr5JXYktCIyaiMyLfMtP4OTOnr",
        "Content-Type": "application/json"
    }
    while True:
        print("Waiting for response...")
        time.sleep(3)

        response = requests.get(url, headers=headers)
        print(response.status_code)
        if response.status_code == 200 and response.json()['status'] == 'succeeded':
            print(response.json())
            urls = response.json()['output']
            id = 0
            for url in urls:
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    with open("replicate-prediction-"+str(reqId) + ("" if len(urls) == 1 else ("-"+str(id)))+".png", 'wb') as f:
                        response.raw.decode_content = True
                        shutil.copyfileobj(response.raw, f)
                        print('Image Downloaded Successfully')
                id = id+1
            exit(0)
else:
    exit(1)
