from dotenv import load_dotenv
load_dotenv()
import os,uuid
import psycopg
from psycopg.types.json import Jsonb
url=os.getenv('DATABASE_URL')
if not url:raise SystemExit('DATABASE_URL missing')
trace=str(uuid.uuid4())
with psycopg.connect(url,connect_timeout=10) as conn:
    with conn.cursor() as cur:
        cur.execute('SELECT current_database(),to_regclass(%s)',('public.wedding_system_logs',))
        print('Database and log table:',cur.fetchone())
        cur.execute("INSERT INTO public.wedding_system_logs (trace_id,level,event_type,service,operation,status,details) VALUES (%s,'INFO','diagnostic.write','debug_verify','insert','success',%s) RETURNING id",(trace,Jsonb({'message':'Application credential write test'})))
        row=cur.fetchone()
        print('Inserted log ID:',row[0])
        cur.execute('SELECT event_type,trace_id FROM public.wedding_system_logs WHERE id=%s',(row[0],))
        print('Read back:',cur.fetchone())
print('PASS: DB log read/write')
