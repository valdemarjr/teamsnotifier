FROM python:3.7-alpine

RUN pip install pymsteams requests

COPY app/send_Release.pyc /app/

WORKDIR /app

CMD ["python","/app/send_Release.pyc"]