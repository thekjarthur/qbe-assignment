# QBE Lead MLE Take Home Assignment
Repo documenating data manipulation, version control and API development. 

# Setting up the project
1. Clone this repository
2. Create a python environment (3.11.3) using: `python -m venv .venv`. You can install pyenv for additional version control.
3. Activate the virtual environment. For Windows, run `.venv/Scripts/activate` for Linux/Max, run `source .venv/bin/activate`.
4. Install poetry: `pip install poetry`.
5. Install packages: `poetry install`.

# Running the project
1. To start the server, run `python app.py` in the main directory
2. To run test cases, run `python app.py` and `poetry run pytest`

# Development Notes
My usual IDE is VSCODE.  I created successive branches using `git branch branchname`. I used the VSCODE Source Control tool, rather than the `git status`, `git add` and `git commit -m commitmessage` sequences since it's easier to spot errors visually, and I can see the differences more visually. 

At each stage, I would run the server using `python app.py` and test it using Postman to make sure it was all running correctly. I used breakpoints and pdb where needed to ensure correct responses.
