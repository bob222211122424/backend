from fastapi import FastAPI, UploadFile, File
from google import genai
import os

app = FastAPI()
api_key = os.getenv("API_key")
client = genai.Client(api_key="API_key")
current_receipt_text = None

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
    try:
        file_bytes = await file.read()

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                "This is a bill/receipt image. Extract all necessary and useful information that could be needed to answer any question the user has.",
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

    if current_receipt_text is None:
        return {
            "error": "You have not uploaded an image yet or I have not received it."
        }

    prompt = f"""
Receipt information:

{current_receipt_text}

Question about receipt:

{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return {
        "answer": response.text
    }
