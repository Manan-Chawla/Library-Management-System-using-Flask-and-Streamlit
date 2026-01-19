from fastapi import FastAPI,Depends
from sqlmodel import Session,select
from db import get_session,create_db_and_tables,engine
from models import Book

app=FastAPI(title="Library API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()  

@app.post("/books/",response_model=Book)
def create_book(book:Book,session:Session=Depends(get_session)):
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@app.get("/books/",response_model=list[Book])
def read_books(session:Session=Depends(get_session)):
    books=session.exec(select(Book)).all()
    return books 
