# Ripple

Ripple is a project and impact management web application built as my CS50x final project. It is designed to help users organize meaningful projects, manage tasks, track progress, and record the impact their work creates.

## Features

- User registration and login
- Create and manage individual projects
- Add tasks to projects
- Mark tasks as completed
- Automatically calculate project progress
- Record volunteer hours and people reached
- View total project impact
- Dashboard showing projects and task progress
- User-specific projects and data
- Logout functionality

## How It Works

After creating an account and logging in, users can create projects from their dashboard. Each project has its own page where tasks can be added and marked as completed.

Ripple calculates project progress based on the number of completed tasks. Users can also record impact information, including volunteer hours and the number of people reached. Multiple impact records are stored in the database and combined to show the project's total impact.

## Technologies

Ripple was built using:

- Python
- Flask
- SQLite
- SQL
- HTML
- CSS
- Jinja

## Database

Ripple uses a SQLite database to store users, projects, tasks, and impact records.

Projects are connected to the user who created them, while tasks and impact records are connected to their corresponding projects.

## Why I Built Ripple

I wanted my final project to combine the programming concepts I learned in CS50x with an idea that could be useful for organizing projects with a purpose.

Building Ripple allowed me to practice working with Flask routes, databases, authentication, SQL queries, HTML templates, and CSS while bringing those concepts together into one complete web application.

## Future Improvements

Possible future improvements include project deadlines, editing and deleting projects, more detailed impact statistics, and additional ways to visualize project progress.
