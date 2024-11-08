from fastapi import FastAPI, HTTPException, Header
from lightning_sdk import Studio

app = FastAPI()

@app.post("/studios")
def start_studio(
    name: str,
    teamspace: str,
    user: str,
    lightning_user_id: str = Header(..., env="LIGHTNING_USER_ID"),
    lightning_api_key: str = Header(..., env="LIGHTNING_API_KEY")
):
    """
    Start a new Lightning studio.
    
    Parameters:
    name (str): The name of the studio.
    teamspace (str): The teamspace to create the studio in.
    user (str): The user to create the studio for.
    lightning_user_id (str): The Lightning user ID (from header).
    lightning_api_key (str): The Lightning API key (from header).
    
    Returns:
    dict: The studio object, including the assigned URL.
    """
    try:
        studio = Studio(name, teamspace=teamspace, user=user)
        studio.start()
        return studio.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/studios/{studio_id}")
def stop_studio(
    studio_id: str,
    lightning_user_id: str = Header(..., env="LIGHTNING_USER_ID"),
    lightning_api_key: str = Header(..., env="LIGHTNING_API_KEY")
):
    """
    Stop a Lightning studio.
    
    Parameters:
    studio_id (str): The ID of the studio to stop.
    lightning_user_id (str): The Lightning user ID (from header).
    lightning_api_key (str): The Lightning API key (from header).
    """
    try:
        studio = Studio.from_id(studio_id, user=lightning_user_id, api_key=lightning_api_key)
        studio.stop()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8008)