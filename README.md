# Blogging Platform API

A RESTful API for a personal blogging platform, built with Flask and SQLite3. Supports full CRUD operations on blog posts, plus a wildcard search across title, content, and category.

This project is part of the [roadmap.sh Backend Developer path](https://roadmap.sh/projects/blogging-platform-api).

## Tech Stack

- **Language:** Python
- **Framework:** Flask
- **Database:** SQLite3

## Project Structure

```
.
├── app.py          # Flask app: routes and request handling
├── init_db.py      # One-time script to create the database and posts table
└── blog.db         # SQLite database file (created by init_db.py, not committed to git)
```

## Setup

1. Clone the repository and navigate into it.

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   source .venv/bin/activate   # macOS/Linux
   ```

3. Install dependencies:

   ```bash
   pip install flask
   ```

4. Initialize the database (run once):

   ```bash
   python init_db.py
   ```

5. Start the server:

   ```bash
   python app.py
   ```

The API will be running at `http://localhost:5000`.

## Data Model

Each blog post has the following fields:

| Field        | Type          | Notes                              |
|--------------|---------------|-------------------------------------|
| `id`         | integer       | Auto-generated                      |
| `title`      | string        | Required                            |
| `content`    | string        | Required                            |
| `category`   | string        | Required                            |
| `tags`       | array of strings | Required; stored as a JSON string internally |
| `created_at` | string        | Auto-generated on creation          |
| `updated_at` | string        | Auto-generated on creation, refreshed on update |

## Endpoints

### Create a post

```
POST /posts
```

**Body:**
```json
{
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post.",
  "category": "Technology",
  "tags": ["Tech", "Programming"]
}
```

**Responses:**
- `201 Created` — returns the newly created post
- `400 Bad Request` — missing required fields

### Get all posts

```
GET /posts
```

Returns an array of all posts.

**Response:** `200 OK`

### Search posts

```
GET /posts?term=tech
```

Performs a wildcard search across `title`, `content`, and `category`, and returns matching posts.

**Response:** `200 OK`

### Get a single post

```
GET /posts/<id>
```

**Responses:**
- `200 OK` — returns the post
- `404 Not Found` — no post with that id

### Update a post

```
PUT /posts/<id>
```

**Body:** same shape as create.

**Responses:**
- `200 OK` — returns the updated post
- `400 Bad Request` — missing required fields
- `404 Not Found` — no post with that id

### Delete a post

```
DELETE /posts/<id>
```

**Responses:**
- `204 No Content` — post deleted
- `404 Not Found` — no post with that id

## Example Usage (curl)

```bash
# Create a post
curl -X POST http://localhost:5000/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Post", "content": "Hello world", "category": "Tech", "tags": ["Tech", "Python"]}'

# Get all posts
curl http://localhost:5000/posts

# Get one post
curl http://localhost:5000/posts/1

# Search posts
curl "http://localhost:5000/posts?term=tech"

# Update a post
curl -X PUT http://localhost:5000/posts/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title", "content": "New content", "category": "Tech", "tags": ["Tech"]}'

# Delete a post
curl -X DELETE http://localhost:5000/posts/1
```

## Notes

- No authentication, authorization, or pagination is implemented, per project scope.
- `tags` are stored as a JSON-serialized string in SQLite (which has no native array type) and converted back to a list on read.
- Each request opens its own database connection, since SQLite connections aren't safe to share across threads and Flask's dev server can handle requests on different threads.
