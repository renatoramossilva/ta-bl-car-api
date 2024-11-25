# Use an official Python image as the base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

# Install Poetry
RUN pip install poetry

# Set the working directory in the container
WORKDIR /app

# Copy the Poetry configuration files to the container
COPY pyproject.toml poetry.lock /app/

# Install the dependencies using Poetry, which should include uvicorn
RUN poetry install --no-dev

# Install uvicorn separately in case it's not included in poetry dependencies
RUN pip install uvicorn

# Copy the rest of your application code to the container
COPY . /app/

# Expose the port that FastAPI will run on
EXPOSE 8000

# Run FastAPI app with Uvicorn (bind to 0.0.0.0 so it's accessible from outside the container)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
