FROM python:3.11-slim

WORKDIR /app

RUN pip install --upgrade pip uv

COPY . .

RUN uv sync

EXPOSE 3978

CMD ["uv", "run", "app.py"]