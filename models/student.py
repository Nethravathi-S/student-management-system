from datetime import datetime
import json

class Student:
    def __init__(self, student_id, name, age, grade, email, phone, address=""):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = grade
        self.email = email
        self.phone = phone
        self.address = address
        self.enrollment_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.is_active = True
    
    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "grade": self.grade,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "enrollment_date": self.enrollment_date,
            "is_active": self.is_active
        }
    
    @classmethod
    def from_dict(cls, data):
        student = cls(
            data["student_id"],
            data["name"],
            data["age"],
            data["grade"],
            data["email"],
            data["phone"],
            data.get("address", "")
        )
        student.enrollment_date = data.get("enrollment_date", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        student.is_active = data.get("is_active", True)
        return student
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ["student_id", "enrollment_date"]:
                setattr(self, key, value)
    
    def __str__(self):
        return f"{self.student_id}: {self.name} (Grade: {self.grade})"
    
    def __repr__(self):
        return f"Student(id={self.student_id}, name={self.name})"
