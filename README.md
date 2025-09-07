Campus Event Reporting — Prototype

Project overview:
The system is designed in such a way that only admins can create events. Student of any college can register and can take part in the event. The attendance of the registered student will be monitored. The registered student can give feedback for the event registered. The system gives the report of the attendance percentage, event popularity, student participation, and top active students.

Technology used:
- backend: FastAPI (Python)
- Database: SQLite
- API docs: Swagger

Quick setup (copy and run):
Create the same folder structure and copy the code. 

Commands you can paste in terminal:

 create & activate virtual environment (optional but recommended) :-

    python -m venv .venv

 mac/linux-

    source .venv/bin/activate

 windows-

    .venv\Scripts\activate

 install dependencies
    pip install -r requirements.txt

 initialize the database with sample data
    python -c "from app.init_db import main as init; init()"

 run the server
    uvicorn app.main:app --reload
open: http://127.0.0.1:8000/docs (ctrl+click on this in your terminal)

How to test (example): 
 1. Create student: Select content type as application/json.
    in edit value type: {"college_id":1,"name":"Akshata","email":"xyz@example.com"}
    or
    in terminal (bash): curl -X POST "http://127.0.0.1:8000/students" -H "Content-Type: application/json" \
                         -d '{"college_id":1,"name":"Akshata","email":"xyz@example.com"}'

 2. Create event (bash): curl -X POST "http://127.0.0.1:8000/events" -H "Content-Type: application/json" \
                          -d '{"college_id":1,"title":"AI Workshop","type":"Workshop","start_at":"2025-09-10 10:00","end_at":"2025-09-10 12:00","capacity":100}'

 3. Register (bash): curl -X POST "http://127.0.0.1:8000/events/1/register" -H "Content-Type: application/json" \
                      -d '{"student_id":1}'

 4. Check-in (bash): curl -X POST "http://127.0.0.1:8000/events/1/attendance/checkin" -H "Content-Type: application/json" \-d '{"student_id":1}'

 5. Feedback (bash): curl -X POST "http://127.0.0.1:8000/events/1/feedback" -H "Content-Type: application/json" \
                      -d '{"student_id":1,"rating":5,"comment":"Great session!"}'

 6. Reports:
  GET /reports/event-popularity
  GET /reports/student-participation/{student_id}
  GET /reports/top-students?limit=3
  GET /reports/events?type=Workshop

Project structure:
  app/ -> FastAPI code (main.py, db.py, init_db.py)

  requirements.txt -> Python dependencies

  design_doc.pdf -> ER Diagram + workflows + assumptions

  Approach_Webknot_Akshata.pdf -> Approach & AI log

  reports_screenshots/ -> JSON-screenshots collected from Postman

  ai_log/ -> AI chat screenshots

  lovable_ui/ ->  Screenshots of UI designed.

Design:
  Used SQLite for prototype (easy setup).

  Used integer autoincrement IDs for simplicity.

  Kept feedback only for registered students.

  Reports are SQL-based for transparency and reproducibility.

UI designed: A add-on UI is designed with the help of lovable- https://eventful-campus-ui.lovable.app/ 

Future improvements: 
  Add authentication & role-based access (admin/student)

  Use Postgres and migrations
  
  Build a small front-end and integrate with APIs


