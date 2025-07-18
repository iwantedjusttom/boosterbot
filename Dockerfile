FROM python:3.10-slim

# Install system dependencies needed for Playwright/Chromium
RUN apt-get update && apt-get install -y \
    curl wget gnupg libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 \
    libxss1 libasound2 libxtst6 libxrandr2 xdg-utils libatk-bridge2.0-0 \
    libgtk-3-0 fonts-liberation fonts-noto-color-emoji \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set workdir and copy files
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Install Playwright browsers during image build
RUN playwright install-deps && playwright install chromium

# ✅ Make sure runtime knows where to find the browsers
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Default command to run your app
CMD ["python", "main.py"]
