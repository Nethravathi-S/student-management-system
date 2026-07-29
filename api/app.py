from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Student Management System API", "status": "running"}

@app.get("/students")
def list_students():
    return {"students": []}

@app.get("/statistics")
def get_statistics():
    return {"message": "Statistics endpoint"}
