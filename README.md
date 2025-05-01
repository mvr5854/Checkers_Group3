# Checkers Board Game 
**Team 3:** Wenceslao Granados Gomez, Maja Kuzmanovic, and Mahfuzur Rahman

AI 801 (Foundations of Artificial Intelligence),
Spring, 2025 

## Description
This project develops a Checkers game with AI agents as part of the AI 801 course. We explore two classic search algorithms — Minimax with alpha–beta pruning and Monte Carlo Tree Search (MCTS). Although Checkers has been fully solved, its simple rules and complex tactics make it an ideal project for experimenting with different search algorithms and custom heuristics.

Our Minimax agent uses a heuristic that considers piece count, board control, promotion potential, king pieces, mobility, edge safety, and threat assessment. In contrast, the MCTS agent relies on random playouts to estimate move effectiveness.

To compare the performance of the two AI agents, we simulate multiple games between Minimax and MCTS, alternating the starting player to ensure fairness. Minimax with alpha–beta pruning outperforms MCTS across all three metrics — decision speed, move quality, and resilience against opponent play.

This project emphasizes the importance of selecting the right algorithm for a specific problem, rather than assuming that newer algorithms are always better. We welcome your feedback and suggestions to help extend and refine this project.

## Python 3.7 and up
The code code run in Python 3.7 and later versions. You can [install Python](https://www.python.org/downloads).

## Installation Guide
Run the following command in a terminal download this project:
```
git clone https://github.com/mvr5854/Checkers_Group3.git
```

Then you need to create a virtual environment and install the basic dependencies to run the project on your system:

```
cd Checkers_Group3
python setup.py             # For windows
python3 setup.py            # For Mac/Linux
```

You can also use docker instead of the virtual environment.

## To Run the Project
Activate the virtual environment if it is not already activated.
For Windows: 
```
venv\Scripts\activate
```
For Mac/Linux:
```
source venv/bin/activate
```
When the virtual environment is active, your terminal typically shows '(venv)' at the beginning.
For example: `(venv) C:\Users\YourUser\project>`

**To run Jupyter Notebook, use the following command:**
```
jupyter notebook --ip=0.0.0.0 --allow-root
```
