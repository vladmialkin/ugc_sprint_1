from fastapi import FastAPI

app = FastAPI(
    docs_url="/api/ugc/docs",
    openapi_url="/api/ugc/openapi.json",
)

@app.get("/api/ugc/v1/index")
def read_root():
    return {"Hello": "World"}
