from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from services.student_service import StudentService

app = FastAPI(title="Student Management System API")
service = StudentService()

class StudentCreate(BaseModel):
    name: str
    age: int
    grade: str
    email: str
    phone: str
    address: Optional[str] = ""

@app.get("/")
def root():
    return {
        "message": "Student Management System API",
        "status": "running",
        "endpoints": [
            "GET / - API Info",
            "GET /students - List all students",
            "POST /students - Add new student",
            "GET /students/{id} - Get student by ID",
            "PUT /students/{id} - Update student",
            "DELETE /students/{id} - Delete student",
            "GET /statistics - Get statistics"
        ]
    }

@app.get("/students")
def list_students():
    students = service.get_all_students()
    active_students = [s.to_dict() for s in students if s.is_active]
    return {
        "count": len(active_students),
        "students": active_students
    }

@app.post("/students")
def create_student(student: StudentCreate):
    try:
        result = service.add_student(
            student.name, student.age, student.grade,
            student.email, student.phone, student.address
        )
        return {"success": True, "student": result.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/statistics")
def get_statistics():
    return service.get_statistics()
