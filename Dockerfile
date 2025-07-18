FROM mcr.microsoft.com/playwright/python:v1.43.0-jammy

WORKDIR /app

COPY . .

# Install Python dependencies and Playwright browsers in one step
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    playwright install --with-deps

ENV PYTHONUNBUFFERED=1
ENV PLAYWRIGHT_BROWSERS_PATH=0

CMD ["python", "main.py"]
