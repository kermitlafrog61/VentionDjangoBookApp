# Book Review API

This is a Book API built using Django Rest Framework (DRF) and Djoser for user authentication. This is a test task for Vention.

## Installation

### Required prerequisites

- Docker Engine
- Docker Compose
- Make installed (optional)
- Python 3.10 (optional)


### Installation process
    
```bash
git clone https://github.com/kermitlafrog61/VentionDjangoBookApp.git
cd VentionDjangoBookAppa
cp .env-example .env
```
Fill out all the necessary fields in .env

## Usage

```bash
make run
```
Wait untill all containers would start, then open localhost on your browser


## Endpoints

### Books
 - GET /books/: Retrieve a list of books with optional filtering by genre author, and publication date range.
 - GET /books/{id}/: Retrieve a detailed information of a book.

### Book Reviews
 - POST /book/{id}/review/: Create a review for a specific book.
 - PUT /book/{id}/review/: Update a review for a specific book.
 - PATCH /book/{id}/review/: Partially update a review for a specific book.
 - DELETE /book/{id}/review/: Delete a review for a specific book.

### Users
 - POST /auth/users/: Register a new user.
 - POST /auth/jwt/create/: Obtain a JSON Web Token (JWT).
 - POST /auth/jwt/refresh/: Refresh an existing JWT.

## Notes
This project was created as a test task for the Vention internship application.
