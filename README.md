# Python 3.7 and up
The code code run in Python 3.7 and later versions. You can [install Python](https://www.python.org/downloads).

## Installation Guide
Run the following command in a terminal download this project:
```
git clone https://github.com/mvr5854/Checkers_Group3.git
```

Then you need to create a virtual environment and install the basic dependencies to run the project on your system:

```
cd Checkers_Group3
python setup.py
```

## To Run the Project
When the virtual environment is active, your terminal typically shows '(venv)' at the beginning.
For example: `(venv) C:\Users\YourUser\project>`

Activate the virtual environment if it is not already activated.
For Windows: 
```
venv\Scripts\activate
```
For Mac/Linux:
```
source venv/bin/activate
```

**To run Jupyter Notebook, use the following command:**
```
jupyter notebook --ip=0.0.0.0 --allow-root
```

## Basic Git commands
**Pull Latest Changes from Remote:**

```
git pull origin main
```
(Replace main with your branch name if different.)

**Push Local Changes to Remote:**

```
git add .                       # Stage all changes
git commit -m "Your message"    # Commit changes
git push origin main            # Push to remote
```
(Replace main with your branch name if different.)

