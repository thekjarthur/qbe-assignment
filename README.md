# QBE Lead MLE Take Home Assignment
Repo documenating data manipulation, version control and API development.

# Setting up the project
1. Clone this repository
2. Create a python environment (3.11.3) using: `python -m venv .venv`. You can install pyenv for additional version control.
3. Activate the virtual environment. For Windows, run `.venv/Scripts/activate` for Linux/Max, run `source .venv/bin/activate`.
4. Install poetry: `pip install poetry`.
5. Install packages: `poetry install`.
6. Install coverage `pip install coverage`.

# Running the project
1. Activate the virtual environment. For Windows, run `.venv/Scripts/activate` for Linux/Max, run `source .venv/bin/activate`.
2. To start the server, run `python qbe_app.py` in the main directory.
3. To run test cases, run `poetry run pytest` to run test cases.
4. To test the server manually, you can use [Postman](https://www.postman.com/). Create a new collection and a new request. Set the address to `http://localhost:3000`, and the request type to `POST`. In the `body` section, change the payload type to `raw` and enter your json data.

# Development Notes
My usual IDE is VSCODE.  I created successive branches using `git branch branchname`. I used the VSCODE Source Control tool, rather than the `git status`, `git add` and `git commit -m commitmessage` sequences since it's easier to spot errors visually, and I can see the differences more visually.

At each stage, I would run the server using `python qbe_app.py` and test it using Postman to make sure it was all running correctly. I used breakpoints and pdb where needed to ensure correct responses.

I installed pre-commits and setup a few checks for coverage, and code quality. Those can be ran manually using `pre-commit run --all-files`, and is automatically run on the Github Actions, whenever a PR that targets main is created. I have added a rule to prevent merging if pre-commit checks fail, though, because this is a private repo with a non-organization github account, that rule is not enforced.
