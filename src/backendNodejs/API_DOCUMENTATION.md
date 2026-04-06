# Calendar Booking Agent API Documentation

This API provides endpoints for authenticating with Google Calendar and booking meetings based on user availability.

## Base URL
`http://localhost:3000`

---

## Authentication Endpoints

### 1. Generate Login Link
Generates a Google OAuth2 login link for the user to grant calendar access.

- **URL:** `/auth`
- **Method:** `GET`
- **Response:** `200 OK` (HTML page with login link)

### 2. OAuth2 Callback
Handles the callback from Google after user authorization. Saves encrypted tokens to the database.

- **URL:** `/oauth2callback`
- **Method:** `GET`
- **Query Parameters:**
  - `code` (required): Authorization code provided by Google.
- **Response:**
  - `200 OK`: Success message and user email.
  - `500 Internal Server Error`: Error details if token retrieval fails.

---

## Booking Endpoints

### 3. Book a Meeting
Checks the target user's availability and books a meeting if the slot is free.

- **URL:** `/book-meeting`
- **Method:** `POST`
- **Request Body (JSON):**
  | Field | Type | Required | Description |
  | :--- | :--- | :--- | :--- |
  | `targetEmail` | `string` | Yes | The email of the person to book the meeting for. |
  | `startTime` | `string` | Yes | Start time in ISO 801 format (e.g., `2023-10-27T10:00:00Z`). |
  | `endTime` | `string` | Yes | End time in ISO 8601 format (e.g., `2023-10-27T11:00:00Z`). |
  | `meetingTitle` | `string` | No | Title of the meeting. Default: `Scheduled Meeting via Agent`. |

- **Validation Rules:**
  - `targetEmail`, `startTime`, and `endTime` must be provided.
  - `startTime` must be chronologically before `endTime`.
  - The `targetEmail` must be previously authenticated via the `/auth` flow.

- **Response:**
  - `200 OK`:
    - `{ "status": "ok" }`: Meeting booked successfully.
    - `{ "status": "not ok" }`: Time slot is busy.
  - `400 Bad Request`: Missing fields or invalid time range.
  - `404 Not Found`: User not found in database.
  - `500 Internal Server Error`: Server error details.

---

## Interactive Documentation

### Swagger UI
An interactive Swagger UI is available for testing the API directly from your browser.

- **URL:** `/api-docs`
- **Method:** `GET`

---

## Testing

To run the automated test suite:
```bash
yarn test
```
The tests cover validation, availability checks, and successful booking scenarios using mocks for MongoDB and Google APIs.
