FROM python:3.9
MAINTAINER musaif bhai
COPY . /main
WORKDIR /main
EXPOSE 8000
RUN pip install -r requirements.txt
ENTRYPOINT ["python","main.py"]
