"""One-time static localization using your OpenRouter API key; outputs bundled JS.
Run when editing website copy. Requires requests and python-dotenv.
"""
import os,re,json,html,sys,time
from pathlib import Path
from dotenv import load_dotenv
import asyncio
from backend.ai_fallback import generate
root=Path(__file__).resolve().parent
load_dotenv(root/'.env')

source=(root/'index.html').read_text()
from html.parser import HTMLParser
class Texts(HTMLParser):
 def __init__(self):super().__init__();self.texts=[];self.skip=0
 def handle_starttag(self,tag,attrs):
  if tag in ('script','style'):self.skip+=1
  for k,v in attrs:
   if k in ('placeholder','aria-label','title') and v and re.search('[A-Za-z]',v):self.texts.append(v.strip())
 def handle_endtag(self,tag):
  if tag in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,data):
  x=html.unescape(data.strip())
  if not self.skip and x and re.search('[A-Za-z]',x) and len(x)<901:self.texts.append(x)
parser=Texts();parser.feed(source)
texts=list(dict.fromkeys(parser.texts));outpath=root/'data'/'static-translations.json'
translations=json.loads(outpath.read_text()) if outpath.exists() else {}
model=os.getenv('OPENROUTER_MODEL','google/gemini-2.5-flash')
for lang,label in [('hi','Hindi'),('or','Odia'),('te','Telugu')]:
 missing=[t for t in texts if not translations.get(t,{}).get(lang)]
 for i in range(0,len(missing),12):
  batch=missing[i:i+12]
  response=asyncio.run(generate([{'role':'system','content':'Translate the following JSON array of wedding UI text into '+label+'. Return only a JSON array of strings in identical order. Preserve names, dates, numbers and punctuation. Return no markdown.'},{'role':'user','content':json.dumps(batch,ensure_ascii=False)}], temperature=0, max_tokens=1800)).strip()
  response=re.sub(r'^```(?:json)?\s*|\s*```$','',response)
  translated=json.loads(response)
  if not isinstance(translated,list) or len(translated)!=len(batch):raise ValueError('Bad translation response')
  for a,b in zip(batch,translated):translations.setdefault(a,{})[lang]=str(b)
  outpath.parent.mkdir(exist_ok=True);outpath.write_text(json.dumps(translations,ensure_ascii=False,indent=2))
  print(lang,i+len(batch),'/',len(missing))
(root/'assets/js/29-static-catalog.js').write_text('window.WEDDING_TRANSLATIONS_OFFLINE='+json.dumps(translations,ensure_ascii=False)+';\n')
print('Built',len(translations),'static translations. Review language quality before publishing.')
