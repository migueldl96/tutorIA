FROM python:3.9.16

WORKDIR /app

COPY ./content_generator/requirements.txt /app/requirements.txt

# Set the PYTHONPATH to the app directory
ENV PYTHONPATH=/app

COPY ./content_generator/requirements.txt /app/requirements.txt
# Install gcc and g++
RUN apt install gcc g++ -y

# Install unixodbc-dev
RUN apt update
RUN apt install -y unixodbc-dev

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./common /app/src/common
COPY ./content_generator/app/ /app/src/content_generator/app

CMD ["python", "src/content_generator/app/main.py"]