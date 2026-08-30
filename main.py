from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from models import get_db

app = FastAPI(title="中文自学系统")
import os
if not os.path.exists("./static"):
    os.mkdir("./static")
app.mount("/static", StaticFiles(directory="./static"), name="static")

@app.get("/")
async def index():
    return FileResponse("./static/index.html")

# Pydantic Schema
class UserSchema(BaseModel):
    username: str
    password: str

class VocabSchema(BaseModel):
    word: str
    pinyin: str
    meaning: str
    example: str

class RecordSchema(BaseModel):
    user_id:int
    vocab_id:int
    status:str

# User CRUD
@app.post("/api/users")
def create_user(item:UserSchema, db:Session=Depends(get_db)):
    db_user = models.User(username=item.username,password=item.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/api/users/{uid}")
def get_user(uid:int, db:Session=Depends(get_db)):
    u = db.query(models.User).filter(models.User.id==uid).first()
    if not u: raise HTTPException(status_code=404,detail="not found")
    return u

@app.put("/api/users/{uid}")
def update_user(uid:int, item:UserSchema, db:Session=Depends(get_db)):
    u = db.query(models.User).filter(models.User.id==uid).first()
    if not u: raise HTTPException(status_code=404,detail="not found")
    u.username=item.username
    u.password=item.password
    db.commit()
    return u

@app.delete("/api/users/{uid}")
def del_user(uid:int, db:Session=Depends(get_db)):
    u = db.query(models.User).filter(models.User.id==uid).first()
    if not u: raise HTTPException(status_code=404,detail="not found")
    db.delete(u)
    db.commit()
    return {"msg":"deleted"}

# Vocabulary CRUD
@app.post("/api/vocab")
def create_vocab(item:VocabSchema, db:Session=Depends(get_db)):
    v = models.Vocabulary(word=item.word,pinyin=item.pinyin,meaning=item.meaning,example=item.example)
    db.add(v)
    db.commit()
    db.refresh(v)
    return v

@app.get("/api/vocab/{vid}")
def get_vocab(vid:int, db:Session=Depends(get_db)):
    v = db.query(models.Vocabulary).filter(models.Vocabulary.id==vid).first()
    if not v: raise HTTPException(status_code=404,detail="not found")
    return v

@app.put("/api/vocab/{vid}")
def update_vocab(vid:int, item:VocabSchema, db:Session=Depends(get_db)):
    v = db.query(models.Vocabulary).filter(models.Vocabulary.id==vid).first()
    if not v: raise HTTPException(status_code=404,detail="not found")
    v.word=item.word
    v.pinyin=item.pinyin
    v.meaning=item.meaning
    v.example=item.example
    db.commit()
    return v

@app.delete("/api/vocab/{vid}")
def del_vocab(vid:int, db:Session=Depends(get_db)):
    v = db.query(models.Vocabulary).filter(models.Vocabulary.id==vid).first()
    if not v: raise HTTPException(status_code=404,detail="not found")
    db.delete(v)
    db.commit()
    return {"msg":"deleted"}

# LearnRecord CRUD
@app.post("/api/record")
def create_record(item:RecordSchema, db:Session=Depends(get_db)):
    r = models.LearnRecord(user_id=item.user_id,vocab_id=item.vocab_id,status=item.status)
    db.add(r)
    db.commit()
    db.refresh(r)
    return r

@app.get("/api/record/{rid}")
def get_record(rid:int, db:Session=Depends(get_db)):
    r = db.query(models.LearnRecord).filter(models.LearnRecord.id==rid).first()
    if not r: raise HTTPException(status_code=404,detail="not found")
    return r

@app.put("/api/record/{rid}")
def update_record(rid:int, item:RecordSchema, db:Session=Depends(get_db)):
    r = db.query(models.LearnRecord).filter(models.LearnRecord.id==rid).first()
    if not r: raise HTTPException(status_code=404,detail="not found")
    r.user_id=item.user_id
    r.vocab_id=item.vocab_id
    r.status=item.status
    db.commit()
    return r

@app.delete("/api/record/{rid}")
def del_record(rid:int, db:Session=Depends(get_db)):
    r = db.query(models.LearnRecord).filter(models.LearnRecord.id==rid).first()
    if not r: raise HTTPException(status_code=404,detail="not found")
    db.delete(r)
    db.commit()
    return {"msg":"deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)