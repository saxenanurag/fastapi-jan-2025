from typing import List
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Session, select
from contextlib import asynccontextmanager

from database import create_db_and_tables, get_session
from models import Ingredient, IngredientCreate, IngredientRead, IngredientUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI app.
    Code before the yield runs on startup (creating tables).
    Code after the yield runs on shutdown.
    """
    create_db_and_tables()
    yield


# Initialize the FastAPI app with the lifespan context manager
app = FastAPI(lifespan=lifespan)


@app.post("/ingredients/", response_model=IngredientRead)
def create_ingredient(
    ingredient: IngredientCreate, session: Session = Depends(get_session)
):
    """
    Create a new ingredient.
    
    - **ingredient**: The data for the new ingredient (validated by IngredientCreate model).
    - **session**: Database session dependency.
    """
    # Convert the Pydantic model (IngredientCreate) to a database model (Ingredient)
    db_ingredient = Ingredient.model_validate(ingredient)
    session.add(db_ingredient)
    session.commit()
    session.refresh(db_ingredient) # Refresh to get the generated ID
    return db_ingredient


@app.get("/ingredients/", response_model=List[IngredientRead])
def read_ingredients(
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    session: Session = Depends(get_session),
):
    """
    Read a list of ingredients with pagination.
    
    - **offset**: Number of items to skip.
    - **limit**: Maximum number of items to return (max 100).
    """
    # Select all ingredients with offset and limit
    ingredients = session.exec(select(Ingredient).offset(offset).limit(limit)).all()
    return ingredients


@app.get("/ingredients/{ingredient_id}", response_model=IngredientRead)
def read_ingredient(ingredient_id: int, session: Session = Depends(get_session)):
    """
    Read a single ingredient by ID.
    """
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
    """
    Update an ingredient. Only provided fields will be updated.
    """
    db_ingredient = session.get(Ingredient, ingredient_id)
    if not db_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    
    # exclude_unset=True only includes fields that were actually sent in the request
    ingredient_data = ingredient.model_dump(exclude_unset=True)
    for key, value in ingredient_data.items():
        setattr(db_ingredient, key, value)
        
    session.add(db_ingredient)
    session.commit()
    session.refresh(db_ingredient)
    return db_ingredient


@app.delete("/ingredients/{ingredient_id}")
def delete_ingredient(ingredient_id: int, session: Session = Depends(get_session)):
    """
    Delete an ingredient by ID.
    """
    ingredient = session.get(Ingredient, ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    session.delete(ingredient)
    session.commit()
    return {"ok": True}