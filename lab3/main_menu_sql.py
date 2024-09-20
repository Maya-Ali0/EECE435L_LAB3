import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.simpledialog import askstring
import sqlite3

conn = sqlite3.connect('../Database/database.sqlite')
cursor = conn.cursor()
print(conn)

class SchoolManagementApp:
    """
    A GUI application for managing students, instructors, and courses in a school.

    This application allows users to add, edit, and manage records of students, instructors,
    and courses, providing an interface for interaction with a SQLite database.
    """
    def __init__(self, root):
        """
        Initializes the School Management Application.

        This method sets up the main application window and creates the menu.

        :param root: The main application window (tkinter.Tk).
        :return: None
        """
        self.root = root
        self.root.title("School Management System")
        self.root.geometry("900x600")
        self.create_menu()

    def clear_window(self):
        """
        Clears the window by destroying all its child widgets.

        This method iterates over all child widgets of the root window and destroys them.

        :return: None
        """
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def create_menu(self):
        """
        Creates the main menu with buttons to add Students, Instructors, and Courses.

        This method creates a title label and a menu frame. It then adds buttons for adding students,
        instructors, courses, registering students for courses, assigning instructors to courses, 
        displaying all records, and searching in records.

        :return: None
        """
        title_label = tk.Label(self.root, text="School Management System", font=("Arial", 18, "bold"))
        title_label.pack(pady=20)
    
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(pady=10)
    
        # Add buttons for adding students, instructors, and courses
        student_button = tk.Button(menu_frame, text="Add Student", command=self.create_student_form)
        student_button.pack(side=tk.LEFT, padx=10)
        instructor_button = tk.Button(menu_frame, text="Add Instructor", command=self.create_instructor_form)
        instructor_button.pack(side=tk.LEFT, padx=10)
        course_button = tk.Button(menu_frame, text="Add Course", command=self.create_course_form)
        course_button.pack(side=tk.LEFT, padx=10)
    
        # Add buttons for registering students for courses and assigning instructors to courses
        register_button = tk.Button(menu_frame, text="Register Student for Course", command=self.create_registration_form)
        register_button.pack(side=tk.LEFT, padx=10)
        assign_button = tk.Button(menu_frame, text="Assign Instructor to Course", command=self.create_instructor_assignment_form)
        assign_button.pack(side=tk.LEFT, padx=10)
    
        # Add buttons for displaying all records and searching in records
        display_button = tk.Button(menu_frame, text="Display All Records", command=self.display_all_records)
        display_button.pack(side=tk.LEFT, padx=10)
        search_button = tk.Button(menu_frame, text="Search in Records", command=self.create_search_form)
        search_button.pack(side=tk.LEFT, padx=10)

    def create_student_form(self):
        """
        Creates a form to add a new student.

        This method clears the current window, sets up the form layout, and defines the
        input fields for student name, age, email, and student ID.

        :return: None
        """
        self.clear_window()
        tk.Label(self.root, text="Add Student", font=("Arial", 16)).pack(pady=10)

        self.student_name_var = tk.StringVar()
        self.student_age_var = tk.IntVar()
        self.student_email_var = tk.StringVar()
        self.student_id_var = tk.StringVar()

        tk.Label(self.root, text="Name:").pack()
        tk.Entry(self.root, textvariable=self.student_name_var).pack()

        tk.Label(self.root, text="Age:").pack()
        tk.Entry(self.root, textvariable=self.student_age_var).pack()

        tk.Label(self.root, text="Email:").pack()
        tk.Entry(self.root, textvariable=self.student_email_var).pack()

        tk.Label(self.root, text="Student ID:").pack()
        tk.Entry(self.root, textvariable=self.student_id_var).pack()

        tk.Button(self.root, text="Add Student", command=self.add_student).pack(pady=10)
        tk.Button(self.root, text="Back to Menu", command=self.back_to_menu).pack(pady=10)

    def add_student(self):
        """
        Adds a new student to the database.

        This method retrieves the student's name, age, email, and ID from the input fields,
        validates the input data, and then inserts the student into the database.

        :raises ValueError: If any of the input fields are empty or invalid.
        :raises Exception: If any other error occurs during the execution of this method.

        :return: None
        """
        try:
            name = self.student_name_var.get().strip()
            age = self.student_age_var.get().strip()
            email = self.student_email_var.get().strip()
            student_id = self.student_id_var.get().strip()

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

            messagebox.showinfo("Success", "Student added successfully!")
            self.clear_window()
            self.create_menu()

        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def create_instructor_form(self):
        """
        Creates a form to add a new instructor.

        This method clears the current window, sets up a form with fields for
        instructor name, age, email, and ID, and adds buttons to add the instructor
        and return to the menu.

        :return: None
        """
        self.clear_window()
        tk.Label(self.root, text="Add Instructor", font=("Arial", 16)).pack(pady=10)

        self.instructor_name_var = tk.StringVar()
        self.instructor_age_var = tk.IntVar()
        self.instructor_email_var = tk.StringVar()
        self.instructor_id_var = tk.StringVar()

        tk.Label(self.root, text="Name:").pack()
        tk.Entry(self.root, textvariable=self.instructor_name_var).pack()

        tk.Label(self.root, text="Age:").pack()
        tk.Entry(self.root, textvariable=self.instructor_age_var).pack()

        tk.Label(self.root, text="Email:").pack()
        tk.Entry(self.root, textvariable=self.instructor_email_var).pack()

        tk.Label(self.root, text="Instructor ID:").pack()
        tk.Entry(self.root, textvariable=self.instructor_id_var).pack()

        tk.Button(self.root, text="Add Instructor", command=self.add_instructor).pack(pady=10)
        tk.Button(self.root, text="Back to Menu", command=self.back_to_menu).pack(pady=10)

    def add_instructor(self):
        """
        Adds a new instructor to the database.

        This method retrieves the instructor's name, age, email, and ID from the input fields,
        validates the input data, and then inserts the instructor into the database.

        :raises ValueError: If any of the input fields are empty or invalid.
        :raises Exception: If any other error occurs during the insertion process.

        :return: None
        """
        try:
            name = self.instructor_name_var.get().strip()
            age = self.instructor_age_var.get().strip()
            email = self.instructor_email_var.get().strip()
            instructor_id = self.instructor_id_var.get().strip()

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
                raise ValueError("Invalid email format!")

            if not instructor_id:
                raise ValueError("Instructor ID cannot be empty!")

            cursor.execute(
                "INSERT INTO instructors (instructor_id, name, age, email) VALUES (?, ?, ?, ?)",
                (instructor_id, name, age_int, email)
            )
            conn.commit()

            messagebox.showinfo("Success", "Instructor added successfully!")
            self.clear_window()
            self.create_menu()

        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def create_course_form(self):
        """
        Creates a form to add a new course.

        This method clears the current window, sets up the form layout, and defines
        the input fields for course ID and course name.

        :return: None
        """
        self.clear_window()
        tk.Label(self.root, text="Add Course", font=("Arial", 16)).pack(pady=10)

        self.course_id_var = tk.StringVar()
        self.course_name_var = tk.StringVar()

        tk.Label(self.root, text="Course ID:").pack()
        tk.Entry(self.root, textvariable=self.course_id_var).pack()

        tk.Label(self.root, text="Course Name:").pack()
        tk.Entry(self.root, textvariable=self.course_name_var).pack()

        tk.Button(self.root, text="Add Course", command=self.add_course).pack(pady=10)
        tk.Button(self.root, text="Back to Menu", command=self.back_to_menu).pack(pady=10)

    def add_course(self):
        """
        Adds a new course to the database.

        This method retrieves the course ID and course name from the input fields,
        validates the input data, and then inserts the course into the database.

        :raises ValueError: If any of the input fields are empty or invalid.
        :raises Exception: If any other error occurs during the insertion process.

        :return: None
        """
        try:
            course_id = self.course_id_var.get()
            course_name = self.course_name_var.get()

            if not course_id or not course_name:
                raise ValueError("Course ID and Course Name cannot be empty!")

            cursor.execute("INSERT INTO courses (course_id, course_name) VALUES (?, ?)", (course_id, course_name))
            conn.commit()
            messagebox.showinfo("Success", "Course added successfully!")
            self.clear_window()
            self.create_menu()
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def load_courses(self):
        """
        Loads available courses from the database.

        This method executes a query to fetch all course IDs and returns them as a list.

        :return: List of course IDs.
        :raises sqlite3.Error: If an error occurs while accessing the database.
        """
        try:
            cursor.execute("SELECT course_id FROM courses")
            courses_data = cursor.fetchall() 

            courses = [course[0] for course in courses_data]  # course[0] is the course_id from the tuple
            return courses
        
        except sqlite3.Error as e:
            print(f"An error occurred while loading courses: {e}")
            return []

        
    def create_registration_form(self):
        """
        Creates a form for students to register for available courses.

        This method clears the current window, sets up the registration form layout,
        and defines input fields for Student ID and available courses.

        :return: None
        """
        self.clear_window()
        tk.Label(self.root, text="Register Student for Course", font=("Arial", 16)).pack(pady=10)

        self.student_id_var = tk.StringVar()
        self.selected_course_var = tk.StringVar()

        tk.Label(self.root, text="Student ID:").pack()
        tk.Entry(self.root, textvariable=self.student_id_var).pack()

        tk.Label(self.root, text="Select Course:").pack()
        available_courses = self.load_courses()

        self.course_dropdown = ttk.Combobox(self.root, textvariable=self.selected_course_var, values=available_courses)
        self.course_dropdown.pack(pady=10)

        tk.Button(self.root, text="Register", command=self.register_student_for_course).pack(pady=10)
        tk.Button(self.root, text="Back to Menu", command=self.back_to_menu).pack(pady=10)
    
    def register_student_for_course(self):
        """
        Registers the student for the selected course.

        This method retrieves the Student ID and selected course, validates them,
        and then inserts the registration into the student_courses table.

        :raises Exception: If the student ID or course is invalid or if any other error occurs.
        :return: None
        """
        student_id = self.student_id_var.get()
        selected_course = self.selected_course_var.get()

        if not student_id or not selected_course:
            messagebox.showerror("Error", "Both Student ID and Course must be selected!")
            return
        
        try:
            cursor.execute("SELECT student_id FROM students WHERE student_id = ?", (student_id,))
            student_data = cursor.fetchone()
            cursor.execute("SELECT course_id FROM courses WHERE course_id = ?", (selected_course,))
            course_data = cursor.fetchone()

            if student_data is not None and course_data is not None:
                cursor.execute("INSERT INTO student_courses (student_id, course_id) VALUES (?, ?);", (student_id, selected_course,))
                messagebox.showinfo("Success", f"Student {student_id} registered for {selected_course}")
                conn.commit()
            else:
                messagebox.showerror("Error", "Student or course doesn't exist.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

        self.clear_window()
        self.create_menu()

    def create_instructor_assignment_form(self):
        """
        Creates a form for assigning an instructor to a course.

        This method clears the current window, sets up the assignment form layout,
        and defines input fields for Instructor ID and available courses.

        :return: None
        """
        self.clear_window()
        tk.Label(self.root, text="Assign Instructor to Course", font=("Arial", 16)).pack(pady=10)

        self.instructor_id_var = tk.StringVar()
        tk.Label(self.root, text="Enter Instructor ID:").pack()
        tk.Entry(self.root, textvariable=self.instructor_id_var).pack(pady=10)

        self.selected_course_var = tk.StringVar()

        tk.Label(self.root, text="Select Course:").pack()
        available_courses = self.load_courses()

        self.course_dropdown = ttk.Combobox(self.root, textvariable=self.selected_course_var, values=available_courses)
        self.course_dropdown.pack(pady=10)

        tk.Button(self.root, text="Assign", command=self.assign_instructor_to_course).pack(pady=10)
        tk.Button(self.root, text="Back to Menu", command=self.back_to_menu).pack(pady=10)

    def assign_instructor_to_course(self):
        """
        Assigns the manually entered instructor to the selected course.

        This method retrieves the Instructor ID and selected course, validates them,
        and updates the course to assign the instructor.

        :raises ValueError: If the instructor ID or course is not found.
        :raises Exception: If any other error occurs during the assignment process.
        :return: None
        """
        instructor_id = self.instructor_id_var.get()
        course_id = self.selected_course_var.get()

        if not instructor_id or not course_id:
            messagebox.showerror("Error", "Both Instructor ID and Course must be provided!")
            return

        try:
            cursor.execute("SELECT instructor_id FROM instructors WHERE instructor_id = ?", (instructor_id,))
            instructor_data = cursor.fetchone()
            cursor.execute("SELECT course_id FROM courses WHERE course_id = ?", (course_id,))
            course_data = cursor.fetchone()

            if course_data is None:
                raise ValueError(f"Course with ID '{course_id}' not found.")
            if instructor_data is None:
                raise ValueError(f"Instructor with ID '{instructor_id}' not found.")

            cursor.execute("SELECT instructor_id FROM courses WHERE course_id = ?", (course_id,))
            inst_course = cursor.fetchone()

            if inst_course and inst_course[0] is not None:
                messagebox.showerror("Error", "Course already has an instructor.")
            else:
                cursor.execute("UPDATE courses SET instructor_id = ? WHERE course_id = ?", (instructor_id, course_id,))
                messagebox.showinfo("Success", f"Instructor {instructor_id} assigned to course {course_id}")
                conn.commit()
        
        except Exception as e:
            messagebox.showerror("Error", str(e))

        self.clear_window()
        self.create_menu()

    def display_all_records(self):
        """
        Displays all students, instructors, and courses in a tabular format using a Treeview widget.

        This method creates a notebook with three tabs: Students, Instructors, and Courses.
        Each tab contains a Treeview that lists records and provides buttons for editing and deleting.

        :return: None
        """
        self.clear_window()
        tk.Label(self.root, text="All Records", font=("Arial", 16)).pack(pady=10)

        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill='both')

        # Frame for Students
        student_frame = ttk.Frame(notebook)
        notebook.add(student_frame, text="Students")
        
        student_tree = ttk.Treeview(student_frame, columns=("ID", "Name", "Age", "Email", "Courses"), show="headings")
        student_tree.heading("ID", text="Student ID")
        student_tree.heading("Name", text="Name")
        student_tree.heading("Age", text="Age")
        student_tree.heading("Email", text="Email")
        student_tree.heading("Courses", text="Courses")
        student_tree.pack(expand=True, fill="both")

        # Load students data
        try:
            cursor.execute("SELECT * FROM students;")
            students = cursor.fetchall()
            
            for student in students:
                cursor.execute("SELECT course_id FROM student_courses WHERE student_id = ?", (student[0],))
                courses = cursor.fetchall()
                course_ids = [course[0] for course in courses]  # Extract course IDs

                student_tree.insert("", "end", values=(student[0], student[1], student[2], student[3], course_ids))

        except Exception as e:
            messagebox.showerror("Error", str(e))

        # Edit and Delete buttons for Students
        student_buttons_frame = tk.Frame(student_frame)
        student_buttons_frame.pack(pady=10)
        tk.Button(student_buttons_frame, text="Edit Student", command=lambda: self.edit_record(student_tree, "student")).pack(side=tk.LEFT, padx=5)
        tk.Button(student_buttons_frame, text="Delete Student", command=lambda: self.delete_record(student_tree, "student")).pack(side=tk.LEFT, padx=5)

        # Frame for Instructors
        instructor_frame = ttk.Frame(notebook)
        notebook.add(instructor_frame, text="Instructors")

        instructor_tree = ttk.Treeview(instructor_frame, columns=("ID", "Name", "Age", "Email", "Courses"), show="headings")
        instructor_tree.heading("ID", text="Instructor ID")
        instructor_tree.heading("Name", text="Name")
        instructor_tree.heading("Age", text="Age")
        instructor_tree.heading("Email", text="Email")
        instructor_tree.heading("Courses", text="Courses")
        instructor_tree.pack(expand=True, fill="both")

        # Load instructors data
        try:
            cursor.execute("SELECT * FROM instructors;")
            instructors = cursor.fetchall()
            
            for instructor in instructors:
                cursor.execute("SELECT course_id FROM courses WHERE instructor_id = ?", (instructor[0],))
                courses = cursor.fetchall()
                course_ids = [course[0] for course in courses]

                instructor_tree.insert("", "end", values=(instructor[0], instructor[1], instructor[2], instructor[3], course_ids))

        except Exception as e:
            messagebox.showerror("Error", str(e))

        # Edit and Delete buttons for Instructors
        instructor_buttons_frame = tk.Frame(instructor_frame)
        instructor_buttons_frame.pack(pady=10)
        tk.Button(instructor_buttons_frame, text="Edit Instructor", command=lambda: self.edit_record(instructor_tree, "instructor")).pack(side=tk.LEFT, padx=5)
        tk.Button(instructor_buttons_frame, text="Delete Instructor", command=lambda: self.delete_record(instructor_tree, "instructor")).pack(side=tk.LEFT, padx=5)

        # Frame for Courses
        course_frame = ttk.Frame(notebook)
        notebook.add(course_frame, text="Courses")

        course_tree = ttk.Treeview(course_frame, columns=("ID", "Name", "Instructor", "Enrolled Students"), show="headings")
        course_tree.heading("ID", text="Course ID")
        course_tree.heading("Name", text="Course Name")
        course_tree.heading("Instructor", text="Instructor ID")
        course_tree.heading("Enrolled Students", text="Enrolled Students")
        course_tree.pack(expand=True, fill="both")

        # Load courses data
        try:
            cursor.execute("SELECT * FROM courses;")
            courses = cursor.fetchall()
            
            for course in courses:
                cursor.execute("SELECT student_id FROM student_courses WHERE course_id = ?", (course[0],))
                students = cursor.fetchall()
                student_ids = [student[0] for student in students]

                course_tree.insert("", "end", values=(course[0], course[1], course[2], student_ids))

        except Exception as e:
            messagebox.showerror("Error", str(e))

        # Edit and Delete buttons for Courses
        course_buttons_frame = tk.Frame(course_frame)
        course_buttons_frame.pack(pady=10)
        tk.Button(course_buttons_frame, text="Edit Course", command=lambda: self.edit_record(course_tree, "course")).pack(side=tk.LEFT, padx=5)
        tk.Button(course_buttons_frame, text="Delete Course", command=lambda: self.delete_record(course_tree, "course")).pack(side=tk.LEFT, padx=5)

        tk.Button(self.root, text="Back to Menu", command=self.back_to_menu).pack(pady=10)

    def back_to_menu(self):
        """
        Clears the window and brings back the main menu.

        This method is used to reset the current view and display the main menu.

        :return: None
        """
        self.clear_window()  
        self.create_menu() 

    def create_search_form(self):
        """
        Creates a search form to filter and display records by name, ID, or course.

        This method sets up the search interface, allowing the user to specify search criteria
        and a search term. The user can select which category (students, instructors, courses) to search.

        :return: None
        """
        self.clear_window()
        
        tk.Label(self.root, text="Search Records", font=("Arial", 16)).pack(pady=10)

        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)

        search_by_label = tk.Label(form_frame, text="Search by:")
        search_by_label.grid(row=0, column=0, padx=10, pady=5)

        self.search_by_var = tk.StringVar(value="Name")
        search_by_dropdown = ttk.Combobox(form_frame, textvariable=self.search_by_var, values=["Name", "ID"])
        search_by_dropdown.grid(row=0, column=1, padx=10, pady=5)

        search_term_label = tk.Label(form_frame, text="Enter Search Term:")
        search_term_label.grid(row=1, column=0, padx=10, pady=5)

        self.search_term_var = tk.StringVar()
        search_term_entry = tk.Entry(form_frame, textvariable=self.search_term_var)
        search_term_entry.grid(row=1, column=1, padx=10, pady=5)

        search_category_label = tk.Label(form_frame, text="Search in:")
        search_category_label.grid(row=2, column=0, padx=10, pady=5)

        self.search_category_var = tk.StringVar(value="Students")
        search_category_dropdown = ttk.Combobox(form_frame, textvariable=self.search_category_var, values=["Students", "Instructors", "Courses"])
        search_category_dropdown.grid(row=2, column=1, padx=10, pady=5)

        search_button = tk.Button(self.root, text="Search", command=self.search_records)
        search_button.pack(pady=10)
        tk.Button(self.root, text="Back to Menu", command=self.back_to_menu).pack(pady=10)

    def search_records(self):
        """
        Filters and displays records based on the search criteria.

        This method executes the search based on the selected category and criteria,
        retrieving relevant records from the database and displaying them in a Treeview.

        :return: None
        """
        search_by = self.search_by_var.get()  
        search_term = self.search_term_var.get()
        category = self.search_category_var.get()  

        if not search_term:
            messagebox.showerror("Error", "Search term cannot be empty!")
            return

        self.clear_window()
        result_tree = ttk.Treeview(self.root, show="headings")

        if category == "Students":
            result_tree["columns"] = ("ID", "Name", "Age", "Email", "Courses")
            result_tree.heading("ID", text="Student ID")
            result_tree.heading("Name", text="Name")
            result_tree.heading("Age", text="Age")
            result_tree.heading("Email", text="Email")
            result_tree.heading("Courses", text="Courses")

            if search_by == "Name":
                cursor.execute("SELECT * FROM students WHERE name = ?", (search_term,))
                students = cursor.fetchall()
                for student in students:
                    cursor.execute("SELECT course_id FROM student_courses WHERE student_id = ?", (student[0],))
                    courses = cursor.fetchall()
                    course_ids = [course[0] for course in courses]
                    result_tree.insert("", "end", values=(student[0], student[1], student[2], student[3], course_ids))

            if search_by == "ID":
                cursor.execute("SELECT * FROM students WHERE student_id = ?", (search_term,))
                students = cursor.fetchall()
                for student in students:
                    cursor.execute("SELECT course_id FROM student_courses WHERE student_id = ?", (student[0],))
                    courses = cursor.fetchall()
                    course_ids = [course[0] for course in courses]
                    result_tree.insert("", "end", values=(student[0], student[1], student[2], student[3], course_ids))

        elif category == "Instructors":
            result_tree["columns"] = ("ID", "Name", "Age", "Email", "Assigned Courses")
            result_tree.heading("ID", text="Instructor ID")
            result_tree.heading("Name", text="Name")
            result_tree.heading("Age", text="Age")
            result_tree.heading("Email", text="Email")
            result_tree.heading("Assigned Courses", text="Assigned Courses")

            if search_by == "Name":
                cursor.execute("SELECT * FROM instructors WHERE name = ?", (search_term,))
                instructors = cursor.fetchall()
                for instructor in instructors:
                    cursor.execute("SELECT course_id FROM courses WHERE instructor_id = ?", (instructor[0],))
                    courses = cursor.fetchall()
                    course_ids = [course[0] for course in courses]
                    result_tree.insert("", "end", values=(instructor[0], instructor[1], instructor[2], instructor[3], course_ids))

            if search_by == "ID":
                cursor.execute("SELECT * FROM instructors WHERE instructor_id = ?", (search_term,))
                instructors = cursor.fetchall()
                for instructor in instructors:
                    cursor.execute("SELECT course_id FROM courses WHERE instructor_id = ?", (instructor[0],))
                    courses = cursor.fetchall()
                    course_ids = [course[0] for course in courses]
                    result_tree.insert("", "end", values=(instructor[0], instructor[1], instructor[2], instructor[3], course_ids))

        elif category == "Courses":
            result_tree["columns"] = ("ID", "Name", "Instructor", "Enrolled Students")
            result_tree.heading("ID", text="Course ID")
            result_tree.heading("Name", text="Course Name")
            result_tree.heading("Instructor", text="Instructor ID")
            result_tree.heading("Enrolled Students", text="Enrolled Students")

            if search_by == "Name":
                cursor.execute("SELECT * FROM courses WHERE course_name = ?", (search_term,))
                courses = cursor.fetchall()
                for course in courses:
                    result_tree.insert("", "end", values=(course[0], course[1], course[2], []))  # No enrolled students

            if search_by == "ID":
                cursor.execute("SELECT * FROM courses WHERE course_id = ?", (search_term,))
                courses = cursor.fetchall()
                for course in courses:
                    result_tree.insert("", "end", values=(course[0], course[1], course[2], []))  # No enrolled students

        result_tree.pack(expand=True, fill="both")

        tk.Button(self.root, text="Back to Menu", command=self.back_to_menu).pack(pady=10)
        tk.Button(self.root, text="Search Again", command=self.create_search_form).pack(pady=10)

    def edit_record(self, tree, record_type):
        """
        Edits a selected record in the specified category (student, instructor, or course).

        This method prompts the user to enter new details for the selected record. If the user
        enters 'NA', the current value is retained. Updates are reflected in both the database 
        and the Treeview.

        :param tree: The Treeview widget containing the records.
        :param record_type: The type of record to edit ("student", "instructor", or "course").
        :return: None
        """
        selected_item = tree.selection()

        if not selected_item:
            messagebox.showwarning("No selection", "Please select a record to edit.")
            return

        record_id = tree.item(selected_item, 'values')[0]

        if record_type == "student":
            try:
                cursor.execute("SELECT * FROM students WHERE student_id = ?", (record_id,))
                student_data = cursor.fetchone()
                
                if not student_data:
                    messagebox.showerror("Error", "Student not found.")
                    return

                current_name, current_age, current_email = student_data[1], student_data[2], student_data[3]
                
                new_name = askstring("Edit Student", f"Enter new name (current: {current_name}, enter 'NA' to keep current):")
                new_age = askstring("Edit Student", f"Enter new age (current: {current_age}, enter 'NA' to keep current):")
                new_email = askstring("Edit Student", f"Enter new email (current: {current_email}, enter 'NA' to keep current):")

                if new_name and new_name != "NA":
                    cursor.execute("UPDATE students SET name = ? WHERE student_id = ?", (new_name, record_id))
                if new_age and new_age != "NA":
                    try:
                        cursor.execute("UPDATE students SET age = ? WHERE student_id = ?", (int(new_age), record_id))
                    except ValueError:
                        messagebox.showwarning("Invalid Input", "Age must be an integer. No changes made to age.")
                if new_email and new_email != "NA":
                    cursor.execute("UPDATE students SET email = ? WHERE student_id = ?", (new_email, record_id))

                conn.commit()
                tree.item(selected_item, values=(record_id, new_name if new_name != "NA" else current_name, new_age if new_age != "NA" else current_age, new_email if new_email != "NA" else current_email))
                messagebox.showinfo("Success", "Student updated successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to edit student: {str(e)}")

        elif record_type == "instructor":
            try:
                cursor.execute("SELECT * FROM instructors WHERE instructor_id = ?", (record_id,))
                instructor_data = cursor.fetchone()

                if not instructor_data:
                    messagebox.showerror("Error", "Instructor not found.")
                    return

                current_name, current_age, current_email = instructor_data[1], instructor_data[2], instructor_data[3]

                new_name = askstring("Edit Instructor", f"Enter new name (current: {current_name}, enter 'NA' to keep current):")
                new_age = askstring("Edit Instructor", f"Enter new age (current: {current_age}, enter 'NA' to keep current):")
                new_email = askstring("Edit Instructor", f"Enter new email (current: {current_email}, enter 'NA' to keep current):")

                if new_name and new_name != "NA":
                    cursor.execute("UPDATE instructors SET name = ? WHERE instructor_id = ?", (new_name, record_id))
                if new_age and new_age != "NA":
                    try:
                        cursor.execute("UPDATE instructors SET age = ? WHERE instructor_id = ?", (int(new_age), record_id))
                    except ValueError:
                        messagebox.showwarning("Invalid Input", "Age must be an integer. No changes made to age.")
                if new_email and new_email != "NA":
                    cursor.execute("UPDATE instructors SET email = ? WHERE instructor_id = ?", (new_email, record_id))

                conn.commit()
                tree.item(selected_item, values=(record_id, new_name if new_name != "NA" else current_name, new_age if new_age != "NA" else current_age, new_email if new_email != "NA" else current_email))
                messagebox.showinfo("Success", "Instructor updated successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to edit instructor: {str(e)}")

        elif record_type == "course":
            try:
                cursor.execute("SELECT * FROM courses WHERE course_id = ?", (record_id,))
                course_data = cursor.fetchone()

                if not course_data:
                    messagebox.showerror("Error", "Course not found.")
                    return

                current_name, current_instructor = course_data[1], course_data[2]

                new_name = askstring("Edit Course", f"Enter new name (current: {current_name}, enter 'NA' to keep current):")
                new_instructor = askstring("Edit Course", f"Enter new instructor ID (current: {current_instructor}, enter 'NA' to keep current):")

                if new_name and new_name != "NA":
                    cursor.execute("UPDATE courses SET course_name = ? WHERE course_id = ?", (new_name, record_id))
                if new_instructor and new_instructor != "NA":
                    cursor.execute("UPDATE courses SET instructor = ? WHERE course_id = ?", (new_instructor, record_id))

                conn.commit()
                tree.item(selected_item, values=(record_id, new_name if new_name != "NA" else current_name, new_instructor if new_instructor != "NA" else current_instructor))
                messagebox.showinfo("Success", "Course updated successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to edit course: {str(e)}")

    def delete_record(self, tree, record_type):
        """
        Deletes a selected record from the specified category (student, instructor, or course).

        This method prompts the user for confirmation before proceeding with the deletion. 
        Upon successful deletion, the record is removed from both the database and the Treeview.

        :param tree: The Treeview widget containing the records.
        :param record_type: The type of record to delete ("student", "instructor", or "course").
        :return: None
        """
        selected_item = tree.selection()

        if not selected_item:
            messagebox.showwarning("No selection", "Please select a record to delete.")
            return

        confirm = messagebox.askyesno("Delete", "Are you sure you want to delete this record?")
        if not confirm:
            return

        selected_id = tree.item(selected_item, 'values')[0]  
        
        try:
            if record_type == "student":
                cursor.execute("DELETE from students where student_id = ?", (selected_id,))
                conn.commit()

            elif record_type == "instructor":
                cursor.execute("DELETE from instructors where instructor_id = ?", (selected_id,))
                conn.commit()

            elif record_type == "course":
                cursor.execute("DELETE from courses where course_id = ?", (selected_id,))
                conn.commit()
        
            tree.delete(selected_item)
            messagebox.showinfo("Success", f"{record_type.capitalize()} deleted successfully!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete {record_type}: {str(e)}")



if __name__ == "__main__":
    root = tk.Tk()
    app = SchoolManagementApp(root)
    root.mainloop()
