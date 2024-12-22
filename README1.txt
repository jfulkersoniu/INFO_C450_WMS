How to Run the Code
Prerequisites
1. Python 3.6 or higher
2. Flask
3. pymongo
4. werkzeug

You can install the required packages using pip:
With Git bash open:
pip install Flask pymongo werkzeug
--------------------------------------------------------------
Setup
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Set up your MongoDB connection in cluster.py by replacing your_secret_key_here with your actual MongoDB connection string.
--------------------------------------------------------------
Running the Application
1. Navigate to the 1_code directory.
2. Run the Flask application:
Git bash: python app.py
3. Open your web browser and go to http://127.0.0.1:5000/.
--------------------------------------------------------------
Application Structure
app.py: Main application file that sets up the Flask app and routes.
blueprints/: Contains all the blueprints for different parts of the application.
templates/: Contains HTML templates for rendering the web pages.
static/: Contains static files like CSS.