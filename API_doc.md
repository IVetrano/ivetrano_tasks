# API Documentation

This documentation provides an overview of the API endpoints, including their functionality, request methods, and expected inputs/outputs.

---

## Base URL
`ivetranotask.pythoneverywhere.com`

---

## Tasks Endpoints

### Get All Tasks
**Endpoint:** `/tasks`

**Method:** GET

**Description:** Retrieves a list of tasks based on provided filters.

**Query Parameters:**
- `title`: Filter by task title (string, optional).
- `status`: Filter by task status (int, optional).
- `priority`: Filter by task priority (int, optional).
- `was_made_by`: Filter by task creator (string, optional).
- `assigned_to`: Filter by assigned user (string, optional).
- `end_date`: Filter by end date (date, optional).
- `creation_date`: Filter by creation date (date, optional).
- `id_parent`: Filter by parent task ID (integer, optional).
- `tags`: Filter by associated tags (list of strings, optional).

**Response:**
- Status: `200 OK`
- Body: JSON array of task objects.

---

### Get Task by ID
**Endpoint:** `/tasks/<int:task_id>`

**Method:** GET

**Description:** Retrieves a single task by its ID.

**Path Parameters:**
- `task_id`: ID of the task (integer, required).

**Response:**
- Status: `200 OK`
- Body: JSON object of the task.

**Error Responses:**
- `404 Not Found`: Task not found.

---

### Create Task
**Endpoint:** `/tasks`

**Method:** POST

**Description:** Creates a new task.

**Body Parameters:**
- `title` (string, required): Task title.
- `description` (string, optional): Task description.
- `priority` (int, required): Task priority.
- `status` (int, required): Task status.
- `end_date` (date, required): Task end date.
- `was_made_by` (string, required): Task creator.
- `id_parent` (integer, optional): Parent task ID.
- `tags` (list of strings, optional): Associated tags.
- `assigned_to` (list of strings, optional): Assigned users.

**Response:**
- Status: `201 Created`
- Body: Success message.

**Error Responses:**
- `400 Bad Request`: Missing required field or integrity error.
- `500 Internal Server Error`: Database error.

---

### Update Task
**Endpoint:** `/tasks/<int:task_id>`

**Method:** PUT

**Description:** Updates an existing task.

**Path Parameters:**
- `task_id`: ID of the task (integer, required).

**Body Parameters:**
- `title`, `description`, `priority`, `status`, `end_date` (all optional).
- `tags`: List of new tags (optional).
- `assigned_users`: List of new assigned users (optional).

**Response:**
- Status: `200 OK`
- Body: Success message.

**Error Responses:**
- `400 Bad Request`: No fields provided for update.
- `404 Not Found`: Task not found.
- `500 Internal Server Error`: Database error.

---

### Delete Task
**Endpoint:** `/tasks/<int:id>`

**Method:** DELETE

**Description:** Deletes a task by its ID.

**Path Parameters:**
- `id`: ID of the task (integer, required).

**Response:**
- Status: `200 OK`
- Body: Success message.

**Error Responses:**
- `404 Not Found`: Task not found.
- `500 Internal Server Error`: Database error.

---

## Users Endpoints

### Get All Users
**Endpoint:** `/users`

**Method:** GET

**Description:** Retrieves a list of users.

**Query Parameters:**
- `name`: Filter by user name (string, optional).

**Response:**
- Status: `200 OK`
- Body: JSON array of user objects.

---

### Get User by Username
**Endpoint:** `/users/<string:username>`

**Method:** GET

**Description:** Retrieves a user by their username.

**Path Parameters:**
- `username`: Username of the user (string, required).

**Response:**
- Status: `200 OK`
- Body: JSON object of the user.

**Error Responses:**
- `404 Not Found`: User not found.

---

### Create User
**Endpoint:** `/users`

**Method:** POST

**Description:** Creates a new user.

**Body Parameters:**
- `username` (string, required): User's username.
- `password` (string, required): User's password.
- `name` (string, required): User's name.
- `email` (string, required): User's email.
- `role` (string, optional): User's role.

**Response:**
- Status: `201 Created`
- Body: Success message.

**Error Responses:**
- `400 Bad Request`: Missing required field or integrity error.
- `500 Internal Server Error`: Database error.

---

### Update User
**Endpoint:** `/users/<string:username>`

**Method:** PUT

**Description:** Updates an existing user's information.

**Path Parameters:**
- `username`: Username of the user (string, required).

**Body Parameters:**
- `name`, `password`, `email`, `role` (all optional).

**Response:**
- Status: `200 OK`
- Body: Success message.

**Error Responses:**
- `400 Bad Request`: No fields provided for update.
- `404 Not Found`: User not found.
- `500 Internal Server Error`: Database error.

---

### Delete User
**Endpoint:** `/users/<string:username>`

**Method:** DELETE

**Description:** Deletes a user by their username.

**Path Parameters:**
- `username`: Username of the user (string, required).

**Response:**
- Status: `200 OK`
- Body: Success message.

**Error Responses:**
- `404 Not Found`: User not found.
- `500 Internal Server Error`: Database error.

---

## Tags Endpoints

### Get All Tags
**Endpoint:** `/tags`

**Method:** GET

**Description:** Retrieves a list of tags.

**Query Parameters:**
- `name`: Filter by tag name (string, optional).

**Response:**
- Status: `200 OK`
- Body: JSON array of tag objects.

---

### Get Tag by Name
**Endpoint:** `/tags/<string:name>`

**Method:** GET

**Description:** Retrieves a tag by its name.

**Path Parameters:**
- `name`: Name of the tag (string, required).

**Response:**
- Status: `200 OK`
- Body: JSON object of the tag.

**Error Responses:**
- `404 Not Found`: Tag not found.

---

### Create Tag
**Endpoint:** `/tags`

**Method:** POST

**Description:** Creates a new tag.

**Body Parameters:**
- `name` (string, required): Tag name.
- `colour` (int, optional): Tag color.

**Response:**
- Status: `201 Created`
- Body: Success message.

**Error Responses:**
- `400 Bad Request`: Missing required field or integrity error.
- `500 Internal Server Error`: Database error.

---

### Update Tag
**Endpoint:** `/tags/<string:name>`

**Method:** PUT

**Description:** Updates an existing tag.

**Path Parameters:**
- `name`: Name of the tag (string, required).

**Body Parameters:**
- `name`, `colour` (all optional).

**Response:**
- Status: `200 OK`
- Body: Success message.

**Error Responses:**
- `400 Bad Request`: No fields provided for update.
- `404 Not Found`: Tag not found.
- `500 Internal Server Error`: Database error.

---

### Delete Tag
**Endpoint:** `/tags/<string:name>`

**Method:** DELETE

**Description:** Deletes a tag by its name.

**Path Parameters:**
- `name`: Name of the tag (string, required).

**Response:**
- Status: `200 OK`
- Body: Success message.

**Error Responses:**
- `404 Not Found`: Tag not found.
- `500 Internal Server Error`: Database error.

