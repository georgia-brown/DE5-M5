FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python3", "./load_and_clean_csv.py"]