ChessAI
=====================================================

![example board](example.png)

**********************************

## DEPENDENCIES
- [python-chess](https://python-chess.readthedocs.io/en/latest/) - move generation, move validation and support for common formats
- [flask](https://flask.palletsprojects.com/en/1.1.x/) - lightweight WSGI web application framework
- [torch](https://pytorch.org/) - open source machine learning framework

## USAGE

```
./server.py # runs webserver on localhost:5000
```

## PROBLEM

Evaluate a given board state and come up with a good move to perform.

Why is it hard?
- ~10^40 legal board states
- ~10^120 different chess games
- ~30 moves per board state
- typical chess game ~80 moves

## APPROACHES

-  [Minimax](https://en.wikipedia.org/wiki/Minimax)
    - minimizing the possible loss for a worst case (maximum loss) scenario
    - reasonably works up to a search depth of *3*
    - already surprinsingly good opponent, but beatable
    - **improvement**
        - [alpha–beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)
        - decreases the number of nodes that are evaluated by minimax and therefore the computation time
        - allows to search faster and works reasonably up to a depth of *4*

- [ANN](https://en.wikipedia.org/wiki/Artificial_neural_network)
    - **mapping to be learned**: board state -> optimal move
    - needs a lot of chess games to train with
    - used PyTorch to implement the neural net

## TRAINING DATA

The net was trained on 110000 standard rated games played on [lichess.org ](https://database.lichess.org/) in [Portable Game Notation (PGN)](https://de.wikipedia.org/wiki/Portable_Game_Notation) format.  
Therefore, based on the above assumptions, the model was trained on approximately 8.8M board positions.
