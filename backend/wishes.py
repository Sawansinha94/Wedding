from fastapi import APIRouter,HTTPException
from .schemas import PublicWish
from pydantic import BaseModel, Field
from .database import DB_LOCK,wishes_db
router=APIRouter()
@router.get('/api/wishes')
def get_wishes():
    with DB_LOCK, wishes_db() as (db, ph):
        rows=db.execute('SELECT id,name,message,created_at FROM public_wedding_wishes ORDER BY id DESC LIMIT 40').fetchall()
    with DB_LOCK, wishes_db() as (db, ph):
        replies=db.execute('SELECT id,wish_id,name,message,created_at FROM wedding_wish_replies WHERE wish_id IN (SELECT id FROM public_wedding_wishes ORDER BY id DESC LIMIT 40) ORDER BY id ASC').fetchall()
    by_wish={}
    for r in replies:
        by_wish.setdefault(r[1],[]).append({'id':r[0],'name':r[2],'message':r[3],'created_at':r[4].isoformat() if hasattr(r[4],'isoformat') else str(r[4])})
    return {'wishes':[{'id':r[0],'name':r[1],'message':r[2],'created_at':r[3].isoformat() if hasattr(r[3],'isoformat') else str(r[3]),'replies':by_wish.get(r[0],[])} for r in rows]}

@router.post('/api/wishes',status_code=201)
def post_wish(payload: PublicWish):
    name=payload.name.strip();message=payload.message.strip()
    if not name or not message:raise HTTPException(422,'Name and message are required')
    with DB_LOCK, wishes_db() as (db, ph):
        db.execute(f'INSERT INTO public_wedding_wishes(name,message) VALUES({ph},{ph})',(name,message))
        # Mirror into the existing normalized wishes table, keeping its approval workflow.
        db.execute('''INSERT INTO wedding_wishes(author_name,wish_text,language_code,is_approved)
                      VALUES (%s,%s,%s,%s)''',(name,message,'en',False))
        db.commit()
        row=db.execute(f'SELECT id,name,message,created_at FROM public_wedding_wishes WHERE name={ph} AND message={ph} ORDER BY id DESC LIMIT 1',(name,message)).fetchone()
    return {'ok':True,'wish':{'id':row[0],'name':row[1],'message':row[2],'created_at':row[3].isoformat() if hasattr(row[3],'isoformat') else str(row[3])+'Z'}}



class WishReplyIn(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    message: str = Field(min_length=1, max_length=1000)

@router.post('/api/wishes/{wish_id}/replies', status_code=201)
def post_wish_reply(wish_id: int, payload: WishReplyIn):
    name=payload.name.strip(); message=payload.message.strip()
    if not name or not message: raise HTTPException(422,'Name and comment are required')
    with DB_LOCK, wishes_db() as (db, ph):
        exists=db.execute('SELECT id FROM public_wedding_wishes WHERE id=%s',(wish_id,)).fetchone()
        if not exists: raise HTTPException(404,'Wish not found')
        row=db.execute('INSERT INTO wedding_wish_replies(wish_id,name,message) VALUES (%s,%s,%s) RETURNING id,created_at',(wish_id,name,message)).fetchone()
        db.commit()
    return {'ok':True,'reply':{'id':row[0],'wish_id':wish_id,'name':name,'message':message,'created_at':row[1].isoformat()}}
