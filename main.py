from fastapi import FastAPI
from controllers.ReceiptController import router as receipt_router
import uvicorn
app = FastAPI()
app.include_router(receipt_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
