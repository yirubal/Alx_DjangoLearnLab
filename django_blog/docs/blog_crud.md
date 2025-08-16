# Django Blog Feature Documentation

This document provides an overview of the blog post features available in the `django_blog` app. It covers the usage, permissions, and data handling details for each implemented feature.

---

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Blog Post Features](#blog-post-features)
    - [Create a Blog Post](#create-a-blog-post)
    - [List All Posts](#list-all-posts)
    - [View Post Details](#view-post-details)
    - [Update a Post](#update-a-post)
    - [Delete a Post](#delete-a-post)
    - [Commenting System (optional)](#commenting-system-optional)
4. [Permissions](#permissions)
5. [Data Handling](#data-handling)
6. [Special Notes](#special-notes)
7. [Contributing](#contributing)

---

## Overview

`django_blog` is a simple Django application that allows users to create, view, update, and delete blog posts. It also supports user authentication for managing permissions.

---

## Installation

1. Add `django_blog` to your Django project's `INSTALLED_APPS` in `settings.py`:

    ```python
    INSTALLED_APPS = [
        ...
        'django_blog',
    ]
    ```

2. Run migrations:

    ```bash
    python manage.py makemigrations django_blog
    python manage.py migrate
    ```

---

## Blog Post Features

### Create a Blog Post

- **Usage:** Authenticated users can create new blog posts using the provided form at `/blog/create/`.
- **Fields:** Title, Content, Author (auto-assigned), Timestamp (auto-assigned).
- **Notes:** Only logged-in users can create posts.

### List All Posts

- **Usage:** View all published blog posts at `/blog/`.
- **Details:** Shows post titles, authors, and snippets of content.
- **Notes:** Publicly accessible unless otherwise restricted.

### View Post Details

- **Usage:** Click on a post title to view full details at `/blog/<post_id>/`.
- **Details:** Displays the full content, author, and timestamp.
- **Notes:** May include a commenting section if implemented.

### Update a Post

- **Usage:** Authors can edit their own posts at `/blog/<post_id>/edit/`.
- **Permissions:** Only the original author or users with staff/admin rights can edit a post.
- **Notes:** Unauthorized users will receive a permission error.

### Delete a Post

- **Usage:** Authors can delete their own posts at `/blog/<post_id>/delete/`.
- **Permissions:** Only the original author or users with staff/admin rights can delete a post.
- **Notes:** Deletion is permanent and cannot be undone.

### Commenting System (optional)

- **Usage:** If implemented, authenticated users can comment on posts.
- **Permissions:** Only logged-in users can comment.
- **Notes:** Comments are moderated by post authors/admins.

---

## Permissions

- **Creating Posts:** Only authenticated users.
- **Editing/Deleting Posts:** Only post authors or users with staff/admin status.
- **Viewing Posts:** By default, all users (can be restricted).

---

## Data Handling

- **User Data:** User information is retrieved from Django's built-in authentication system.
- **Post Data:** Stored in the database with references to the author.
- **Comment Data:** (If implemented) Linked to both the post and the user.

---

## Special Notes

- **Security:** All data-modifying actions require user authentication.
- **Validation:** All forms include server-side validation.
- **Extensibility:** You can add features like tags, categories, or image uploads by extending the models.

---

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes with descriptive messages.
4. Submit a pull request.

---

## License

This project is licensed under the MIT License.

---

**For more detailed API or code documentation, see comments in the respective Python files.**