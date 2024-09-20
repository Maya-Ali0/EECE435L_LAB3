import re
import json

class Person:

    def __init__(self, name, age, email):
        self.name = self.validate_name(name)
        self.age = self.validate_age(age)
        self._email = self.validate_email(email) 

    def validate_name(self, name):
        if not isinstance(name, str):
            raise ValueError("Invalid name")
        return name

    def validate_email(self, email):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")
        return email

    def validate_age(self, age):
        if age < 0:
            raise ValueError("Invalid age")
        return age

    def introduce(self):
        print(f"Hello, I'm {self.name}. I'm {self.age} years old.")

    def to_dict(self):
        """Convert the Person object to a dictionary."""
        return {
            'name': self.name,
            'age': self.age,
            'email': self._email
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Person object from a dictionary."""
        return cls(name=data['name'], age=data['age'], email=data['email'])

    def save_to_json(self, filename):
        """Save the Person object to a JSON file."""
        with open(filename, 'a') as file:
            json.dump(self.to_dict(), file, indent=4)

    @classmethod
    def load_from_json(cls, filename):
        """Load a Person object from a JSON file."""
        with open(filename, 'r') as file:
            data = json.load(file)
            return cls.from_dict(data)


# person = Person("Alice", 28, "alice@example.com")
# person.save_to_json('./Serialization/Person.json')
# loaded_person = Person.load_from_json('./Serialization/Person.json')
# loaded_person.introduce()
