from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
from fastapi import Request

app = FastAPI()

# CORS settings
origins = [
    "http://localhost",  # Your local development environment
    "http://localhost:3000",  # If you're running your frontend on a different port, e.g., React
    # Add other domains if needed
    "http://172.26.224.1",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    return {"message": "FastAPI server is running!"}



@app.post("/api/chat")
async def get_response(request: Request):
    try:
        data = await request.json()
        print("Received data:", data)
        # print(data['messages'][0]['content'])
        # 
        payload = {
    "model": "llama2:latest",
    "messages": [
        {
            "role": "system",
            "content": (
                "You're BNHS AI assistant. You are knowledgeable about BNHS (Bombay Natural "
                "History Society) and wildlife. Please respond to questions related to "
                "wildlife or BNHS"
            )
        },
        {
            "role": "user",
            "content": data['prompt']  # User's query
        },
    ],
    "stream": False
} 
        print("Sending Payload:", payload)

        # Sending request to external service
        response = requests.post("http://localhost:11434/api/chat", json=payload)

        result = response.json()['message']['content']

        if response.status_code == 200:
            return {"response": result}
        else:
            return {"error": f"Failed to get response. Status code: {response.status_code}"}

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
