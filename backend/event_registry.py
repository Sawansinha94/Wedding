# Synchronize the four published ceremonies with the existing wedding_events table.
from .database import wishes_db
EVENTS=(
 ('lagan','Lagan Ceremony','2026-11-20 16:00:00+05:30',None,None,'Saffron & Traditional Ethnic'),
 ('haldi','Haldi Ceremony','2026-11-22 18:00:00+05:30',None,None,'Golden Yellow Festive Attire'),
 ('wedding','Wedding Ceremony','2026-11-24 19:00:00+05:30','Swastik Foundation','Ranchi Ring Road, Ranchi, Jharkhand','Royal Festive Attire'),
 ('reception','Reception & Blessings','2026-11-27 19:00:00+05:30','Our Residence','Baghmara, Talcher, Odisha','Festive Elegance'),
)
def sync_events():
    with wishes_db() as (db,_):
        for key,name,start,venue,address,dress in EVENTS:
            db.execute('''INSERT INTO wedding_events(event_key,event_name,starts_at,venue_name,venue_address,dress_code)
              VALUES (%s,%s,%s::timestamptz,%s,%s,%s)
              ON CONFLICT (event_key) DO UPDATE SET event_name=EXCLUDED.event_name,
                starts_at=EXCLUDED.starts_at,ends_at=NULL,venue_name=EXCLUDED.venue_name,
                venue_address=EXCLUDED.venue_address,dress_code=EXCLUDED.dress_code,updated_at=now()''',
                (key,name,start,venue,address,dress))
        db.commit()
