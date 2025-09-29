import tkinter as tk
from tkinter import messagebox, scrolledtext
import random

# --- Constants ---
EASY_LEVEL_TURNS = 10
HARD_LEVEL_TURNS = 5
BG_COLOR = "#f0f0f0"
FONT_NAME = "Helvetica"
TITLE_FONT = (FONT_NAME, 18, "bold")
LABEL_FONT = (FONT_NAME, 12)
BUTTON_FONT = (FONT_NAME, 12, "bold")
STATS_FONT = (FONT_NAME, 10)
HISTORY_FONT = (FONT_NAME, 10)

class NumberGuessingGame:
    def __init__(self, master):
        """Initialize the game and set up the UI."""
        self.master = master
        self.master.title("Number Guessing Game")
        self.master.config(padx=40, pady=20, bg=BG_COLOR)
        self.master.resizable(False, False)
        
        # --- Game State Attributes ---
        self.secret_number = 0
        self.turns_left = 0
        self.current_guess_history = []
        
        # --- Statistics Attributes ---
        self.games_played = 0
        self.games_won = 0
        self.games_lost = 0
        
        self.difficulty_var = tk.StringVar(value="easy")
        
        self._create_widgets()
        self.start_new_game()

    def _create_widgets(self):
        """Creates and places all the UI elements in the window."""
        # --- Title ---
        title_label = tk.Label(
            self.master, text="Welcome to the Number Guessing Game!",
            font=TITLE_FONT, bg=BG_COLOR, pady=10
        )
        title_label.pack()

        # --- Main Frame for Controls and History ---
        main_frame = tk.Frame(self.master, bg=BG_COLOR)
        main_frame.pack(pady=5)

        # --- Left Frame for Game Controls ---
        controls_frame = tk.Frame(main_frame, bg=BG_COLOR, padx=10)
        controls_frame.grid(row=0, column=0, sticky="ns")

        # --- Right Frame for Guess History ---
        history_frame = tk.Frame(main_frame, bg=BG_COLOR, padx=10)
        history_frame.grid(row=0, column=1, sticky="ns")

        # --- Difficulty Selection ---
        tk.Radiobutton(
            controls_frame, text="Easy", variable=self.difficulty_var, value="easy",
            font=LABEL_FONT, bg=BG_COLOR, command=self.start_new_game
        ).pack(anchor="w")
        tk.Radiobutton(
            controls_frame, text="Hard", variable=self.difficulty_var, value="hard",
            font=LABEL_FONT, bg=BG_COLOR, command=self.start_new_game
        ).pack(anchor="w")

        # --- Guess Input ---
        input_frame = tk.Frame(controls_frame, bg=BG_COLOR, pady=10)
        input_frame.pack()
        tk.Label(input_frame, text="Your Guess:", font=LABEL_FONT, bg=BG_COLOR).pack(side="left", padx=5)
        self.guess_entry = tk.Entry(input_frame, width=8, font=LABEL_FONT, justify="center")
        self.guess_entry.pack(side="left")
        self.guess_entry.bind("<Return>", lambda event: self.check_guess())

        # --- Buttons ---
        button_frame = tk.Frame(controls_frame, bg=BG_COLOR)
        button_frame.pack(pady=10)
        self.guess_button = tk.Button(
            button_frame, text="Guess", command=self.check_guess, font=BUTTON_FONT, width=10
        )
        self.guess_button.pack(side="left", padx=5)
        tk.Button(
            button_frame, text="New Game", command=self.start_new_game, font=BUTTON_FONT, width=10
        ).pack(side="left", padx=5)

        # --- Guess History Widgets ---
        tk.Label(history_frame, text="Guess History", font=LABEL_FONT, bg=BG_COLOR).pack()
        self.history_text = scrolledtext.ScrolledText(
            history_frame, width=25, height=10, wrap=tk.WORD, font=HISTORY_FONT,
            state="disabled", bg="#ffffff", relief="solid", borderwidth=1
        )
        self.history_text.pack(pady=5)

        # --- Feedback and Status ---
        self.feedback_label = tk.Label(self.master, text="", font=LABEL_FONT, bg=BG_COLOR, pady=5)
        self.feedback_label.pack()
        self.turns_label = tk.Label(self.master, text="", font=LABEL_FONT, bg=BG_COLOR, pady=5)
        self.turns_label.pack()

        # --- Statistics Display ---
        stats_frame = tk.Frame(self.master, bg=BG_COLOR, pady=10)
        stats_frame.pack(fill="x", side="bottom")
        tk.Label(stats_frame, text="--- Statistics ---", font=(FONT_NAME, 11, "bold"), bg=BG_COLOR).pack()
        
        self.played_label = tk.Label(stats_frame, text="Games Played: 0", font=STATS_FONT, bg=BG_COLOR)
        self.played_label.pack()
        self.won_label = tk.Label(stats_frame, text="Wins: 0", font=STATS_FONT, bg=BG_COLOR)
        self.won_label.pack()
        self.lost_label = tk.Label(stats_frame, text="Losses: 0", font=STATS_FONT, bg=BG_COLOR)
        self.lost_label.pack()

    def start_new_game(self):
        """Resets the game state for a new round."""
        self.secret_number = random.randint(1, 100)
        self.turns_left = EASY_LEVEL_TURNS if self.difficulty_var.get() == "easy" else HARD_LEVEL_TURNS
        self.current_guess_history.clear()
        
        self.update_turns_label()
        self._update_history_display()
        self.feedback_label.config(text="Guess a number between 1 and 100.", fg="black")
        
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.config(state="normal")
        self.guess_button.config(state="normal")
        self.guess_entry.focus_set()

    def check_guess(self):
        """Handles the user's guess, provides feedback, and updates game state."""
        try:
            user_guess = int(self.guess_entry.get())
            if not 1 <= user_guess <= 100:
                messagebox.showwarning("Invalid Range", "Please guess a number between 1 and 100.")
                return
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid whole number.")
            return

        self.guess_entry.delete(0, tk.END)
        self.turns_left -= 1
        
        if user_guess == self.secret_number:
            self.feedback_label.config(text=f"🎉 You got it! The answer was {self.secret_number}. 🎉", fg="green")
            self.current_guess_history.append(f"{user_guess} -> Correct!")
            self.end_game(won=True)
        elif user_guess > self.secret_number:
            self.feedback_label.config(text="Too high. Try again!", fg="orange red")
            self.current_guess_history.append(f"{user_guess} -> Too High")
        else: # user_guess < self.secret_number
            self.feedback_label.config(text="Too low. Try again!", fg="dodger blue")
            self.current_guess_history.append(f"{user_guess} -> Too Low")
            
        self._update_history_display()
        self.update_turns_label()
        
        if self.turns_left == 0 and user_guess != self.secret_number:
            self.feedback_label.config(text=f"😢 You've run out of guesses. The number was {self.secret_number}.", fg="red")
            self.end_game(won=False)

    def end_game(self, won):
        """Disables inputs, updates, and displays final stats."""
        self.guess_entry.config(state="disabled")
        self.guess_button.config(state="disabled")
        
        self.games_played += 1
        if won:
            self.games_won += 1
        else:
            self.games_lost += 1
        
        self._update_stats_display()

    def _update_history_display(self):
        """Updates the guess history box with the latest guesses."""
        self.history_text.config(state="normal")
        self.history_text.delete('1.0', tk.END)
        if not self.current_guess_history:
             self.history_text.insert('1.0', "Your guesses will appear here...")
        else:
            history_str = "\n".join(self.current_guess_history)
            self.history_text.insert('1.0', history_str)
        self.history_text.config(state="disabled")

    def _update_stats_display(self):
        """Updates the statistics labels."""
        self.played_label.config(text=f"Games Played: {self.games_played}")
        self.won_label.config(text=f"Wins: {self.games_won}")
        self.lost_label.config(text=f"Losses: {self.games_lost}")

    def update_turns_label(self):
        """Updates the display for remaining turns."""
        self.turns_label.config(text=f"Turns Remaining: {self.turns_left}")

# --- Main execution block ---
if __name__ == "__main__":
    root = tk.Tk()
    app = NumberGuessingGame(root)
    root.mainloop()