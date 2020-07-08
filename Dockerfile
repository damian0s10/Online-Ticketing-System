FROM python:3.7
ENV PYTHONUNBUFFERED 1
ADD requirements.txt /
RUN pip install -r requirements.txt
WORKDIR /app
#COPY entrypoint.sh /entrypoint.sh
#RUN chmod +x /entrypoint.sh