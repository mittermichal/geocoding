FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=src

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
RUN pip install uvicorn[standard]

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]