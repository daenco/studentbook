import logging

from app import app

logging.basicConfig(
    filename='logger.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    filemode='wt',
    level=logging.DEBUG
)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)