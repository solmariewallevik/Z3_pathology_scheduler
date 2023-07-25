
# Resource Scheduling For The Pathology Department 
## Using Z3 (an SMT solver), written in Python
This is the code created for my master thesis where I am exploring if an SMT solver is able to solve a resources scheduling problem and if it
is possible to optimize the solution provided with the help of the Z3 with Optimize.  
By applying the results to the pathology department with the help of actual data collected from the department. 


I created a base case and gradually added more constraints in order to accomodate all of the different demands and rules that the department has. 
The base case can be found in **scheduler_BaseCase.py**. This part only deals with the distribution of sampels. Making sure that the 
correct amount of points are distributed and that the correct samples goes to the correct pathologists. 


In **problem_setup.py**, the z3 logic is found for the expansion of the base case. The optimization part of the program is also found here.
**main.py** contains the number of pathologists, simulation of amount of samples and the simulation of a week. 
It is also where the code needs to be run from.

The last file important in this directory is **test_data.py**. This is where all of the data collected from the pathology department is stored. 
The rest of the files are just to be ignored. 