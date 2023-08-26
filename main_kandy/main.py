from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from kandy import KandyControlnet

app = FastAPI()

kandy_controlnet = KandyControlnet()


@app.get("/images")
async def func(request: Request):
    query = request.headers.get('query')
    negative = request.headers.get('negative')
    print(query, negative)
    
    image = kandy_controlnet.imagine(prompt=query, negative_prompt=negative)
    path = "images/tmp.jpg"
    image.save(path)
    return FileResponse(path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8730)