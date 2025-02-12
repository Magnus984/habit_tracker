# Habit Tracker

## Introduction
Welcome to the Habit Tracker project, designed to help users effectively create, track, and manage their habits on a daily basis. Built with FastAPI, this application ensures a seamless experience by integrating powerful authentication and database management capabilities.

## Installation 
To set up the Habit Tracker application, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   ```
2. **Navigate to the project directory:**
   ```bash
   cd habit_tracker
   ```
3. **Install dependencies:**
   Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   pip install -r requirements.txt
   ```
4. **Set up the database:**
   Configure your database details in `config/config.py` and make sure that the database is running.

5. **Run the application:**
   ```bash
   uvicorn app:app --reload
   ```

## Project Structure

├── README.md ├── api │ └── v1 │ └── routes │ ├── auth.py │ ├── habit_logs.py │ ├── habits.py │ └── users.py ├── app.py ├── config │ ├── config.py │ └── db.py └── schemas ├── schema.py └── utils

### Core Components
- **`app.py`**: Initializes the FastAPI application and configures routes. It includes database schema creation on engine start-up.
- **`config`**: Contains configuration files.
  - `config.py`: Manages application settings using Pydantic.
  - `db.py`: Creates a database engine and session for SQLAlchemy, connecting to a MySQL database.

## Features

### Authentication
Handled by `auth.py`, this module provides endpoints for token management and secure user authentication. It uses OAuth2 for secure login.

### User Management
Managed within `users.py`, this component supports user registration, sending verification emails, and retrieving user details.
- Register a new user
- Verify email addresses
- Retrieve user details

### Habit Management
`habits.py` manages the creation, retrieval, updating, and deletion of habits. 
- Each habit includes details such as name, description, frequency, and reminder time.

### Habit Logs
`habit_logs.py` facilitates logging user activity with habits, offering endpoints to log, update, and retrieve habit logs.

## API Endpoints

This section provides detailed information about the API endpoints available in the project. Each endpoint is designed to handle specific functionalities related to authentication, habit logging, habit management, and user management.

**Note:** All paths are prefixed with **"/api/v1/"**

### Authentication Endpoints

- **Login**
  - **Path**: `/login`
  - **Method**: POST
  - **Description**: Generates an access token used for logging in.

- **Get Current User**
  - **Path**: `/users/me/`
  - **Method**: GET
  - **Description**: Retrieves the current user based on the provided token.

### Habit Logs Endpoints

- **Log Habit**
  - **Path**: `/habit-logs/`
  - **Method**: POST
  - **Description**: Logs a habit for the authenticated user.

- **Get All Logs**
  - **Path**: `/habit-logs/`
  - **Method**: GET
  - **Description**: Retrieves all habit logs for the authenticated user.

- **Get One Log**
  - **Path**: `/habit-logs/:id`
  - **Method**: GET
  - **Description**: Retrieves a specific habit log for the authenticated user.

- **Update Status**
  - **Path**: `/habit-logs/:id`
  - **Method**: PATCH
  - **Description**: Updates the status of a specific habit log.

- **Remove Log**
  - **Path**: `/habit-logs/:id`
  - **Method**: DELETE
  - **Description**: Removes a specific habit log.

### Habits Endpoints

- **Create Habit**
  - **Path**: `/habits/`
  - **Method**: POST
  - **Description**: Creates a new habit for the authenticated user.

- **Get All Habits**
  - **Path**: `/habits/`
  - **Method**: GET
  - **Description**: Retrieves all habits for the authenticated user.

- **Get One Habit**
  - **Path**: `/habits/:id`
  - **Method**: GET
  - **Description**: Retrieves a specific habit for the authenticated user.

- **Update Habit**
  - **Path**: `/habits/:id`
  - **Method**: PATCH
  - **Description**: Updates a specific habit for the authenticated user.

- **Remove Habit**
  - **Path**: `/habits/:id`
  - **Method**: DELETE
  - **Description**: Removes a specific habit for the authenticated user.

### User Management Endpoints

- **Register**
  - **Path**: `/register`
  - **Method**: POST
  - **Description**: Registers a new user and sends a verification email.

- **Verify Email**
  - **Path**: `/verify-email`
  - **Method**: GET
  - **Description**: Verifies email upon registration.

## Contribution
We welcome contributions! Please follow the process of creating a fork, making desired changes, and submitting a pull request.

## License
This project is licensed under the MIT License. See `LICENSE` for further details.