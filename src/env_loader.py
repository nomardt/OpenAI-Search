import os

import dotenv


# Load environment variables from .env file
dotenv.load_dotenv()

# Accessing environment variables
API_KEY = os.getenv("API_KEY")


def write_env_var(key, value):
    dotenv.set_key(dotenv.find_dotenv(), key, value)
