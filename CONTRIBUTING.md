# Contributing to the repository

Thanks for your interest in contributing to the repository!

To submit PRs, please fill out the PR template along with the PR. If the PR
fixes an issue, don't forget to link the PR to the issue!

## Development Requirements

For development and testing, we use [Poetry](https://python-poetry.org/) for dependency management. The library dependencies and those for development and testing are listed in the `pyproject.toml` file. You may use whatever virtual environment management tool that you would like. These include conda, poetry itself, and virtualenv.

The easiest way to create and activate a virtual environment is by using the [virtualenv](https://pypi.org/project/virtualenv/) package:
```bash
virtualenv "ENV_PATH"
source "ENV_PATH/bin/activate"
pip install --upgrade pip poetry
poetry install --with "test, codestyle"
```

Note that the with command is installing all libraries required for the full development workflow. See the `pyproject.toml` file for additional details as to what is installed with each of these options.

If you need to update the environment libraries, you should change the requirements in the `pyproject.toml` and then update the `poetry.lock` using the command `poetry update`

## Coding guidelines

For code style, we recommend the [google style guide](https://google.github.io/styleguide/pyguide.html).

Pre-commit hooks apply [black](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html) code formatting.

We also use [flake8](https://flake8.pycqa.org/en/latest/) and [pylint](https://pylint.pycqa.org/en/stable/) for further static code analysis. The pre-commit hooks show errors which you need to fix before submitting a PR.

Last but not least, we use type hints in our code which are checked using [mypy](https://mypy.readthedocs.io/en/stable/). The mypy checks are strictly enforced. That is, all mypy checks must pass or the associated PR will not be merge-able.

The settings for `mypy` are in the `mypy.ini`, settings for `flake8` are contained in the `.flake8` file. Settings for `black` and `isort` come from the `pyproject.toml` and some standard checks are defined directly in the `.pre-commit-config.yaml` settings.

All of these checks and formatters are invoked by pre-commit hooks. These hooks are run remotely on GitHub. In order to ensure that your code conforms to these standards, and, therefore, passes the remote checks, you can install the pre-commit hooks to be run locally. This is done by running (with your environment active)

```bash
pre-commit install
```

To run the checks, some of which will automatically re-format your code to fit the standards, you can run
```bash
pre-commit run --all-files
```
It can also be run on a subset of files by omitting the `--all-files` option and pointing to specific files or folders.

If you're using VS Code for development, pre-commit should setup git hooks that execute the pre-commit checks each time you check code into your branch through the integrated source-control as well. This will ensure that each of your commits conform to the desired format before they are run remotely and without needing to remember to run the checks before pushing to a remote. If this isn't done automatically, you can find instructions for setting up these hooks manually online.
