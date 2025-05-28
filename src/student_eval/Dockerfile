FROM python:3.7.16

WORKDIR /app

COPY ./student_eval/requirements.txt /app/requirements.txt
# Install gcc and g++
RUN apk add --no-cache gcc g++

# Install unixodbc-dev
RUN apk add --no-cache unixodbc-dev

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./common /app/src/common
COPY ./student_eval/app/ /app/src/student_eval/app

CMD ["python", "src/student_eval/app/main.py"]