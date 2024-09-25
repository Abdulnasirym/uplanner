# Task Planner

A comprehensive task management tool that helps users organize and track their tasks efficiently. This web-based application allows users to create, edit, and delete tasks, set deadlines, receive email reminders, and track task completion. Built with Flask, SQLAlchemy, and integrated with Celery for background tasks like email reminders.

## Table of Contents
- [Introduction](#introduction)
- [Live Demo](#live-demo)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Related Projects](#related-projects)
- [Author](#author)
- [License](#license)

---

## Introduction

The Task Planner is designed to assist users in managing their tasks with features such as start and due dates, notifications for upcoming deadlines, and user authentication. It is a simple and efficient tool for individuals who want to stay on top of their tasks without getting overwhelmed.

The application offers the following features:
- User authentication (login, registration)
- Task creation and editing
- Start and end dates for tasks
- Email reminders for tasks close to their deadline
- Task completion tracking

## Live Demo

Check out the live version of the Task Planner: [Task Planner Deployed Site](https://alxportfolio-9e1b632803db.herokuapp.com/)  
Read the blog post on the final project: [Project Blog Article](#)

## Installation

To set up the Task Planner locally, follow these steps:

### Prerequisites
- Python 3.x
- Flask
- SQLAlchemy
- Celery
- Redis (for background tasks)
- Flask-Mail

### Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/abdulnasirym/uplanner.git
    cd task-planner
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the project root directory and configure the following variables:

    ```bash
    FLASK_APP=run.py
    FLASK_ENV=development
    SECRET_KEY=your_secret_key
    CELERY_BROKER_URL=redis://localhost:6379/0
    CELERY_RESULT_BACKEND=redis://localhost:6379/0
    MAIL_SERVER=smtp.gmail.com
    MAIL_PORT=587
    MAIL_USERNAME=your-email@gmail.com
    MAIL_PASSWORD=your-app-password
    MAIL_USE_TLS=True
    MAIL_USE_SSL=False
    ```

5. **Set up the database:**

    ```bash
    flask db upgrade
    ```

6. **Run the application:**

    ```bash
    flask run
    ```

7. **Run Celery worker:**

    In a separate terminal window, run:

    ```bash
    celery -A app.celery worker --loglevel=info
    ```

8. **Run Redis (if needed):**

    Make sure Redis is running in the background for Celery to process tasks.

## Usage

Once the application is running:

1. Visit the [local app](http://localhost:5000) in your browser.
2. Register for an account or log in if you already have an account.
3. Start creating and managing tasks.
4. Edit or delete tasks as needed.
5. Receive email reminders before task deadlines.

## Contributing

We welcome contributions to the Task Planner project. To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

Please make sure your code follows best practices and includes tests for new functionality.

## Related Projects

Here are some related projects that inspired the Task Planner or are related to task management systems:

- [Trello](https://trello.com/)
- [Todoist](https://todoist.com/)
- [Microsoft To Do](https://to-do.microsoft.com/)

## Author

**Yakubu Abdulnasir Muhammad**  
- LinkedIn: [Yakubu's LinkedIn](https://www.linkedin.com/in/abdulnasirym/) 
- GitHub: [Your GitHub Profile](https://github.com/abdulnasirym)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

