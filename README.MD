# IAS Login System

A secure, minimalist login application built with **Python Flask**, **SQLite**, HTML, CSS, and JavaScript.

## Features

- Secure password hashing using Werkzeug (scrypt).
- SQLite database for user accounts.
- CSRF protection using Flask-WTF.
- Login rate limiting (5 attempts per minute).
- Server-side session management.
- Secure HTTP response headers.
- Responsive monochrome user interface.
- Login and logout functionality.
- Flash messages for login feedback.

## Project Structure

```text
IAS-LOGINPAGE/
│
├── login/
│   ├── app.py
│   ├── requirements.txt
│   └── users.db
│
├── templates/
│   ├── login.html
│   └── welcome.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── confetti.js
│
├── .venv/
├── start.sh
└── README.md
```

## Requirements

- Python 3.9 or newer
- Internet access the first time you run the launcher, to install dependencies

## Run on macOS or Windows

Open a terminal in the project folder and run the same launcher. It creates a
`.venv`, installs dependencies when needed, generates a Flask secret key, and
starts the development server.

macOS:

```bash
python3 run.py
```

Windows PowerShell or Command Prompt:

```powershell
py -3 run.py
```

Then open <http://127.0.0.1:5000>. Keep the terminal open while using the app;
press `Ctrl+C` to stop it. The virtual environment is reused on later runs.

## Access the Application

Open your browser and visit:

```text
http://127.0.0.1:5000
```

**Important:** Keep the terminal open while using the application.

To stop the server, press:

```text
CTRL + C
```

## Creating a User Account

Make sure your virtual environment is activated and your Flask secret key is set.

Run:

```bash
python3 -m flask --app login.app create-user
```

Enter the following when prompted:

1. Username
2. Password
3. Confirm password

Password requirements:

- Minimum 12 characters.
- Maximum 1024 characters.
- Username must contain 3–80 characters.
- Allowed username characters: letters, numbers, periods, underscores, and hyphens.

## Database

The application uses SQLite.

Database location:

```text
login/users.db
```

The database automatically initializes when the Flask application starts.

User passwords are stored as secure password hashes, not plain text.

## Security Implementation

| Security Feature | Implementation |
|---|---|
| Password Protection | Werkzeug scrypt hashing |
| CSRF Protection | Flask-WTF |
| Login Rate Limiting | Flask-Limiter |
| Session Security | HTTP-only cookies |
| Session Expiration | 30 minutes |
| Clickjacking Protection | X-Frame-Options |
| MIME Sniffing Protection | X-Content-Type-Options |
| Referrer Protection | Referrer-Policy |
| Database | SQLite |

## Troubleshooting

### Error: No module named Flask

Activate your virtual environment:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python3 -m pip install -r login/requirements.txt
```

### Error: Could not open requirements.txt

Make sure you are inside the main project folder.

Check your current directory:

```bash
pwd
```

Use the correct requirements path:

```bash
python3 -m pip install -r login/requirements.txt
```

### Error: Set FLASK_SECRET_KEY before starting the application

Generate a new key:

```bash
export FLASK_SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_urlsafe(48))')"
```

### Error: TemplateNotFound

Check that your Flask configuration points to the correct folders:

```python
app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)
```

### Port 5000 is already in use

Stop the existing Flask process with `CTRL + C` in its terminal, or use another port:

```bash
python3 -m flask --app login.app run --debug --port 5001
```

## Development Notes

- The `.venv` directory contains isolated Python dependencies.
- The `login/users.db` file stores registered user accounts.
- The `templates` directory contains the HTML pages.
- The `static` directory contains CSS and JavaScript files.
- The `start.sh` script simplifies application startup.

## Important Security Notes

- Never commit `.venv`, `users.db`, or secret keys to a public Git repository.
- Keep `FLASK_SECRET_KEY` private.
- Do not use Flask's debug server for public production hosting.
- Use HTTPS and a production WSGI server when deploying publicly.
- Configure a persistent secret key for production instead of generating a new one every time.

## Author

IAS Login System  
Developed using Python Flask and SQLite.

---

**Project Status:** Local Development  
**Platform:** macOS  
**Framework:** Flask  
**Database:** SQLite  
**Language:** Python, HTML, CSS, JavaScript
