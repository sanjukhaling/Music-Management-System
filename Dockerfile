FROM python:3.11-slim


ENV PYTHONBUFFERED=1

WORKDIR /app
ADD . /app 



# Copy requirements and install dependencies
COPY ./requirements.txt /app/requirements.txt

# Install necessary system dependencies
RUN apt-get update && \
    apt-get install -y \
    postgresql-client \
    libpq-dev

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application files
COPY . /app/

CMD ["python","manage.py","runserver","0.0.0.0:8000"]