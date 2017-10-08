# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Naked Twins is a constraint found while solving Soduku where two boxes (of a UNIT - either row, square, column or diagonal) 
have exactly two and same options. This effectively contraints other box in that UNIT 
to have any of the two digits which are already contained in naked twins.
<BR>
Contraint propogation was used to solve the naked twins problem by removing the values of twins (both digits) from all the 
remaining boxes in the UNIT.
<BR>
<BR>**Sample:**
<BR>Found a twin:  57 ['B2', 'F6'] ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'] ['2', '57', '1', '457', '9', '57', '8', '6', '3']
<BR>After reduction of twin:  57 ['B2', 'F6'] ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'] ['2', '57', '1', '4', '9', '57', '8', '6', '3']


# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Constraint propogation was used to solve diagonal Sudoku problem by adding two diagonal UNITs in the initial initialization.
This ensured that 
<li>all constraints like peers of a particular box etc were found based on diagonal constraints
<li>all strategies like Eliminate, Only Choice and Naked Twins are also applied on diagonal constraints

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - Fill in the required functions in this file to complete the project.
* `test_solution.py` - You can test your solution by running `python -m unittest`.
* `PySudoku.py` - This is code for visualizing your solution.
* `visualize.py` - This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

