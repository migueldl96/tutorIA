FROM python:3.9.22-alpine3.21

WORKDIR /app

FROM python:3.7.16

COPY ./student-eval/requirements.txt /app/requirements.txt
# Install gcc and g++
RUN apk add --no-cache gcc g++

# Install unixodbc-dev
RUN apk add --no-cache unixodbc-dev

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./common /app/src/common
COPY ./student-eval/app/ /app/src/student-eval/app

CMD ["python", "src/student-eval/app/main.py"]