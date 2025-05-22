import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    SECRET_KEY = 'your-secret-key-here'  # Change this to a random string
    
    # Display settings
    DISPLAY_METHOD = 'dev'  # Options: 'tiv', 'fbi', 'ascii'
    
    # Ensure upload directory exists
    @classmethod
    def init_app(cls):
        os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)