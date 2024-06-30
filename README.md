# Backend for Chatbot and Inventory Management
This repository houses the backend for a versatile system that manages both chatbot interactions and inventory operations. Built with scalability and efficiency in mind, this backend ensures seamless communication and robust inventory management.

# Features
- **Chatbot Endpoints:** Efficiently handles user queries, providing instant and accurate responses.
- **Inventory Endpoints:** Manages inventory data, ensuring up-to-date stock levels, and supporting CRUD operations.
- **Scalable Architecture:** Designed to handle high traffic and large datasets.
- **RESTful API:** Adheres to REST principles, facilitating easy integration with various frontend applications.
- **Secure and Reliable:** Implements authentication and authorization to protect data integrity and user privacy.

# Technologies Used
- **FastAPI:** For creating the API endpoints with high performance.
- **Python:** The core language for backend logic and data processing.
- **OpenAIAPI:** For Chatbot.

# Getting Started
**1. Clone the repository:**
    git clone https://github.com/your-username/repo-name.git
**2. Navigate to the project directory:**
    cd repo-name
**3. Install dependencies:**
    pip install -r requirements.txt
**4. Run the application:**
    uvicorn main:app --reload --host 127.0.0.1 --port 8000 --env-file dev.env
