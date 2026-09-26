from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from app.agent import car_agent
from langchain_core.messages import AIMessage, HumanMessage

app = FastAPI(title="AutoExpert RAG & Web API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Initializing the car agent...")
agent = car_agent()
print("Car agent initialized successfully.")

class History(BaseModel):
    role: str
    content: str

class ChatPayload(BaseModel):
    message: str
    history: Optional[List[History]] = []

class ChatResponse(BaseModel):
    response: str
    tools_used: List[str]

@app.post("/api/chat")
async def chat_endpoint(payload: ChatPayload, max_tokens: Optional[int] = 150):
    """
    Endpoint to handle chat messages.
    Expects a list of messages in the format:
    [
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi there!"}
    ]
    """
    try:
        # Convert incoming messages to the appropriate format
        formatted_messages = []
        for msg in payload.history[-6:]:
            if msg.role == "user":
                formatted_messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                formatted_messages.append(AIMessage(content=msg.content))
            else:
                raise ValueError(f"Invalid role: {msg.role}")

        response = agent.invoke({
            "messages": [*formatted_messages, HumanMessage(content=payload.message)]
        })

        messages = response.get("messages", [])
        tools_used = [
            tool_call["name"]
            for message in messages
            for tool_call in getattr(message, "tool_calls", [])
            if tool_call.get("name")
        ]
        assistant_message = next(
            (message for message in reversed(messages) if isinstance(message, AIMessage)),
            None,
        )

        return ChatResponse(
            response=assistant_message.content if assistant_message else "",
            tools_used=list(dict.fromkeys(tools_used)),
        )

    except Exception as e:
        print(f"Error in chat_endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
def health_check():
    """
    Health check endpoint to verify that the API is running.
    """
    return {"status": "healthy"}