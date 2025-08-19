# Use Miniconda as base image
FROM continuumio/miniconda3:latest

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV CONDA_ENV_NAME=pix2surf_py39

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libglu1-mesa \
    libxi6 \
    libxkbcommon-x11-0 \
    libxrandr2 \
    libxss1 \
    libxcursor1 \
    libxcomposite1 \
    libasound2 \
    libatk1.0-0 \
    libdrm2 \
    libxdamage1 \
    libxfixes3 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy conda environment file if it exists, otherwise create one
COPY environment.yml* ./
RUN if [ -f environment.yml ]; then \
        conda env create -f environment.yml; \
    else \
        conda create -n $CONDA_ENV_NAME python=3.9 -y; \
    fi

# Activate conda environment and install common packages
RUN echo "source activate $CONDA_ENV_NAME" >> ~/.bashrc
SHELL ["/bin/bash", "-c"]

# Install Python packages in the conda environment
RUN source activate $CONDA_ENV_NAME && \
    conda install -y pytorch torchvision torchaudio cpuonly -c pytorch && \
    conda install -y opencv pillow numpy scipy matplotlib && \
    pip install django opencv-python-headless

# Download and install Blender (headless version)
RUN wget -q https://download.blender.org/release/Blender3.6/blender-3.6.5-linux-x64.tar.xz \
    && tar -xf blender-3.6.5-linux-x64.tar.xz \
    && mv blender-3.6.5-linux-x64 /opt/blender \
    && ln -s /opt/blender/blender /usr/local/bin/blender \
    && rm blender-3.6.5-linux-x64.tar.xz

# Copy the entire project
COPY . .

# Set environment variable for Blender
ENV BLENDER_BIN=/usr/local/bin/blender

# Create necessary directories
RUN mkdir -p /app/backend/data/media \
    && mkdir -p /app/backend/static \
    && mkdir -p /app/logs

# Set correct permissions
RUN chmod +x /app/backend/manage.py

# Create a startup script that activates conda environment
RUN echo '#!/bin/bash\n\
source activate '"$CONDA_ENV_NAME"'\n\
echo "Starting Virtual Try-On System..."\n\
echo "Conda environment: $CONDA_ACTIVE_ENV"\n\
echo "Python version: $(python --version)"\n\
echo "Blender path: $(which blender)"\n\
echo "Django version: $(python -c \"import django; print(django.get_version())\")"\n\
cd /app/backend\n\
python manage.py migrate --noinput\n\
python manage.py collectstatic --noinput\n\
echo "Starting Django development server..."\n\
python manage.py runserver 0.0.0.0:8000\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Start the application
CMD ["/app/start.sh"]