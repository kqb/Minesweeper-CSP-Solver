Solving minesweeper using CSP 

Intro
Minesweeper is a popular classic video game included by some operating systems. It is a puzzled board game where a preset about of mines are placed in a board of grids with variable sizes, the mines are hidden to the players, a player must click on all grids without mines to win the game, players can also right-click to place flag on where they think the mines are. The player starts off with clicking a random grid, which then will review all surrounding grids without any mines in its vicinity (all surrounding 8 grids) all the grids with mines in its vicinity will also be shown, with a number indicating the total amount of mines in a grid’s vicinity. With enough hints, a player can deduce grids that have mines for certain, more difficult cases can occur where the player has to randomly select a grid with no information, or with hints that fail to provide the user with a decisive next move.

The general way to play Minesweeper is to eliminate possibilities based on the hints that are given. The basic strategy to solve the game is to first see if there are any grids where the number on the square is identical to the adjacent number of flags plus the adjacent number of grids that are unrevealed, if they are, the unrevealed grids should be flagged to indicate that they must be mines. The next step is to click any unrevealed grids that are around numbered grids where the number of flags are identical to the number on the grid. If a player follow this strategy properly, they should have enough information to solve the game without making mistakes. In more difficult cases, players cannot determine the placement of mines on just looking at one grid, more than one constraints need to be combined in order to deduce the position of mines. One common strategy to solve Minesweeper is to start in the corner as a first move. This is because corners are the most likely places to have unsolvable positions with logic, the more corner removed gives the player a higher chance of being able to solve the puzzle without getting into tough end-game positions. Since the starting move is guaranteed to not be a mine, starting at a corner can reduce the chance of being stuck in a unsolvable corner by quarter. The reason that corners are unfavorable is because the clues you can get there are fewer than open positions. 
Design
A CSP minesweeper solver is designed to apply cspbase.py and propagators.py from A2. minesweeper_csp.py handles the CSP model for solving our minesweeper game. 

For every step in the minesweeper game, all grids in the game board are assigned with a corresponding variable, we set a variable’s domain to be 1 if it is flagged, and 0 if it revealed and not a mine. For any unrevealed grids, a domain of [0, 1] is assigned. 

Constraints:
The most important part in our CSP solver, is how much information that we can extract from visible grids in a game board, and translate these information to csp constraints.

First, all constraints will be initialized, in this step, all known variables will be assigned a value (0 for revealed, 1 for flagged). In the case where a grid is revealed and has a surrounding mine value, the number of surrounding flags will be subtracted from this value, and this value is subsequently used as the sum of surrounding mines that will be added to the constraints list along with the name and scope of the constraint 
The obvious clues we have are those visible grids:
                        
				figure 1                              figure 2
For example in figure 1, there are 3 unassigned variables named v1, v2 and v3. (as shown in figure 2). The first step creates constraints as follow:
c1: v1 + v2 + v3 = 2
c2:         v1 + v2 = 1
c3:         v2 + v3 = 1
Our csp can not assign any values based on current constraints c1,c2 and c3.
In the next step, we reduce the constraints’ domain, this is done by updating constraints if a subscope exists in constraints e.g. c1=[v1,v2,v3],c2=[v1,v2] => c1 = [v3]. After the reduction of all constraints’ scope if we get constraints with only one variable in the domain, we can be certain that a mine exists on that grid (variable).
We can get more information based on the constraints we created in first step. As the example shown above, c2 scope’s variables are all in c1, and we can reduce c1 to:
c1 - c2: v1 + v2 + v3 - (v1 + v2) = 2 - 1
       c1: v3 = 1
Now by this extra information, we can assign v3 = 1
Additionally, we add new constraints if two constraint has at least two same variables in scope; a new variable is created for overlapped variables. This can infer information about sets of squares. e.g. C1 = [V1,V2,V3], C2 = [V2,V3,V4] => C3 = [V1,V2V3], C4 = [V2V3, V4] where V2V3 is a new variable with domain [0, 1, 2].
Are there any more information we can extract? Let’s take a look at another example:
                         
figure 1                                 figure 2
In figure 1 example, by current constraints we created so far, there is no grid we can assigned a certain value. But is that true? Let’s take a look at figure 2, consider those two underlined assigned variables, we have constraints from above steps:
c1: v1 + v2 + v3 = 2 
c2: v2 + v3 + v4 = 1
and there satisfied tuples are:
c1: {(1,1,0), (1,0,1), (0,1,1)}   c2: {(1,0,0), (0,1,0), (0,0,1)}
When our csp checking v1,v2,v3,v4 ‘s domains, we can see that all values in domain (0 and 1) can find a satisfied tuple, and therefore no assignments. But we could see c1 and c2 have variables v2 and v3 in common. And we know that by c1’s sum, v2 + v3 can not both be 0. So one of them must be a mine. And therefore in c2, v4 must be 0. 
And by c2’s sum, v2 + v3 can not be 2, therefore in c1, v1 must be 1. For pass this information to our csp, we create a new variable and create two new constraints:
let v2v3 be a new variable, and domain is [0, 1, 2] (all possible sums of them):
c3: v1 + v2v3 = 2
c4: v2v3 + v4 = 1
And here are the satisfied tuples for c3 and c4 when we create them:
c3: {(1, 1), (0, 2)}   c4:{(1,0), (0,1)}
Hence our csp can get rid of value 2 since no satisfied tuple in c4. And then c3 only has one satisfied tuple (1,1). So now csp can assign values: v1 = 1, v4 = 0
Search strategy:
For our search strategy, we slightly modified the behavior of CSP.py, first is to keep a variable’s assigned value instead of restoring them each step in the original. The second so to recreate the constants. When we reach a step without a solvable next-step position, we randomly pick the next move.

Minesweeper game
We decided to implement our version of the Minesweeper game (minesweeper.py)  in python with the tkinter GUI library. The game behaves and functions exactly the same as the original except for the first-click behavior.
In the original Windows Minesweeper game, the player is always guaranteed to step on a safe grid, i.e. one without a mine. To ensure this, if a mine is in the position of a player’s first clock, the mine is moved to the upper-left corner of the board before the said grid is uncovered. If the upper-left corner already has a mine, it is moved to the grid directly right of it. This, however does not guarantee that players can have enough clues to deduce a next-step moved. For the purpose of assisting our solver, we decided to follow the logic of Window Vista’s version of minesweeper, In the Windows Vista version of the game, the first clicked square is always a zero (i.e. is not a mine and has no mines adjacent to it). At this time it is not known if the Vista Minesweeper board is generated before or after the player first clicks a square in a new game, but for our game, we generated the mines after the first click, making sure that they are not in the first grid and its vicinity (9 grids). For the board size, we follow the standard Minesweeper game’s 3 different difficulty, beginner: 9x9 with 10, medium: 16x16 with 40, expert: 30x16 with 99










Experiment on success rate of different strategy (other than csp)
based on 1000 times


9x9 grids
10 mines
16x16 grids
40 mines
16x30 grids
99 mines
c1
79.5%
47.7%
1.9%
c1 + c2
92.9%
75.6%
20.0%
c1 + c2 + c3
95.0%
79.0%
33.3%
  c1 + c2 + c3 + c4* 
96.5%
83.8%
35.9%
*c4 is discussed below
Discussion 

Often near the end of a minesweeper game, a player could be stuck in a tricky end-game situation where they do not have enough information to deduce the next step in more than one locations on the board, the bigger the board, the higher the chance of this situation arising. A human player would consider the number of remaining mines in this along with their guesswork. In order to use this information in our solver for improving our win-rate, we first reduce the scope of the constraints, and then add all the remaining variables to equal the number of remaining mines as one constraint so our domain of our satisfying tuples can be smaller. In the worst case we still have an exponential run time based on the amount of variables. For the reason, we choose a small enough threshold before we start applying this constraint, in our case, we chose an arbitrary small number to apply this constraint, in our case we apply the constraint when the number of remaining grids are 20. This number is by no means the optimal number, as it would require extensive experimentation to find the optimal value.

Improvement 1: Use remaining mine info for end-game



    
                 figure 4                     					figure 5

In figure 4, base on our constraints created, csp can not assign any values. But actually we can. There is one information that we haven’t use yet: remaining mines. In figure 5, in those red frames, by the surrounding grids we know that grids in each frame has one mine. And since there are only 4 mines remain, we can know the rest grids are safe, and hence we could click them. One way to extract this information is, create a constraint that contains all variables and the sum is total mine number. But then there is an extreme large set of satisfied tuples, and that will slow down the program dramatically. The best way to do it is to create this constraint when it’s nearly at the end of a game. And when is the end game? That’s the main problem to solve. 
Also there are many ways to get those frames (by different visible grid), how can we decide which one should be frame and maximize the number of the rest unclick grids?

We can use solve the Minesweeper game in 2 ways: logic, or probability.
Solving Minesweeper as a CSP, we deal with logically proving that certain grids have mines, and thus infer the next safe move. While this can take us through most cases, there are cases that we could not logically deduce the next step, In this case using probability (finding the probability of having mines for grids)

Improvement 2: Use probability to chose the best move for indeterminate cases.
Our current algorithm only guesses a random next-move if an indecisive step is reached. We experimented with applying one example case using bayes net, in our particular case (figure 6) 
How to apply Bayesian Network to choose the best move, it is the topic for our future research.


References


http://nothings.org/games/minesweeper/

http://www.techuser.net/mineclick.html

http://www.minesweeper.info/wiki/One_Click_Bug

http://www.cs.toronto.edu/~cvs/minesweeper/minesweeper.pdf


