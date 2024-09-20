import sys
import json
import csv
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QFormLayout, QAbstractItemView, QTableWidgetItem, QTableWidget, QTabWidget, QComboBox, QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QStackedWidget
from PyQt5.QtCore import Qt
from Classes.Course import Course
from Classes.Instructor import Instructor
from Classes.Student import Student

class SchoolManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 900, 600)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.central_layout = QVBoxLayout(self.central_widget)
        self.stacked_widget = QStackedWidget()
        self.central_layout.addWidget(self.stacked_widget)

        self.create_menu()

    def create_menu(self):
      """Creates the main menu view"""
      menu_widget = QWidget()
      menu_layout = QVBoxLayout(menu_widget)  

      title_label = QLabel("School Management System", self)
      title_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
      title_label.setAlignment(Qt.AlignCenter) 
      menu_layout.addWidget(title_label)

      button_layout = QVBoxLayout()  

      buttons = [
         ("Add Student", self.show_student_form),
         ("Add Instructor", self.show_instructor_form),
         ("Add Course", self.show_course_form),
         ("Register Student for Course", self.create_registration_form),
         ("Assign Instructor to Course", self.create_instructor_assignment_form),
         ("Display All Records", self.display_all_records),
         ("Search in Records", self.create_search_form),
         ("Export to CSV", self.export_to_csv)  
      ]

      for text, slot in buttons:
         button = QPushButton(text, self)
         button.setFixedSize(200, 50) 
         button.clicked.connect(slot)
         button_layout.addWidget(button)

      button_layout.setAlignment(Qt.AlignCenter) 
      menu_layout.addLayout(button_layout) 

      self.stacked_widget.addWidget(menu_widget)


    def show_student_form(self):
        student_widget = QWidget()
        student_layout = QVBoxLayout(student_widget)
        student_layout.setAlignment(Qt.AlignCenter)  

        title = QLabel("Add Student", self)
        title.setStyleSheet("font-size: 16pt;")
        title.setAlignment(Qt.AlignCenter) 
        student_layout.addWidget(title)

        self.student_name_edit = QLineEdit(self)
        self.student_name_edit.setPlaceholderText("Name")
        self.student_name_edit.setFixedSize(200, 50)  
        student_layout.addWidget(self.student_name_edit)

        self.student_age_edit = QLineEdit(self)
        self.student_age_edit.setPlaceholderText("Age")
        self.student_age_edit.setFixedSize(200, 50)  
        student_layout.addWidget(self.student_age_edit)

        self.student_email_edit = QLineEdit(self)
        self.student_email_edit.setPlaceholderText("Email")
        self.student_email_edit.setFixedSize(200, 50) 
        student_layout.addWidget(self.student_email_edit)

        self.student_id_edit = QLineEdit(self)
        self.student_id_edit.setPlaceholderText("Student ID")
        self.student_id_edit.setFixedSize(200, 50)  
        student_layout.addWidget(self.student_id_edit)

        add_button = QPushButton("Add Student", self)
        add_button.setFixedSize(200, 50) 
        add_button.clicked.connect(self.add_student)
        student_layout.addWidget(add_button)

        back_button = QPushButton("Back to Menu", self)
        back_button.setFixedSize(200, 50)  
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        student_layout.addWidget(back_button)

        self.stacked_widget.addWidget(student_widget)
        self.stacked_widget.setCurrentWidget(student_widget)

    def add_student(self):
        try:
            name = self.student_name_edit.text()
            age = self.student_age_edit.text()
            age_int = int(age)
            email = self.student_email_edit.text()
            student_id = self.student_id_edit.text()

            if not name or not age_int or not email or not student_id:
                raise ValueError("All fields must be filled!")

            student = Student(name, age_int, email, student_id)
            student.save_to_json('./Serialization/Student.json')  
            QMessageBox.information(self, "Success", "Student added successfully!")
            self.stacked_widget.setCurrentIndex(0)  
            
        except ValueError as e:
            QMessageBox.warning(self, "Validation Error", str(e))

    def show_instructor_form(self):
        instructor_widget = QWidget()
        instructor_layout = QVBoxLayout(instructor_widget)
        instructor_layout.setAlignment(Qt.AlignCenter) 

        title = QLabel("Add Instructor", self)
        title.setStyleSheet("font-size: 16pt;")
        title.setAlignment(Qt.AlignCenter)  
        instructor_layout.addWidget(title)

        self.instructor_name_edit = QLineEdit(self)
        self.instructor_name_edit.setPlaceholderText("Name")
        self.instructor_name_edit.setFixedSize(200, 50)  
        instructor_layout.addWidget(self.instructor_name_edit)

        self.instructor_age_edit = QLineEdit(self)
        self.instructor_age_edit.setPlaceholderText("Age")
        self.instructor_age_edit.setFixedSize(200, 50)  
        instructor_layout.addWidget(self.instructor_age_edit)

        self.instructor_email_edit = QLineEdit(self)
        self.instructor_email_edit.setPlaceholderText("Email")
        self.instructor_email_edit.setFixedSize(200, 50) 
        instructor_layout.addWidget(self.instructor_email_edit)

        self.instructor_id_edit = QLineEdit(self)
        self.instructor_id_edit.setPlaceholderText("Instructor ID")
        self.instructor_id_edit.setFixedSize(200, 50) 
        instructor_layout.addWidget(self.instructor_id_edit)

        add_button = QPushButton("Add Instructor", self)
        add_button.setFixedSize(200, 50) 
        add_button.clicked.connect(self.add_instructor)
        instructor_layout.addWidget(add_button)

        back_button = QPushButton("Back to Menu", self)
        back_button.setFixedSize(200, 50) 
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        instructor_layout.addWidget(back_button)

        self.stacked_widget.addWidget(instructor_widget)
        self.stacked_widget.setCurrentWidget(instructor_widget)

    def add_instructor(self):
        try:
            name = self.instructor_name_edit.text()
            age = self.instructor_age_edit.text()
            age_int = int(age)
            email = self.instructor_email_edit.text()
            instructor_id = self.instructor_id_edit.text()

            if not name or not age or not email or not instructor_id:
                raise ValueError("All fields must be filled!")

            instructor = Instructor(name, age_int, email, instructor_id)
            instructor.save_to_json('./Serialization/Instructor.json')
            QMessageBox.information(self, "Success", "Instructor added successfully!")
            self.stacked_widget.setCurrentIndex(0)  

        except ValueError as e:
            QMessageBox.warning(self, "Validation Error", str(e))

    def show_course_form(self):
        course_widget = QWidget()
        course_layout = QVBoxLayout(course_widget)
        course_layout.setAlignment(Qt.AlignCenter)  

        title = QLabel("Add Course", self)
        title.setStyleSheet("font-size: 16pt;")
        title.setAlignment(Qt.AlignCenter)  
        course_layout.addWidget(title)

        self.course_id_edit = QLineEdit(self)
        self.course_id_edit.setPlaceholderText("Course ID")
        self.course_id_edit.setFixedSize(200, 50)  
        course_layout.addWidget(self.course_id_edit)

        self.course_name_edit = QLineEdit(self)
        self.course_name_edit.setPlaceholderText("Course Name")
        self.course_name_edit.setFixedSize(200, 50)  
        course_layout.addWidget(self.course_name_edit)

        add_button = QPushButton("Add Course", self)
        add_button.setFixedSize(200, 50)  
        add_button.clicked.connect(self.add_course)
        course_layout.addWidget(add_button)

        back_button = QPushButton("Back to Menu", self)
        back_button.setFixedSize(200, 50)  
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        course_layout.addWidget(back_button)

        self.stacked_widget.addWidget(course_widget)
        self.stacked_widget.setCurrentWidget(course_widget)

    def add_course(self):
        try:
            course_id = self.course_id_edit.text()
            course_name = self.course_name_edit.text()

            if not course_id or not course_name:
                raise ValueError("All fields must be filled!")

            course = Course(course_id, course_name, None)
            course.save_to_json('./Serialization/Course.json')
            QMessageBox.information(self, "Success", "Course added successfully!")
            self.stacked_widget.setCurrentIndex(0)  

        except ValueError as e:
            QMessageBox.warning(self, "Validation Error", str(e))

    def load_courses(self):
        """Loads available courses from a JSON file."""
        try:
            with open('./Serialization/Course.json', 'r') as file:
                courses_data = json.load(file)
            courses = [course['course_id'] for course in courses_data]
            return courses
        except FileNotFoundError:
            return []
        
    def search_course_by_id(self, course_id):
        """Search for a course by its ID and return the course object."""
        courses = Course.load_from_json('./Serialization/Course.JSON')
        for course in courses:
            if course.course_id == course_id:
                return course
        return None

    def search_student_by_id(self, student_id):
        students = Student.load_from_json('./Serialization/Student.JSON')
        for student in students:
            if student.student_id == student_id:
                return student
        return None
    
    def create_registration_form(self):
      registration_widget = QWidget()
      registration_layout = QVBoxLayout(registration_widget)
      registration_layout.setAlignment(Qt.AlignCenter)

      title = QLabel("Register Student for Course", self)
      title.setStyleSheet("font-size: 16pt;")
      title.setAlignment(Qt.AlignCenter)
      registration_layout.addWidget(title)

      self.student_id_edit = QLineEdit(self)
      self.student_id_edit.setPlaceholderText("Student ID")
      self.student_id_edit.setFixedSize(200, 50)
      registration_layout.addWidget(self.student_id_edit)

      available_courses = self.load_courses()
      self.course_dropdown = QComboBox(self)
      self.course_dropdown.addItems(available_courses)
      self.course_dropdown.setFixedSize(200, 50)
      registration_layout.addWidget(self.course_dropdown)

      register_button = QPushButton("Register", self)
      register_button.setFixedSize(200, 50)
      register_button.clicked.connect(self.register_student_for_course)
      registration_layout.addWidget(register_button)

      back_button = QPushButton("Back to Menu", self)
      back_button.setFixedSize(200, 50)
      back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
      registration_layout.addWidget(back_button)

      self.stacked_widget.addWidget(registration_widget)
      self.stacked_widget.setCurrentWidget(registration_widget)

    def register_student_for_course(self):
      student_id = self.student_id_edit.text()
      selected_course = self.course_dropdown.currentText()

      if not student_id or not selected_course:
         QMessageBox.warning(self, "Error", "Both Student ID and Course must be selected!")
         return

      try:
         student = self.search_student_by_id(student_id)
         course = self.search_course_by_id(selected_course)

         if student_id in course.enrolled_students:
               raise ValueError("Student already enrolled.")

         course.add_student(student)
         QMessageBox.information(self, "Success", f"Student {student_id} registered for {selected_course}")
         
      except ValueError as e:
         QMessageBox.warning(self, "Error", str(e))
      except Exception as e:
         QMessageBox.warning(self, "Error", str(e))

      self.stacked_widget.setCurrentIndex(0)

      
    def create_instructor_assignment_form(self):
      instructor_assignment_widget = QWidget()
      instructor_assignment_layout = QVBoxLayout(instructor_assignment_widget)
      instructor_assignment_layout.setAlignment(Qt.AlignCenter)

      title_label = QLabel("Assign Instructor to Course", self)
      title_label.setStyleSheet("font-size: 16pt;")
      title_label.setAlignment(Qt.AlignCenter)
      instructor_assignment_layout.addWidget(title_label)

      self.instructor_id_edit = QLineEdit(self)
      self.instructor_id_edit.setPlaceholderText("Enter Instructor ID")
      self.instructor_id_edit.setFixedSize(200, 50)
      instructor_assignment_layout.addWidget(self.instructor_id_edit)

      available_courses = self.load_courses()
      self.course_dropdown = QComboBox(self)
      self.course_dropdown.addItems(available_courses)
      self.course_dropdown.setFixedSize(200, 50)
      instructor_assignment_layout.addWidget(self.course_dropdown)

      assign_button = QPushButton("Assign", self)
      assign_button.setFixedSize(200, 50)
      assign_button.clicked.connect(self.assign_instructor_to_course)
      instructor_assignment_layout.addWidget(assign_button)

      back_button = QPushButton("Back to Menu", self)
      back_button.setFixedSize(200, 50)
      back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
      instructor_assignment_layout.addWidget(back_button)

      self.stacked_widget.addWidget(instructor_assignment_widget)
      self.stacked_widget.setCurrentWidget(instructor_assignment_widget)


    def assign_instructor_to_course(self):
      instructor_id = self.instructor_id_edit.text()
      course_id = self.course_dropdown.currentText()

      if not instructor_id or not course_id:
         QMessageBox.critical(self, "Error", "Both Instructor ID and Course must be provided!")
         return

      try:
         course = self.search_course_by_id(course_id)
         instructor = Instructor.load_instructor_by_id(Instructor, './Serialization/Instructor.json', instructor_id)

         if course is None:
               raise ValueError(f"Course with ID '{course_id}' not found.")
         if instructor is None:
               raise ValueError(f"Instructor with ID '{instructor_id}' not found.")

         instructor.assign_course(course)
         QMessageBox.information(self, "Success", f"Instructor {instructor_id} assigned to course {course_id}")

      except Exception as e:
         QMessageBox.critical(self, "Error", str(e))

      self.stacked_widget.setCurrentIndex(0)

    
    def display_all_records(self):
      """Displays all students, instructors, and courses in a tabular format using QTableWidget."""
      records_widget = QWidget()
      records_layout = QVBoxLayout(records_widget)
      records_layout.setAlignment(Qt.AlignCenter)

      title_label = QLabel("All Records", self)
      title_label.setStyleSheet("font-size: 16pt;")
      title_label.setAlignment(Qt.AlignCenter)
      records_layout.addWidget(title_label)

      tab_widget = QTabWidget(self)
      records_layout.addWidget(tab_widget)

      # Student Table
      student_table = QTableWidget()
      student_table.setColumnCount(5)  
      student_table.setHorizontalHeaderLabels(["Student ID", "Name", "Age", "Email", "Enrolled Courses"])
      student_table.horizontalHeader().setStretchLastSection(True)
      student_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
      tab_widget.addTab(student_table, "Students")

      try:
         students = Student.load_from_json('./Serialization/Student.json')
         student_table.setRowCount(len(students))
         for row, student in enumerate(students):
               enrolled_courses = ', '.join(student.registered_courses)  
               student_table.setItem(row, 0, QTableWidgetItem(student.student_id))
               student_table.setItem(row, 1, QTableWidgetItem(student.name))
               student_table.setItem(row, 2, QTableWidgetItem(str(student.age)))
               student_table.setItem(row, 3, QTableWidgetItem(student._email))
               student_table.setItem(row, 4, QTableWidgetItem(enrolled_courses))
      except FileNotFoundError:
         print("Student JSON file not found")
      except json.JSONDecodeError as e:
         print(f"Error reading student JSON file: {e}")

      # Instructor Table
      instructor_table = QTableWidget()
      instructor_table.setColumnCount(5) 
      instructor_table.setHorizontalHeaderLabels(["Instructor ID", "Name", "Age", "Email", "Courses Taught"])
      instructor_table.horizontalHeader().setStretchLastSection(True)
      instructor_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
      tab_widget.addTab(instructor_table, "Instructors")

      try:
         instructors = Instructor.load_from_json('./Serialization/Instructor.json')
         instructor_table.setRowCount(len(instructors))
         for row, instructor in enumerate(instructors):
               taught_courses = ', '.join(instructor.assigned_courses)  
               instructor_table.setItem(row, 0, QTableWidgetItem(instructor.instructor_id))
               instructor_table.setItem(row, 1, QTableWidgetItem(instructor.name))
               instructor_table.setItem(row, 2, QTableWidgetItem(str(instructor.age)))
               instructor_table.setItem(row, 3, QTableWidgetItem(instructor._email))
               instructor_table.setItem(row, 4, QTableWidgetItem(taught_courses))
      except FileNotFoundError:
         print("Instructor JSON file not found")
      except json.JSONDecodeError as e:
         print(f"Error reading instructor JSON file: {e}")

      # Course Table
      course_table = QTableWidget()
      course_table.setColumnCount(4)
      course_table.setHorizontalHeaderLabels(["Course ID", "Course Name", "Instructor ID", "Enrolled Students"])
      course_table.horizontalHeader().setStretchLastSection(True)
      course_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
      tab_widget.addTab(course_table, "Courses")

      try:
         courses = Course.load_from_json('./Serialization/Course.json')
         course_table.setRowCount(len(courses))
         for row, course in enumerate(courses):
               enrolled_students = ', '.join(course.enrolled_students)
               course_table.setItem(row, 0, QTableWidgetItem(course.course_id))
               course_table.setItem(row, 1, QTableWidgetItem(course.course_name))
               course_table.setItem(row, 2, QTableWidgetItem(course.instructor.instructor_id if course.instructor is not None else ""))
               course_table.setItem(row, 3, QTableWidgetItem(enrolled_students))
      except FileNotFoundError:
         print("Course JSON file not found")
      except json.JSONDecodeError as e:
         print(f"Error reading course JSON file: {e}")

      # Button Layout
      button_layout = QHBoxLayout()
      button_layout.setAlignment(Qt.AlignCenter)

      back_button = QPushButton("Back to Menu", self)
      back_button.setFixedSize(200, 50)
      back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
      button_layout.addWidget(back_button)

      edit_button = QPushButton("Edit Selected", self)
      edit_button.setFixedSize(200, 50)
      edit_button.clicked.connect(lambda: self.edit_record(student_table, "student") if tab_widget.currentWidget() == student_table else
                                    self.edit_record(instructor_table, "instructor") if tab_widget.currentWidget() == instructor_table else
                                    self.edit_record(course_table, "course"))
      button_layout.addWidget(edit_button)

      delete_button = QPushButton("Delete Selected", self)
      delete_button.setFixedSize(200, 50)
      delete_button.clicked.connect(lambda: self.delete_record(student_table, "student") if tab_widget.currentWidget() == student_table else
                                       self.delete_record(instructor_table, "instructor") if tab_widget.currentWidget() == instructor_table else
                                       self.delete_record(course_table, "course"))
      button_layout.addWidget(delete_button)

      records_layout.addLayout(button_layout)

      self.stacked_widget.addWidget(records_widget)
      self.stacked_widget.setCurrentWidget(records_widget)

    def edit_record(self, table_widget, record_type):
      selected_items = table_widget.selectedItems()

      if not selected_items:
         QMessageBox.warning(self, "No selection", "Please select a record to edit.")
         return

      record_id = selected_items[0].text()

      if record_type == "student":
         try:
               students = Student.load_from_json('./Serialization/Student.json')
               student = next(student for student in students if student.student_id == record_id)

               new_name, ok = QInputDialog.getText(self, "Edit Student", f"Enter new name (current: {student.name}, enter 'NA' to keep current):")
               if ok and new_name and new_name != "NA":
                  student.name = new_name

               new_age, ok = QInputDialog.getText(self, "Edit Student", f"Enter new age (current: {student.age}, enter 'NA' to keep current):")
               if ok and new_age and new_age != "NA":
                  try:
                     student.age = int(new_age)
                  except ValueError:
                     QMessageBox.warning(self, "Invalid Input", "Age must be an integer. No changes made to age.")

               new_email, ok = QInputDialog.getText(self, "Edit Student", f"Enter new email (current: {student._email}, enter 'NA' to keep current):")
               if ok and new_email and new_email != "NA":
                  student._email = new_email

               with open('./Serialization/Student.json', 'w') as file:
                  json.dump([s.to_dict() for s in students], file, indent=4)

               for row in range(table_widget.rowCount()):
                  if table_widget.item(row, 0).text() == student.student_id:
                     table_widget.setItem(row, 0, QTableWidgetItem(student.student_id))
                     table_widget.setItem(row, 1, QTableWidgetItem(student.name))
                     table_widget.setItem(row, 2, QTableWidgetItem(str(student.age)))
                     table_widget.setItem(row, 3, QTableWidgetItem(student._email))
                     break

               QMessageBox.information(self, "Success", "Student updated successfully!")

         except Exception as e:
               QMessageBox.critical(self, "Error", f"Failed to edit student: {str(e)}")

      elif record_type == "instructor":
         try:
               instructors = Instructor.load_from_json('./Serialization/Instructor.json')
               instructor = next(instructor for instructor in instructors if instructor.instructor_id == record_id)

               new_name, ok = QInputDialog.getText(self, "Edit Instructor", f"Enter new name (current: {instructor.name}, enter 'NA' to keep current):")
               if ok and new_name and new_name != "NA":
                  instructor.name = new_name

               new_age, ok = QInputDialog.getText(self, "Edit Instructor", f"Enter new age (current: {instructor.age}, enter 'NA' to keep current):")
               if ok and new_age and new_age != "NA":
                  try:
                     instructor.age = int(new_age)
                  except ValueError:
                     QMessageBox.warning(self, "Invalid Input", "Age must be an integer. No changes made to age.")

               new_email, ok = QInputDialog.getText(self, "Edit Instructor", f"Enter new email (current: {instructor._email}, enter 'NA' to keep current):")
               if ok and new_email and new_email != "NA":
                  instructor._email = new_email

               with open('./Serialization/Instructor.json', 'w') as file:
                  json.dump([i.to_dict() for i in instructors], file, indent=4)

               for row in range(table_widget.rowCount()):
                  if table_widget.item(row, 0).text() == instructor.instructor_id:
                     table_widget.setItem(row, 0, QTableWidgetItem(instructor.instructor_id))
                     table_widget.setItem(row, 1, QTableWidgetItem(instructor.name))
                     table_widget.setItem(row, 2, QTableWidgetItem(str(instructor.age)))
                     table_widget.setItem(row, 3, QTableWidgetItem(instructor._email))
                     break

               QMessageBox.information(self, "Success", "Instructor updated successfully!")

         except Exception as e:
               QMessageBox.critical(self, "Error", f"Failed to edit instructor: {str(e)}")

      elif record_type == "course":
         try:
               courses = Course.load_from_json('./Serialization/Course.json')
               course = next(course for course in courses if course.course_id == record_id)

               new_name, ok = QInputDialog.getText(self, "Edit Course", f"Enter new name (current: {course.course_name}, enter 'NA' to keep current):")
               if ok and new_name and new_name != "NA":
                  course.course_name = new_name

               new_instructor, ok = QInputDialog.getText(self, "Edit Course", f"Enter new instructor ID (current: {course.instructor}, enter 'NA' to keep current):")
               if ok and new_instructor and new_instructor != "NA":
                  course.instructor = new_instructor

               with open('./Serialization/Course.json', 'w') as file:
                  json.dump([c.to_dict() for c in courses], file, indent=4)

               enrolled_students = ', '.join(course.enrolled_students)
               for row in range(table_widget.rowCount()):
                  if table_widget.item(row, 0).text() == course.course_id:
                     table_widget.setItem(row, 0, QTableWidgetItem(course.course_id))
                     table_widget.setItem(row, 1, QTableWidgetItem(course.course_name))
                     table_widget.setItem(row, 2, QTableWidgetItem(course.instructor if course.instructor else ""))
                     table_widget.setItem(row, 3, QTableWidgetItem(enrolled_students))
                     break

               QMessageBox.information(self, "Success", "Course updated successfully!")

         except Exception as e:
               QMessageBox.critical(self, "Error", f"Failed to edit course: {str(e)}")

    def delete_record(self, table_widget, record_type):
      selected_items = table_widget.selectedItems()

      if not selected_items:
         QMessageBox.warning(self, "No selection", "Please select a record to delete.")
         return

      record_id = selected_items[0].text()
      confirmation = QMessageBox.question(self, "Confirm Deletion",
                                          f"Are you sure you want to delete the selected {record_type} record?",
                                          QMessageBox.Yes | QMessageBox.No)

      if confirmation == QMessageBox.Yes:
         try:
               if record_type == "student":
                  students = Student.load_from_json('./Serialization/Student.json')
                  students = [s for s in students if s.student_id != record_id]
                  with open('./Serialization/Student.json', 'w') as file:
                     json.dump([s.to_dict() for s in students], file, indent=4)

               elif record_type == "instructor":
                  instructors = Instructor.load_from_json('./Serialization/Instructor.json')
                  instructors = [i for i in instructors if i.instructor_id != record_id]
                  with open('./Serialization/Instructor.json', 'w') as file:
                     json.dump([i.to_dict() for i in instructors], file, indent=4)

               elif record_type == "course":
                  courses = Course.load_from_json('./Serialization/Course.json')
                  courses = [c for c in courses if c.course_id != record_id]
                  with open('./Serialization/Course.json', 'w') as file:
                     json.dump([c.to_dict() for c in courses], file, indent=4)

               for row in range(table_widget.rowCount()):
                  if table_widget.item(row, 0).text() == record_id:
                     table_widget.removeRow(row)
                     break

               QMessageBox.information(self, "Success", f"{record_type.capitalize()} deleted successfully!")

         except Exception as e:
               QMessageBox.critical(self, "Error", f"Failed to delete {record_type}: {str(e)}")
    
    def create_search_form(self):
      """Creates a search form to filter and display records by name, ID, or course."""
      search_widget = QWidget()
      search_layout = QVBoxLayout(search_widget)
      search_layout.setAlignment(Qt.AlignCenter)

      title_label = QLabel("Search Records", self)
      title_label.setStyleSheet("font-size: 16pt;")
      title_label.setAlignment(Qt.AlignCenter)
      search_layout.addWidget(title_label)

      form_layout = QFormLayout()
      search_layout.addLayout(form_layout)

      self.search_by_var = QComboBox(self)
      self.search_by_var.addItems(["Name", "ID"])
      form_layout.addRow(QLabel("Search by:"), self.search_by_var)

      self.search_term_var = QLineEdit(self)
      self.search_term_var.setPlaceholderText("Enter Search Term")
      form_layout.addRow(QLabel("Enter Search Term:"), self.search_term_var)

      self.search_category_var = QComboBox(self)
      self.search_category_var.addItems(["Students", "Instructors", "Courses"])
      form_layout.addRow(QLabel("Search in:"), self.search_category_var)

      button_layout = QHBoxLayout()
      button_layout.setAlignment(Qt.AlignCenter)

      search_button = QPushButton("Search", self)
      search_button.setFixedSize(200, 50)
      search_button.clicked.connect(self.search_records)
      button_layout.addWidget(search_button)

      back_button = QPushButton("Back to Menu", self)
      back_button.setFixedSize(200, 50)
      back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
      button_layout.addWidget(back_button)

   
      search_layout.addLayout(button_layout)

      self.stacked_widget.addWidget(search_widget)
      self.stacked_widget.setCurrentWidget(search_widget)

    def search_records(self):
      """Filters and displays records based on the search criteria."""
      search_by = self.search_by_var.currentText()  
      search_term = self.search_term_var.text().lower()  
      category = self.search_category_var.currentText() 

      if not search_term:
         QMessageBox.critical(self, "Error", "Search term cannot be empty!")
         return

      search_results_widget = QWidget()
      search_results_layout = QVBoxLayout(search_results_widget)
      search_results_layout.setAlignment(Qt.AlignCenter)

      result_table = QTableWidget()
      search_results_layout.addWidget(result_table)

      if category == "Students":
         result_table.setColumnCount(4)
         result_table.setHorizontalHeaderLabels(["Student ID", "Name", "Age", "Email"])
         result_table.horizontalHeader().setStretchLastSection(True)

         students = Student.load_from_json('./Serialization/Student.json')
         filtered_students = [student for student in students
                              if (search_by == "Name" and search_term in student.name.lower()) or
                              (search_by == "ID" and search_term == student.student_id.lower())]

         result_table.setRowCount(len(filtered_students))
         for row, student in enumerate(filtered_students):
               result_table.setItem(row, 0, QTableWidgetItem(student.student_id))
               result_table.setItem(row, 1, QTableWidgetItem(student.name))
               result_table.setItem(row, 2, QTableWidgetItem(str(student.age)))
               result_table.setItem(row, 3, QTableWidgetItem(student._email))

      elif category == "Instructors":
         result_table.setColumnCount(5)
         result_table.setHorizontalHeaderLabels(["Instructor ID", "Name", "Age", "Email", "Assigned Courses"])
         result_table.horizontalHeader().setStretchLastSection(True)

         instructors = Instructor.load_from_json('./Serialization/Instructor.json')
         filtered_instructors = [instructor for instructor in instructors
                                 if (search_by == "Name" and search_term in instructor.name.lower()) or
                                 (search_by == "ID" and (search_term == instructor.instructor_id.lower() or search_term in ', '.join(instructor.assigned_courses).lower()))]

         result_table.setRowCount(len(filtered_instructors))
         for row, instructor in enumerate(filtered_instructors):
               assigned_courses = ', '.join(instructor.assigned_courses)
               result_table.setItem(row, 0, QTableWidgetItem(instructor.instructor_id))
               result_table.setItem(row, 1, QTableWidgetItem(instructor.name))
               result_table.setItem(row, 2, QTableWidgetItem(str(instructor.age)))
               result_table.setItem(row, 3, QTableWidgetItem(instructor._email))
               result_table.setItem(row, 4, QTableWidgetItem(assigned_courses))

      elif category == "Courses":
         result_table.setColumnCount(4)
         result_table.setHorizontalHeaderLabels(["Course ID", "Course Name", "Instructor ID", "Enrolled Students"])
         result_table.horizontalHeader().setStretchLastSection(True)

         courses = Course.load_from_json('./Serialization/Course.json')
         filtered_courses = [course for course in courses
                              if (search_by == "Name" and search_term in course.course_name.lower()) or
                              (search_by == "ID" and search_term == course.course_id.lower())]

         result_table.setRowCount(len(filtered_courses))
         for row, course in enumerate(filtered_courses):
               enrolled_students = ', '.join(course.enrolled_students)
               result_table.setItem(row, 0, QTableWidgetItem(course.course_id))
               result_table.setItem(row, 1, QTableWidgetItem(course.course_name))
               result_table.setItem(row, 2, QTableWidgetItem(course.instructor.instructor_id if course.instructor else ""))
               result_table.setItem(row, 3, QTableWidgetItem(enrolled_students))

      button_layout = QHBoxLayout()
      button_layout.setAlignment(Qt.AlignCenter)

      back_button = QPushButton("Back to Menu", self)
      back_button.setFixedSize(200, 50)
      back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
      button_layout.addWidget(back_button)

      search_again_button = QPushButton("Search Again", self)
      search_again_button.setFixedSize(200, 50)
      search_again_button.clicked.connect(self.create_search_form)
      button_layout.addWidget(search_again_button)

      search_results_layout.addLayout(button_layout)

      self.stacked_widget.addWidget(search_results_widget)
      self.stacked_widget.setCurrentWidget(search_results_widget)

    def json_to_csv(self, json_file, csv_file, fieldnames):
      """Convert JSON file to CSV file and return a status message."""
      try:
         with open(json_file, 'r') as f:
               data = json.load(f)

         with open(csv_file, 'w', newline='', encoding='utf-8') as f:
               writer = csv.DictWriter(f, fieldnames=fieldnames)
               writer.writeheader()
               for item in data:
                  writer.writerow(item)

         return f"Successfully exported {json_file} to {csv_file}"

      except FileNotFoundError:
         return f"{json_file} not found."
      except json.JSONDecodeError as e:
         return f"Error decoding JSON from {json_file}: {e}"
      except Exception as e:
         return f"An error occurred while exporting {json_file}: {e}"

    def export_to_csv(self):
      """Exports all records (students, instructors, courses) to CSV files and shows a dialog with status messages."""
      student_fieldnames = ["student_id", "name", "age", "email", "registered_courses"]
      instructor_fieldnames = ["instructor_id", "name", "age", "email", "assigned_courses"]
      course_fieldnames = ["course_id", "course_name", "instructor", "enrolled_students"]

      messages = []
      messages.append(self.json_to_csv('./Serialization/Student.json', './Serialization/Student.csv', student_fieldnames))
      messages.append(self.json_to_csv('./Serialization/Instructor.json', './Serialization/Instructor.csv', instructor_fieldnames))
      messages.append(self.json_to_csv('./Serialization/Course.json', './Serialization/Course.csv', course_fieldnames))

   
      QMessageBox.information(self, "Export Complete", "\n".join(messages))

      
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SchoolManagementApp()
    window.show()
    sys.exit(app.exec_())
