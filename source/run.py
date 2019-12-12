from config import Testing as Config
from app import app

if __name__ == '__main__':
    app.run(host=Config.HOST, port=Config.PORT)
