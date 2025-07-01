# Employee Search Microservice (FastAPI)

This is a containerized Python FastAPI-based microservice for an HR platform, designed to serve a **searchable employee directory** with multi-tenant support, column customization, performance considerations, and a custom-built rate limiter.

---

## Features

-  **Search API** with filters for:
  - `status` (active, not_started, terminated)
  - `location`, `department`, `position`
  - `company_id` (multi-tenant isolation)
-  **Dynamic Column Output** per organization
-  **Strict Multi-Tenant Protection** — no data leaks between companies
-  **Rate Limiting** per client IP (standard lib only, no external deps)
-  **OpenAPI / Swagger Docs** at `/docs`
-  **Dockerized Deployment**
-  **Unit Test Support**

---

### Query Parameters:

| Parameter     | Type     | Description                      |
|---------------|----------|----------------------------------|
| `company_id`  | int      | Required — organization ID     |
| `status`      | list[str]| Optional — employee statuses      |
| `location`    | str      | Optional — case-insensitive       |
| `department`  | str      | Optional — case-insensitive       |
| `position`    | str      | Optional — case-insensitive       |
| `page`        | int      | Default: 1                        |
| `page_size`   | int      | Default: 10                       |

---

## Rate Limiting (Custom)

This API includes a **custom-built in-memory rate limiter** using only Python's standard library (`time`, `collections.defaultdict`), as required by the task.

###  Default Settings:

- `5` requests
- Per IP address
- In a rolling window of `60` seconds

### Example:

| Request | Result    |
|---------|-----------|
| 1–5     |  Allowed |
| 6th     |  `429 Too Many Requests` with message:<br>`" Rate limit exceeded. Try again later."`

---

## Running with Docker

```bash
# Step 1: Build the image
docker build -t employee-search-api .

# Step 2: Run the container (attach test.db if seeded externally)
docker run -p 8000:8000 --name employee-search employee-search-api
