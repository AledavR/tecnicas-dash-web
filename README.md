# Dash Web - MDTC

This repository contains a dash web page implementation of different mathematical models.

## Setup

To run the dash web page follow these steps:

1. Clone this repository

2. Create a python virtual environment in the repository's directory

```
python -m venv dash-web-venv
```

3. Source the virtual environment

- On windows: 
```
.\venv\dash-web-venv\Scripts\activate
```

- On Linux:
```
source dash-web-venv/bin/activate
```

4. Install python dependencies:

```
pip install numpy scipy dash sympy dash-daq dash-mantine-components
```

5. Run the server:

```
python app.py
```


## Contribution

- When pushing a commit be sure to be descriptive with your changes. 
- Make sure that your code works before pushing.
- When creating your `venv` use any name that ends in venv e.g. `dash-venv` or `.venv`
