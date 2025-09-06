Based on the provided image of the project directory and your instructions, here is a README file for the `AgriAssist-Backend` repository.

### **AgriAssist-Backend**

This is the backend for the AgriAssist project, an AI-powered agricultural assistant. The backend is built using Python and leverages various tools to provide information to farmers.

### **Key Features**

  * **Intelligent Query Parsing:** Uses a `Query_Parser` and `Refined_Farmer_Query` to understand and process user queries.
  * **Specialized Tools:** Includes dedicated tools for specific tasks, such as:
      * `Mandi_Price_Tool.py`: Retrieves real-time mandi (market) prices.
      * `Soil_Tool.py`: Provides information related to soil data.
      * `Web_Crawler.py`: Gathers data from the web.
      * `weather_tool.py`: Fetches weather information.
  * **Media Processing:** The `process_media.py` utility handles media-related tasks.
  * **Agent-based Architecture:** An `Agent.py` orchestrates the flow and uses the various tools to generate relevant responses.

### **Technologies Used**

  * **Python:** The core programming language.
  * **`requirements.txt`:** Specifies all the necessary Python libraries.
  * **Uvicorn:** Used to run the application server.

### **Getting Started**

Follow these steps to set up and run the project locally.

#### **1. Clone the Repository**

First, clone the project to your local machine using git.

#### **2. Set Up Environment Variables**

Create a `.env` file in the root directory of the project to store your environment variables. You will need to get the required keys and values and add them to this file.

An example of a `.env` file structure might look like this:

```
# Example .env file
AWS_ACCESS_KEY="your_aws_access_key"
AWS_REGION="your_aws_region"
AWS_SECRET_KEY="your_aws_secret_key"
EE_SERVICE_KEY="your_ee_service_key"
FRONTEND_URL="your_frontend_url"
GEMINI_API_KEY="your_gemini_api_key"
GOV_API_KEY="your_gov_api_key"
KNOWLEDGE_BASE_ID="your_knowledge_base_id"
LOCATION_API_KEY="your_location_api_key"
```

#### **3. Install Dependencies**

Install all the required Python libraries using `pip`.

```bash
pip install -r requirements.txt
```

#### **4. Run the Application**

Start the backend server using Uvicorn. The `app.py` file contains the main application logic.

```bash
uvicorn app:app --reload
```

The application will now be running on your local machine, typically at `http://127.0.0.1:8000`.
