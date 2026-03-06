import uvicorn
import os
from fastapi import FastAPI, Query
from api.routes.clip import handle_clip_request
from dotenv import load_dotenv

load_dotenv() 

app = FastAPI()
#

@app.get("/api/clip")
async def create_clip(
    user: str = Query(..., description="The user creating the clip"),
    msg: str = Query(..., description="The title of the clip and offset"),
    channelid: str = Query(..., description="The YouTube Channel ID"),
    secret: str = Query(..., description="The secret password to protect the API")
):
    if secret != os.getenv("API_SECRET"):
        return {"message": "Error: Unauthorized API Access."}

    result = handle_clip_request(user, msg, channelid)
    return result

if __name__ == "__main__":
    print("🚀 Starting the Tsnip-Pro Server...")
    uvicorn.run("api.index:app", host="127.0.0.1", port=8000, reload=True)