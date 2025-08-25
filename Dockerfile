FROM python:3.13

WORKDIR /app

# Install system dependencies & ODBC driver
RUN apt-get update && \
    apt-get install -y curl gnupg apt-transport-https unixodbc-dev build-essential libgssapi-krb5-2 && \
    curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg && \
    curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list | tee /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

# Copy app code
COPY ./app /app

EXPOSE 10000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
