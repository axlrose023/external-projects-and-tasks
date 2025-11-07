import uvicorn
from fastapi import FastAPI
import router

app = FastAPI(title="Cocktail RAG System", version="1.0.0")
app.include_router(router.api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
