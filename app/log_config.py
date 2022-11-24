def log_config():
    """
    Get Log configurations
    Return:
        Log configuration with respect to settings
    """
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "format": "[%(asctime)s,%(msecs)03d] [%(levelname)s] %(message)s",
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "format": "[%(asctime)s,%(msecs)03d] [%(levelname)s] %(message)s",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "uvicorn.error": {"level": log, "handlers": ["default"], "propogate": False},
            "uvicorn.access": {"level": log, "handlers": ["access"], "propagate": "no"},
        },
    }