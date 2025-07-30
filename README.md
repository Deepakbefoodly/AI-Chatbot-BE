# FastAPI Langchain Kit

FastAPI supporting OpenAI LLMs real-time / streaming text and chat  user interfaces.

## Getting Started

### Setting Up the FastAPI Backend Application

There are two methods to set up the backend:

**Option 1: Using Docker**
1. Add your `OPENAI_API_KEY` to the `.env` file located at `.env`.
2. Execute `docker-compose up -d` from the root directory to start the backend.

**Option 2: Setting Up Locally with Python Virtual Environment (venv)**
1. Create a Python virtual environment with `python -m venv env`.
2. Activate the virtual environment:
   - On macOS/Linux: `source env/bin/activate`.
   - On Windows: `env\Scripts\activate`.
3. Install the required dependencies by running `pip install -r requirements.txt`.
4. Add your `OPENAI_API_KEY` to the `.env` file.
5. run `start-server.sh`
6. Or Start the FastAPI backend app with `uvicorn --reload --proxy-headers --host 0.0.0.0 --port 8000 src.main:app`.
   - Note: If you encounter a `ModuleNotFoundError`, ensure that the virtual environment is activated.
