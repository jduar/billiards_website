# # SEAI_B

## Repository structure
    
   Inside the coms directory we (at the moment) find one folder:
       1 flaskproject
    
 
   Inside the folder, flaskproject, we can find the website, i.e, 
    the frontend and backend. It's structured using blueprints, which is a fancy way of saying that
    inside each folder (eg, "Users") we will only find routes and forms, related to 
    the users.
    
## How to setup your python environment

   There are two options to set up the environment:
   * Install system wide
   * Install using virtual environments
    
   In our directory's root folder one can find a "requirements.txt" file which lists
   module names and version numbers. This file is used to avoid manually isntalling every module
   inside by hand.

   ### Virtual environment path

   To create a virtual environment:
   ```
   $ python3 -m venv venv
   ```

   To enter the virtual environment:
   ```
   $ source venv/bin/activate
   ```

   Or if you're using the fish shell:
   ```
   $ source venv/bin/activate.fish
   ```

   ***

    
   To install the libraries use the command below, either system wide or inside your virtual environment:
   ```    
   $ python3 -m pip install -r requirements.txt
   ```
    
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
