# Use official Playwright Python base image with Chromium installed
FROM mcr.microsoft.com/playwright/python:v1.53.0-jammy

# Set working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install Playwright browsers and dependencies
#generic comment
RUN playwright install --with-deps

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PLAYWRIGHT_BROWSERS_PATH=0

# Start the application
CMD ["python", "main.py"]
