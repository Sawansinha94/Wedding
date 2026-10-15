"""Run on owner's machine. Prints private bearer invitation codes; never commit or share list."""
import argparse,os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(__file__).resolve().parent/'.env')
from backend.private_invites import profiles,issue
p=argparse.ArgumentParser();p.add_argument('--profile-id',required=True);p.add_argument('--days',type=int,default=45);a=p.parse_args()
if not 1<=a.days<=365:p.error('days must be 1..365')
record=next((x for x in profiles() if x['id']==a.profile_id),None)
if not record:p.error('unknown profile id')
print('Name:',record['name']);print('Invitation code:',issue(record['id'],a.days))
