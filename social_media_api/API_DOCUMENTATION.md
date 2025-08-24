# Social Media API Documentation

This document provides a detailed overview of the API endpoints for the **Social Media API** project. The endpoints cover functionalities such as user authentication, posting, commenting, liking, and retrieving feeds. Each endpoint is backed by Django REST Framework (DRF) and supports JSON input and output. Authentication is required for certain endpoints, as specified in each section.

---

## Base URL
All endpoints listed below assume the base API URL is:
```
http://<your-domain>/api/
```


---

## API Endpoints

### **Posts API**
Endpoints for creating, retrieving, updating, and deleting **posts**.

| Endpoint                                           | HTTP Method | Description                                                                                | Authentication |
|----------------------------------------------------|-------------|--------------------------------------------------------------------------------------------|----------------|
| `/posts/`                                          | GET         | Retrieve a list of all posts. Supports filters (`title`, `content`).                      | Optional       |
| `/posts/`                                          | POST        | Create a new post. Only the logged-in user can create a post.                              | Required       |
| `/posts/{id}/`                                     | GET         | Retrieve a specific post by its ID.                                                       | Optional       |
| `/posts/{id}/`                                     | PUT/PATCH   | Update a specific post by its ID. Only the post's author can update the post.             | Required       |
| `/posts/{id}/`                                     | DELETE      | Delete a specific post by its ID. Only the post's author can delete the post.             | Required       |

#### **Post Fields**
- **title**: The title of the post (string).
- **content**: The main content of the post (string).
- **author**: The user who created the post (automatically set).
- **created_at**: Timestamp when the post was created.
- **updated_at**: Timestamp when the post was last updated.

---

### **Comments API**
Endpoints for managing comments on posts. Comments are tied to specific posts.

| Endpoint                                           | HTTP Method | Description                                                                                | Authentication |
|----------------------------------------------------|-------------|--------------------------------------------------------------------------------------------|----------------|
| `/posts/{post_id}/comments/`                       | GET         | Retrieve a list of comments for a specific post.                                           | Optional       |
| `/posts/{post_id}/comments/`                       | POST        | Add a new comment to a specific post.                                                     | Required       |
| `/posts/{post_id}/comments/{comment_id}/`          | GET         | Retrieve details of a specific comment on a post.                                         | Optional       |
| `/posts/{post_id}/comments/{comment_id}/`          | PUT/PATCH   | Update a comment. Only the comment's author can modify it.                                | Required       |
| `/posts/{post_id}/comments/{comment_id}/`          | DELETE      | Delete a comment. Only the comment's author can delete it.                                | Required       |

#### **Comment Fields**
- **post**: The ID of the post the comment belongs to.
- **content**: The content of the comment (string).
- **author**: The user who created the comment (automatically set).
- **created_at**: Timestamp when the comment was created.

---

### **Like and Unlike API**
Endpoints for liking and unliking a post.

| Endpoint                                           | HTTP Method | Description                                                                                | Authentication |
|----------------------------------------------------|-------------|--------------------------------------------------------------------------------------------|----------------|
| `/posts/{id}/like/`                                | POST        | Like a specific post. If already liked, it returns a response indicating so.               | Required       |
| `/posts/{id}/unlike/`                              | DELETE      | Unlike a specific post. If not liked, it returns a response indicating so.                | Required       |

#### **Like Behavior**
- A user can only like a post once.
- When a user likes a post authored by another user, a notification is sent.

---

### **Feed API**
Retrieve a feed of posts by users the current user is following.

| Endpoint                                           | HTTP Method | Description                                                                                | Authentication |
|----------------------------------------------------|-------------|--------------------------------------------------------------------------------------------|----------------|
| `/feed/`                                           | GET         | Retrieve a list of posts by users the current user is following, sorted by recency.        | Required       |

#### **Feed Behavior**
- If the user is authenticated, posts from followed users are retrieved.
- If the user is unauthenticated, an empty response is returned.

---

### Permissions
The API uses **Django's permissions framework** to enforce access control:
- **IsAuthenticatedOrReadOnly**: Anyone can read (GET), but only authenticated users can perform write operations (POST, PUT, DELETE).
- **IsAuthorOrReadOnly**: Only the content's author can modify or delete it.

---

### Error Responses
All API endpoints return appropriate HTTP status codes and JSON-formatted error messages when errors occur. Some common examples include:

- **401 Unauthorized**: The request requires authentication but no valid credentials were provided.
```json
{
      "detail": "Authentication credentials were not provided."
    }
```

- **403 Forbidden**: The user does not have permissions to perform the action.
```json
{
      "detail": "You do not have permission to perform this action."
    }
```

- **404 Not Found**: The requested resource does not exist.
```json
{
      "detail": "Not found."
    }
```


---

### Example Usage

#### Example 1: Create a New Post
**Request**:
```
POST /api/posts/
Content-Type: application/json
Authorization: Token <user_token>
{
  "title": "My First Post",
  "content": "This is an example post."
}
```


**Response**:
```
201 Created
{
  "id": 1,
  "title": "My First Post",
  "content": "This is an example post.",
  "author": "username",
  "created_at": "2025-08-24T10:00:00Z"
}
```


---

#### Example 2: Like a Post
**Request**:
```
POST /api/posts/1/like/
Authorization: Token <user_token>
```


**Response**:
```
201 Created
{
  "detail": "Liked."
}
```


---

#### Example 3: Retrieve Feed
**Request**:
```
GET /api/feed/
Authorization: Token <user_token>
```


**Response**:
```
200 OK
[
  {
    "id": 1,
    "title": "User1's Post",
    "content": "A great post by User1",
    "author": "user1",
    "created_at": "2025-08-23T14:30:00Z"
  },
  {
    "id": 2,
    "title": "User2's Post",
    "content": "Another fantastic post by User2",
    "author": "user2",
    "created_at": "2025-08-24T08:30:00Z"
  }
]
```


---

### Testing the API
To test this API, you can use tools like:
- [Postman](https://www.postman.com/)
- [Curl](https://curl.se/)
- Django's **browsable API**, available in development mode. Access it via `/api/` in your web browser.

---

This documentation provides an overview of the endpoints for implementing and interacting with the **Social Media API**. Let me know if more details or examples are required!