FROM python:3.8-slim

## Step 1:
# Create a working directory
WORKDIR /app

## Step 2:
# Copy source code to working directory
EXPOSE 8080


## Step 3:
# Install packages from requirements.txt
# hadolint ignore=DL3013
RUN pip install --upgrade pip && pip install -r requirements.txt
## Step 4:
# Expose porcd /path/to/your-projectt 80
EXPOSE 8080

## Step 5:docker build -t image1
# Run app.py at container launch
ENTRYPOINT ["python", "app.py"]





