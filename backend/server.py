import uvicorn

def start():
    uvicorn.run("backend.app.app:app", host="localhost", port=80, reload=True)

if __name__ == "__main__":
    start()