# Replicate AI Images SDXL python desktop app frontend

This project is a Python application that interacts with the Replicate AI API to generate images using a given prompt and seed. It utilizes the PySimpleGUI library for creating a user interface, as well as the requests library for making API calls and the Pillow library (PIL) for handling images.

## Getting Started

1. Clone this repository to your local machine.

```
git clone https://github.com/Scavix/replicate-sdxl-python-desktop-interface.git
cd replicate-sdxl-python-desktop-interface
```

2. Install the required dependencies. Make sure you have Python and pip installed.

```
pip install -r requirements.txt
```
3.  Obtain an API key from Replicate AI (the GUI allows you to save it locally)

## Usage
Run the main.py script to start the application.

```
python main.py
```

1. The application window will appear, allowing you to input the prompt, seed, number of images, and API token.

2. If you want to save the API key for future use, check the "Save KEY" checkbox.

3. Click the "Ok" button to start generating images based on the provided input.

4. The application will display a loading animation while waiting for the API response. Once the response is received and the images are generated, they will be displayed in the interface.

5. If the API response indicates an error, an error message will be displayed, and the process will terminate.

## GUI Screenshot
<p align="center">
  <img src="https://github.com/Scavix/replicate-sdxl-python-desktop-interface/blob/main/screenshot.PNG" />
</p>

## License
This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/) .

Feel free to modify and enhance the project as needed. If you encounter any issues or have questions, please don't hesitate to open an issue on this repository.
