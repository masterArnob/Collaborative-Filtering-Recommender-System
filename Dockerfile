# base image
FROM python:3.9-slim

# workdir
WORKDIR /app

# copy
COPY . /app

# run
RUN pip install -r requirements.txt

# port
EXPOSE 5000

# command
CMD ["streamlit", "run", "app.py", "--server.port=5000", "--server.address=0.0.0.0", "--server.headless=true"]