# Demo API Requirements

- GET `/health` -> `{ "status": "ok" }`
- POST `/echo` -> returns whatever JSON body was sent, under `received`.
- Project is covered by automated tests in `tests/`.
