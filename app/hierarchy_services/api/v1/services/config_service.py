from dotenv import load_dotenv


def load_config():
    """Loads the config file"""
    config = load_dotenv(r"configs/staging.env")
    return config
