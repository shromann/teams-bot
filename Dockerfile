FROM python:3.11-slim

WORKDIR /app

# Upgrade pip and install uv (package manager)
RUN pip install --upgrade pip uv

COPY . .

# Install dependencies defined in your project (uv sync)
RUN uv sync

EXPOSE 3978

# Run the aiohttp server via python
CMD ["python", "app.py"]
