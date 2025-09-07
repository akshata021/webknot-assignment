from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .db import get_connection


app = FastAPI(title="Campus Event Reporting Prototype")

class StudentIn(BaseModel):
    college_id: int
    name: str
    email: str

class EventIn(BaseModel):
    college_id: int
    title: str
    type: str
    start_at: str
    end_at: str
    capacity: int

class RegistrationIn(BaseModel):
    student_id: int

class AttendanceIn(BaseModel):
    student_id: int

class FeedbackIn(BaseModel):
    student_id: int
    rating: int
    comment: str | None = None

@app.post("/students")
def create_student(student: StudentIn):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO students (college_id, name, email) VALUES (?,?,?)", (student.college_id, student.name, student.email))
        conn.commit()
        return {"id": cur.lastrowid, **student.dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@app.post("/events")
def create_event(event: EventIn):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO events (college_id, title, type, start_at, end_at, capacity) VALUES (?,?,?,?,?,?)",
    (event.college_id, event.title, event.type, event.start_at, event.end_at, event.capacity))
    conn.commit()
    return {"id": cur.lastrowid, **event.dict()}

@app.post("/events/{event_id}/register")
def register_student(event_id: int, reg: RegistrationIn):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO registrations (student_id, event_id) VALUES (?,?)", (reg.student_id, event_id))
        conn.commit()
        return {"message": "Registered"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@app.post("/events/{event_id}/attendance/checkin")
def checkin(event_id: int, att: AttendanceIn):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO attendance (student_id, event_id) VALUES (?,?)", (att.student_id, event_id))
        conn.commit()
        return {"message": "Check-in recorded"}
    except Exception as e:
      raise HTTPException(status_code=400, detail=str(e))
    finally:
      conn.close()

@app.post("/events/{event_id}/feedback")
def give_feedback(event_id: int, fb: FeedbackIn):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO feedback (student_id, event_id, rating, comment) VALUES (?,?,?,?)", (fb.student_id, event_id, fb.rating, fb.comment))
        conn.commit()
        return {"message": "Feedback saved"}
    except Exception as e:
      raise HTTPException(status_code=400, detail=str(e))
    finally:
      conn.close()

@app.get("/reports/event-popularity")
def report_event_popularity():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT e.title, COUNT(r.id) as registrations FROM events e LEFT JOIN registrations r ON e.id=r.event_id GROUP BY e.id ORDER BY registrations DESC")
    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return rows


@app.get("/reports/student-participation/{student_id}")
def report_student_participation(student_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT e.title, a.checkin_time FROM attendance a JOIN events e ON a.event_id=e.id WHERE a.student_id=?", (student_id,))
    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return rows


@app.get("/reports/top-students")
def report_top_students(limit: int = 3):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT s.name, COUNT(a.id) as events_attended FROM students s JOIN attendance a ON s.id=a.student_id GROUP BY s.id ORDER BY events_attended DESC LIMIT ?", (limit,))
    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return rows


@app.get("/reports/events")
def report_events_by_type(type: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM events WHERE type=?", (type,))
    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return rows