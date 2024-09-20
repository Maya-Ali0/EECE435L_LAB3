import sys
import json
import csv
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QFormLayout, QAbstractItemView, QTableWidgetItem, QTableWidget, QTabWidget, QComboBox, QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QStackedWidget
from PyQt5.QtCore import Qt
from Classes.Course import Course
from Classes.Instructor import Instructor
from Classes.Student import Student
import sqlite3

conn = sqlite3.connect('Database/database.sqlite')
cursor = conn.cursor()
print(conn)


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
         ("Export to CSV", self.save_data_to_csv)  
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
            name = self.student_name_edit.text().strip()
            age = self.student_age_edit.text().strip()
            email = self.student_email_edit.text().strip()
            student_id = self.student_id_edit.text().strip()

            if not name:
                raise ValueError("Name cannot be empty!")
            
            if not age:
                raise ValueError("Age cannot be empty!")
            
            try:
                age_int = int(age)
                if age_int <= 0:
                    raise ValueError("Age must be a positive integer!")
            except ValueError:
                raise ValueError("Age must be a valid integer!")

            if not email:
                raise ValueError("Email cannot be empty!")
            
            if '@' not in email or '.' not in email:
                raise ValueError("Email format is invalid!")

            if not student_id:
                raise ValueError("Student ID cannot be empty!")

            cursor.execute(
                "INSERT INTO students (student_id, name, age, email) VALUES (?, ?, ?, ?)",
                (student_id, name, age_int, email)
            )
            conn.commit()

            QMessageBox.information(self, "Success", "Student added successfully!")
            self.stacked_widget.setCurrentIndex(0)

        except ValueError as e:
            QMessageBox.warning(self, "Validation Error", str(e))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


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
            name = self.instructor_name_edit.text().strip()
            age = self.instructor_age_edit.text().strip()
            email = self.instructor_email_edit.text().strip()
            instructor_id = self.instructor_id_edit.text().strip()

            if not name:
                raise ValueError("Name cannot be empty!")

            if not age:
                raise ValueError("Age cannot be empty!")

            try:
                age_int = int(age)
                if age_int <= 0:
                    raise ValueError("Age must be a positive integer!")
            except ValueError:
                raise ValueError("Age must be a valid integer!")

            if not email:
                raise ValueError("Email cannot be empty!")
            
            if '@' not in email or '.' not in email:
                raise ValueError("Email format is invalid!")

            if not instructor_id:
                raise ValueError("Instructor ID cannot be empty!")

            cursor.execute(
                "INSERT INTO instructors (instructor_id, name, age, email) VALUES (?, ?, ?, ?)",
                (instructor_id, name, age_int, email)
            )
            conn.commit()

            QMessageBox.information(self, "Success", "Instructor added successfully!")
            self.stacked_widget.setCurrentIndex(0)

        except ValueError as e:
            QMessageBox.warning(self, "Validation Error", str(e))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


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

            cursor.execute("INSERT INTO courses (course_id, course_name) VALUES (?, ?)", (course_id, course_name))
            conn.commit()
            QMessageBox.information(self, "Success", "Course added successfully!")
            self.stacked_widget.setCurrentIndex(0)  

        except ValueError as e:
            QMessageBox.warning(self, "Validation Error", str(e))

    def load_courses(self):
       try:
            cursor.execute("SELECT course_id FROM courses")
            courses_data = cursor.fetchall() 

            courses = [course[0] for course in courses_data]  # course[0] is the course_id from the tuple
            return courses
        
       except sqlite3.Error as e:
            print(f"An error occurred while loading courses: {e}")
            return []
        
    # def search_course_by_id(self, course_id):
    #     """Search for a course by its ID and return the course object."""
    #     courses = Course.load_from_json('./Serialization/Course.JSON')
    #     for course in courses:
    #         if course.course_id == course_id:
    #             return course
    #     return None

    # def search_student_by_id(self, student_id):
    #     students = Student.load_from_json('./Serialization/Student.JSON')
    #     for student in students:
    #         if student.student_id == student_id:
    #             return student
    #     return None
    
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
          cursor.execute("SELECT student_id FROM students WHERE student_id = ?", (student_id,))
          student_data = cursor.fetchone()
          print(student_data)
          cursor.execute("SELECT course_id FROM courses WHERE course_id = ?", (selected_course,))
          course_data = cursor.fetchone()
                
          if student_data is not None and course_data is not None:
              cursor.execute("INSERT INTO student_courses (student_id, course_id) VALUES (?, ?);", (student_id, selected_course,))
              QMessageBox.information(self, "Success", f"Student {student_id} registered for {selected_course}")
              conn.commit()
        
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
        cursor.execute("SELECT instructor_id FROM instructors WHERE instructor_id = ?", (instructor_id,))
        instructor_data = cursor.fetchone()
           
        cursor.execute("SELECT instructor_id FROM courses WHERE course_id = ?", (course_id,))
        inst_course = cursor.fetchone()
        print(inst_course[0])
           
        cursor.execute("SELECT course_id FROM courses WHERE course_id = ?", (course_id,))

        course_data = cursor.fetchone()

        if course_data is None:
               raise ValueError(f"Course with ID '{course_id}' not found.")
        if instructor_data is None:
               raise ValueError(f"Instructor with ID '{instructor_id}' not found.")

        if inst_course[0] is not None:
                QMessageBox.information(self,"Failed", "Course already have an instructor.")

        else:
            cursor.execute("UPDATE courses set instructor_id = ? where course_id = ?", (instructor_id, course_id,))
            QMessageBox.information(self, "Success", f"Instructor {instructor_id} assigned to course {course_id}")

            conn.commit()  
  
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
          cursor.execute("SELECT * FROM students;")
          students = cursor.fetchall()
          student_table.setRowCount(len(students))
               
          for row, student in enumerate(students):
             
                cursor.execute("SELECT course_id FROM student_courses where student_id = ?", (student[0],))
                courses = cursor.fetchall()
                
                student_table.setItem(row, 0, QTableWidgetItem(student[0]))
                student_table.setItem(row, 1, QTableWidgetItem(student[1]))
                student_table.setItem(row, 2, QTableWidgetItem(str(student[2])))
                student_table.setItem(row, 3, QTableWidgetItem(student[3]))
                student_table.setItem(row, 4, QTableWidgetItem(str(courses)))

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
          cursor.execute("SELECT * FROM instructors;")
          instructors = cursor.fetchall()
          instructor_table.setRowCount(len(instructors))
               
          for row, instructor in enumerate(instructors):
               
                cursor.execute("SELECT course_id FROM courses where instructor_id = ?", (instructor[0],))
                courses = cursor.fetchall()
              
                instructor_table.setItem(row, 0, QTableWidgetItem(instructor[0]))
                instructor_table.setItem(row, 1, QTableWidgetItem(instructor[1]))
                instructor_table.setItem(row, 2, QTableWidgetItem(str(instructor[2])))
                instructor_table.setItem(row, 3, QTableWidgetItem(instructor[3]))
                instructor_table.setItem(row, 4, QTableWidgetItem(str(courses)))
                
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
          cursor.execute("SELECT * FROM courses;")
          courses = cursor.fetchall()
          course_table.setRowCount(len(courses))
          print(courses)
          for row, course in enumerate(courses):
                cursor.execute("SELECT student_id FROM student_courses where course_id = ?", (course[0],))
                students = cursor.fetchall()
                course_table.setItem(row, 0, QTableWidgetItem(course[0]))
                course_table.setItem(row, 1, QTableWidgetItem(course[1]))
                course_table.setItem(row, 2, QTableWidgetItem(course[2]))
                course_table.setItem(row, 3, QTableWidgetItem(str(students)))
                
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
                cursor.execute("SELECT * FROM students WHERE student_id = ?", (record_id,))
                student_data = cursor.fetchone()

                if not student_data:
                    QMessageBox.critical(self, "Error", "Student not found.")
                    return

                current_name, current_age, current_email = student_data[1], student_data[2], student_data[3]

                new_name, ok = QInputDialog.getText(self, "Edit Student", f"Enter new name (current: {current_name}, enter 'NA' to keep current):")
                if ok and new_name and new_name != "NA":
                    cursor.execute("UPDATE students SET name = ? WHERE student_id = ?", (new_name, record_id))

                new_age, ok = QInputDialog.getText(self, "Edit Student", f"Enter new age (current: {current_age}, enter 'NA' to keep current):")
                if ok and new_age and new_age != "NA":
                    try:
                        cursor.execute("UPDATE students SET age = ? WHERE student_id = ?", (int(new_age), record_id))
                    except ValueError:
                        QMessageBox.warning(self, "Invalid Input", "Age must be an integer. No changes made to age.")

                new_email, ok = QInputDialog.getText(self, "Edit Student", f"Enter new email (current: {current_email}, enter 'NA' to keep current):")
                if ok and new_email and new_email != "NA":
                    cursor.execute("UPDATE students SET email = ? WHERE student_id = ?", (new_email, record_id))

                conn.commit()

                for row in range(table_widget.rowCount()):
                    if table_widget.item(row, 0).text() == record_id:
                        table_widget.setItem(row, 0, QTableWidgetItem(record_id))
                        table_widget.setItem(row, 1, QTableWidgetItem(new_name if new_name != "NA" else current_name))
                        table_widget.setItem(row, 2, QTableWidgetItem(str(new_age) if new_age != "NA" else str(current_age)))
                        table_widget.setItem(row, 3, QTableWidgetItem(new_email if new_email != "NA" else current_email))
                        break

                QMessageBox.information(self, "Success", "Student updated successfully!")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to edit student: {str(e)}")

        elif record_type == "instructor":
            try:
                cursor.execute("SELECT * FROM instructors WHERE instructor_id = ?", (record_id,))
                instructor_data = cursor.fetchone()

                if not instructor_data:
                    QMessageBox.critical(self, "Error", "Instructor not found.")
                    return

                current_name, current_age, current_email = instructor_data[1], instructor_data[2], instructor_data[3]

                new_name, ok = QInputDialog.getText(self, "Edit Instructor", f"Enter new name (current: {current_name}, enter 'NA' to keep current):")
                if ok and new_name and new_name != "NA":
                    cursor.execute("UPDATE instructors SET name = ? WHERE instructor_id = ?", (new_name, record_id))

                new_age, ok = QInputDialog.getText(self, "Edit Instructor", f"Enter new age (current: {current_age}, enter 'NA' to keep current):")
                if ok and new_age and new_age != "NA":
                    try:
                        cursor.execute("UPDATE instructors SET age = ? WHERE instructor_id = ?", (int(new_age), record_id))
                    except ValueError:
                        QMessageBox.warning(self, "Invalid Input", "Age must be an integer. No changes made to age.")

                new_email, ok = QInputDialog.getText(self, "Edit Instructor", f"Enter new email (current: {current_email}, enter 'NA' to keep current):")
                if ok and new_email and new_email != "NA":
                    cursor.execute("UPDATE instructors SET email = ? WHERE instructor_id = ?", (new_email, record_id))

                conn.commit()

                for row in range(table_widget.rowCount()):
                    if table_widget.item(row, 0).text() == record_id:
                        table_widget.setItem(row, 0, QTableWidgetItem(record_id))
                        table_widget.setItem(row, 1, QTableWidgetItem(new_name if new_name != "NA" else current_name))
                        table_widget.setItem(row, 2, QTableWidgetItem(str(new_age) if new_age != "NA" else str(current_age)))
                        table_widget.setItem(row, 3, QTableWidgetItem(new_email if new_email != "NA" else current_email))
                        break

                QMessageBox.information(self, "Success", "Instructor updated successfully!")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to edit instructor: {str(e)}")

        elif record_type == "course":
            try:
                cursor.execute("SELECT * FROM courses WHERE course_id = ?", (record_id,))
                course_data = cursor.fetchone()

                if not course_data:
                    QMessageBox.critical(self, "Error", "Course not found.")
                    return

                current_name, current_instructor = course_data[1], course_data[2]

                new_name, ok = QInputDialog.getText(self, "Edit Course", f"Enter new name (current: {current_name}, enter 'NA' to keep current):")
                if ok and new_name and new_name != "NA":
                    cursor.execute("UPDATE courses SET course_name = ? WHERE course_id = ?", (new_name, record_id))

                new_instructor, ok = QInputDialog.getText(self, "Edit Course", f"Enter new instructor ID (current: {current_instructor}, enter 'NA' to keep current):")
                if ok and new_instructor and new_instructor != "NA":
                    cursor.execute("UPDATE courses SET instructor = ? WHERE course_id = ?", (new_instructor, record_id))

                conn.commit()

                enrolled_students = ', '.join(self.get_enrolled_students(record_id))
                for row in range(table_widget.rowCount()):
                    if table_widget.item(row, 0).text() == record_id:
                        table_widget.setItem(row, 0, QTableWidgetItem(record_id))
                        table_widget.setItem(row, 1, QTableWidgetItem(new_name if new_name != "NA" else current_name))
                        table_widget.setItem(row, 2, QTableWidgetItem(new_instructor if new_instructor != "NA" else current_instructor))
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
                 cursor.execute("DELETE from students where student_id = ?", (record_id,))
                 conn.commit()


               elif record_type == "instructor":
                   cursor.execute("DELETE from instructors where instructor_id = ?", (record_id,))
                   conn.commit()

               elif record_type == "course":
                    cursor.execute("DELETE from courses where course_id = ?", (record_id,))
                    conn.commit()

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

            if search_by == "Name":
                cursor.execute("SELECT * FROM students WHERE LOWER(name) LIKE ?", ('%' + search_term + '%',))
            elif search_by == "ID":
                cursor.execute("SELECT * FROM students WHERE LOWER(student_id) = ?", (search_term,))

            students = cursor.fetchall()
            result_table.setRowCount(len(students))
            for row, student in enumerate(students):
                result_table.setItem(row, 0, QTableWidgetItem(student[0]))
                result_table.setItem(row, 1, QTableWidgetItem(student[1]))
                result_table.setItem(row, 2, QTableWidgetItem(str(student[2])))
                result_table.setItem(row, 3, QTableWidgetItem(student[3]))

        elif category == "Instructors":
            result_table.setColumnCount(5)
            result_table.setHorizontalHeaderLabels(["Instructor ID", "Name", "Age", "Email", "Assigned Courses"])
            result_table.horizontalHeader().setStretchLastSection(True)

            if search_by == "Name":
                cursor.execute("SELECT * FROM instructors WHERE LOWER(name) LIKE ?", ('%' + search_term + '%',))
            elif search_by == "ID":
                cursor.execute("SELECT * FROM instructors WHERE LOWER(instructor_id) = ? OR LOWER(assigned_courses) LIKE ?", (search_term, '%' + search_term + '%'))

            instructors = cursor.fetchall()
            result_table.setRowCount(len(instructors))
            for row, instructor in enumerate(instructors):
                assigned_courses = instructor[4] 
                result_table.setItem(row, 0, QTableWidgetItem(instructor[0]))
                result_table.setItem(row, 1, QTableWidgetItem(instructor[1]))
                result_table.setItem(row, 2, QTableWidgetItem(str(instructor[2])))
                result_table.setItem(row, 3, QTableWidgetItem(instructor[3]))
                result_table.setItem(row, 4, QTableWidgetItem(assigned_courses))

        elif category == "Courses":
            result_table.setColumnCount(4)
            result_table.setHorizontalHeaderLabels(["Course ID", "Course Name", "Instructor ID", "Enrolled Students"])
            result_table.horizontalHeader().setStretchLastSection(True)

            if search_by == "Name":
                cursor.execute("SELECT * FROM courses WHERE LOWER(course_name) LIKE ?", ('%' + search_term + '%',))
            elif search_by == "ID":
                cursor.execute("SELECT * FROM courses WHERE LOWER(course_id) = ?", (search_term,))

            courses = cursor.fetchall()
            result_table.setRowCount(len(courses))
            for row, course in enumerate(courses):
                enrolled_students = course[3] 
                result_table.setItem(row, 0, QTableWidgetItem(course[0]))
                result_table.setItem(row, 1, QTableWidgetItem(course[1]))
                result_table.setItem(row, 2, QTableWidgetItem(course[2]))
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

    def load_courses_from_db(self):
        cursor.execute("""
            SELECT c.course_name, c.course_id, i.email, i.instructor_id,
            GROUP_CONCAT(sc.student_id) as enrolled_students
            FROM courses c
            LEFT JOIN instructors i ON c.instructor_id = i.instructor_id
            LEFT JOIN student_courses sc ON sc.course_id = c.course_id
            GROUP BY c.course_id;
        """)
        return cursor.fetchall()

    def load_instructors_from_db(self):
        cursor.execute("""
            SELECT i.name, i.age, i.email, i.instructor_id,
            GROUP_CONCAT(c.course_id) as assigned_courses
            FROM instructors i
            LEFT JOIN courses c ON c.instructor_id = i.instructor_id
            GROUP BY i.instructor_id;
        """)
        return cursor.fetchall()

    def load_students_from_db(self):
        cursor.execute("""
            SELECT s.name, s.age, s.email, s.student_id,
            GROUP_CONCAT(sc.course_id) as registered_courses
            FROM students s
            LEFT JOIN student_courses sc ON sc.student_id = s.student_id
            GROUP BY s.student_id;
        """)
        return cursor.fetchall()

    def save_data_to_csv(self):
        try:


            file_paths = {
                'students': f"Serialization/students.csv",
                'instructors': f"Serialization/instructors.csv",
                'courses': f"Serialization/courses.csv"
            }

            course_data = self.load_courses_from_db()
            self.write_csv(file_paths['courses'], course_data,
                        ['Course Name', 'Course ID', 'Instructor Email', 'Instructor ID', 'Enrolled Students'],
                        lambda course: {
                            'Course Name': course[0],
                            'Course ID': course[1],
                            'Instructor Email': course[2] if course[2] else '',
                            'Instructor ID': course[3] if course[3] else '',
                            'Enrolled Students': course[4]
                        })

            instructor_data = self.load_instructors_from_db()
            self.write_csv(file_paths['instructors'], instructor_data,
                        ['Name', 'Age', 'Email', 'Instructor ID', 'Assigned Courses'],
                        lambda instructor: {
                            'Name': instructor[0],
                            'Age': instructor[1],
                            'Email': instructor[2],
                            'Instructor ID': instructor[3],
                            'Assigned Courses': instructor[4]
                        })

            student_data = self.load_students_from_db()
            self.write_csv(file_paths['students'], student_data,
                        ['Name', 'Age', 'Email', 'Student ID', 'Registered Courses'],
                        lambda student: {
                            'Name': student[0],
                            'Age': student[1],
                            'Email': student[2],
                            'Student ID': student[3],
                            'Registered Courses': student[4]
                        })

            QMessageBox.critical(self,"Success", "Data successfully exported to CSV files.")

        except Exception as error:
             QMessageBox.critical(self, "Error", f"An error occurred while exporting data: {str(error)}")

    def write_csv(self, filepath, data, headers, transform_row):
        with open(filepath, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            for row in data:
                writer.writerow(transform_row(row))
                    
      
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SchoolManagementApp()
    window.show()
    sys.exit(app.exec_())
