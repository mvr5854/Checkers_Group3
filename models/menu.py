from enum import Enum

class Option(Enum):
    """Enum for menu options."""
    HUMAN_VS_MINIMAX_AI = "Human vs Minimax AI"
    HUMAN_VS_MCTS_AI = "Human vs MCTS AI"
    HUMAN_VS_HUMAN = "Human vs Human"
    MINIMAX_AI_VS_MCTS_AI = "Minimax AI vs MCTS AI"

class Menu:
    """Class for displaying the menu and handling user input."""

    def __init__(self, title):
        self.options = list(Option)
        self.title = title

    def display_menu(self):
        """Display the menu options."""
        print(f"Welcome to the {self.title}!")
        for i, option in enumerate(self.options, start=1):
            print(f"{i}. {option.value}")

    def read_user_input(self):
        """Get user choice from the menu."""
        while True:
            try:
                choice = int(input("Select game mode (1-4): ")) - 1
                if 0 <= choice < len(self.options):
                    return self.options[choice]
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")