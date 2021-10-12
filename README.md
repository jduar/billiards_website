# # SEAI_B

## Repository structure
    
Inside the coms directory we (at the moment) find one folder:
      1 flaskproject
   

Inside the folder, flaskproject, we can find the website, i.e, 
   the frontend and backend. It's structured using blueprints, which is a fancy way of saying that
   inside each folder (eg, "Users") we will only find routes and forms, related to 
   the users.

In our directory's root folder one can find a requirements directory which contains:
* "common.txt" - contains the main dependencies needed to run the application
* "development.txt" - contains additional dependencies that help in development
    
## How to setup your python environment

There are two options to set up the environment:
* Install system wide (actually, don't)
* Install using virtual environments

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

   
To install all development libraries use the command below, either system wide or inside your virtual environment:
```    
$ python3 -m pip install -r requirements/development.txt
```

### Setting up pre-commit

Pre-commit automatically runs a few hooks before a commit in order to ensure the code we commit follows certain rules of linting, adherance to PEP8, general styling guidelines, etc. This makes it easier for committed code to look cleaner and have a standard styling.

In order to install these pre-commmit hooks, run the following inside your virtual environment:
```
$ pre-commit install
```

When you commit for the first time after this step, the process will take longer in order to set up the pre-commit hooks. The isort and black hooks will generally automatically fix the issues it finds, so re-running your commit will usually be enough to get past these. The flake8 hook will take manually fixing whatever it says is wrong.

You can read more about pre-commit [here](https://pre-commit.com/).
    
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
