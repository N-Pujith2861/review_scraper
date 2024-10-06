# Review Extraction API

## Overview
This API extracts reviews from product pages using browser automation and OpenAI's LLM for dynamic CSS identification.

## API Endpoint
### `GET /api/reviews`
- **Query Parameters**:
  - `url` (required): The URL of the product page to scrape.
  - `page_number` (optional): The page number of reviews to retrieve (default is `1`).

- **Response Format**:
    ```json
    {
      "reviews_count": 100,
      "reviews": [
        {
          "title": "Review Title",
          "body": "Review body text",
          "rating": 5,
          "reviewer": "Reviewer Name"
        }
      ]
    }
    ```

## Error Handling
- Returns HTTP status code `500` with an error message for unexpected errors.
- Returns specific HTTP status codes for client errors (e.g., invalid URL).

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone <repository-url>
