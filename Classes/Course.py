from .Instructor import Instructor
from .Student import Student
import json
import os

class Course:
    def __init__(self, course_id, course_name, instructor, enrolled_students=None):
        self.course_id = self.validate_course_id(course_id)
        self.course_name = self.validate_course_name(course_name)
        self.instructor = self.validate_instructor(instructor)
        self.enrolled_students = self.validate_list(enrolled_students if enrolled_students is not None else [])


    @classmethod
    def load_existing_ids(cls, filename):
        try:
            with open(filename, 'r') as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = []
                except json.JSONDecodeError:
                    data = []
        except FileNotFoundError:
            data = []
        
        return {course['course_id'] for course in data}
    
    def add_student(self, student_id):
        
        self.enrolled_students.append(student_id.student_id)
        self.update('./Serialization/Course.JSON')
        student_id.update('./Serialization/Student.JSON')



    def validate_list(self, enrolled_students):
        if isinstance(enrolled_students, list):
            return enrolled_students
        else:
            raise ValueError("Not a list")

    def validate_course_id(self, course_id):
        if not isinstance(course_id, str):
            raise ValueError("Invalid ID")
        return course_id

    def validate_course_name(self, course_name):
        if not isinstance(course_name, str):
            raise ValueError("Invalid name")
        return course_name

    def validate_instructor(self, instructor):
        return instructor

    # def validate_students(self, students):
    #     for student in students:
    #         if not isinstance(student, Student):
    #             raise ValueError("Not a student")
    #     return students

    def to_dict(self):
        """Convert the Course object to a dictionary."""
        if self.instructor is not None:
            return {
                'course_id': self.course_id,
                'course_name': self.course_name,
                'instructor': self.instructor.to_dict(),
                'enrolled_students': [student for student in self.enrolled_students] if self.enrolled_students else []
            }
        else:
            return {
                'course_id': self.course_id,
                'course_name': self.course_name,
                'instructor': None,
                'enrolled_students': [student for student in self.enrolled_students] if self.enrolled_students else []
            }

    @classmethod
    def from_dict(cls, data):
        """Create a Course object from a dictionary."""
        from .Instructor import Instructor
        from .Student import Student
        instructor = Instructor.from_dict(data['instructor']) if 'instructor' in data else None
        enrolled_students_ids = data.get('enrolled_students', [])
        
        return cls(
            course_id=data['course_id'],
            course_name=data['course_name'],
            instructor=instructor,
            enrolled_students=enrolled_students_ids 
        )

    def __str__(self):
        """Return a string representation of the Course object."""
        instructor_info = f"Instructor: {self.instructor.name} (Email: {self.instructor._email})" if self.instructor else "No instructor assigned"
        student_list = ', '.join([student.student_id for student in self.enrolled_students]) if self.enrolled_students else "No students enrolled"
        return f"Course(ID: {self.course_id}, Name: {self.course_name}, {instructor_info}, Enrolled Students: [{student_list}])"

    def save_to_json(self, filename):
        """Save the Course object to a JSON file, appending to existing data if present."""
        existing_course_ids = self.load_existing_ids(filename)
        if self.course_id not in existing_course_ids:
            existing_course_ids.add(self.course_id)
            if os.path.exists(filename):
                with open(filename, 'r') as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
            else:
                data = []
            data.append(self.to_dict())

            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
        else: 
            raise ValueError("Course already exists!")

    @classmethod
    def load_from_json(cls, filename):
        """Load a Course object from a JSON file."""
        courses = []
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                try:
                    data = json.load(file)
                    if isinstance(data, list):
                        for instructor_data in data:
                            courses.append(cls.from_dict(instructor_data))
                except json.JSONDecodeError:
                    pass  
        return courses


    @staticmethod
    def load_course_by_id(cls, filename, course_id):
        with open(filename, 'r') as f:
            data = json.load(f)
        for course_data in data:
            if course_data['course_id'] == course_id:
                return cls.from_dict(course_data)
        return None
    
    def update(self, filename):
        """Update the course in the JSON file by replacing the old entry with the same course_id."""
        try:
            # Step 1: Load existing courses
            if os.path.exists(filename):
                with open(filename, 'r') as file:
                    try:
                        data = json.load(file)
                        if not isinstance(data, list):
                            data = []
                    except json.JSONDecodeError:
                        data = []
            else:
                data = []

            # Step 2: Remove the old course if it exists
            updated_data = [course for course in data if course['course_id'] != self.course_id]

            # Step 3: Add the updated course
            updated_data.append(self.to_dict())

            # Step 4: Write the updated data back to the file
            with open(filename, 'w') as file:
                json.dump(updated_data, file, indent=4)

        except Exception as e:
            raise ValueError(f"An error occurred while updating the course: {str(e)}")
