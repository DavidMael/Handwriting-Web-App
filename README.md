# Handwriting-Web-App

This web app lets the user write by hand in their browser and reads the text from the produced image. The frontend handling the writing input is written in JavaScript, using the React.js library. The backend where the character recognition runs is written in Python, and uses the Flask and TensorFlow libraries.

The neural netowork that performs the character recognition is trained on the EMNIST dataset.

## Running the Application

Running the web app requires the aformentioned languages and libraries, the flask_restful and dotenv Python libraries, and npm.

To train the model, run `backend/model/train_model_letters.py`
To start the backend, start a new virtual environment with `py -3 -m venv venv`, then start the server with `backend/python backend.py`.
To start the frontend, run `writing-frontend/npm start`.

In the browser window that opens, the portion of the screen below the text line can be drawn in with the cursor. The buttons above wipe the drawn content, download it as a PNG, and send it to the server for processing.

## Example Screenshot

![Application reading the words "HELLO", "WORLD", "ABC", and "X"](https://github.com/DavidMael/Handwriting-Web-App/blob/main/uiScreenshot2.png "Example Screenshot")
Example of the application reading separated words on different lines.