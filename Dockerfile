# Python 3.10
FROM python:3.10-slim

# set workspace
WORKDIR /app

# install system dependency
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# copy requirements.txt
COPY requirements.txt /app/

# install requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# copy
COPY . /app/

# port
EXPOSE 5001

# enviroment setting
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

# start flash app
CMD ["python", "run.py"]