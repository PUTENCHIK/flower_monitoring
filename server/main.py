import uvicorn
from src import Config

if __name__ == "__main__":
    uvicorn.run(app=Config.app.name,
                    host=Config.app.host,
                    port=Config.app.port,
                    reload=True)