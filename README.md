ChessAI
=====================================================

Approach to build a program that beats me in the game of chess.

**********************************

### DEPENDENCIES
- [python-chess](https://python-chess.readthedocs.io/en/latest/) - move generation, move validation and support for common formats
- [flask](https://flask.palletsprojects.com/en/1.1.x/) - lightweight WSGI web application framework

I need an approach that evaluates a given board state and comes up with a good move to perform.

### 1st approach: [Minimax](https://en.wikipedia.org/wiki/Minimax)
- minimizing the possible loss for a worst case (maximum loss) scenario
- reasonably works up to a search depth of *3*
- already surprinsingly good opponent, but beatable
- **improvement**
    - [alpha–beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)
    - decrease the number of nodes that are evaluated by the minimax algorithm and therefore the computation time
    - allows to search faster and works reasonably up to a depth of *4*

### 2nd approach: Neural Network
- **mapping**: board state -> move to be performed
- need a lot of chess games to train with