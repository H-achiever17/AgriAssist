# AgriAssist: AI-Powered Agricultural Assistant

AgriAssist is a comprehensive platform designed to provide farmers with timely and relevant information through an intuitive web interface and a widely accessible SMS service. This project leverages AI to parse queries and deliver data on market prices, weather, soil conditions, and more.

## Project Structure

The project is a monorepo containing three core, independent services:

* **[Backend](./Backend/)**: A Python-based server built with Uvicorn. It features an AI agent that uses a suite of specialized tools to process farmer queries and retrieve information from various sources.
* **[Frontend](./Frontend/)**: A modern, responsive web application built with JavaScript and styled with Tailwind CSS. It provides a rich user interface for interacting with the backend services.
* **[SMS](./SMS/)**: An SMS-based interaction layer powered by the Capcom6 SMS Gateway on an Android device, a Python webhook server, and Ngrok for tunneling. This ensures the service is accessible even with limited internet connectivity.

## Getting Started

Each service has its own dependencies and setup instructions. To get the entire platform running locally, you must set up each component individually.

Please refer to the detailed guides within each directory:

1.  **Backend Setup**: See the **[Backend README](./Backend/README.md)**
2.  **Frontend Setup**: See the **[Frontend README](./Frontend/README.md)**
3.  **SMS Service Setup**: See the **[SMS README](./SMS/README.md)**

## Core Technologies

This project integrates a variety of technologies to deliver its features:

* **Backend**: Python, Uvicorn, Quart
* **Frontend**: JavaScript, HTML, CSS, Tailwind CSS
* **SMS**: Capcom6 Android Gateway, Ngrok, Python
* **DevOps**: Git, Environment Variables (`.env`)
