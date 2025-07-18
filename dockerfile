FROM mcr.microsoft.com/playwright/python:v1.43.0-jammy

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install Playwright dependencies manually
RUN apt-get update && \
    apt-get install -y libglib2.0-0 libnss3 libx11-xcb1 libxcomposite1 libxcursor1 \
    libxdamage1 libxext6 libxfixes3 libxi6 libxtst6 libatk1.0-0 \
    libatk-bridge2.0-0 libcups2 libdrm2 libdbus-1-3 libxrandr2 \
    libgtk-3-0 libasound2 libxss1 lsb-release wget

# Install Playwright and browsers
RUN playwright install --with-deps

ENV PYTHONUNBUFFERED=1
ENV PLAYWRIGHT_BROWSERS_PATH=0

CMD ["python", "main.py"]
