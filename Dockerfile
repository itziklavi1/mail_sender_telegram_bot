# Use the official Python image as base image
FROM python:3.9-slim


#TBD
# Set environment variables
#ENV PYTHONUNBUFFERED=1 \
#    TOKEN="********" \
#    BOT_USERNAME="@Itzik_mail_sender_bot"

# Set work directory
WORKDIR /app

# Copy requirements.txt to the work directory
COPY requirements.txt .

#update and install wget
RUN apt-get update && apt-get install -y wget

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files to the work directory
COPY . .

# Expose port
EXPOSE 80

CMD ["python", "main.py"]
