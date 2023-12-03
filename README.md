# ammf.at URL Shortener

API blueprint for URL shortener with FastAPI.

## How to Run

1. Build a virtual environment.

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

1. Install the dependencies.

    ```bash
    pip install -r requirements.txt
    ```

1. Initiate environment variables in `.env` file.

    e.g.:

    ```bash
    echo -e "ENV_NAME=\"Development\"\nBASE_URL=\"http://localhost:8000\"\nDB_URL=\"sqlite:///./shortener.db\"" > .env
    ```

    Look at `.env_sample` as environment file reference.

1. Run the server.
    ```bash
    uvicorn shortener_app.main:app --reload
    ```

1. Open the homepage in [localhost:8000](http://localhost:8000).

1. Open the API documentation in [Swagger UI](http://localhost:8000/docs).