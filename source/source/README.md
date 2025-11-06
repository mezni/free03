# 🔐 Auth Service API

The **Auth Service** is a Rust-based microservice built on **Actix-Web** that integrates with **Keycloak** for user authentication (AuthN) and authorization (AuthZ).  
It exposes a simplified and secure REST API for managing users, roles, permissions, and tokens.

This service provides:
- 🧍 User registration & authentication  
- 👤 User, role, and permission management  
- 🔑 Token generation, validation, and refresh  
- 🧩 Integration with Keycloak’s Admin REST API  
- 📘 OpenAPI documentation via `utoipa`

---

## 🏗️ Architecture Overview

      ┌───────────────────────────────┐
      │          Frontend / API       │
      └──────────────┬────────────────┘
                     │
       (REST calls to Auth Service)
                     │
    ┌────────────────┴──────────────────┐
    │          Auth Service              │
    │ Actix-Web + Reqwest + Keycloak API │
    └────────────────┬──────────────────┘
                     │
                     ▼
         ┌────────────────────────┐
         │        Keycloak         │
         │ (Users, Roles, Tokens)  │
         └────────────────────────┘

---
## 🔐 Registration, Login and Tokens Sequence

![alt text](<auth_sequence.svg>)

## 🔐 role and permission management
![alt text](<role_sequence.svg>)

## ⚙️ Configuration

Environment variables:

```env
# Keycloak
KEYCLOAK_BASE_URL=http://localhost:8080
KEYCLOAK_REALM=myrealm
KEYCLOAK_CLIENT_ID=auth-service
KEYCLOAK_CLIENT_SECRET=xxxxxxxxxxxx
KEYCLOAK_ADMIN_USER=admin
KEYCLOAK_ADMIN_PASSWORD=admin

# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=8081
LOG_LEVEL=info
```

## 🔐 Authentication Endpoints (Public)
| Method   | Endpoint                | Description                                       | Request Example                                                                 | Response Example                                                                                  |
| -------- | ----------------------- | ------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| **POST** | `/api/v1/auth/register` | Register a new user                               | `{ "username": "john", "email": "john@example.com", "password": "Secret123!" }` | `{ "id": "uuid", "username": "john", "email": "john@example.com" }`                               |
| **POST** | `/api/v1/auth/login`    | Authenticate user and get access & refresh tokens | `{ "username": "john", "password": "Secret123!" }`                              | `{ "access_token": "...", "refresh_token": "...", "expires_in": 3600 }`                           |
| **POST** | `/api/v1/auth/refresh`  | Refresh access token using refresh token          | `{ "refresh_token": "..." }`                                                    | `{ "access_token": "...", "refresh_token": "...", "expires_in": 3600 }`                           |
| **POST** | `/api/v1/auth/logout`   | Logout user (invalidate refresh/access token)     | `{ "refresh_token": "..." }`                                                    | `204 No Content`                                                                                  |
| **POST** | `/api/v1/auth/validate` | Validate JWT token (introspection)                | `{ "token": "..." }`                                                            | `{ "active": true, "user_id": "uuid", "roles": ["user"] }`                                        |
| **GET**  | `/api/v1/auth/userinfo` | Get user info from access token                   | Header: `Authorization: Bearer <token>`                                         | `{ "sub": "uuid", "email": "john@example.com", "roles": ["user"], "preferred_username": "john" }` |


## 👤 User Management (Admin Only)
| Method     | Endpoint            | Description          | Request Example                                                                          | Response Example                                                        |
| ---------- | ------------------- | -------------------- | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| **GET**    | `/users`            | List all users       | —                                                                                        | `[ { "id": "uuid", "username": "john", "email": "john@example.com" } ]` |
| **GET**    | `/users/{id}`       | Get user by ID       | —                                                                                        | `{ "id": "uuid", "username": "john", "roles": ["user"] }`               |
| **POST**   | `/users`            | Create user          | `{ "username": "admin", "email": "a@a.com", "password": "Pass123", "roles": ["admin"] }` | `{ "id": "uuid", "username": "admin" }`                                 |
| **PUT**    | `/users/{id}`       | Update user info     | `{ "email": "new@domain.com" }`                                                          | `{ "id": "uuid", "username": "john", "email": "new@domain.com" }`       |
| **DELETE** | `/users/{id}`       | Delete a user        | —                                                                                        | `204 No Content`                                                        |
| **POST**   | `/users/{id}/roles` | Assign roles to user | `{ "roles": ["manager", "viewer"] }`                                                     | `200 OK`                                                                |

## 🧩 Role Management
| Method     | Endpoint                  | Description                | Request Example                                        | Response Example                                            |
| ---------- | ------------------------- | -------------------------- | ------------------------------------------------------ | ----------------------------------------------------------- |
| **GET**    | `/roles`                  | List roles                 | —                                                      | `[ { "id": "uuid", "name": "admin" } ]`                     |
| **GET**    | `/roles/{id}`             | Get role by ID             | —                                                      | `{ "id": "uuid", "name": "user", "permissions": ["read"] }` |
| **POST**   | `/roles`                  | Create new role            | `{ "name": "manager", "description": "Manage teams" }` | `{ "id": "uuid", "name": "manager" }`                       |
| **PUT**    | `/roles/{id}`             | Update role                | `{ "description": "Updated desc" }`                    | `{ "id": "uuid", "name": "manager" }`                       |
| **DELETE** | `/roles/{id}`             | Delete role                | —                                                      | `204 No Content`                                            |
| **POST**   | `/roles/{id}/permissions` | Assign permissions to role | `{ "permissions": ["user:read", "user:write"] }`       | `200 OK`                                                    |

## ⚙️ Permission Management
| Method     | Endpoint            | Description           | Request Example                                            | Response Example                            |
| ---------- | ------------------- | --------------------- | ---------------------------------------------------------- | ------------------------------------------- |
| **GET**    | `/permissions`      | List permissions      | —                                                          | `[ { "id": "uuid", "name": "user:read" } ]` |
| **GET**    | `/permissions/{id}` | Get permission by ID  | —                                                          | `{ "id": "uuid", "name": "user:delete" }`   |
| **POST**   | `/permissions`      | Create new permission | `{ "name": "user:create", "description": "Create users" }` | `{ "id": "uuid", "name": "user:create" }`   |
| **PUT**    | `/permissions/{id}` | Update permission     | `{ "description": "Updated" }`                             | `{ "id": "uuid", "name": "user:create" }`   |
| **DELETE** | `/permissions/{id}` | Delete permission     | —                                                          | `204 No Content`                            |
