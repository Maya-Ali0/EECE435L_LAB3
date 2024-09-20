import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.simpledialog import askstring
from Classes.Course import Course
from Classes.Instructor import Instructor
from Classes.Student import Student
import json

class SchoolManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("School Management System")
        self.root.geometry("900x600")

        self.create_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def create_menu(self):
        """Creates the main menu with buttons to add Students, Instructors, and Courses"""
        title_label = tk.Label(self.root, text="School Management System", font=("Arial", 18, "bold"))
        title_label.pack(pady=20)

        menu_frame = tk.Frame(self.root)
        menu_frame.pack(pady=10)


        student_button = tk.Button(menu_frame, text="Add Student", command=self.create_student_form)
        student_button.pack(side=tk.LEFT, padx=10)

        instructor_button = tk.Button(menu_frame, text="Add Instructor", command=self.create_instructor_form)
        instructor_button.pack(side=tk.LEFT, padx=10)

        course_button = tk.Button(menu_frame, text="Add Course", command=self.create_course_form)
        course_button.pack(side=tk.LEFT, padx=10)

        register_button = tk.Button(menu_frame, text="Register Student for Course", command=self.create_registration_form)
        register_button.pack(side=tk.LEFT, padx=10)

        assign_button = tk.Button(menu_frame, text="Assign Instructor to Course", command=self.create_instructor_assignment_form)
        assign_button.pack(side=tk.LEFT, padx=10)

        assign_button = tk.Button(menu_frame, text="Display All Records", command=self.display_all_records)
        assign_button.pack(side=tk.LEFT, padx=10)

        assign_button = tk.Button(menu_frame, text="Search in Records", command=self.create_search_form)
        assign_button.pack(side=tk.LEFT, padx=10)
        

    def create_student_form(self):
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
        try:
            name = self.student_name_var.get()
            age = self.student_age_var.get()
            email = self.student_email_var.get()
            student_id = self.student_id_var.get()

            student = Student(name, age, email, student_id)
            student.save_to_json('./Serialization/Student.json')  
            messagebox.showinfo("Success", "Student added successfully!")
            self.clear_window()
            self.create_menu()
            
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))


    def create_instructor_form(self):
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
        try:
            name = self.instructor_name_var.get()
            age = self.instructor_age_var.get()
            email = self.instructor_email_var.get()
            instructor_id = self.instructor_id_var.get()

           
            instructor = Instructor(name, age, email, instructor_id)
            instructor.save_to_json('./Serialization/Instructor.json') 
            messagebox.showinfo("Success", "Instructor added successfully!")
            self.clear_window()
            self.create_menu()
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))

    def create_course_form(self):
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
        try:
            course_id = self.course_id_var.get()
            course_name = self.course_name_var.get()

            course = Course(course_id, course_name, None)
            course.save_to_json('./Serialization/Course.json')  
            messagebox.showinfo("Success", "Course added successfully!")
            self.clear_window()
            self.create_menu()
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))

    def load_courses(self):
        """Loads available courses from a JSON file."""
        try:
            with open('./Serialization/Course.json', 'r') as file:
                courses_data = json.load(file)
            courses = [course['course_id'] for course in courses_data]
            return courses
        except FileNotFoundError:
            return []
        
    def create_registration_form(self):
        """Creates a form for students to register for available courses."""
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
    
    def register_student_for_course(self):
        """Registers the student for the selected course."""
        student_id = self.student_id_var.get()
        selected_course = self.selected_course_var.get()
        print(selected_course)

        if not student_id or not selected_course:
            messagebox.showerror("Error", "Both Student ID and Course must be selected!")
            return
        else:
            try:
                student = self.search_student_by_id(student_id)
                course = self.search_course_by_id(selected_course)

                for students in course.enrolled_students:
                    if students == student_id:
                        raise ValueError("Student already enrolled.")
                    
                course.add_student(student)
                messagebox.showinfo("Success", f"Student {student_id} registered for {selected_course}")
            except Exception as e:
                messagebox.showerror("Error")

        
        tk.Button(self.root, text="Back to Menu", command=self.back_to_menu).pack(pady=10)
        self.clear_window()
        self.create_menu()
           
    def create_instructor_assignment_form(self):
        """Creates a form for assigning an instructor to a course."""
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
        """Assigns the manually entered instructor to the selected course."""
        instructor_id = self.instructor_id_var.get()
        course_id = self.selected_course_var.get()

        if not instructor_id or not course_id:
            messagebox.showerror("Error", "Both Instructor ID and Course must be provided!")
            return

        try:
            course = self.search_course_by_id(course_id)
            instructor = Instructor.load_instructor_by_id(Instructor, './Serialization/Instructor.json', instructor_id)

            if course is None:
                raise ValueError(f"Course with ID '{course_id}' not found.")
            if instructor is None:
                raise ValueError(f"Instructor with ID '{instructor_id}' not found.")
            
            
            instructor.assign_course(course)
            messagebox.showinfo("Success", f"Instructor {instructor_id} assigned to course {course_id}")

        
        except Exception as e:
            messagebox.showerror("Error", str(e))

        self.clear_window()
        self.create_menu()


    def display_all_records(self):
        """Displays all students, instructors, and courses in a tabular format using a Treeview widget."""
        self.clear_window()
        tk.Label(self.root, text="All Records", font=("Arial", 16)).pack(pady=10)

        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill='both')

        # Frame for Students
        student_frame = ttk.Frame(notebook)
        notebook.add(student_frame, text="Students")
        
        student_tree = ttk.Treeview(student_frame, columns=("ID", "Name", "Age", "Email"), show="headings")
        student_tree.heading("ID", text="Student ID")
        student_tree.heading("Name", text="Name")
        student_tree.heading("Age", text="Age")
        student_tree.heading("Email", text="Email")
        student_tree.pack(expand=True, fill="both")

        # Load students data
        try:
            students = Student.load_from_json('./Serialization/Student.json') 
            for student in students:
                student_tree.insert("", "end", values=(student.student_id, student.name, student.age, student._email))
        except FileNotFoundError:
            print("Student JSON file not found")
        except json.JSONDecodeError as e:
            print(f"Error reading student JSON file: {e}")

        # Edit and Delete buttons for Students
        student_buttons_frame = tk.Frame(student_frame)
        student_buttons_frame.pack(pady=10)
        tk.Button(student_buttons_frame, text="Edit Student", command=lambda: self.edit_record(student_tree, "student")).pack(side=tk.LEFT, padx=5)
        tk.Button(student_buttons_frame, text="Delete Student", command=lambda: self.delete_record(student_tree, "student")).pack(side=tk.LEFT, padx=5)

        # Frame for Instructors
        instructor_frame = ttk.Frame(notebook)
        notebook.add(instructor_frame, text="Instructors")

        instructor_tree = ttk.Treeview(instructor_frame, columns=("ID", "Name", "Age", "Email"), show="headings")
        instructor_tree.heading("ID", text="Instructor ID")
        instructor_tree.heading("Name", text="Name")
        instructor_tree.heading("Age", text="Age")
        instructor_tree.heading("Email", text="Email")
        instructor_tree.pack(expand=True, fill="both")

        # Load instructors data
        try:
            instructors = Instructor.load_from_json('./Serialization/Instructor.json')
            for instructor in instructors:
                instructor_tree.insert("", "end", values=(instructor.instructor_id, instructor.name, instructor.age, instructor._email))
        except FileNotFoundError:
            print("Instructor JSON file not found")
        except json.JSONDecodeError as e:
            print(f"Error reading instructor JSON file: {e}")

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
            courses = Course.load_from_json('./Serialization/Course.json')
            for course in courses:
                enrolled_students = ', '.join([student_id for student_id in course.enrolled_students])
                course_tree.insert("", "end", values=(course.course_id, course.course_name, course.instructor , enrolled_students))
        except FileNotFoundError:
            print("Course JSON file not found")
        except json.JSONDecodeError as e:
            print(f"Error reading course JSON file: {e}")

        # Edit and Delete buttons for Courses
        course_buttons_frame = tk.Frame(course_frame)
        course_buttons_frame.pack(pady=10)
        tk.Button(course_buttons_frame, text="Edit Course", command=lambda: self.edit_record(course_tree, "course")).pack(side=tk.LEFT, padx=5)
        tk.Button(course_buttons_frame, text="Delete Course", command=lambda: self.delete_record(course_tree, "course")).pack(side=tk.LEFT, padx=5)

        tk.Button(self.root, text="Back to Menu", command=self.back_to_menu).pack(pady=10)

    
    def back_to_menu(self):
        """Clears the window and brings back the main menu."""
        self.clear_window()  
        self.create_menu() 

    def create_search_form(self):
        """Creates a search form to filter and display records by name, ID, or course."""
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
        """Filters and displays records based on the search criteria."""
        search_by = self.search_by_var.get()  
        search_term = self.search_term_var.get().lower()
        category = self.search_category_var.get()  

        if not search_term:
            messagebox.showerror("Error", "Search term cannot be empty!")
            return

        self.clear_window()
        result_tree = ttk.Treeview(self.root, show="headings")

        if category == "Students":
            result_tree["columns"] = ("ID", "Name", "Age", "Email")
            result_tree.heading("ID", text="Student ID")
            result_tree.heading("Name", text="Name")
            result_tree.heading("Age", text="Age")
            result_tree.heading("Email", text="Email")

            students = Student.load_from_json('./Serialization/Student.json')

            for student in students:
                if (search_by == "Name" and search_term in student.name.lower()) or \
                        (search_by == "ID" and search_term == student.student_id.lower()):
                    result_tree.insert("", "end", values=(student.student_id, student.name, student.age, student._email))

        elif category == "Instructors":
            result_tree["columns"] = ("ID", "Name", "Age", "Email", "Assigned Courses")
            result_tree.heading("ID", text="Instructor ID")
            result_tree.heading("Name", text="Name")
            result_tree.heading("Age", text="Age")
            result_tree.heading("Email", text="Email")
            result_tree.heading("Assigned Courses", text="Assigned Courses")

            instructors = Instructor.load_from_json('./Serialization/Instructor.json')

            for instructor in instructors:
                assigned_courses = ', '.join([course_id for course_id in instructor.assigned_courses])
                if (search_by == "Name" and search_term in instructor.name.lower()) or \
                        (search_by == "ID" and (search_term == instructor.instructor_id.lower() or search_term in assigned_courses.lower())):
                    result_tree.insert("", "end", values=(instructor.instructor_id, instructor.name, instructor.age, instructor._email, assigned_courses))

        elif category == "Courses":
            result_tree["columns"] = ("ID", "Name", "Instructor", "Enrolled Students")
            result_tree.heading("ID", text="Course ID")
            result_tree.heading("Name", text="Course Name")
            result_tree.heading("Instructor", text="Instructor ID")
            result_tree.heading("Enrolled Students", text="Enrolled Students")

            courses = Course.load_from_json('./Serialization/Course.json')

            for course in courses:
                if (search_by == "Name" and search_term in course.course_name.lower()) or \
                        (search_by == "ID" and search_term == course.course_id.lower()):
                    enrolled_students = ', '.join([student_id for student_id in course.enrolled_students])
                    result_tree.insert("", "end", values=(course.course_id, course.course_name, course.instructor, enrolled_students))

        result_tree.pack(expand=True, fill="both")

        tk.Button(self.root, text="Back to Menu", command=self.back_to_menu).pack(pady=10)
        tk.Button(self.root, text="Search Again", command=self.create_search_form).pack(pady=10)


    def edit_record(self, tree, record_type):
        selected_item = tree.selection()

        if not selected_item:
            messagebox.showwarning("No selection", "Please select a record to edit.")
            return

        record_id = tree.item(selected_item, 'values')[0]

        if record_type == "student":
            try:
                students = Student.load_from_json('./Serialization/Student.json')
                student = next(student for student in students if student.student_id == record_id)

                new_name = askstring("Edit Student", f"Enter new name (current: {student.name}, enter 'NA' to keep current):")
                new_age = askstring("Edit Student", f"Enter new age (current: {student.age}, enter 'NA' to keep current):")
                new_email = askstring("Edit Student", f"Enter new email (current: {student._email}, enter 'NA' to keep current):")

                if new_name and new_name != "NA":
                    student.name = new_name
                if new_age and new_age != "NA":
                    try:
                        student.age = int(new_age) 
                    except ValueError:
                        messagebox.showwarning("Invalid Input", "Age must be an integer. No changes made to age.")
                        new_age = None  
                if new_email and new_email != "NA":
                    student._email = new_email

                with open('./Serialization/Student.json', 'w') as file:
                    json.dump([s.to_dict() for s in students], file, indent=4)

                tree.item(selected_item, values=(student.student_id, student.name, student.age, student._email))
                messagebox.showinfo("Success", "Student updated successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to edit student: {str(e)}")

        elif record_type == "instructor":
            try:
                instructors = Instructor.load_from_json('./Serialization/Instructor.json')
                instructor = next(instructor for instructor in instructors if instructor.instructor_id == record_id)

                new_name = askstring("Edit Instructor", f"Enter new name (current: {instructor.name}, enter 'NA' to keep current):")
                new_age = askstring("Edit Instructor", f"Enter new age (current: {instructor.age}, enter 'NA' to keep current):")
                new_email = askstring("Edit Instructor", f"Enter new email (current: {instructor._email}, enter 'NA' to keep current):")

                if new_name and new_name != "NA":
                    instructor.name = new_name
                if new_age and new_age != "NA":
                    try:
                        instructor.age = int(new_age)  # Convert to integer
                    except ValueError:
                        messagebox.showwarning("Invalid Input", "Age must be an integer. No changes made to age.")
                        new_age = None  # Reset new_age to None to avoid saving invalid data
                if new_email and new_email != "NA":
                    instructor._email = new_email

                with open('./Serialization/Instructor.json', 'w') as file:
                    json.dump([i.to_dict() for i in instructors], file, indent=4)

                tree.item(selected_item, values=(instructor.instructor_id, instructor.name, instructor.age, instructor._email))
                messagebox.showinfo("Success", "Instructor updated successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to edit instructor: {str(e)}")

        elif record_type == "course":
            try:
                courses = Course.load_from_json('./Serialization/Course.json')
                course = next(course for course in courses if course.course_id == record_id)

                new_name = askstring("Edit Course", f"Enter new name (current: {course.course_name}, enter 'NA' to keep current):")
                new_instructor = askstring("Edit Course", f"Enter new instructor ID (current: {course.instructor}, enter 'NA' to keep current):")

                if new_name and new_name != "NA":
                    course.course_name = new_name
                if new_instructor and new_instructor != "NA":
                    course.instructor = new_instructor

                with open('./Serialization/Course.json', 'w') as file:
                    json.dump([c.to_dict() for c in courses], file, indent=4)

                enrolled_students = ', '.join([student_id for student_id in course.enrolled_students])
                tree.item(selected_item, values=(course.course_id, course.course_name, course.instructor, enrolled_students))
                messagebox.showinfo("Success", "Course updated successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to edit course: {str(e)}")

    def delete_record(self, tree, record_type):
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
                students = Student.load_from_json('./Serialization/Student.json')
                updated_students = [student for student in students if student.student_id != selected_id]
                with open('./Serialization/Student.json', 'w') as file:
                    json.dump([student.to_dict() for student in updated_students], file, indent=4)

            elif record_type == "instructor":
                instructors = Instructor.load_from_json('./Serialization/Instructor.json')
                updated_instructors = [instructor for instructor in instructors if instructor.instructor_id != selected_id]
                with open('./Serialization/Instructor.json', 'w') as file:
                    json.dump([instructor.to_dict() for instructor in updated_instructors], file, indent=4)

            elif record_type == "course":
                courses = Course.load_from_json('./Serialization/Course.json')
                updated_courses = [course for course in courses if course.course_id != selected_id]
                with open('./Serialization/Course.json', 'w') as file:
                    json.dump([course.to_dict() for course in updated_courses], file, indent=4)

        
            tree.delete(selected_item)
            messagebox.showinfo("Success", f"{record_type.capitalize()} deleted successfully!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete {record_type}: {str(e)}")




if __name__ == "__main__":
    root = tk.Tk()
    app = SchoolManagementApp(root)
    root.mainloop()
