# AST Rule Engine

The AST Rule Engine is a backend application built with **FastAPI** and **PostgreSQL** (hosted on Supabase). It provides a robust API for managing rules and evaluating them based on input data.

---

## Features

- **Rule Management**: Create, read, update, and delete rules.
- **Rule Evaluation**: Evaluate rules against input data.
- **Database**: Uses **PostgreSQL** hosted on **Supabase** for data storage.

---

## Technologies Used

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: [PostgreSQL](https://www.postgresql.org/) (hosted on [Supabase](https://supabase.com/))
- **ORM**: SQLAlchemy
- **Validation**: Pydantic

---



```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── rules.py       # Rule management endpoints
│   │       └── router.py          # Main API router
│   ├── core/
│   │   ├── config.py              # Application configuration
│   │   └── settings.py            # Environment settings
│   ├── db/
│   │   ├── base.py                # Database connection setup
│   │   └── migrations/            # Database migrations
│   ├── models/
│   │   ├── rule.py                # Rule model
│   ├── schemas/
│   │   ├── rule.py                # Rule schemas
│   └── services/
│       └── rule_engine.py         # Rule evaluation logic
├── tests/                         # Test files
└── main.py                        # Application entry point
```

---

## API Endpoints

### Rules (`rules.py`)
- **POST /rules/**: Create a new rule.
  - **Request Body**:
    ```json
    {
      "name": "Sample Rule",
      "description": "Sample Description",
      "code": "input_data['value'] > 10"
    }
    ```
  - **Response**: Created rule details.

- **GET /rules/**: List all rules.
  - **Response**: List of rules.

- **GET /rules/{rule_id}**: Get a specific rule.
  - **Response**: Rule details.

- **PUT /rules/{rule_id}**: Update a specific rule.
  - **Request Body**:
    ```json
    {
      "name": "Updated Rule",
      "description": "Updated Description",
      "code": "input_data['value'] > 20"
    }
    ```
  - **Response**: Updated rule details.

- **DELETE /rules/{rule_id}**: Delete a specific rule.
  - **Response**: No content (204).

- **POST /rules/evaluate**: Evaluate a rule against input data.
  - **Request Body**:
    ```json
    {
      "rule_id": 1,
      "input_data": {
        "value": 15
      }
    }
    ```
  - **Response**: Evaluation result (true/false based on the rule logic).

---

## Database Schema

### Rules Table
- `id`: Unique identifier (Primary Key).
- `name`: Name of the rule.
- `description`: Description of the rule.
- `code`: The rule logic (e.g., `input_data['value'] > 10`).
- `is_active`: Whether the rule is active.
- `created_at`: Timestamp of creation.
- `updated_at`: Timestamp of last update.

---

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL (hosted on Supabase)
- FastAPI
- SQLAlchemy
- Pydantic

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ast-rule-engine.git
   cd ast-rule-engine/backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the `backend` directory.
   - Add your Supabase PostgreSQL URL and other configurations:
     ```env
     POSTGRES_URL=postgresql://user:password@host:port/dbname
     ```

4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

5. Access the API documentation:
   - Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.

---

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
