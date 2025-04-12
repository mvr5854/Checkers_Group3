import sys
from enum import Enum

class IOHelper:
    """Base class for handling input and output operations."""
    def __init__(self, options):
        self.options = options

    def display_menu(self, max_per_line=1):
        """Display the menu options."""
        for i, option in enumerate(self.options, start=1):
            end = "\n" if i % max_per_line == 0 else "\t"
            print(f"{i}. {option}", end=end)

        if len(self.options) % max_per_line != 0:
            print()
        print("0. Quit")

    def read_user_input(self):
        """Get user choice from the menu."""
        while True:
            try:
                choice_num = len(self.options)
                choice = int(input(f"Choice (0-{choice_num}): "))
                if choice == 0:
                    print("Exiting the program...")
                    sys.exit(0)
                if 0 < choice <= choice_num:
                    return self.options[choice - 1]
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

class Option(Enum):
    """Enum for menu options."""
    HUMAN_VS_MINIMAX_AI = "Human vs Minimax AI"
    HUMAN_VS_MCTS_AI = "Human vs MCTS AI"
    HUMAN_VS_HUMAN = "Human vs Human"
    MINIMAX_AI_VS_MCTS_AI = "Minimax AI vs MCTS AI"

class Menu(IOHelper):
    """Class for displaying the menu and handling user input using IOHelper."""
    
    def __init__(self):
        # Initialize Menu with a list of options from the Option enum
        options = [option.value for option in Option]
        super().__init__(options)