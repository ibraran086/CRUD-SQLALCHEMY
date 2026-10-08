from sqlalchemy import create_engine,Column,String,INTEGER
from sqlalchemy.orm import Session,sessionmaker,declarative_base
from fastapi import FastAPI,Depends,HTTPException
app=FastAPI()
#DATABASE_URL
DATABASE_URL="sqlite:///./test.db"
#create_engine(DB connection)
engine=create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}
)
#Session(DB operation ka liya)
sessionLocal=sessionmaker(bind=engine)
#Base(model ka liya)
Base=declarative_base()
#Table(Model)
class Todo(Base):
    __tablename__="todos"
    id=Column(INTEGER,primary_key=True,index=True)
    title=Column(String)
    completed=Column(String)
#Table create
Base.metadata.create_all(bind=engine)
#Dependency(DB Session provide karegy)
def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()
#CREATE API
@app.post("/todos")
def create_todo(title:str,db:Session=Depends(get_db)):
    todo=Todo(title=title,completed="False")
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return {
        "message":"todo created",
        "data":todo
    }
#Read all data
@app.get("/todos")
def get_todos(db:Session=Depends(get_db)):
    todos=db.query(Todo).all()
    return {
        "Total":len(todos),
        "data":todos
    }
#check on id
@app.get("/todos/{todo_id}")
def get_todo(todo_id=int,db:Session=Depends(get_db)):
    todo=db.query(Todo).filter(Todo.id==todo_id).first()
    if not todo:
        raise HTTPException(status_code=404,detail="Todo not found")
    return todo
