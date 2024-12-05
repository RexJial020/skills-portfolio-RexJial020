from tkinter import *
from PIL import Image, ImageTk
from random import choice

class JokeApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry('500x600')
        self.root.title("Random Alexa Jokes")
        
        
        self.bg_image_tk = None
        self.resize_background()  

        
        self.root.bind("<Configure>", self.resize_background)

        
        for i in range(7):  
            root.grid_rowconfigure(i, weight=1)
        root.grid_columnconfigure(0, weight=1)

        
        self.jokes = self.load_jokes(r"C:\Users\rexte\OneDrive\Obsidian Files\Creative Computing Year 1\Code Lab YR 1 SEM 1\web dev\Web-Dev-1-Set-exercises\skills-portfolio-RexJial020\A1 - Skills Portfolio\Exercise2\randomJokes.txt")

       
        self.joke_label = Label(root, text="Click the button to see a joke!", font=('arial', 14), wraplength=400, justify="center", bg="#ffffff", fg="black")
        self.joke_label.grid(row=1, column=0, pady=10)

        
        self.click_button = Button(root, text="Click For Jokes", font=('arial', 14), command=self.show_jokes)
        self.click_button.grid(row=2, column=0, pady=10)

        
        self.quit_button = Button(root, text="Quit", font=('arial', 14), command=self.quit_program)
        self.quit_button.grid(row=3, column=0, pady=10)

    def load_jokes(self, file_path):
        """Load jokes from a text file."""
        try:
            with open(file_path, "r") as file:
                jokes = [line.strip() for line in file if line.strip()]
                return jokes
        except FileNotFoundError:
            print(f"Error: {file_path} not found. Ensure the file is in the correct directory.")
            return ["Error: Unable to load jokes. Please check the jokes file."]
        except Exception as e:
            print(f"Unexpected error reading jokes: {e}")
            return ["Error: Unable to load jokes due to an unexpected error."]

    def show_jokes(self):
        """Display a random joke."""
        self.joke_label.config(text=choice(self.jokes))

    def quit_program(self):
        """Exit the program."""
        self.root.quit()

    def resize_background(self, event=None):
        try:
            
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()

            
            background_image = Image.open(r"C:\Users\rexte\OneDrive\Obsidian Files\Creative Computing Year 1\Code Lab YR 1 SEM 1\web dev\Web-Dev-1-Set-exercises\skills-portfolio-RexJial020\A1 - Skills Portfolio\Exercise2\alexajokes.jpg")
            background_image = background_image.resize((window_width, window_height), Image.Resampling.LANCZOS)  # Resize to fit the window
            self.bg_image_tk = ImageTk.PhotoImage(background_image)

            
            if hasattr(self, 'background_label'):
                self.background_label.config(image=self.bg_image_tk)
            else:
                self.background_label = Label(self.root, image=self.bg_image_tk)
                self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
                self.background_label.lower()  
        except FileNotFoundError:
            print("Error: 'alexajokes.jpg' file not found. Ensure the image is in the correct directory.")
        except Exception as e:
            print(f"Unexpected error loading background image: {e}")


root = Tk()
app = JokeApp(root)
root.mainloop()
