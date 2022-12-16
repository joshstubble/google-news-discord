FROM python:3.8

# Create a working directory
WORKDIR /app

# Install the required packages
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the source code into the working directory
COPY . .

# Set the entrypoint for the container
ENTRYPOINT ["python", "news_bot.py"]
