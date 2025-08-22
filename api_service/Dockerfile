FROM python:3.13-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Create directory 
WORKDIR /app
# Copy all contents from api_service directory to this app directory
COPY . /app

# We do not want to run our code with root so we need to create a user
RUN api_service_user -u 5678 --disabled-password --gecos "" api_service_user && chown -R api_service_user /app
USER api_service_user

CMD ["uvicorn", "api_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
