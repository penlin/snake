## Snake 
### Requirement 
* require python 3 with library ``asciimatics`` for terminal display
```
pip3 install asciimatics
```

* require python 3 with library ``opencv`` and ``numpy`` for window display
  * if ``opencv`` is not installed, game would be played on terminal by default
```
conda install opencv numpy 
```

### How to play
```
usage: snake_game.py [-h] [--resume RECORD] [--fps FPS] [--size SIZE]
                     [--scale SCALE] [--ai AI_name]

Play Snake Game

optional arguments:
  -h, --help       show this help message and exit
  --resume RECORD  resume from the specified saved record
  --fps FPS        frame rate
  --size SIZE      game board size
  --scale SCALE    grid size
  --ai AI_name     AI name to run the snake Game
```
* ``FPS == 0`` would not show any window/GUI util the game finished

#### Manually Control
* Up: ``i``
* Down: ``k``
* Left: ``j``
* Right: ``l``
* Pause/Resume: ``p``
* Save a temporarily record: ``s`` 
* Quit the game: ``q``
* Restart the game: ``r`` in game over screen

#### AI 
* there are several AI supported :
  1. __SimpleAI__: which would only go to the border and circling through the border. It only can win the game when Snake Board size if _Nx2_ or _2xN_
  2. __SmartAI__: which would aggresively run to the candy to would die easily when it grows longer by running into itself
  3. __TraceTailAI__: which would run to the candy base on __SmartAI__ but ensuring the head has route to its lase tail brick
  4. __BFSAI__ : which take strategy like __SmartAI__ but using BFS map to calculate the distance to the candy instead of euclidean distance. It may die when the candy can not seen and there are body grids located in border