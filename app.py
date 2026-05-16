from flask import Flask, Response, request, jsonify
from pymongo import MongoClient
import certifi
from openai import OpenAI
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

app = Flask(__name__)

client = MongoClient(
    os.getenv("MONGO_URL"),
    tlsCAFile=certifi.where()
)

db = client["ai_project"]

prompts_collection = db["prompts"]
history_collection = db["history"]

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


@app.route("/ask", methods=["POST"])
def ask_question():

    data = request.get_json()

    user_input = data.get("userInput")

    if not user_input:
        return jsonify({
            "error": "Please provide userInput and Must be array"
        }), 400

    prompt_data = prompts_collection.find_one({
        "_id": "Education_Prompt"
    })
    if not prompt_data or "template" not in prompt_data:
        return jsonify({
            "error": "Prompt not found or missing template in MongoDB"
        }), 404

    template = prompt_data["template"]

    final_prompt = template.replace(
        "{{userInput}}",
        user_input
    )

# Fake Api Response (for testing without hitting OpenAI API)
    ai_response = f"This is a fake response for testing purposes. Replace this with actual OpenAI API call in production.{user_input}"




    # Real OpenAI API call for now we are not using it .
#   response = openai_client.chat.completions.create(
#      model="gpt-4.1-mini",
#      messages=[
#           {
#              "role": "user",
#             "content": final_prompt
#        }
#   ]
#)
#   ai_response = response.choices[0].message.content



    history_collection.insert_one({
        "question": user_input,
        "response": ai_response
    })

    return jsonify({
        "response": ai_response
    })


async def generate_ai_response(question, template):

    final_prompt = template.replace(
        "{{userInput}}",
        question
    )



    # real OpenAI API call
#    response = openai_client.chat.completions.create(
#        model="gpt-4.1-mini",
#        messages=[
#            {
#                "role": "user",
#                "content": final_prompt
#            }
#        ]
#    )
#    ai_response = response.choices[0].message.content




# Fake Api Response (for testing purpose without hitting OpenAI API)
    ai_response = f"This is a fake response for testing purposes. Replace this with actual OpenAI API call in production.{question}"

    history_collection.insert_one({
        "question": question,
        "response": ai_response
    })
    return ai_response

@app.route("/bulk-ask", methods=["POST"])
def bulk_ask():

    data = request.get_json()
    questions = data.get("userInputs")

    if not questions:
        return jsonify({"error": "userInputs missing"}), 400

    if isinstance(questions, str):
        questions = [questions]

    if not isinstance(questions, list):
        return jsonify({"error": "userInputs must be string or list"}), 400

    prompt_data = prompts_collection.find_one({
        "_id": "Education_Prompt"
    })

    if not prompt_data:
        return jsonify({"error": "Prompt not found"}), 404

    template = prompt_data.get("template")

    responses = []

    for q in questions:
        ai_response = f"This is a fake response for testing purpose: {q}"

        history_collection.insert_one({
            "question": q,
            "response": ai_response
        })

        responses.append(ai_response)

    return jsonify({
        "responses": responses
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)