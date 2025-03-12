# Computer Vision Project

## Setup Virtual Environment and Install Dependencies

This guide will help you set up a Python virtual environment and install the necessary dependencies for the project.

### Prerequisites
- Ensure you have **Python 3** installed on your system.
- You can check your Python version by running:
  ```sh
  python --version
  ```
  or
  ```sh
  python3 --version
  ```

### 1. Create a Virtual Environment

Run the following command in the project directory:

```sh
python -m venv venv
```

This will create a new folder named `venv`, which contains the isolated Python environment.

### 2. Activate the Virtual Environment

- **Windows** (Command Prompt):
  ```sh
  venv\Scripts\activate
  ```
- **Windows** (PowerShell):
  ```sh
  venv\Scripts\activate.ps1
  ```
- **Mac/Linux**:
  ```sh
  source venv/bin/activate
  ```

After activation, your terminal should show `(venv)` at the beginning of the command line.

### 3. Install Requirements

Once the virtual environment is activated, install the required dependencies:

```sh
pip install -r requirements.txt
```

### 4. Verify Installation

Check if the required packages are installed correctly:

```sh
pip list
```

### 5. Deactivate the Virtual Environment (When Done)

To exit the virtual environment, run:

```sh
deactivate
```

Now your environment is set up, and you can start working on the project! 🚀

