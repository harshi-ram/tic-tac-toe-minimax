# Tic Tac Toe with Minimax AI

An unbeatable Tic Tac Toe game powered by the Minimax algorithm. It features an AI opponent that uses recursive game tree evaluation and backtracking for optimal play. Built with Python, Pygame, and Numpy.

## Tech Stack

Python • Pygame • NumPy

## Features

- Unbeatable AI using Minimax algorithm with backtracking
- Interactive GUI with mouse input and score tracking
- Efficient win detection using NumPy array operations

## Installation
```
py -m pip install pygame numpy
py tic_tac_toe.py
```

## How to Play

- Click on any square to make your move (you are X)
- AI responds immediately (plays O)
- Press R to restart

## Algorithm

The Minimax algorithm recursively evaluates all possible game states:
- AI maximizes its score (+1 for win, 0 for draw, -1 for loss)
- Assumes optimal play from both players
- Uses backtracking to explore the entire game tree
