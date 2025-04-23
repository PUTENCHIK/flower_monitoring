import uvicorn


if __name__ == "__main__":
    uvicorn.run(app="src.app:app",
                host="0.0.0.0",
                port=5050,
                reload=True)