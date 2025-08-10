#!/usr/bin/env python3

import subprocess
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

_HOST = "0.0.0.0"
_PORT = 8099
_DEFAULT_SESSION_NAME = "my-session"
app = FastAPI(title="Voice Command Listener")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextCommand(BaseModel):
    text: str
    session_name: str = _DEFAULT_SESSION_NAME


@app.post("/listen")
async def listen(command: TextCommand):
    try:
        # Send the text command to the specified tmux session
        subprocess.run(
            [
                "tmux",
                "send-keys",
                "-t",
                command.session_name,
                command.text,
            ],
            check=True,
        )

        return {"status": "success", "message": f"Sent command: {command.text}"}

    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to send command to tmux: {e}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@app.get("/")
async def serve_ui():
    """Serve the voice command listener HTML interface"""
    html_file_path = os.path.join(os.path.dirname(__file__), "listener.html")
    if os.path.exists(html_file_path):
        return FileResponse(html_file_path, media_type="text/html")
    else:
        raise HTTPException(status_code=404, detail="UI file not found")


if __name__ == "__main__":
    uvicorn.run(app, host=_HOST, port=_PORT)
