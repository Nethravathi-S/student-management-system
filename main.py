import sys
from services.student_service import StudentService

class StudentManagementSystem:
    def __init__(self):
        self.service = StudentService()
        self.running = True
    
    def display_menu(self):
        print("\n" + "="*50)
        print("     STUDENT MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Add New Student")
        print("2. View All Students")
        print("3. Search Students")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Restore Student")
        print("7. View Statistics")
        print("8. Exit")
        print("="*50)
    
    def add_student_ui(self):
        print("\n--- ADD NEW STUDENT ---")
        try:
            name = input("Name: ").strip()
            age = int(input("Age: ").strip())
            grade = input("Grade (e.g., A, B, C): ").strip().upper()
            email = input("Email: ").strip()
            phone = input("Phone: ").strip()
            address = input("Address (optional): ").strip()
            
            student = self.service.add_student(name, age, grade, email, phone, address)
            print(f"\n✓ Student added successfully! ID: {student.student_id}")
            
        except ValueError as e:
            print(f"\n✗ Error: {e}")
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")
    
    def view_all_students_ui(self):
        print("\n--- ALL STUDENTS ---")
        students = self.service.get_all_students()
        active_students = [s for s in students if s.is_active]
        
        if not active_students:
            print("No active students found.")
            return
        
        print(f"\nTotal: {len(active_students)} students\n")
        print("ID    Name                  Age  Grade  Email                    Phone")
        print("-" * 80)
        
        for student in active_students:
            print(f"{student.student_id:4}  {student.name:20}  {student.age:3}   {student.grade:2}    {student.email:25}  {student.phone}")
    
    def search_students_ui(self):
        print("\n--- SEARCH STUDENTS ---")
        query = input("Enter search term (name, email, or phone): ").strip()
        
        if not query:
            print("Search term cannot be empty.")
            return
        
        results = self.service.search_students(query)
        
        if not results:
            print(f"No students found matching '{query}'")
            return
        
        print(f"\nFound {len(results)} student(s):\n")
        for student in results:
            print(f"ID: {student.student_id} | Name: {student.name} | Grade: {student.grade} | Email: {student.email}")
    
    def update_student_ui(self):
        print("\n--- UPDATE STUDENT ---")
        student_id = input("Enter student ID: ").strip()
        
        if not student_id:
            print("Student ID cannot be empty.")
            return
        
        student = self.service.get_student_by_id(student_id)
        if not student:
            print(f"No active student found with ID: {student_id}")
            return
        
        print(f"\nCurrent details:")
        print(f"Name: {student.name}")
        print(f"Age: {student.age}")
        print(f"Grade: {student.grade}")
        print(f"Email: {student.email}")
        print(f"Phone: {student.phone}")
        print(f"Address: {student.address}")
        
        print("\nEnter new values (press Enter to keep current):")
        updates = {}
        
        name = input(f"Name [{student.name}]: ").strip()
        if name:
            updates["name"] = name
        
        age_input = input(f"Age [{student.age}]: ").strip()
        if age_input:
            try:
                updates["age"] = int(age_input)
            except ValueError:
                print("Invalid age format. Keeping current value.")
        
        grade = input(f"Grade [{student.grade}]: ").strip().upper()
        if grade:
            updates["grade"] = grade
        
        email = input(f"Email [{student.email}]: ").strip()
        if email:
            updates["email"] = email
        
        phone = input(f"Phone [{student.phone}]: ").strip()
        if phone:
            updates["phone"] = phone
        
        address = input(f"Address [{student.address}]: ").strip()
        if address:
            updates["address"] = address
        
        if updates:
            try:
                updated_student = self.service.update_student(student_id, **updates)
                print("\n✓ Student updated successfully!")
            except ValueError as e:
                print(f"\n✗ Error: {e}")
        else:
            print("No changes made.")
    
    def delete_student_ui(self):
        print("\n--- DELETE STUDENT ---")
        student_id = input("Enter student ID to delete: ").strip()
        
        if not student_id:
            print("Student ID cannot be empty.")
            return
        
        student = self.service.get_student_by_id(student_id)
        if not student:
            print(f"No active student found with ID: {student_id}")
            return
        
        print(f"\nStudent to delete:")
        print(f"Name: {student.name}")
        print(f"Grade: {student.grade}")
        print(f"Email: {student.email}")
        
        confirm = input("\nAre you sure you want to delete this student? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Deletion cancelled.")
            return
        
        try:
            self.service.delete_student(student_id, permanent=False)
            print("\n✓ Student deleted successfully (soft delete).")
        except ValueError as e:
            print(f"\n✗ Error: {e}")
    
    def restore_student_ui(self):
        print("\n--- RESTORE STUDENT ---")
        student_id = input("Enter student ID to restore: ").strip()
        
        if not student_id:
            print("Student ID cannot be empty.")
            return
        
        try:
            restored = self.service.restore_student(student_id)
            if restored:
                print(f"\n✓ Student restored successfully!")
                print(f"Name: {restored.name}")
            else:
                print(f"No deleted student found with ID: {student_id}")
        except ValueError as e:
            print(f"\n✗ Error: {e}")
    
    def view_statistics_ui(self):
        print("\n--- STATISTICS ---")
        stats = self.service.get_statistics()
        
        print(f"\nTotal Students (Active): {stats['total_active']}")
        print(f"Total Students (All): {stats['total_all']}")
        print(f"Inactive Students: {stats['inactive_count']}")
        print(f"Average Age: {stats['average_age']} years")
        
        print("\nGrade Distribution:")
        if stats['grade_distribution']:
            for grade, count in sorted(stats['grade_distribution'].items()):
                print(f"  Grade {grade}: {count} student(s)")
        else:
            print("  No data available")
    
    def run(self):
        print("\nWelcome to Student Management System!")
        
        while self.running:
            self.display_menu()
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == '1':
                self.add_student_ui()
            elif choice == '2':
                self.view_all_students_ui()
            elif choice == '3':
                self.search_students_ui()
            elif choice == '4':
                self.update_student_ui()
            elif choice == '5':
                self.delete_student_ui()
            elif choice == '6':
                self.restore_student_ui()
            elif choice == '7':
                self.view_statistics_ui()
            elif choice == '8':
                print("\nThank you for using Student Management System. Goodbye!")
                self.running = False
            else:
                print("\nInvalid choice. Please enter a number between 1 and 8.")

if __name__ == "__main__":
    try:
        app = StudentManagementSystem()
        app.run()
    except KeyboardInterrupt:
        print("\n\nApplication terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)
