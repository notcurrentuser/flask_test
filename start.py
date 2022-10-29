import os

from dotenv import load_dotenv

from app import models, api
from scripts import parse_csv

load_dotenv()


if __name__ == '__main__':
    if os.getenv("IS_FIRST_START") == '1':
        models.reset_db()
        parse_csv.parse()

    api.start_api()
