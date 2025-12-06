# story-backend

This is the backend for the Story application, built with Node.js, Express, and MongoDB.

## Features

- User authentication (signup, login, logout)
- Story creation, reading, updating, and deletion
- User profile management
- Secure password hashing with bcrypt
- JWT-based authentication
- MongoDB for data storage

## Prerequisites

- Node.js (v14 or later)
- MongoDB (local or cloud instance)
- npm or yarn

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/story-backend.git
   cd story-backend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file in the root directory and add your environment variables:
   ```env
   PORT=5000
   MONGODB_URI=your_mongodb_connection_string
   JWT_SECRET=your_jwt_secret_key
   ```

4. Start the server:
   ```bash
   npm start
   ```

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register a new user
- `POST /api/auth/login` - Login
