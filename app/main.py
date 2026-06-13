from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message":"Cloud File Processing Pipeline API is running"}

@app.get("/health")
def get_health():
    return {"status":"ok"}