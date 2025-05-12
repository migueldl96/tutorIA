FROM python:3.9.22-alpine3.21

WORKDIR /app

# Set the PYTHONPATH to the app directory
ENV PYTHONPATH=/app

COPY ./content_generator/requirements.txt /app/requirements.txt
# Install gcc and g++
RUN apk add --no-cache gcc g++

# Install unixodbc-dev
RUN apk add --no-cache unixodbc-dev

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./common /app/src/common
COPY ./content_generator/app/ /app/src/content_generator/app

CMD ["python", "src/content_generator/app/main.py"]