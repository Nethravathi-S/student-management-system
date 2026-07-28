from typing import List, Optional, Dict
from models.student import Student
from utils.file_handler import FileHandler

class StudentService:
    def __init__(self):
        self.file_handler = FileHandler()
        self.data = self.file_handler.read_data()
        self.students = self._load_students()
    
    def _load_students(self) -> List[Student]:
        return [Student.from_dict(s) for s in self.data.get("students", [])]
    
    def _save_students(self):
        self.data["students"] = [s.to_dict() for s in self.students]
        self.file_handler.write_data(self.data)
    
    def add_student(self, name: str, age: int, grade: str, email: str, phone: str, address: str = "") -> Student:
        try:
            if not name or not age or not grade or not email or not phone:
                raise ValueError("All fields except address are required")
            
            if age < 1 or age > 120:
                raise ValueError("Age must be between 1 and 120")
            
            new_id = self.data.get("last_id", 0) + 1
            self.data["last_id"] = new_id
            
            student = Student(str(new_id), name, age, grade, email, phone, address)
            self.students.append(student)
            self._save_students()
            return student
            
        except Exception as e:
            print(f"Error adding student: {e}")
            raise
    
    def get_all_students(self) -> List[Student]:
        return self.students
    
    def get_student_by_id(self, student_id: str) -> Optional[Student]:
        for student in self.students:
            if student.student_id == student_id and student.is_active:
                return student
        return None
    
    def search_students(self, query: str) -> List[Student]:
        query = query.lower()
        results = []
        for student in self.students:
            if student.is_active:
                if (query in student.name.lower() or 
                    query in student.email.lower() or 
                    query in student.phone):
                    results.append(student)
        return results
    
    def update_student(self, student_id: str, **kwargs) -> Optional[Student]:
        student = self.get_student_by_id(student_id)
        if not student:
            raise ValueError(f"Student with ID {student_id} not found")
        
        if "age" in kwargs and (kwargs["age"] < 1 or kwargs["age"] > 120):
            raise ValueError("Age must be between 1 and 120")
        
        student.update(**kwargs)
        self._save_students()
        return student
    
    def delete_student(self, student_id: str, permanent: bool = False) -> bool:
        student = self.get_student_by_id(student_id)
        if not student:
            raise ValueError(f"Student with ID {student_id} not found")
        
        if permanent:
            self.students = [s for s in self.students if s.student_id != student_id]
        else:
            student.is_active = False
        
        self._save_students()
        return True
    
    def restore_student(self, student_id: str) -> Optional[Student]:
        for student in self.students:
            if student.student_id == student_id and not student.is_active:
                student.is_active = True
                self._save_students()
                return student
        return None
    
    def get_statistics(self) -> Dict:
        total = len([s for s in self.students if s.is_active])
        total_all = len(self.students)
        
        grades = {}
        for student in self.students:
            if student.is_active:
                grade = student.grade.upper()
                grades[grade] = grades.get(grade, 0) + 1
        
        ages = [s.age for s in self.students if s.is_active]
        avg_age = sum(ages) / len(ages) if ages else 0
        
        return {
            "total_active": total,
            "total_all": total_all,
            "grade_distribution": grades,
            "average_age": round(avg_age, 1),
            "inactive_count": total_all - total
        }
