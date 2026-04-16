======================================================
      ClariCare v2 - AI Health Guidance Platform
                 Run Instructions
======================================================

Follow these steps to run the ClariCare application on your Windows machine.

--- Prerequisites ---
Make sure you have Python 3.9+ installed on your system.

--- Step 1: Open Terminal ---
Open PowerShell or Command Prompt and navigate to the project ROOT directory the overarching 'clariCare' folder:
> cd path\to\clariCare

--- Step 2: Set up Virtual Environment ---
It is highly recommended to use a virtual environment to keep dependencies isolated.

1. Create the virtual environment (if not already created):
> python -m venv venv

2. Activate the virtual environment:
> .\venv\Scripts\activate

***(Troubleshooting for Windows users: If you see a red error saying "running scripts is disabled on this system" in PowerShell, this is a built-in security policy. To easily bypass this, simply type `cmd` and press Enter to switch your terminal to Command Prompt, then try running `.\venv\Scripts\activate` again).***

3. Install all required dependencies from the 'code' directory:
> pip install -r code\requirements.txt

*(Note: PyTorch and Transformers are required for the AI NLP engine. This installation may take a few minutes).*

--- Step 3: Run the Backend Server ---
The entire application (both frontend and backend API) is served via a FastAPI server.

Navigate to the deployment directory and run the application:
> cd deployment
> python app.py

The application will now start. 
Wait until you see "Application startup complete." and "Uvicorn running on http://0.0.0.0:8000" in the terminal output. 
During the first run, the system may download NLP components securely (like BioBERT models or NLTK stopwords).

--- Step 4: Access the Application ---
Open your web browser and go to the landing page:
🌐 http://localhost:8000

Other Direct URLs available in v2:
💬 Chatbot: http://localhost:8000/chat
🩻 Symptom Explorer: http://localhost:8000/explore
ℹ️ About / Tech Stack: http://localhost:8000/about

(Note: You do not need to start a separate frontend server. The FastAPI backend automatically serves all HTML, CSS, and JS files).

--- Stopping the Server ---
To stop the server, go to your terminal window and press CTRL + C. 
To exit the Python virtual environment, type:
> deactivate
