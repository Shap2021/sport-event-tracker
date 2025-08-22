FROM python:3.13-slim

EXPOSE 8001

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Create an event folder
WORKDIR /event
COPY . /event 

# We do not want to run our code with root so we need to create a user
RUN event_user -u 5679 --disabled-password --gecos "" event_user && chown -R event_user /event
USER event_user

CMD ["uvicorn", "event_consumer.main:app", "--host", "0.0.0.0", "--port", "8001"]
