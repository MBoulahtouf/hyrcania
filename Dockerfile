# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Configure poetry to not create virtual environment (Docker handles this)
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev

# Copy project files
COPY . .

# Create data directory if it doesn't exist
RUN mkdir -p data/extracted

# Expose Jupyter port
EXPOSE 8888

# Create a startup script
RUN echo '#!/bin/bash\n\
echo "Starting Hyrcania Project..."\n\
echo "Available commands:"\n\
echo "  jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token=\'\' --NotebookApp.password=\'\'"\n\
echo "  python -c \"import ramanspy; print(\'RamanSPy version:\', ramanspy.__version__)\""\n\
echo "  python -c \"import torch; print(\'PyTorch version:\', torch.__version__)\""\n\
echo ""\n\
echo "To start Jupyter Lab, run:"\n\
echo "  docker run -p 8888:8888 -v \$(pwd)/data:/app/data hyrcania jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token=\'\' --NotebookApp.password=\'\'"\n\
echo ""\n\
echo "To run the notebook directly:"\n\
echo "  docker run -p 8888:8888 -v \$(pwd)/data:/app/data hyrcania jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token=\'\' --NotebookApp.password=\'\'"\n\
' > /app/start.sh && chmod +x /app/start.sh

# Set default command
CMD ["/app/start.sh"] 