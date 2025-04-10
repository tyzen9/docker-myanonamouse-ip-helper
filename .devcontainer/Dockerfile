FROM python:3-alpine
LABEL maintainer="steve@tyzen9.com"

# Install the Alpine libraries that we need using APK
RUN apk add --no-cache \
        bash \
        curl \
        lftp \
        openssh 

# Set the working directory inside of the image's fileystem
WORKDIR /usr/src

# Installed the required Python libraries
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Make the /downloads directory to mount to
RUN mkdir /downloads

# Make a place to store the known hosts file
RUN mkdir -p /root/.ssh && chmod 700 /root/.ssh

# Make a directory on the image's filesystem
# and copy the application into that directory
RUN mkdir -p tyzen9
COPY app/. tyzen9/.

# Copy the lftp configuration file 
COPY lftp.conf /etc/.

# Production entry point
ENTRYPOINT ["python3", "tyzen9/main.py"]