FROM python:3.7.16

WORKDIR /app

COPY ./student_eval/requirements.txt /app/requirements.txt
# Install gcc and g++
RUN apt install gcc g++ -y

# Install unixodbc-dev
RUN apt update
RUN apt install -y unixodbc-dev

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./common /app/src/common
COPY ./student_eval/app/ /app/src/student_eval/app

CMD ["python", "src/student_eval/app/main.py"]