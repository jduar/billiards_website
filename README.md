# # SEAI_B

## Repository structure
    
   Inside the coms directory we (at the moment) find one folder:
       1 flaskproject
    
 
   Inside the folder, flaskproject, we can find the website, i.e, 
    the frontend and backend. It's structured using blueprints, which is a fancy way of saying that
    inside each folder (eg, "Users") we will only find routes and forms, related to 
    the users.
    
## How to setup your python environment

   There are two options of setting up the  environment:
   * Install system wide
   * Install using virtual environments
    
   In our root folder of the directory one can find a "requirements.txt" file,
   that has inside modules names and version numbers. This file is used to avoid manually isntalling
   every module inside by hand.
    
   To install the libraries it's only needed to use the command:
       python -m pip install -r requirements.txt
    
   Or, if using PyCharm, it automatically notices the file and a popup appears to install the modules

## How to run the code
   Execute the run.py file
  
## Todo:
    
  - [ ] Change the hard coded Secret key and databse uri
  - [ ] Add unit tests 
  - [ ] Create statistical analysis of each player
  - [ ] Implement a notification system
  - [ ] Create a friend system (Will need a revamp of the database architecture)
  - [ ] Revamp the game joining process
  - [ ] Implement support for tournaments 

