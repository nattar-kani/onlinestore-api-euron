FROM python:3.13

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
<<<<<<< HEAD
    apt-get install -y curl gnupg apt-transport-https unixodbc-dev && \
    curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg && \
    curl -sSL https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt
=======
    apt-get install -y curl gnupg apt-transport-https unixodbc-dev build-essential

COPY requirements.txt /app/

# Upgrade pip and install requirements
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
>>>>>>> 6682234 (update dockerfile: fix pip and ODBC driver issues)

COPY ./app /app

EXPOSE 10000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
