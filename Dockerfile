FROM python:3.11-slim

WORKDIR /app

# Install required packages
RUN pip install --no-cache-dir yfinance pandas

COPY script.py .

CMD ["python", "script.py"]
