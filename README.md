# Debate Arena

Welcome to **Debate Arena**, a dynamic web application built with Django that allows users to create, join, and participate in online debates. Engage in intellectual battles, argue your stance, earn points based on argument quality, and rise to the top of the leaderboard. Whether you're a seasoned debater or a curious newcomer, Debate Arena is your platform to shine!

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features
- **Create Debates**: Start your own debate with a custom topic and settings.
- **Join Debates**: Participate in active debates using a unique 6-digit code or direct links.
- **Guest and Authenticated Users**: Join as a guest with a unique name or log in for a personalized experience.
- **Real-Time Scoring**: Arguments are scored using Google Generative AI, rewarding clarity, relevance, and persuasiveness.
- **Interactive Interface**: Styled with Tailwind CSS for a modern, responsive design.
- **History and Results**: View your debate history and see detailed results, including winners.
- **Login and Signup**: Secure user authentication with Django's built-in system.

## Technologies Used
- **Backend**: Django 5.1.7
- **Frontend**: HTML, Tailwind CSS
- **AI Integration**: Google Generative AI for argument scoring
- **Deployment**: Render
- **Other Tools**: Gunicorn (WSGI server), Python 3.11

## Installation

### Prerequisites
- Python 3.11 or higher
- Git
- pip (Python package manager)

### Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/debate-arena.git
   cd debate-arena
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   - Create a `.env` file in the project root or set environment variables directly.
   - Add the following (replace with your actual keys):
     ```
     GOOGLE_API_KEY=your-google-generative-ai-api-key
     SECRET_KEY=your-django-secret-key
     DEBUG=True  # Set to False for production
     ALLOWED_HOSTS=['*']  # Use specific hosts (e.g., ['localhost', '127.0.0.1']) for development
     ```

5. **Apply Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```
   - Visit `http://127.0.0.1:8000/` in your browser to see the app.


## Usage
- **Home Page**: Access the welcome page at `/` to create a debate or join an active one.
- **Create a Debate**: Navigate to `/create/` (login required) to start a new debate. Unauthenticated users will see a popup prompting them to log in.
- **Join a Debate**: Use `/join/` with a 6-digit code or click an active debate link.
- **Debate Room**: Participate in real-time at `/debate/<debate_id>/`, submitting arguments and viewing scores.
- **History**: View your hosted debates at `/history/` (login required).
- **Signup/Login**: Register at `/signup/` or log in at `/accounts/login/`.


## Contributing
We welcome contributions to improve Debate Arena! Here's how you can help:
1. **Fork the Repository**
2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/new-feature
   ```
3. **Commit Your Changes**
   ```bash
   git commit -m "Add new feature"
   ```
4. **Push to the Branch**
   ```bash
   git push origin feature/new-feature
   ```
5. **Open a Pull Request**
   - Describe your changes and request a review.

### Guidelines
- Follow PEP 8 style guidelines.
- Write tests for new features.
- Update the README if you add significant features.

## License
This project is open source.

## Contact
- **Author**: Siddharth Tripathi
- **Email**: sid.dev.2006@gmail.com

Feel free to open an issue or contact me for questions, bugs, or suggestions!
