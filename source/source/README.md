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



// README.md
# Project Support### Introduction
Project Support is an open source platform that enable users share causes they're passionate about and actively involved with with the hopes of connecting with other users equally interested in working with them on the given cause.### Project Support Features
* Users can signup and login to their accounts
* Public (non-authenticated) users can access all causes on the platform
* Authenticated users can access all causes as well as create a new cause, edit their created cause and also delete what they've created.### Installation Guide
* Clone this repository [here](https://github.com/blackdevelopa/ProjectSupport.git).
* The develop branch is the most stable branch at any given time, ensure you're working from it.
* Run npm install to install all dependencies
* You can either work with the default mLab database or use your locally installed MongoDB. Do configure to your choice in the application entry file.
* Create an .env file in your project root folder and add your variables. See .env.sample for assistance.### Usage
* Run npm start:dev to start the application.
* Connect to the API using Postman on port 7066.### API Endpoints
| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |
| POST | /api/user/signup | To sign up a new user account |
| POST | /api/user/login | To login an existing user account |
| POST | /api/causes | To create a new cause |
| GET | /api/causes | To retrieve all causes on the platform |
| GET | /api/causes/:causeId | To retrieve details of a single cause |
| PATCH | /api/causes/:causeId | To edit the details of a single cause |
| DELETE | /api/causes/:causeId | To delete a single cause |### Technologies Used
* [NodeJS](https://nodejs.org/) This is a cross-platform runtime environment built on Chrome's V8 JavaScript engine used in running JavaScript codes on the server. It allows for installation and managing of dependencies and communication with databases.* [ExpressJS](https://www.expresjs.org/) This is a NodeJS web application framework.* [MongoDB](https://www.mongodb.com/) This is a free open source NOSQL document database with scalability and flexibility. Data are stored in flexible JSON-like documents.* [Mongoose ODM](https://mongoosejs.com/) This makes it easy to write MongoDB validation by providing a straight-forward, schema-based solution to model to application data.### Authors
* [Black Developa](https://github.com/blackdevelopa)
* ![alt text](https://avatars0.githubusercontent.com/u/29962968?s=400&u=7753a408ed02e51f88a13a5d11014484bc4d80ee&v=4)### License
This project is available for use under the MIT License.

