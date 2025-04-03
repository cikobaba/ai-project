import tkinter as tk
import random

class NumberDivisionGame:
    def __init__(self, master):
        self.master = master
        master.title("Number Division Game")

        self.create_widgets()
        self.generate_numbers()

    def create_widgets(self):
        self.title = tk.Label(self.master, text="Number Division Game", font=("Arial", 16))
        self.title.pack(pady=10)

        self.start_label = tk.Label(self.master, text="Who starts?")
        self.start_label.pack()
        self.start_var = tk.StringVar(value="Human")
        self.start_menu = tk.OptionMenu(self.master, self.start_var, "Human", "Computer")
        self.start_menu.pack()

        self.alg_label = tk.Label(self.master, text="Choose algorithm:")
        self.alg_label.pack()
        self.alg_var = tk.StringVar(value="Random")
        self.alg_menu = tk.OptionMenu(self.master, self.alg_var, "Minimax", "Alpha-Beta", "Random")
        self.alg_menu.pack()

        self.num_label = tk.Label(self.master, text="Choose starting number:")
        self.num_label.pack()
        self.start_num_var = tk.StringVar()
        self.num_menu = tk.OptionMenu(self.master, self.start_num_var, "")
        self.num_menu.pack()

        self.start_button = tk.Button(self.master, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=10)

        self.display = tk.Text(self.master, height=15, width=50)
        self.display.pack()

        self.action_frame = tk.Frame(self.master)
        self.div2_btn = tk.Button(self.action_frame, text="Divide by 2", command=lambda: self.player_move(2))
        self.div3_btn = tk.Button(self.action_frame, text="Divide by 3", command=lambda: self.player_move(3))
        self.div2_btn.pack(side="left", padx=10)
        self.div3_btn.pack(side="left", padx=10)
        self.action_frame.pack(pady=5)

        self.reset_btn = tk.Button(self.master, text="New Game", command=self.generate_numbers)
        self.reset_btn.pack(pady=10)

    def generate_numbers(self):
        self.available_numbers = random.sample([n for n in range(10000, 20001) if n % 6 == 0], 5)
        self.start_num_var.set(str(self.available_numbers[0]))

        menu = self.num_menu["menu"]
        menu.delete(0, "end")
        for num in self.available_numbers:
            menu.add_command(label=str(num), command=lambda value=num: self.start_num_var.set(str(value)))

        self.display.delete(1.0, tk.END)
        self.display.insert(tk.END, "Choose settings and press 'Start Game'.\n")

    def reset_game(self):
        self.current_number = int(self.start_num_var.get())
        self.player_score = 0
        self.computer_score = 0
        self.bank = 0
        self.is_player_turn = True
        self.display.delete(1.0, tk.END)
        self.display.insert(tk.END, f"New Game!\nStarting number: {self.current_number}\n")
        self.update_action_buttons()

    def start_game(self):
        self.reset_game()
        starter = self.start_var.get()
        algo = self.alg_var.get()
        self.display.insert(tk.END, f"{starter} starts first. Computer will use: {algo}\n\n")
        self.is_player_turn = (starter == "Human")
        if not self.is_player_turn:
            self.master.after(1000, self.computer_move)

    def player_move(self, divisor):
        if not self.is_player_turn:
            return
        self.make_move(divisor, is_player=True)
        if not self.is_game_over():
            self.master.after(1000, self.computer_move)

    def computer_move(self):
        if self.is_player_turn:
            return
        valid_moves = [d for d in [2, 3] if self.current_number % d == 0]
        if not valid_moves:
            self.display.insert(tk.END, "No valid moves left. Game over!\n")
            self.display.insert(tk.END, self.end_game())
            return
        divisor = self.choose_best_move(valid_moves)
        self.make_move(divisor, is_player=False)

    def choose_best_move(self, valid_moves):
        algo = self.alg_var.get()
        if algo == "Minimax":
            return self.minimax(self.current_number, True, depth=5)[1]
        elif algo == "Alpha-Beta":
            return self.alphabeta(self.current_number, True, float('-inf'), float('inf'), depth=5)[1]
        else:
            return random.choice(valid_moves)

    def minimax(self, number, is_maximizing, depth):
        if depth == 0 or number in [2, 3] or (number % 2 != 0 and number % 3 != 0):
            return self.evaluate_state(number), None

        best_score = float('-inf') if is_maximizing else float('inf')
        best_move = None

        for move in [2, 3]:
            if number % move != 0:
                continue
            new_number = number // move
            score, _ = self.minimax(new_number, not is_maximizing, depth - 1)

            if is_maximizing:
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move

        return best_score, best_move

    def alphabeta(self, number, is_maximizing, alpha, beta, depth):
        if depth == 0 or number in [2, 3] or (number % 2 != 0 and number % 3 != 0):
            return self.evaluate_state(number), None

        best_move = None

        for move in [2, 3]:
            if number % move != 0:
                continue
            new_number = number // move
            score, _ = self.alphabeta(new_number, not is_maximizing, alpha, beta, depth - 1)

            if is_maximizing:
                if score > alpha:
                    alpha = score
                    best_move = move
                if alpha >= beta:
                    break
            else:
                if score < beta:
                    beta = score
                    best_move = move
                if beta <= alpha:
                    break

        return (alpha if is_maximizing else beta), best_move

    def evaluate_state(self, number):
        if number == 2:
            return 10
        elif number == 3:
            return -10
        return -abs(number - 2)

    def make_move(self, divisor, is_player):
        actor = "Player" if is_player else "Computer"
        self.display.insert(tk.END, f"{actor} chooses to divide by {divisor}\n")
        self.current_number //= divisor
        self.display.insert(tk.END, f"New number: {self.current_number}\n")

        if self.current_number % 2 == 0:
            if is_player:
                self.player_score += 1
                self.display.insert(tk.END, "Player gains 1 point.\n")
            else:
                self.computer_score += 1
                self.display.insert(tk.END, "Computer gains 1 point.\n")
        else:
            if is_player:
                self.player_score -= 1
                self.display.insert(tk.END, "Player loses 1 point.\n")
            else:
                self.computer_score -= 1
                self.display.insert(tk.END, "Computer loses 1 point.\n")

        if str(self.current_number)[-1] in ["0", "5"]:
            self.bank += 1
            self.display.insert(tk.END, "1 point added to the game bank.\n")

        self.display.insert(tk.END, f"Scores => Player: {self.player_score}, Computer: {self.computer_score}, Bank: {self.bank}\n\n")
        self.is_player_turn = not is_player
        self.update_action_buttons()

        if self.is_game_over():
            self.display.insert(tk.END, self.end_game())
        elif self.current_number % 2 != 0 and self.current_number % 3 != 0:
            self.display.insert(tk.END, "No valid moves left. Game over!\n")
            self.display.insert(tk.END, self.end_game())

    def update_action_buttons(self):
        self.div2_btn.config(state="normal" if self.current_number % 2 == 0 else "disabled")
        self.div3_btn.config(state="normal" if self.current_number % 3 == 0 else "disabled")

    def is_game_over(self):
        return self.current_number in [2, 3]

    def end_game(self):
        winner = ""
        if self.current_number == 2:
            if not self.is_player_turn:
                self.player_score += self.bank
                winner = "Player collects the bank!"
            else:
                self.computer_score += self.bank
                winner = "Computer collects the bank!"
        elif self.current_number == 3:
            winner = "Ends with 3. No one collects the bank."
        else:
            winner = "No valid moves. No one collects the bank."

        result = f"\nFinal Scores:\nPlayer: {self.player_score}, Computer: {self.computer_score}\n{winner}\n"
        if self.player_score > self.computer_score:
            result += "Player wins!"
        elif self.computer_score > self.player_score:
            result += "Computer wins!"
        else:
            result += "It's a draw!"
        return result

# Run the GUI
root = tk.Tk()
game = NumberDivisionGame(root)
root.mainloop()