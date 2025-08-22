from fastapi import Request, HTTPException

def get_producer(request: Request):
    producer = getattr(request.app.state, "producer", None)
    if producer is None:
        raise HTTPException(status_code=503, detail='Producer has not started...')
    return producer
