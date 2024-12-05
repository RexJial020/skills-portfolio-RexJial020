import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import random


class ArithmeticQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Arithmetic Quiz")
        self.root.geometry("400x500")
        self.root.configure(bg="purple")

        self.score = 0
        self.current_question = 0
        self.level = 1

        self.bg_image_tk = None
        self.bg_label = None

        self.setup_menu()

        
        self.root.bind("<Configure>", self.resize_background)

    def setup_menu(self):
    
     self.clear_window()

    
     self.resize_background()

    
     self.root.configure(bg="white")

    #Title and buttons for difficulty levels
     tk.Label(self.root, text="MATHS QUIZ", font=("Arial", 16, "bold"), bg="purple").pack(pady=15)
     tk.Label(self.root, text="PLEASE SELECT YOUR DIFFICULTY LEVEL", font=("Arial", 10, "bold"), bg="purple").pack(pady=20)

     tk.Button(self.root, text="Easy (Single-digit)", command=lambda: self.start_quiz(1), width=20).pack(pady=10)
     tk.Button(self.root, text="Moderate (Double-digit)", command=lambda: self.start_quiz(2), width=20).pack(pady=10)
     tk.Button(self.root, text="Advanced (Four-digit)", command=lambda: self.start_quiz(3), width=20).pack(pady=10)

    def resize_background(self, event=None):
        
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        
        background_image = Image.open(r"C:\Users\rexte\OneDrive\Obsidian Files\Creative Computing Year 1\Code Lab YR 1 SEM 1\web dev\Web-Dev-1-Set-exercises\skills-portfolio-RexJial020\A1 - Skills Portfolio\Exercise1\mathquiz.jpg")
        background_image = background_image.resize((window_width, window_height))  
        self.bg_image_tk = ImageTk.PhotoImage(background_image)

        if self.bg_label:
            
            self.bg_label.config(image=self.bg_image_tk)
            self.bg_label.image = self.bg_image_tk
        else:
            
            self.bg_label = tk.Label(self.root, image=self.bg_image_tk)
            self.bg_label.image = self.bg_image_tk
            self.bg_label.place(relwidth=1, relheight=1)
            self.bg_label.lower()  

    def start_quiz(self, level):
        self.level = level
        self.score = 0
        self.current_question = 0
        self.questions = self.generate_questions()

        #This sets background color based on difficulty level
        if self.level == 1:
            self.root.configure(bg="green")
        elif self.level == 2:
            self.root.configure(bg="yellow")
        elif self.level == 3:
            self.root.configure(bg="red")

        self.show_question()

    def generate_questions(self):
        questions = []
        for _ in range(10):
            num1 = self.random_int(self.level)
            num2 = self.random_int(self.level)
            operation = random.choice(['+', '-'])
            correct_answer = num1 + num2 if operation == '+' else num1 - num2
            questions.append((num1, num2, operation, correct_answer))
        return questions

    def random_int(self, level):
        if level == 1:
            return random.randint(1, 9)
        elif level == 2:
            return random.randint(10, 99)
        elif level == 3:
            return random.randint(1000, 9999)

    def show_question(self):
        self.clear_window()

        if self.current_question < 10:
            num1, num2, operation, correct_answer = self.questions[self.current_question]

            tk.Label(self.root, text=f"Question {self.current_question + 1}", font=("Arial", 14), bg=self.root.cget("bg")).pack(pady=10)
            tk.Label(self.root, text=f"{num1} {operation} {num2} =", font=("Arial", 16), bg=self.root.cget("bg")).pack(pady=10)

            self.answer_var = tk.StringVar()
            tk.Entry(self.root, textvariable=self.answer_var, font=("Arial", 14), justify="center").pack(pady=10)

            tk.Button(self.root, text="Submit", command=lambda: self.check_answer(correct_answer)).pack(pady=10)
        else:
            self.show_results()

        tk.Button(self.root, text="Return to Main Page", command=self.setup_menu, bg="white").pack(pady=20)


    def check_answer(self, correct_answer):
        try:
            user_answer = int(self.answer_var.get())
            if user_answer == correct_answer:
                self.score += 10
                messagebox.showinfo("Correct!", "Great job! Correct answer.")
                self.current_question += 1
                self.show_question()
            else:
                self.score -= 5  
                messagebox.showwarning("Incorrect", "That is incorrect. Try again!")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    def show_results(self):
        self.clear_window()

        self.root.configure(bg="white")  
        tk.Label(self.root, text="Quiz Complete!", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Label(self.root, text=f"Your score: {self.score} / 100", font=("Arial", 14)).pack(pady=10)

        if self.score > 90:
            rank = "A+"
        elif self.score > 80:
            rank = "A"
        elif self.score > 70:
            rank = "B"
        elif self.score > 60:
            rank = "C"
        else:
            rank = "D"

        tk.Label(self.root, text=f"Your rank: {rank}", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.root, text="Play Again", command=self.setup_menu).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ArithmeticQuiz(root)
    root.mainloop()
