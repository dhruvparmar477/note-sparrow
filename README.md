# note-sparrow

# 📝 NoteSparrow

NoteSparrow is a Django-based web application that allows users to create, manage, and share notes. It supports AI-generated notes using the Google Generative AI API, Markdown formatting, and MySQL as the backend database.

---

## 🚀 Features

- Create and manage personal notes  
- Markdown and rich-text formatting  
- AI-powered note generation  
- Share notes using usernames  
- Secure user authentication (Django admin)

---

## ⚙️ Setup Instructions

Follow these steps to set up the project on your local machine:

#1. Clone the repository
   git clone <your-repo-url>
   cd note-sparrow

#2. Create and activate a virtual environment
   python -m venv VE
   cd VE/Scripts
   activate
   cd ../..

#3. Install project dependencies
   pip install django
   pip install mysqlclient
   pip install python-dotenv
   pip install markdown
   pip install markdownify
   pip install django-markdownify
   pip install google-generativeai

#4. Navigate to the project directory
   cd project_notes

#5. Create a superuser (for Django admin)
   python manage.py createsuperuser

#6. Run the development server
   python manage.py runserver


Now open http://127.0.0.1:8000 in your browser to view the app.


Environment Variables
Create a .env file in the root directory to securely store your API keys and secrets:

GOOGLE_API_KEY=your_google_generative_ai_key


🙌 Contribution
Feel free to fork this repository, make enhancements, and submit a pull request. Contributions are always welcome!
---

Let me know if you'd like to add sections for **screenshots**, **API integration**, or **MySQL DB setup** too!
