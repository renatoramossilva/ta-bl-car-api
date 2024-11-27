# Use an official Python image as the base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

# Install Poetry and other dependencies
RUN pip install --no-cache-dir poetry uvicorn

# Set the working directory in the container
WORKDIR /app

# Copy the Poetry configuration files to the container
COPY pyproject.toml poetry.lock /app/

# Install the dependencies using Poetry
RUN poetry install --no-dev

# Copy the rest of your application code to the container
COPY . .

# Run tests and generate coverage report
RUN coverage run -m pytest && coverage html

# Expose the ports: 8000 for the app and 5001 for the coverage report
EXPOSE 8000 5001

# Start the app and serve the coverage report
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 & python -m http.server 5001 --directory htmlcov"]
