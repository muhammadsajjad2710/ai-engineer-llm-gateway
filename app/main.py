from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel

PROVIDERS = {"local": 0.0, "small": 0.002, "large": 0.02}

class RouteIn(BaseModel):
    prefer: str = "local"
    max_cost: float = 0.01

def pick(prefer: str, max_cost: float) -> dict:
    if prefer in PROVIDERS and PROVIDERS[prefer] <= max_cost:
        return {"provider": prefer, "cost": PROVIDERS[prefer]}
    options = [n for n, c in PROVIDERS.items() if c <= max_cost]
    if not options:
        return {"error": "no_provider"}
    name = min(options, key=lambda n: PROVIDERS[n])
    return {"provider": name, "cost": PROVIDERS[name]}

def create_app() -> FastAPI:
    app = FastAPI(title="LLM gateway")
    @app.post("/route")
    def route(payload: RouteIn):
        return pick(payload.prefer, payload.max_cost)
    return app

app = create_app()
