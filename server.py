from flask_app import app
from flask_app.controllers import index


# Entry point for the application
if __name__ == "__main__":
    # Run the Flask application in debug mode
    app.run(debug=True)
