from typing import Optional
from sqlmodel import Field, SQLModel


class IngredientBase(SQLModel):
    name: str = Field(index=True)
    category: str = Field(default="Condiment", index=True)
    quantity: int = Field(default=0)
    description: Optional[str] = None


class Ingredient(IngredientBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class IngredientCreate(IngredientBase):
    pass


class IngredientRead(IngredientBase):
    id: int


class IngredientUpdate(SQLModel):
    name: Optional[str] = None
    category: Optional[str] = None
    quantity: Optional[int] = None
    description: Optional[str] = None
