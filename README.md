# Pacman-Multi-Agent-Search
Helping Pacman win mazes by avoiding and consuming ghosts

![alt text](https://inst.eecs.berkeley.edu/~cs188/sp21/assets/images/pacman_multi_agent.png)


<h3> Question 1 : Reflex Agent </h3> <br>

We can test our implementation by checking different maze sizes (tiny medium big)

suggested tests: </br>

```
python pacman.py -p ReflexAgent -l testClassic
```

```
python pacman.py --frameTime 0 -p ReflexAgent -k 1
```
autograder

```
python autograder.py -q q1
```

<br>


<h3> Question 2 : Minimax </h3> <br>

We can test our implementation by checking different maze sizes (tiny medium big)

suggested test: </br>

```
python pacman.py -p MinimaxAgent -l trappedClassic -a depth=3
```

autograder

```
python autograder.py -q q2
```

<br>



<h3> Question 3 : Alpha-Beta Pruning </h3> <br>

We can test our implementation by checking different maze sizes (tiny medium big)

suggested test: </br>

```
python pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic
```


autograder

```
python autograder.py -q q3
```

<br>



<h3> Question 4 : Expectimax </h3> <br>

We can test our implementation by checking different maze sizes (tiny medium big)

suggested tests: </br>

```
python pacman.py -p ExpectimaxAgent -l minimaxClassic -a depth=3
```
autograder

```
python autograder.py -q q4
```

<br>




<h3> Question 5 : Evaluation Function </h3> <br>

We can test our implementation by checking different maze sizes (tiny medium big)</br>

autograder (no graphics) :  

```
python autograder.py -q q5 --no-graphics
```


autograder

```
python autograder.py -q q5
```

<br>
