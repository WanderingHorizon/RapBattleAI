# 🎤 RapBattleAI
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)

Rap against some of the biggest rapping titans in the world: Eminem, Jay-Z, Nas, Kendrick, and Drake.

These AIs have been trained on songs from each artist and told specifically to match the artists' style. After some testing, it is not perfect, but then again, it is only v1.

> **Note:** This project is provided as-is and **will NOT be updated**.

---

## Instructions for Setup

Follow these steps carefully to get the application running on your local machine.

### Step 1: Get the Project Files

Place all the project files (`app.py`, `index.html`, `style.css`, `main.js`, etc.) into a single project folder on your computer (e.g., `ai-rap-battle`).

### Step 2: Verify Folder Structure

For the application to work, your files **must** be organized in this exact folder structure. Pay close attention to the `static` and `templates` folders.

```
/ai-rap-battle/
|
├── app.py
├── requirements.txt
├── .env
|
├── eminem.txt
├── jayz.txt
├── kendricklamar.txt
├── nas.txt
├── drake.txt
|
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js   <-- Note: The JS file is named main.js
|
└── templates/
    └── index.html
```

### Step 3: Create the `requirements.txt` File

In your main project folder, create a file named `requirements.txt` and add the following lines. This file tells Python which packages to install.

```txt
Flask
groq
python-dotenv
```

### Step 4: Create a Virtual Environment

Using a virtual environment is highly recommended to keep project dependencies isolated. Open your terminal or command prompt in the project folder and run:

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```
> You'll know it's active when you see `(venv)` at the beginning of your terminal prompt.

### Step 5: Install Dependencies

With your virtual environment active, run the following command to install the packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Step 6: Set Up Your API Key

The AI requires a secret API key from Groq to function.

1.  In the main project folder, create a new file named exactly `.env`
2.  Open the `.env` file and add your Groq API key in the following format:

    ```
    GROQ_API_KEY="YOUR_SECRET_GROQ_API_KEY_HERE"
    ```
> **IMPORTANT:** Never share this file or commit it to a public repository.

### Step 7: Add Rapper Training Data (CRITICAL)

The AI's personality is defined by the lyrics you provide. You **must** create the five `.txt` files listed in the folder structure above.

For each file (`eminem.txt`, `jayz.txt`, etc.), paste in a large collection of that rapper's lyrics. The more lyrics you provide, the better the AI will be at capturing their style.

---

## How to Run the Application

Once all the setup steps are complete:

1.  Make sure your virtual environment is still active (you should see `(venv)` in your prompt).
2.  Run the Flask application from your terminal:
    ```bash
    python app.py
    ```
3.  The terminal will show that the server is running, usually on port 5001.
    ```
     * Running on http://127.0.0.1:5001
    ```
4.  Open your web browser and go to the following address:
    **[http://127.0.0.1:5001](http://127.0.0.1:5001)**

The AI Rap Battle Room should now be live.
