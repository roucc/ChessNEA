# Chess Engine with Machine Learning

This is my A Level Computer Science Project. It was my first major project (I have got a lot better at coding since then) but I still think it is quite interesting.

See the [full PDF](CS%20NEA%20chess%20engine%20using%20ML.pdf) for the write up.

A Python-based chess engine capable of playing both standard chess and Fischer Random (Chess960), integrating AI and machine learning for board evaluation.

## Features

* Human vs Human, Human vs Computer or Computer vs Computer play
* Support for Chess960 randomised starting positions
* AI opponents using:
  * Simple evaluation (piece weights)
  * Minimax and Alpha-Beta pruning search
  * Neural Network–based evaluation trained on Lichess data
* Machine Learning integration with TensorFlow
* Interactive GUI with drag-and-drop, move highlighting, and automatic board flipping
* Full unit testing suite for all major modules

## Project Goals

1. Implement a complete chess game with rules and visualisation.
2. Develop an AI using Minimax and Alpha-Beta pruning.
3. Train a neural network to evaluate board states more effectively than heuristic methods.

## Architecture

* Object-Oriented Design with modular classes: `Board`, `Player`, `GUI`, `AI`, `Training`, etc.
* Follows PEP 8 style conventions.
* Implements test-driven development (TDD)
* Neural network trained on millions of chess positions (FEN format).

## Technologies

* Python 3
* TensorFlow / Keras
* Pygame (for GUI)
* Stockfish (for evaluation comparison)
* Google Colab (for GPU training)

## Performance

* Alpha-Beta pruning is 2 times faster than Minimax.
* Neural network AI competes with Stockfish at 2000 Elo at depth 3.

## Future Improvements

* Multithreading and move ordering for faster search.
* Better batching for neural evaluations.
* Implement transposition tables and iterative deepening.
* Rewrite core in C for performance gains.

## Author

Dougal Craig-Wood
