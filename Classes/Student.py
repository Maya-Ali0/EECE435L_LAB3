from .Person import Person
import json
import os

class Student(Person):
    def __init__(self, name, age, email, student_id, registered_courses=None):
        super().__init__(name, age, email)
        self.student_id = self.validate_student_id(student_id)
        self.registered_courses = self.validate_list(registered_courses if registered_courses is not None else [])


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
        
        return {student['student_id'] for student in data}
    
    
    def validate_courses(self, courses):
        from .Course import Course  
        for course in courses:
            if not isinstance(course, Course):
                raise ValueError("Not a course")
        return courses

    def validate_student_id(self, student_id):
        if not isinstance(student_id, str):
            raise ValueError("Invalid ID")
        return student_id

    def validate_list(self, registered_courses):
        if isinstance(registered_courses, list):
            return self.validate_courses(registered_courses)
        else:
            raise ValueError("Not a list")

    def register_course(self, course):
        from .Course import Course  
        if not isinstance(course, Course):
            raise ValueError("Wrong type of object appended")
        else:
            course.add_student(self)

        self.registered_courses.append(course.course_id)
        self.update("./Serialization/Student.json")
        course.update("./Serialization/Course.json")

    def to_dict(self):
        """Convert the Student object to a dictionary."""
        return {
            'name': self.name,
            'age': self.age,
            'email': self._email,
            'student_id': self.student_id,
            'registered_courses': [course for course in self.registered_courses] if self.registered_courses else []
        }

    @classmethod
    def from_dict(cls, data):
        from .Course import Course  
        """Create a Student object from a dictionary."""
        registered_courses = [Course.course_id for course_data in data.get('registered_courses', [])]
        return cls(name=data['name'], age=data['age'], email=data['email'], student_id=data['student_id'], registered_courses=registered_courses)


    def __str__(self):
        """Return a string representation of the Student object."""
        course_list = ', '.join([course.course_id for course in self.registered_courses]) if self.registered_courses else 'No courses registered'
        return f"Student(Name: {self.name}, Age: {self.age}, Email: {self._email}, Student ID: {self.student_id}, Registered Courses: [{course_list}])"


    def save_to_json(self, filename):
        """Save the Student object to a JSON file, appending to existing data if present."""
        existing_student_ids = self.load_existing_ids(filename)

        if self.student_id not in existing_student_ids: 
            existing_student_ids.add(self.student_id)
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
            raise ValueError("Student already exists!")
            

    @classmethod
    def load_from_json(cls, filename):
        """Load a Student object from a JSON file."""
        students = []
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                try:
                    data = json.load(file)
                    if isinstance(data, list):
                        for instructor_data in data:
                            students.append(cls.from_dict(instructor_data))
                except json.JSONDecodeError:
                    pass  
        return students


    @staticmethod
    def load_student_by_id(cls, filename, student_id):
        with open(filename, 'r') as f:
            data = json.load(f)
        for student_data in data:
            if student_data['student_id'] == student_id:
                return cls.from_dict(student_data)
        return None

    
    def update(self, filename):
        """Update an existing student in the JSON file and synchronize the student ID set."""
        existing_student_ids =  self.load_existing_ids(filename)

        if self.student_id not in existing_student_ids:
             raise ValueError("Student ID not found!")

        if os.path.exists(filename):
            with open(filename, 'r') as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = []
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        for i, student_data in enumerate(data):
            if student_data['student_id'] == self.student_id:
                data[i] = self.to_dict()
                break

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
  