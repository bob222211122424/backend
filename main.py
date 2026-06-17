from fastapi import FastAPI, UploadFile, File
from google import genai
from google.genai import types
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
client = genai.Client(api_key=os.getenv("API_key"))

current_receipt_text = None
conversation_history = []

origins = [
    "https://frontend-exyb.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/chat")
def chat(prompt: str):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return {"answer": response.text}

    except Exception as x:
        return {"error": str(x)}


@app.post("/analyze_bill")
async def analyze_bill(file: UploadFile = File(...)):
    global current_receipt_text
    global conversation_history

    conversation_history = []

    try:
        file_bytes = await file.read()

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                "This is a bill/receipt image. Extract all necessary and useful information that could be needed to answer any question the user has as well as errors, next steps, and other information the user could use. Roughly 200 words",
                types.Part.from_bytes(
                    data=file_bytes,
                    mime_type=file.content_type,
                ),
            ],
        )

        current_receipt_text = response.text

        return {"answer": response.text}

    except Exception as e:
        return {"error": str(e)}


@app.get("/ask")
def ask(question: str):
    global current_receipt_text
    global conversation_history

    if current_receipt_text is None:
        return {
            "error": "You have not uploaded an image yet or I have not received it."
        }

    history_text = ""

    for message in conversation_history:
        history_text += f"{message['role']}: {message['text']}\n"

    prompt = f"""
Receipt information:

{current_receipt_text}

Conversation History:

{history_text}

Question about receipt:

{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    conversation_history.append({
        "role": "user",
        "text": question
    })

    conversation_history.append({
        "role": "assistant",
        "text": response.text
    })

    return {
        "answer": response.text
    }
