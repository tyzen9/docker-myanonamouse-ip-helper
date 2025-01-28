FROM python:3-alpine
LABEL maintainer="steve@tyzen9.com"

# Install the Alpine libraries that we need using APK
RUN apk add --no-cache \
        bash \
        curl 

# Set the working directory inside of the image's fileystem
WORKDIR /usr/src/app

# Installed the required Python libraries
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Make a directory on the image's filesystem
# and copy the application into that directory
RUN mkdir -p tyzen9
COPY app/. ./tyzen9/.

# This entry point is used for development, just hangs the container
# so you can interact with the shell
# ENTRYPOINT ["tail", "-f", "/dev/null"]

# Production entry point
ENTRYPOINT ["python3", "tyzen9/main.py"]