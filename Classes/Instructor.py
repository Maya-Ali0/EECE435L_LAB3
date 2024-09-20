from .Person import Person
import json
import os 

class Instructor(Person):

    def __init__(self, name, age, email, instructor_id, assigned_courses=None):
        super().__init__(name, age, email)
        self.instructor_id = self.validate_instructor_id(instructor_id)
        self.assigned_courses = self.validate_list(assigned_courses if assigned_courses is not None else [])



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
        
        return {instructor['instructor_id'] for instructor in data}
    
    
    def validate_instructor_id(self, instructor_id):
        if not isinstance(instructor_id, str):
            raise ValueError("Invalid ID")
        return instructor_id

    def validate_list(self, assigned_courses):
        if isinstance(assigned_courses, list):
            return self.validate_courses(assigned_courses)
        else:
            raise ValueError("Not a list")

    def validate_courses(self, courses):
        return courses

    def assign_course(self, course):
        from Classes.Course import Course
        if not isinstance(course, Course):
            raise ValueError("Wrong type of object appended")
        else:

            if course.instructor == None:
              course.instructor = self  
              self.assigned_courses.append(course.course_id)
             
              self.update("./Serialization/Instructor.json")
              course.update("./Serialization/Course.json")
              print(self)
              print(self.load_instructor_by_id(Instructor, "./Serialization/Instructor.json", self.assigned_courses))

            else:
                raise ValueError("Instructor for this course already exists!")



    def to_dict(self):
        """Convert the Instructor object to a dictionary."""
        return {
            'name': self.name,
            'age': self.age,
            'email': self._email,
            'instructor_id': self.instructor_id,
            'assigned_courses': [course for course in self.assigned_courses] if self.assigned_courses else []
        }

    @classmethod
    def from_dict(cls, data):
        from Classes.Course import Course
        """Create an Instructor object from a dictionary."""
        if data != None:
            assigned_courses = [course_data for course_data in data.get('assigned_courses', [])]
            return cls(name=data['name'], age=data['age'], email=data['email'], instructor_id=data['instructor_id'], assigned_courses=assigned_courses)
        else:
            return None
        
    def __str__(self):
        return f"Instructor(Name: {self.name}, Age: {self.age}, Email: {self._email}, Instructor ID: {self.instructor_id}, Courses: {[course_id for course_id in self.assigned_courses]})"

    def save_to_json(self, filename):
        """Save the Instructor object to a JSON file, appending to existing data if present."""
        existing_instructor_ids = self.load_existing_ids(filename)

        if self.instructor_id not in existing_instructor_ids:
            existing_instructor_ids.add(self.instructor_id)
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
            raise ValueError("Instructor ID already in use.")

    @classmethod
    def load_from_json(cls, filename):
        """Load all Instructor objects from a JSON file."""
        instructors = []
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                try:
                    data = json.load(file)
                    if isinstance(data, list):
                        for instructor_data in data:
                            instructors.append(cls.from_dict(instructor_data))
                except json.JSONDecodeError:
                    pass  
        return instructors  

    @staticmethod
    def load_instructor_by_id(cls, filename, instructor_id):
        """Load an Instructor object from a JSON file by instructor ID."""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        for instructor_data in data:
            if instructor_data['instructor_id'] == instructor_id:
                return cls.from_dict(instructor_data) 
        return None
    
    def update(self, filename):
        """Update the Instructor in the JSON file by replacing the old entry with the same instructor_id."""
        try:
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

            updated_data = [instructor for instructor in data if instructor['instructor_id'] != self.instructor_id]

            updated_data.append(self.to_dict())
            
            with open(filename, 'w') as file:
                json.dump(updated_data, file, indent=4)

        except Exception as e:
            raise ValueError(f"An error occurred while updating the course: {str(e)}")
