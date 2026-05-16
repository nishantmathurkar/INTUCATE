# INTUCATE
AI Prompt Processing System (Flask + MongoDB + OpenAI)

# Overview

This project is a backend AI system built using Flask, MongoDB, and OpenAI API.
It processes user questions, injects them into stored prompt templates, generates AI responses, and stores history for analytics.


# Tech Stack
Flask – Backend API
MongoDB – Database
OpenAI – AI response generation
Python AsyncIO – Parallel processing (bulk requests)

# Database Structure (MongoDB)
1. prompts collection

Stores AI prompt templates in database.
{
  "_id": "Education_Prompt",
  "template": "You are an expert in education domain. Answer the following: {{userInput}}"
}

2. history collection 

Stores all user interactions.
{
  "question": "User question here",
  "response": "AI response here"
}

#  API Endpoints

1. POST/ask

Request:

{
  "userInput": "How much should I score in CA final?"
}
Response:

{
  "response": "AI generated answer"
}

# Flow:
	1.Fetch prompt template from MongoDB
	2.Replace {{userInput}}
	3.Call OpenAI API
	4.Store Q&A in history collection
	5.Return response

2. POST /bulk-ask
{
  "response": "AI generated answer"
}

Response:
{
  "responses": [
    "Answer 1",
    "Answer 2"
  ]
}
# Flow:
    1.Fetch prompt template
	2.Process each question independently
	3.Run requests in parallel using asyncio
	4.Return ordered responses

# Run Project

1. Install Dependencies

pip install flask pymongo python-dotenv openai certifi

2. add .env file

MONGO_URL= -
OPENAI_API_KEY = -

3. Run Server

python3 app.py

Server runs on :
http://localhost:5000

# Postman

For Single Response 
post : http://127.0.0.1:5000/ask
body raw json
input:
{
  "userInput": "How much should I score in each subject to pass CA final?"
}

output:
{
    "response": "This is a fake response for testing purposes. Replace this with actual OpenAI API call in production.How much should I score in each subject to pass CA final?"
}


For Multiple and Bulk 
Post : http://127.0.0.1:5000/bulk-ask
body raw json
input:
{
  "userInputs": [
    "What is CA final passing marks?"
  ]
}
output:
{
    "responses": [
        "This is a fake response for testing purpose: What is CA final passing marks?"
    ]
}



