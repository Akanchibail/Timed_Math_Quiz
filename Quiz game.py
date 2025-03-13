import tkinter as tk
import random
import time

# Defining Constants
OPERATORS = ["+", "-", "*"]
MIN_OPERAND = 3
MAX_OPERAND = 12
TOTAL_PROBLEMS = 10

class MathQuizGame:
    # Initializing the Class
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quiz Game")
        self.root.geometry("400x300")

        # Game Variables
        self.wrong_attempts = 0
        self.current_problem = 0
        self.start_time = None
        self.expr = ""
        self.answer = 0
        self.game_over = False  # Flag to stop the timer when the game ends

        # UI Components
        self.label_title = tk.Label(root, text="Math Quiz Game", font=("Arial", 18, "bold"), fg="red")
        self.label_title.pack(pady=10)

        self.label_problem = tk.Label(root, text="Click on 'Start Game' to Start!", font=("Arial", 16))
        self.label_problem.pack(pady=10)

        self.entry_answer = tk.Entry(root, font=("Arial", 14))
        self.entry_answer.pack(pady=5)
        self.entry_answer.bind("<Return>", self.check_answer)  # Press Enter instead of clicking Submit

        self.button_submit = tk.Button(root, text="Submit", command=self.check_answer, font=("Arial", 14))
        self.button_submit.pack(pady=5)

        self.label_feedback = tk.Label(root, text="", font=("Arial", 14))
        self.label_feedback.pack(pady=5)

        self.label_timer = tk.Label(root, text="Time: 0 seconds", font=("Arial", 14))
        self.label_timer.pack(pady=5)

        # Start Game Button
        self.button_start = tk.Button(root, text="Start Game", command=self.start_game, font=("Arial", 14))
        self.button_start.pack(pady=10)

    def start_game(self):
        """Start the game when the user clicks 'Start Game'"""
        self.start_time = time.time()  # Start the timer when the game starts
        self.label_problem.config(text="Problem #1:")  # Display the first problem
        self.next_problem()  # Go to the first problem
        self.update_timer()  # Start the timer updates

        # Remove Start Button after the game begins
        self.button_start.pack_forget()

    def generate_problem(self):
        """Generate a random math problem."""
        left = random.randint(MIN_OPERAND, MAX_OPERAND)
        right = random.randint(MIN_OPERAND, MAX_OPERAND)
        operator = random.choice(OPERATORS)
        self.expr = f"{left} {operator} {right}"
        self.answer = eval(self.expr)

    def next_problem(self):
        """Move to the next problem or finish the game."""
        if self.current_problem < TOTAL_PROBLEMS:
            self.generate_problem()
            self.label_problem.config(text=f"Problem #{self.current_problem + 1}: {self.expr} = ?")
            self.entry_answer.delete(0, tk.END)
            self.label_feedback.config(text="")
            self.current_problem += 1
        else:
            self.end_game()

    def check_answer(self, event=None):
        """Check the answer and provide feedback."""
        user_input = self.entry_answer.get()
        try:
            user_answer = int(user_input)  # Convert to integer (allows negatives)
            if user_answer == self.answer:
                self.next_problem()
            else:
                self.wrong_attempts += 1
                self.label_feedback.config(text="Wrong! Try again.", fg="red")
        except ValueError:
            self.label_feedback.config(text="Invalid input! Enter a number.", fg="red")

    def update_timer(self):
        """Update the timer in real-time, stopping when the game ends."""
        if self.game_over:
            return  # Stop updating once the game is over

        elapsed_time = round(time.time() - self.start_time, 2) if self.start_time else 0
        self.label_timer.config(text=f"Time: {elapsed_time} seconds")
        self.root.after(1000, self.update_timer)  # Update every second

    def end_game(self):
        """Display final score and time taken."""
        self.game_over = True  # Stop the timer updates
        total_time = round(time.time() - self.start_time, 2)

        # Display final results
        self.label_problem.config(text="Game Over!")
        self.label_feedback.config(text=f"You finished in {total_time} seconds with {self.wrong_attempts} mistakes.", fg="red")
        self.label_timer.config(text=f"Time: {total_time} seconds")  # Ensure timer matches final result

        # Hide input fields
        self.entry_answer.pack_forget()
        self.button_submit.pack_forget()


# Run the GUI application
root = tk.Tk()
game = MathQuizGame(root)
root.mainloop()
