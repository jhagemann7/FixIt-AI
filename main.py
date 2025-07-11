from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import openai
import base64
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/diagnose")
async def diagnose(
    symptom_description: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        image_bytes = await file.read()
        img_base64 = base64.b64encode(image_bytes).decode("utf-8")

        system_prompt = (
            "You are a home repair mentor and expert technician. "
            "I will send you an image of a home appliance or HVAC unit and describe the symptoms. "
            "Based on what you see and what I describe, diagnose the issue, possible causes, "
            "estimated repair costs, and whether to DIY or call a pro."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Symptom Description: {symptom_description}\nImage (base64): {img_base64}"}
        ]

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        answer = response.choices[0].message.content
        return {"diagnosis": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to the FixIt AI backend!"}
