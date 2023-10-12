FROM python:3.11
WORKDIR /app/
ENV FLASK_APP loft_app/app.py
ENV FLASK_RUN_HOST 0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir
CMD ["flask", "run"]
