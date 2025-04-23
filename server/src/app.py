from fastapi import FastAPI


app = FastAPI()


@app.post("/test")
async def test(data: str):
    return {'Server received': data}
