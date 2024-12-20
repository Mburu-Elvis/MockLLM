---
title: MockLLM
app_file: json_chatbot.py
sdk: gradio
sdk_version: 4.31.0
---
# MockLLM
Project Overview

This project implements a Retrieval-Augmented Generation (RAG) system using OpenAI's fine-tuned model to provide medical patients with accurate and context-aware responses. The system leverages patient data and hospital information to answer inquiries about health status, hospital locations, and other relevant details. Additionally, APIs are created to facilitate querying the model, trigger fine-tuning, and manage contextual memory.

## Features

    ## Fine-Tuned OpenAI Model

        The model is fine-tuned using anonymized medical patient data and hospital details.

        Context-aware interactions allow the system to remember and build upon prior conversations.

    ## Patient Inquiry Handling

        Patients can ask about their health status, treatment plans, and other personal medical details.

        Provides hospital-related information such as location, services, and operational details.

    ## APIs for Enhanced Functionality

        - Query API: Allows users to interact with the model by asking questions.

        - Training API: Triggers the fine-tuning process with updated data.

        - Context Memory API: Ensures the model retains and manages conversational context.

        - Data Retrieval System:  Integrates with a retrieval mechanism to fetch up-to-date information on hospitals and patient data as needed.

## System Architecture

The project consists of the following components:

    ### 1. Fine-Tuned Model

        Developed using OpenAI's GPT framework.

        Trained with specialized datasets containing patient and hospital information.

    ### 2. Backend

        Built with Flask to handle API requests and integrate the model with the data retrieval system.

        Implements authentication and authorization mechanisms to secure sensitive patient data.

    ### 3. Data Storage

        MySQL Database for storing patient records and hospital information.

        Chroma Vector database for document embeddings to enhance retrieval efficiency.

    ## 4. Frontend

        used Gradio for a quick access to the chatbot for testing purposes but the chatbot was deployed to a mobile application that's part of a closed source project for now
        
## APIs
  
  ### 1. Appointment Reminders
  
  **Endpoint**: `/appoitmentReminders`
  
  **Method**: `GET`
  
  **Description**: Retrieves reminders for upcoming appointments.
  
  ### 2. Patient Insurance Details
  
  **Endpoint**: `/patients/insuarance/<int:id>`
  
  **Method**: `GET`
  
  **Description**: Fetches insurance details for a patient by ID.
  
  ### 3. Patient Information
  
  **Endpoint**: `/patients/<string:number>`
  
  **Method**: `GET`
  
  **Description**: Retrieves patient details by their contact number.
  
  ### 4. Medications
  
  **Endpoint**: `/medications/<int:id>`
  
  **Method**: `GET`
  
  **Description**: Fetches medication details for a patient by ID.
  
  ### 5. Medical History
  
  **Endpoint**: `/medicalHistory/<int:id>`
  
  **Method**: `GET`
  
  **Description**: Retrieves a patient’s medical history by ID.
  
  ### 6. Appointment Details
  
  **Endpoint**: `/appointments/<int:id>`
  
  **Method**: `GET`
  
  **Description**: Retrieves details of a specific appointment by ID.
  
  ### 7. All Appointments
  
  **Endpoint**: `/appointments`
  
  **Method**: `GET`
  
  **Description**: Fetches a list of all appointments.
  
  ### 8. Query LLM
  
  **Endpoint**: `/llm`
  
  **Method**: `POST`
  
  **Request Body**:
  ```json  
  {
    "query": "string",
    "userId": "string"
  }
  ```
  **Response**:
```json  
  {
    "response": "string",
    "context": "string"
  }
  ```
  
  ### 9. Train Model
  
  **Endpoint**: `/trainModel/<string:phoneNumber>`
  
  **Method**: `POST`
  
  **Description**: Triggers training of the model using the data associated with the specified phone number.
    
## Getting Started

    ### Prerequisites

    Python 3.9+

    Flask framework

    OpenAI Python library

    Vector database (e.g., Pinecone, Weaviate)

    Database (e.g., PostgreSQL, MongoDB)

### Installation

    Clone the repository:
    git clone https://github.com/your-repo/rag-project.git
    cd rag-project

    Install dependencies:
    pip install -r requirements.txt

    Configure environment variables:

        OpenAI API key

        Database connection strings

        Other necessary credentials

### Running the Application

    Start the backend server:
    flask run

    Access the application via http://localhost:5000.



### Future Enhancements

    Adding multilingual support for global accessibility.

    Integrating advanced context-handling techniques like memory modules.

    Implementing real-time data updates from hospital systems.


