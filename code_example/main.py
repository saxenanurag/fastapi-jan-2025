from typing import List
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Session, select
from contextlib import asynccontextmanager

from database import create_db_and_tables, get_session
from models import Ingredient, IngredientCreate, IngredientRead, IngredientUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/ingredients/", response_model=IngredientRead)
def create_ingredient(
    ingredient: IngredientCreate, session: Session = Depends(get_session)
):
    db_ingredient = Ingredient.model_validate(ingredient)
    session.add(db_ingredient)
    session.commit()
    session.refresh(db_ingredient)
    return db_ingredient


@app.get("/ingredients/", response_model=List[IngredientRead])
def read_ingredients(
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    session: Session = Depends(get_session),
):
    ingredients = session.exec(select(Ingredient).offset(offset).limit(limit)).all()
    return ingredients


@app.get("/ingredients/{ingredient_id}", response_model=IngredientRead)
def read_ingredient(ingredient_id: int, session: Session = Depends(get_session)):
    ingredient = session.get(Ingredient, ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient


@app.patch("/ingredients/{ingredient_id}", response_model=IngredientRead)
def update_ingredient(
    ingredient_id: int,
    ingredient: IngredientUpdate,
    session: Session = Depends(get_session),
):
    db_ingredient = session.get(Ingredient, ingredient_id)
    if not db_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    
    ingredient_data = ingredient.model_dump(exclude_unset=True)
    for key, value in ingredient_data.items():
        setattr(db_ingredient, key, value)
        
    session.add(db_ingredient)
    session.commit()
    session.refresh(db_ingredient)
    return db_ingredient


@app.delete("/ingredients/{ingredient_id}")
def delete_ingredient(ingredient_id: int, session: Session = Depends(get_session)):
    ingredient = session.get(Ingredient, ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    session.delete(ingredient)
    session.commit()
    return {"ok": True}