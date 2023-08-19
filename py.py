import requests
import shutil
import time
import PySimpleGUI as sg
import os 
from PIL import Image, ImageTk
from TokenManager import TokenManager

# https://replicate.com/stability-ai/sdxl

def main():
    im = Image.open("loading.gif")
    im = im.resize((300, 300), resample=Image.BICUBIC)
    outstr = ""
    
    api_manager = TokenManager("api_key.key")
    if os.path.exists("api.txt"):
        with open("api.txt", "rb") as f:
            encrypted_api = f.read()
        api = api_manager.decrypt(encrypted_api)
    else:
        api='INSERT API KEY HERE'
    
    # All the stuff inside your window.
    layout = [  [sg.Image(key='-IMAGE0-'),sg.Image(key='-IMAGE1-')],
                [sg.Image(key='-IMAGE2-'),sg.Image(key='-IMAGE3-')],
                [sg.Text('Enter prompt'), sg.InputText(key='-PROMPT-', default_text='an ugly cat')],
                [sg.Text('Enter API token'), sg.InputText(key='-API-', default_text=api),sg.Checkbox(text='Save KEY',key='-CBOX-', default=True)],
                [sg.Text('Enter Seed'), sg.InputText(key='-SEED-',default_text=42), sg.Text('Num of images'),sg.Combo([1,2,3,4], default_value=1, key='-NUM_IMG-')],
                [sg.Multiline(default_text="", expand_x=True, expand_y=True, key='-OUTPUT-')],
                [sg.Button('Ok'), sg.Button('Cancel')]]

    # Create the Window
    window = sg.Window('Replicate AI images sdxl', layout, element_justification='c', finalize=True)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                break
        elif event == 'Ok':
            prompt=window['-PROMPT-'].get()
            seed=window['-SEED-'].get()
            num_img=window['-NUM_IMG-'].get()

            if window['-CBOX-'].get():
                api = window['-API-'].get()
                encrypted_api = api_manager.encrypt(api)
                with open("api.txt", "wb") as f:
                    f.write(encrypted_api)

            outstr = str(prompt) + " " + str(seed) + " " + str(num_img) + " " + str(api)
            print(outstr)
            window['-OUTPUT-'].update(value=outstr)

            url = "https://api.replicate.com/v1/predictions"
            data = {
                "version": "2b017d9b67edd2ee1401238df49d75da53c523f36e363881e057f5dc3ed3c5b2",
                "input": {"prompt": prompt, "seed": seed, "num_outputs": num_img}
            }
            headers = {
                "Authorization": "Token " + api,
                "Content-Type": "application/json"
            }
            response = requests.post(url, json=data, headers=headers)

            outstr += "\n" + str(response.status_code) + "\n" + str(response.json()) + "\n"
            print(outstr)
            window['-OUTPUT-'].update(value=outstr)

            if response.status_code == 201:
                reqId = response.json()['id']
                url = "https://api.replicate.com/v1/predictions/"+reqId
                headers = {
                    "Authorization": "Token r8_YXpUpYn13jRFr5JXYktCIyaiMyLfMtP4OTOnr",
                    "Content-Type": "application/json"
                }
                
                image = ImageTk.PhotoImage(im)
                window['-IMAGE0-'].update(data=image)
                window['-IMAGE1-'].update(data=image)
                window['-IMAGE2-'].update(data=image)
                window['-IMAGE3-'].update(data=image)

                while True:
                    time.sleep(1)
                    print("Waiting for response...")
                    window['-OUTPUT-'].update(value="Waiting for response...")

                    window["-IMAGE0-"].UpdateAnimation("loading.gif",time_between_frames=100)
                    window["-IMAGE1-"].UpdateAnimation("loading.gif",time_between_frames=100)
                    window["-IMAGE2-"].UpdateAnimation("loading.gif",time_between_frames=100)
                    window["-IMAGE3-"].UpdateAnimation("loading.gif",time_between_frames=100)
                    response = requests.get(url, headers=headers)
                    print(response.status_code)
                    window['-OUTPUT-'].update(value=outstr+str(response.status_code))
                    if response.status_code == 200 and response.json()['status'] == 'succeeded':
                        print(response.json())
                        window['-OUTPUT-'].update(value=outstr+str(response.json()))
                        urls = response.json()['output']
                        id = 0
                        for url in urls:
                            response = requests.get(url, stream=True)
                            if response.status_code == 200:
                                img_name="replicate-prediction-"+str(reqId) + ("" if len(urls) == 1 else ("-"+str(id)))+".png"
                                with open(img_name, 'wb') as f:
                                    response.raw.decode_content = True
                                    shutil.copyfileobj(response.raw, f)
                                    print('Image Downloaded Successfully')
                                    window['-OUTPUT-'].update(value='Image Downloaded Successfully')
                                    im = Image.open(img_name)
                                    image=ImageTk.PhotoImage(im)
                                    window["-IMAGE"+str(id)+"-"].Update(data=image)
                            id = id+1
                        exit(0)
            else:
                window['-OUTPUT-'].update(value="Error: " + str(response.status_code) + "\n" + str(response.json())
                print("Error: " + str(response.status_code) + "\n" + str(response.json()))
                break
    window.close()

if __name__ == "__main__":
    main()