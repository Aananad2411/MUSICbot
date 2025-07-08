FROM python:3.11

WORKDIR /bot

COPY . .

RUN pip install --upgrade pip \
 && pip install -r requirements.txt

CMD ["python3", "run.py"]
