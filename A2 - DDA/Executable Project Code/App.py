import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO


class Pokemon:
    def __init__(self, name, types, abilities, stats, image_url):
        self.name = name
        self.types = types
        self.abilities = abilities
        self.stats = stats
        self.image_url = image_url

    def display_info(self):
        type_str = ", ".join(self.types)
        abilities_str = ", ".join(self.abilities)
        stats_str = "\n".join([f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}" for stat in self.stats])
        return f"Name: {self.name.capitalize()}\nType: {type_str}\nAbilities: {abilities_str}\nStats:\n{stats_str}"


class PokeAPI:
    BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

    @staticmethod
    def get_pokemon_by_name(name):
        try:
            response = requests.get(f"{PokeAPI.BASE_URL}{name.lower()}", timeout=5)
            response.raise_for_status()
            data = response.json()
            name = data['name']
            types = [t['type']['name'] for t in data['types']]
            abilities = [a['ability']['name'] for a in data['abilities']]
            stats = data['stats']
            image_url = data['sprites']['front_default']
            return Pokemon(name, types, abilities, stats, image_url)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        return None


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("RexieDex")
        self.root.configure(bg="#ff0000")
        self.recent_searches = [] 

        # Top section: Title and Profile Picture
        self.top_frame = tk.Frame(self.root, bg="#ff0000")
        self.top_frame.pack(pady=5)

        self.title_label = tk.Label(
            self.top_frame, text="RexieDex", font=("Helvetica", 20, "bold"), bg="#8b0000", fg="white"
        )
        self.title_label.pack(side="left", padx=10)

        self.profile_frame = tk.Frame(self.top_frame, bg="#ff0000")
        self.profile_frame.pack(side="right", padx=10)

        self.profile_label = tk.Label(
            self.profile_frame, text="User Profile", font=("Helvetica", 10, "bold"), bg="#8b0000", fg="white"
        )
        self.profile_label.pack(pady=5)

        # Load and display the profile image
        try:
            self.profile_image_data = Image.open(r"C:\Users\user\OneDrive\Obsidian Files\skills-portfolio-RexJial020\A2 - DDA\Executable Project Code\Hades.png")
            self.profile_image_data = self.profile_image_data.resize((100, 100))  
            self.profile_image = ImageTk.PhotoImage(self.profile_image_data)

            self.profile_image_label = tk.Label(
                self.profile_frame, image=self.profile_image, bg="#a9a9a9", relief="groove"
            )
            self.profile_image_label.pack()
        except FileNotFoundError:
            messagebox.showerror("Error", "Profile image 'Hades.png' not found.")
            self.profile_image_label = tk.Label(
                self.profile_frame, text="[Profile Pic]", bg="#a9a9a9", fg="black", width=15, height=5, relief="groove"
            )
            self.profile_image_label.pack()

        # Search Section
        self.search_frame = tk.Frame(self.root, bg="#ff0000")
        self.search_frame.pack(pady=10)

        self.search_label = tk.Label(
            self.search_frame, text="Enter Pokémon Name:", bg="#ff0000", fg="white"
        )
        self.search_label.grid(row=0, column=0, padx=5)

        self.search_entry = tk.Entry(self.search_frame, bg="#a9a9a9", fg="black", insertbackground="black")
        self.search_entry.grid(row=0, column=1, padx=5)

        self.search_button = tk.Button(
            self.search_frame, text="Search", command=self.search_pokemon, bg="#8b0000", fg="white", relief="flat"
        )
        self.search_button.grid(row=0, column=2, padx=5)

        # Pokémon Result Display
        self.result_frame = tk.Frame(self.root, bg="#ff0000")
        self.result_frame.pack(pady=10)

        self.result_text = tk.Text(
            self.result_frame, height=10, width=40, state="disabled", bg="#a9a9a9", fg="black"
        )
        self.result_text.pack()

        self.pokemon_image_label = tk.Label(self.root, bg="#ff0000")
        self.pokemon_image_label.pack(pady=10)

    def search_pokemon(self):
        name = self.search_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a Pokémon name.")
            return

        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Loading...")
        self.result_text.config(state="disabled")
        self.root.update_idletasks()

        pokemon = PokeAPI.get_pokemon_by_name(name)
        if pokemon:
            self.display_pokemon(pokemon)
        else:
            self.result_text.config(state="normal")
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Pokémon '{name}' not found.")
            self.result_text.config(state="disabled")

    def display_pokemon(self, pokemon):
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, pokemon.display_info())
        self.result_text.config(state="disabled")

        if pokemon.image_url:
            response = requests.get(pokemon.image_url)
            img_data = Image.open(BytesIO(response.content))
            img_data = img_data.resize((100, 100))
            img = ImageTk.PhotoImage(img_data)
            self.pokemon_image_label.config(image=img)
            self.pokemon_image_label.image = img


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
