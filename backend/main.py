# uvicorn main:app --reload

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openapi


#Custom Functions
from functions.database import store_messages, reset_message
from functions.openai_requests import audio_to_text, get_response
from functions.text_to_speech import text_to_speech

app = FastAPI()

# ACCEPTED DOMAINS
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:4174",
    "http://localhost:3000",
]



# Middleware to control access HTTP Requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#reset
@app.get("/reset")
async def reset():
    reset_message()
    return {"message": "Conversation reset"}


class AudioHandler:
    @staticmethod
    def handle_file_upload(file: UploadFile):
        with open(file.filename, "wb") as buffer:
            buffer.write(file.file.read())
        audio_input = open(file.filename, "rb")
        return audio_input

    @staticmethod
    def decode_audio(audio_input):
        # Perform audio decoding to text
        message_decoded = audio_to_text(audio_input)
        return message_decoded

    @staticmethod
    def get_chat_response(message_decoded):
        # Get chat response based on the decoded message
        chat_response = get_response(message_decoded)
        return chat_response

    @staticmethod
    def store_messages(message_decoded, chat_response):
        # Store the message and chat response
        store_messages(message_decoded, chat_response)

    @staticmethod
    def convert_to_audio(chat_response):
        # Convert chat response to audio
        audio_output = text_to_speech(chat_response)
        return audio_output


async def post_audio(file: UploadFile = File(...)):
    audio_input = AudioHandler.handle_file_upload(file)

    message_decoded = AudioHandler.decode_audio(audio_input)

    if not message_decoded:
        raise HTTPException(status_code=400, detail="Failed to decode audio")

    chat_response = AudioHandler.get_chat_response(message_decoded)

    if not chat_response:
        raise HTTPException(status_code=400, detail="Failed to get chat response")

    AudioHandler.store_messages(message_decoded, chat_response)

    audio_output = AudioHandler.convert_to_audio(chat_response)

    if not audio_output:
        raise HTTPException(status_code=400, detail="Failed to get audio response")

    def iterfile():
        yield audio_output

    return StreamingResponse(iterfile(), media_type="application/octet-stream")


@app.post("/post-audio")
async def handle_post_audio(file: UploadFile = File(...)):
    return await post_audio(file)

@app.post("/get-message-decoded")
async def get_message_decoded(file: UploadFile = File(...)):
    audio_input = AudioHandler.handle_file_upload(file)

    message_decoded = AudioHandler.decode_audio(audio_input)

    if not message_decoded:
        raise HTTPException(status_code=400, detail="Failed to decode audio")

    return {"message_decoded": message_decoded}


@app.post("/get-chat-response")
async def get_chat_response(file: UploadFile = File(...)):
    audio_input = AudioHandler.handle_file_upload(file)

    message_decoded = AudioHandler.decode_audio(audio_input)

    if not message_decoded:
        raise HTTPException(status_code=400, detail="Failed to decode audio")

    chat_response = AudioHandler.get_chat_response(message_decoded)

    if not chat_response:
        raise HTTPException(status_code=400, detail="Failed to get chat response")

    return {"chat_response": chat_response}