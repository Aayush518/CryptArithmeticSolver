from flask_frozen import Freezer
from app import app  # Import your Flask app instance

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()
