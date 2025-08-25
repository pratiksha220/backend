### Blink Tracker Backend and Dashboard

A backend API for the Blink Tracker application, providing authentication, data handling, and syncing capabilities. Built with FastAPI and deployed on Railway.

---

##  Tech Stack

- **Python 3.10**
- **FastAPI** – For building RESTful API endpoints
- **SQLAlchemy** – ORM for database interactions
- **SQLite / PostgreSQL** – Database (SQLite for local dev; PostgreSQL on production via Railway)
- **JWT Authentication** – Secures login/register endpoints
- **Railway** – Deployment platform for backend API and database
- **React.js** – Frontend dashboard interface (if included in the `frontend/` folder)
- **Procfile** & **runtime.txt** – Support configuration for deployment on Railway or Heroku-like environments

---

##  Installation & Development

```bash
git clone https://github.com/pratiksha220/Blink_Tracker_Backend.git
cd Blink_Tracker_Backend
python -m venv venv

pip install -r requirements.txt
```
---

##  Deployment

-  railway.json — contains Railway-specific configuration
-  runtime.txt — defines the Python version environment
-  Procfile — defines the startup command:

```
web: uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
```
---
##  Notes on Functionality

-  auth.py handles user authentication and generates JWT tokens.
-  crud.py provides functions for creating, reading, updating, and deleting blink data.
-  models.py defines the data structures, such as User and BlinkRecord.
-  database.py sets up the connection to the SQLite/PostgreSQL database.
-  frontend/ directory (if present) houses a React dashboard for frontend visualization
---
##  Credits

-  Developed as the backend for Blink Tracker — part of a complete system combining PyQt6 frontend, MediaPipe detection, and FastAPI backend deployed on Railway.
