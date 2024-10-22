import random
import tkinter as tk
from tkinter import messagebox, ttk
from functools import partial
from copy import deepcopy


class TicTacToe:
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.sign = 0
        self.buttons = []
        self.current_player_label = None

    def reset_game(self, game_board, label1, label2, vs_ai=False):
        """Reinicia el juego al estado inicial"""
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.sign = 0
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(
                    text=" ", state="normal", bg="#061340", fg="black"
                )
        self.update_current_player_label()

    def update_current_player_label(self):
        """Actualiza la etiqueta del jugador actual"""
        if self.current_player_label:
            current = "X" if self.sign % 2 == 0 else "O"
            self.current_player_label.config(
                text=f"Turno actual: {current}",
                fg="#2196F3" if current == "X" else "#F44336",
            )

    def check_winner(self, b, player):
        winning_combinations = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],  # Horizontales
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],  # Verticales
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)],  # Diagonales
        ]

        for combo in winning_combinations:
            if all(b[i][j] == player for i, j in combo):
                # Resalta la combinación ganadora
                for i, j in combo:
                    self.buttons[i][j].config()  # Verde para la línea ganadora
                return True
        return False

    def is_board_full(self):
        return all(cell != " " for row in self.board for cell in row)

    def update_board(self, i, j, game_board, label1, label2, vs_ai=False):
        if self.board[i][j] == " ":
            current_player = "X" if self.sign % 2 == 0 else "O"
            self.board[i][j] = current_player

            # Actualiza el botón con animación
            self.buttons[i][j].config(
                text=current_player,
                state="disabled",
                disabledforeground="#2196F3" if current_player == "X" else "#F44336",
            )

            self.sign += 1
            self.update_current_player_label()

            if self.check_winner(self.board, current_player):
                winner = (
                    "Jugador 1"
                    if current_player == "X"
                    else ("IA" if vs_ai else "Jugador 2")
                )
                response = messagebox.askyesno(
                    "¡Fin del juego!",
                    f"¡{winner} ha ganado!\n¿Desean jugar otra partida?",
                )
                if response:
                    self.reset_game(game_board, label1, label2, vs_ai)
                else:
                    game_board.destroy()
            elif self.is_board_full():
                response = messagebox.askyesno(
                    "¡Empate!",
                    "El juego ha terminado en empate.\n¿Desean jugar otra partida?",
                )
                if response:
                    self.reset_game(game_board, label1, label2, vs_ai)
                else:
                    game_board.destroy()
            elif vs_ai and self.sign % 2 != 0:
                game_board.after(500, lambda: self.ai_move(game_board, label1, label2))

    def ai_move(self, game_board, label1, label2):
        best_score = -float("inf")
        best_move = None

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    self.board[i][j] = "O"
                    score = self.minimax(self.board, 0, False)
                    self.board[i][j] = " "
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        if best_move:
            self.update_board(best_move[0], best_move[1], game_board, label1, label2)

    def minimax(self, b, depth, is_maximizing):
        if self.check_winner(b, "O"):
            return 1
        elif self.check_winner(b, "X"):
            return -1
        elif self.is_board_full():
            return 0

        if is_maximizing:
            best_score = -float("inf")
            for i in range(3):
                for j in range(3):
                    if b[i][j] == " ":
                        b[i][j] = "O"
                        score = self.minimax(b, depth + 1, False)
                        b[i][j] = " "
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(3):
                for j in range(3):
                    if b[i][j] == " ":
                        b[i][j] = "X"
                        score = self.minimax(b, depth + 1, True)
                        b[i][j] = " "
                        best_score = min(score, best_score)
            return best_score

    def create_game_board(self, game_board, label1, label2, vs_ai=False):
        # Frame para el tablero
        board_frame = ttk.Frame(game_board, padding="10")
        board_frame.grid(row=0, column=0, padx=20, pady=20)

        self.buttons = []
        for i in range(3):
            self.buttons.append([])
            for j in range(3):
                button = tk.Button(
                    board_frame,
                    text=" ",
                    width=8,
                    height=4,
                    font=("Helvetica", 16, "bold"),
                    relief="ridge",
                    # bg="#E8E8E8",
                    bg="#061340",
                    command=partial(
                        self.update_board, i, j, game_board, label1, label2, vs_ai
                    ),
                )
                button.grid(row=i, column=j, padx=2, pady=2)
                self.buttons[i].append(button)

        # Frame para información del juego
        info_frame = ttk.Frame(game_board, padding="10")
        info_frame.grid(row=1, column=0, pady=10)

        # Etiquetas de jugadores con estilos mejorados
        label1.config(font=("Arial", 12, "bold"), fg="#2196F3", padx=10)
        label2.config(font=("Arial", 12, "bold"), fg="#F44336", padx=10)

        label1.grid(row=0, column=0, in_=info_frame)
        label2.grid(row=0, column=1, in_=info_frame)

        # Etiqueta para mostrar el turno actual
        self.current_player_label = tk.Label(
            info_frame, text="Turno actual: X", font=("Arial", 12, "bold"), fg="#2196F3"
        )
        self.current_player_label.grid(row=1, column=0, columnspan=2, pady=10)

        # Botón de reinicio
        reset_button = ttk.Button(
            info_frame,
            text="Reiniciar juego",
            command=lambda: self.reset_game(game_board, label1, label2, vs_ai),
        )
        reset_button.grid(row=2, column=0, columnspan=2, pady=10)


def create_styled_button(parent, text, command):
    """Crea un botón estilizado para el menú"""
    return tk.Button(
        parent,
        text=text,
        width=20,
        font=("Arial", 12),
        fg="white",
        bg="#2196F3",
        activebackground="#3f3f3f",
        activeforeground="white",
        relief="raised",
        pady=10,
        command=command,
    )


def start_single_player_game(menu):
    menu.destroy()
    game = TicTacToe()
    game_board = tk.Tk()
    game_board.title("Tic-Tac-Toe vs IA")
    game_board.configure(bg="white")
    game_board.resizable(False, False)

    label1 = tk.Label(game_board, text="Jugador: X")
    label2 = tk.Label(game_board, text="IA: O")

    game.create_game_board(game_board, label1, label2, vs_ai=True)
    game_board.mainloop()


def start_two_player_game(menu):
    menu.destroy()
    game = TicTacToe()
    game_board = tk.Tk()
    game_board.title("Tic-Tac-Toe")
    game_board.configure(bg="white")
    game_board.resizable(False, False)

    label1 = tk.Label(game_board, text="Jugador 1: X")
    label2 = tk.Label(game_board, text="Jugador 2: O")

    game.create_game_board(game_board, label1, label2)
    game_board.mainloop()


def main_menu():
    menu = tk.Tk()
    menu.title("Tic-Tac-Toe")
    menu.configure(bg="white")
    menu.resizable(False, False)

    # Frame principal con padding
    main_frame = ttk.Frame(menu, padding="20")
    main_frame.pack(expand=True)

    # Título del juego
    title_label = tk.Label(
        main_frame,
        text="Tic-Tac-Toe",
        font=("Arial", 24, "bold"),
        fg="#2196F3",
        pady=20,
    )
    title_label.pack()

    # Botones del menú
    create_styled_button(
        main_frame, "Un jugador", lambda: start_single_player_game(menu)
    ).pack(pady=5)
    create_styled_button(
        main_frame, "Dos jugadores", lambda: start_two_player_game(menu)
    ).pack(pady=5)
    create_styled_button(main_frame, "Salir", menu.quit).pack(pady=5)

    menu.mainloop()


if __name__ == "__main__":
    main_menu()
