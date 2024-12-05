import os
import tkinter as tk
from tkinter import messagebox


FILE_PATH = (r"C:\Users\rexte\OneDrive\Obsidian Files\Creative Computing Year 1\Code Lab YR 1 SEM 1\web dev\Web-Dev-1-Set-exercises\skills-portfolio-RexJial020\A1 - Skills Portfolio\Exercise3\studentMarks.txt")


def load_data(file_path):
    students = []
    with open(file_path, "r") as file:
        lines = file.readlines()
        num_students = int(lines[0].strip())
        for line in lines[1:]:
            parts = line.strip().split(",")
            student_number = int(parts[0])
            name = parts[1]
            coursework = list(map(int, parts[2:5]))
            exam_mark = int(parts[5])
            students.append({
                "student_number": student_number,
                "name": name,
                "coursework": coursework,
                "exam_mark": exam_mark,
                "total_coursework": sum(coursework),
                "overall_score": sum(coursework) + exam_mark
            })
    return num_students, students


def calculate_percentage_and_grade(student):
    max_marks = 160
    percentage = (student["overall_score"] / max_marks) * 100
    grade = "F"
    if percentage >= 70:
        grade = "A"
    elif percentage >= 60:
        grade = "B"
    elif percentage >= 50:
        grade = "C"
    elif percentage >= 40:
        grade = "D"
    return percentage, grade


def display_student_record(student):
    percentage, grade = calculate_percentage_and_grade(student)
    record = f"Name: {student['name']}\n"
    record += f"Student Number: {student['student_number']}\n"
    record += f"Total Coursework Marks: {student['total_coursework']}\n"
    record += f"Exam Mark: {student['exam_mark']}\n"
    record += f"Overall Percentage: {percentage:.2f}%\n"
    record += f"Grade: {grade}\n"
    return record


def update_output(output_text):
    output_text.delete(1.0, tk.END)


def view_all_students(students, output_text):
    update_output(output_text)
    total_percentage = 0
    for student in students:
        record = display_student_record(student)
        output_text.insert(tk.END, record + "\n" + "-" * 30 + "\n")
        percentage, _ = calculate_percentage_and_grade(student)
        total_percentage += percentage
    average_percentage = total_percentage / len(students)
    summary = f"Total Students: {len(students)}\n"
    summary += f"Average Percentage: {average_percentage:.2f}%\n"
    output_text.insert(tk.END, summary)

def view_individual_student(students, output_text):
    def on_select_student(event):
        try:
            selected_student = student_input.get()
            student = next((s for s in students if s['name'].lower() == selected_student.lower() or str(s['student_number']) == selected_student), None)
            if student:
                record = display_student_record(student)
                update_output(output_text)
                output_text.insert(tk.END, record)
            else:
                messagebox.showwarning("Selection Error", "Student not found.")
        except Exception as e:
            messagebox.showwarning("Error", f"Error: {e}")

    student_input_label = tk.Label(window, text="Enter Student Name or Number:", font=("Arial", 14), bg="#f0f0f0")
    student_input_label.pack(pady=10)

    
    input_frame = tk.Frame(window, bg="#f0f0f0")
    input_frame.pack(pady=10)

    student_input = tk.Entry(input_frame, font=("Arial", 12), width=40)
    student_input.pack(side=tk.LEFT, padx=10)  

    
    search_button = tk.Button(input_frame, text="Search", command=lambda: on_select_student(None), font=("Arial", 12), bg="#4CAF50", fg="white", padx=20, pady=10)
    search_button.pack(side=tk.LEFT)  



def show_student_with_extreme_score(students, output_text, highest=True):
    update_output(output_text)
    student = max(students, key=lambda x: x["overall_score"]) if highest else min(students, key=lambda x: x["overall_score"])
    record = display_student_record(student)
    label = "Highest" if highest else "Lowest"
    output_text.insert(tk.END, f"Student with {label} score:\n")
    output_text.insert(tk.END, record)


def main():
    if not os.path.exists(FILE_PATH):
        messagebox.showerror("File Not Found", f"File '{FILE_PATH}' not found!")
        return
    
    num_students, students = load_data(FILE_PATH)

    
    global window
    window = tk.Tk()
    window.title("Student Records Manager")
    window.configure(bg="#f0f0f0")  
    window.geometry("800x600")  
    window.resizable(False, False)  

    
    frame = tk.Frame(window, bg="#f0f0f0")
    frame.pack(fill=tk.BOTH, expand=True)

   
    canvas = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.config(yscrollcommand=scrollbar.set)

    output_text = tk.Text(canvas, height=15, width=80, font=("Arial", 12), padx=10, pady=10)
    output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(fill=tk.BOTH, expand=True)

    
    def menu_selection():
        choice = menu_var.get()
        if choice == "View All Student Records":
            view_all_students(students, output_text)
        elif choice == "View Individual Student Record":
            view_individual_student(students, output_text)
        elif choice == "Show Student with Highest Mark":
            show_student_with_extreme_score(students, output_text, highest=True)
        elif choice == "Show Student with Lowest Mark":
            show_student_with_extreme_score(students, output_text, highest=False)
        else:
            window.quit()

    
    menu_var = tk.StringVar(window)
    menu_var.set("View All Student Records")  
    
    menu_label = tk.Label(window, text="Select Option:", font=("Arial", 14), bg="#f0f0f0")
    menu_label.pack(pady=10)

    menu = tk.OptionMenu(window, menu_var, 
                         "View All Student Records", 
                         "View Individual Student Record", 
                         "Show Student with Highest Mark", 
                         "Show Student with Lowest Mark", 
                         "Exit Program")
    menu.config(font=("Arial", 12), width=25)
    menu.pack(pady=10)

    
    menu_button = tk.Button(window, text="Execute", command=menu_selection, font=("Arial", 12), bg="#4CAF50", fg="white", relief="raised", padx=20, pady=10)
    menu_button.pack(pady=20)

    
    window.mainloop()

if __name__ == "__main__":
    main()
