# Online Store API (Euron)

This is a FastAPI-based backend for a simple online store.  
It supports products and orders, including stock management, order updates, and a secure payment webhook.

## Features

- CRUD operations for **Products**
- CRUD operations for **Orders**
- Stock validation for orders
- HMAC-SHA256 secured **Payment Webhook**
- Swagger UI documentation at `/docs`
- Examples for request/response bodies

## Tech Stack

- Python 3.13
- FastAPI
- SQLAlchemy
- SQL Server (via pyodbc)
- Pydantic for request/response validation

## Getting Started

1. Clone the repo:
```bash
git clone https://github.com/nattar-kani/onlinestore-api-euron.git
cd onlinestore-api-euron
