# Student Placement System (Flask + MySQL)

This is a ready-to-run starter project for a Student Placement Record System using:
- Flask (Python)
- MySQL (SQLAlchemy + PyMySQL)
- Bootstrap 5 for simple UI

## How to use (Windows / PowerShell)

1. Open PowerShell and navigate to the `backend` folder:
   ```
   cd student-placement-system/backend
   ```
2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create the database using the SQL file in `database/placement_schema.sql` (use MySQL Workbench or CLI).
5. Copy `.env.example` to `.env` and update values (SECRET_KEY, DATABASE_URI).
6. Run the app:
   ```
   python app.py
   ```
7. Visit http://127.0.0.1:5000 in your browser.
