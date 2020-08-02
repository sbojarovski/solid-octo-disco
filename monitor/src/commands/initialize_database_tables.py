from src.models import (
    WebsiteHealth,
)

MODELS = [
    WebsiteHealth,
]

if __name__ == '__main__':

    for model in MODELS:
        model._create_table()
