import uvicorn

if __name__ == '__main__':
    uvicorn.run("Quera.asgi:application", reload=True)