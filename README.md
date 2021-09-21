# Handwriting-Web-App

This web app lets the user write by hand in their browser and reads the text from the produced image. The frontend handling the writing input is written in JavaScript, using the React.js library. The backend where the character recognition runs is written in Python, and uses the Flask and TensorFlow libraries.

## Running the Application

Running the web app requires the aformentioned languages and libraries, the flask_restful and dotenv Python libraries, and npm.

To start the backend, start a new virtual environment with `py -3 -m venv venv`, then start the server in `/backend` with `python backend.py`.
To start the frontend, run `npm start` in /writing-frontend.

In the browser window that opens, the portion of the screen below the text line can be drawn in with the cursor. The buttons above wipe the drawn content, download it as a PNG, and send it to the server for processing.