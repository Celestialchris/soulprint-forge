# SoulPrint Developer Setup Guide

Welcome, wanderer. You are about to enter the forge.

This guide will help you run SoulPrint on your local machine.

---

## 🔧 Prerequisites

- Python 3.10+
- Git
- `pip` or `pipx`
- Recommended: virtual environment support (`venv`, `virtualenv`, or `pipenv`)

---

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/Celestialchris/soulprint-forge.git
   cd soulprint-forge
   ```
2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**
    ```bash
   pip install -r requirements.txt
4. **Copy the environment conig**
    ```bash
    cp .env.example .env
5. **Run the application**
    ```bash
   flask run

---

## 💽 Database Notes

- SoulPrint currently uses SQLite for quick bootstrapping.
- Your data is stored locally (unless redirected).
- Uploaded files (Markdown) are stored in /uploads.

---

## 🧭 Project Structure

   ```bash
   soulprint/
   ├── app/
   │   ├── routes.py        # Flask routes
   │   ├── models/          # SQLAlchemy models
   │   ├── templates/       # HTML templates (if used)
   ├── uploads/             # Markdown files go here
   ├── requirements.txt     # Dependencies
   └── run.py               # Entry point
   ```

---

## 🕊️ Philosophical Context

SoulPrint is not just a Flask app — it is a memory sanctum.
Every line of code captures echoes, impressions, and the effort of becoming.

Contribute with clarity. Build with intent.

## 🛠️ Support

If you run into errors, open an issue or contact the forge keeper.

🜂 Welcome to SoulPrint. Shape memory with fire.
