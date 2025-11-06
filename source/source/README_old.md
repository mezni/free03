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




## ⚙️ Configuration


| Product Name  | Description                              | Category    |
| :------------ | :--------------------------------------- | :---------- |
| iPhone 15 Pro | Latest smartphone with A17 Pro chip      | Mobile      |
| MacBook Air   | Lightweight and portable laptop          | Computer    |
| AirPods Pro   | Active noise-cancelling wireless earbuds | Accessories |

## TT
## SmartyPants

SmartyPants converts ASCII punctuation characters into "smart" typographic punctuation HTML entities. For example:

|     Method           |Endpoint                          |Description                         |
|----------------|-------------------------------|-----------------------------|
|POST   |/api/v1/auth/register            |Register a new user           |
|Quotes          |`"Isn't this fun?"`            |"Isn't this fun?"            |
|Dashes          |`-- is en-dash, --- is em-dash`|-- is en-dash, --- is em-dash|

// README.md
# Project Support
### Introduction
API Endpoints
Method	Endpoint	Description	Request Example	Response Example
POST	/register	Register new user	{ "username": "john", "email": "john@example.com", "password": "Secret123!" }	{ "id": "uuid", "username": "john", "email": "john@example.com" }
POST	/login	Authenticate user and get tokens	{ "username": "john", "password": "Secret123!" }	{ "access_token": "...", "refresh_token": "...", "expires_in": 3600 }
POST	/refresh	Refresh access token	{ "refresh_token": "..." }	{ "access_token": "...", "refresh_token": "...", "expires_in": 3600 }
POST	/logout	Invalidate refresh/access token	{ "refresh_token": "..." }	204 No Content
POST	/validate	Validate JWT (introspection)	{ "token": "..." }	{ "active": true, "user_id": "uuid", "roles": ["user"] }
