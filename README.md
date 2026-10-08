# ⏰ Daily Routine & Habit Tracker - College Project

> **A modern, data-driven daily routine and habit management web application built using Python, Streamlit, and SQLite.**

---

## 📌 1. Project Abstract & Objectives

In modern academic and personal life, consistency and time management are critical for students and professionals. Traditional paper-based routine tracking is cumbersome, easily forgotten, and lacks visual progress metrics.

The **Daily Routine & Habit Tracker** is an interactive, local-first web application that allows users to:
1. **Plan & Organize**: Set up recurring daily routines categorized by Study, Fitness, Productivity, and Personal tasks.
2. **Track in Real-Time**: Check off completed tasks with an instant reactive progress bar.
3. **Build Consistency**: Calculate daily streaks and unlock achievement badges based on discipline.
4. **Visualize Performance**: View weekly completion trends and category distributions using analytical charts.
5. **Zero-Configuration Persistence**: Uses an embedded SQLite database requiring no external database server.

---

## 📂 2. Project Directory Structure

```
daily_routine_tracker/
│
├── app.py                 # Main Streamlit web application & UI tabs
├── database.py            # SQLite database manager (CRUD & logs)
├── analytics.py           # Streaks, metrics, and chart computations
├── routine_tracker.db     # SQLite local database (auto-created on first run)
├── requirements.txt       # Python dependencies (Streamlit, Pandas)
├── run_app.bat            # 1-Click launcher script for Windows
└── README.md              # Complete documentation and teacher viva guide
```

---

## 🛠️ 3. Technology Stack

| Component | Technology / Library | Reason for Choice |
|---|---|---|
| **Programming Language** | Python 3.10+ | Clean syntax, robust ecosystem, rapid development |
| **Frontend & UI** | Streamlit | Reactive Python web framework with zero HTML boilerplate |
| **Database** | SQLite3 | Serverless, zero-config, ACID-compliant embedded relational database |
| **Data Processing** | Pandas | Efficient data handling, CSV export, and chart data formatting |

---

## 🗄️ 4. Database Schema

The application uses two relational tables linked via foreign key:

### Table: `routines`
- `id` (INTEGER PRIMARY KEY): Unique identifier.
- `title` (TEXT): Name of the routine/task.
- `category` (TEXT): Grouping (Study, Fitness, Productivity, Personal, etc.).
- `time_slot` (TEXT): Scheduled time (e.g. 09:00 AM).
- `priority` (TEXT): High / Medium / Low.
- `frequency` (TEXT): Daily / Weekdays / Weekends.
- `is_active` (INTEGER): Active status flag (1 or 0).
- `created_at` (TIMESTAMP): Creation time.

### Table: `daily_logs`
- `id` (INTEGER PRIMARY KEY): Unique identifier.
- `routine_id` (INTEGER): References `routines(id)` with cascading delete.
- `log_date` (DATE): Target date (YYYY-MM-DD).
- `completed` (INTEGER): 1 if completed, 0 if pending.
- `completion_time` (TIMESTAMP): Exact time when marked done.
- `notes` (TEXT): Optional reflection or notes.
- *Constraint:* `UNIQUE(routine_id, log_date)` prevents duplicate logs for the same day.

---

## 🚀 5. How to Run the Application

### Method 1: 1-Click Launch (Recommended for Windows)
Simply double-click the **`run_app.bat`** file inside the project folder. It will automatically detect Python, verify requirements, and launch the dashboard in your default web browser!

### Method 2: Manual Terminal Command
Open Command Prompt (cmd) or PowerShell inside the `daily_routine_tracker` directory:

```bash
# Step 1: Install dependencies (one-time only)
py -m pip install -r requirements.txt

# Step 2: Run the Streamlit web application
py -m streamlit run app.py
```

The app will start at: `http://localhost:8501`

---

## 📦 6. How to Submit to Your College Teacher

Follow these simple steps when submitting this project:

1. **Create a Clean ZIP File**:
   - Right-click the `daily_routine_tracker` folder.
   - Select **Send to -> Compressed (zipped) folder** (or use WinRAR / 7-Zip).
   - Name the file: `Daily_Routine_Tracker_<Your_Name>_<Roll_Number>.zip`.

2. **Files to Include in Submission**:
   - ✅ `app.py`
   - ✅ `database.py`
   - ✅ `analytics.py`
   - ✅ `requirements.txt`
   - ✅ `run_app.bat`
   - ✅ `README.md`
   - *(Note: `routine_tracker.db` can be included so the teacher sees sample data immediately!)*

3. **In the Submission Email / Portal**:
   - Mention the Project Title: **Daily Routine & Habit Tracker**.
   - Explain how to run: *"Double-click `run_app.bat` or run `py -m streamlit run app.py`"*.

---

## 🎓 7. Teacher Viva & Oral Presentation Q&A

Here are the most common questions college professors ask and the exact answers you should give:

#### Q1: What problem does your project solve?
> **Answer:** It solves the problem of personal inconsistency and lack of productivity tracking among students. It provides a centralized digital dashboard to schedule routines, view real-time completion progress, maintain streaks, and analyze weekly productivity habits.

#### Q2: Why did you use SQLite instead of MySQL or PostgreSQL?
> **Answer:** SQLite is an embedded, serverless database that stores everything in a single portable file (`routine_tracker.db`). Because this is a desktop/personal web tool, SQLite requires zero setup on the teacher's or user's computer, yet it still provides full relational ACID guarantees and SQL query capabilities.

#### Q3: How does Streamlit handle state and user interactions?
> **Answer:** Streamlit uses an event-driven execution model. When a user clicks a checkbox or submits a form, Streamlit reruns the script top-to-bottom while preserving session state. Our application connects each interaction directly to SQLite database functions to make all changes persistent across refreshes.

#### Q4: How is the streak calculated?
> **Answer:** In `analytics.py`, the `calculate_streaks` function queries the `daily_logs` table for distinct dates where tasks were completed. It sorts these dates and iterates backward from today or yesterday to calculate the consecutive sequence of days with completed routines.

#### Q5: What security or validation checks are implemented?
> **Answer:** We enforce parameterized SQL queries using `?` placeholders across all database queries to prevent SQL Injection attacks. We also validate that required fields (Title, Time Slot) cannot be empty.
