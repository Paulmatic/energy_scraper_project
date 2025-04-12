# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Make sure your script is copied correctly
RUN ls -la /app  # This will list files in /app, check if scrape_energy_data.py exists

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5432 for PostgreSQL connection if needed
EXPOSE 5432

# Run the script when the container launches
CMD ["python3", "scrape_energy_data.py"]
