# AI Business Assistant

## About the Project

AI Business Assistant is a web application developed using Django and Python. The main aim of this project is to help users understand their business data by asking questions.
For example, users can ask questions like:
- What is the total revenue?
- Which product has the highest sales?
- What are the monthly sales?
- Which region performs better?

The application processes the user's question, retrieves the required information from the database, and displays the result in an understandable format.

## Technologies Used

- **Python** – Main programming language.
- **Django** – Backend framework.
- **Django REST Framework** – For creating API endpoints.
- **HTML** – Structure of the web pages.
- **CSS** – Styling and layout.
- **JavaScript** – Handling user interactions and API requests.
- **SQLite** – Database.
- **AI / LLM API** – For AI-based question processing, where integrated.

## Features

- Simple chatbot interface.
- Users can ask business-related questions in natural language.
- Backend processes questions and retrieves relevant data.
- Displays business information in a readable format.
- Uses Django ORM for database operations.
- Handles invalid or unsupported questions.
- Provides a simple interface for interacting with business data.


## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the Project Directory

```bash
cd ai_business_assistant
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Linux:

```bash
source venv/bin/activate
```

For Windows:

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables

If the application uses an external AI API, create a `.env` file in the project root and add the required API key.

```env
AI_API_KEY=your_api_key
```

Do not upload your actual API key to GitHub.

### 7. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Run the Development Server

```bash
python manage.py runserver
```

Open the following URL in your browser:

```text
http://127.0.0.1:8000/
```

## Architecture

1. The user enters a business-related question through the chatbot interface.
2. JavaScript sends the question to the Django backend using an API request.
3. Django processes the question and identifies the required operation.
4. The backend retrieves the required information from the database.
5. The result is converted into a readable response.
6. The response is sent back to the frontend and displayed to the user.

## Conclusion

Through this project, I got practical experience with Django, database operations, API integration, and frontend-backend communication. I also learned how a chatbot can be used to make business data easier to understand without requiring users to know SQL.
