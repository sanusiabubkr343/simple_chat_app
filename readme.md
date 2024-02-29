
```markdown
# Simple Chat API

## Overview
Simple Chat API is a backend service that provides functionalities for user authentication, messaging, and message tracking.This project demonstrates a non-monolithic architecture, where the frontend and backend are decoupled. It allows for flexibility in choosing the frontend framework. This README provides instructions on setting up the project locally and utilizing its features.


## Getting Started

1. Clone the repository:

```bash
git clone <repository_url>
cd simple-chat-api
```

2. Create a `.env` file in the root folder by copying the `.env.sample` file. Fill in the required environmental variables in the `.env` file.

3. Build and start the Docker containers:

```bash
docker-compose -f docker-compose.dev.yml build
docker-compose -f docker-compose.dev.yml up
```

## Usage

After starting the service, you can interact with it using the provided API endpoints. Below are some essential routes:

- **Signup and Login:** 
  - Use the provided API documentation to sign up and log in:
    - [API Documentation](http://0.0.0.0:10009/api/v1/doc/#/)

  ![Screenshot from 2024-02-29 17-53-35](https://github.com/sanusiabubkr343/simple_chat_app/assets/68224344/2da4f81d-4eb1-4ff2-b6c0-58f7a56aeb2f)
  ![Screenshot from 2024-02-29 17-55-43](https://github.com/sanusiabubkr343/simple_chat_app/assets/68224344/2347800d-6d24-48be-aec7-ad99ece95346)
  ![Screenshot from 2024-02-29 17-57-16](https://github.com/sanusiabubkr343/simple_chat_app/assets/68224344/682670c8-83e8-466f-aebb-e29dfbe64c85)
  ![Screenshot from 2024-02-29 17-58-04](https://github.com/sanusiabubkr343/simple_chat_app/assets/68224344/41794d5e-428a-4751-b5d3-d6e09bb0cf98)




- **WebSocket Messaging:**
  - Connect to the WebSocket using the provided URL and access token.
  - Use Postman to create a new WebSocket request and connect to the URL. Pass the access token as a parameter.
  - Send JSON payload requests to send messages.

  ```json
  { 
    "message": "Good morning, kalshnikov",
    "receiver": 2,
    "unique_identifier": "unique_identifier-1-and-2"
  }
  ```

  Unique identifiers are generated from the frontend to facilitate message tracking. Messages are saved to the database.

  ![Screenshot from 2024-02-29 18-00-24](https://github.com/sanusiabubkr343/simple_chat_app/assets/68224344/7232cb18-7fef-4aac-83b9-24d6b4306e56)
 ![Screenshot from 2024-02-29 18-02-08](https://github.com/sanusiabubkr343/simple_chat_app/assets/68224344/3c0703bb-c7b1-44ee-8c31-d13f553fc670)


- **Viewing Messages:**
  - Access the API documentation to view all messages.
  - Use the chat viewsets to fetch messages between users or groups.

 ![Screenshot from 2024-02-29 18-05-12](https://github.com/sanusiabubkr343/simple_chat_app/assets/68224344/d4fba525-2b39-4a02-948c-ac088580e722)
 ![Screenshot from 2024-02-29 18-07-18](https://github.com/sanusiabubkr343/simple_chat_app/assets/68224344/c2e5d43c-d561-40c0-9674-de935dc1c7d1)



- **Updating Read Recipient:**
  - Execute the `confirm_recipient` endpoint to update `read_recipient` to true.

## Docker Image

You can also pull the Docker image directly:

```bash
docker pull sanusiabubakr343/simple-chat-api
```

## Thanks


