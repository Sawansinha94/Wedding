"""ONE-TIME localization catalog generator. Run with working OpenRouter/Bedrock credentials.
Never runs during website load. Persists translations in assets/js/29-static-catalog.js.
"""
import ast,asyncio,html,json,os,re,sys
from html.parser import HTMLParser
from pathlib import Path
from dotenv import load_dotenv
from backend.ai_fallback import generate
ROOT=Path(__file__).resolve().parent
load_dotenv(ROOT/'.env')
class Reader(HTMLParser):
 def __init__(self):super().__init__();self.items=[];self.skip=0
 def handle_starttag(self,tag,attrs):
  if tag in ('script','style'):self.skip+=1
  for k,v in attrs:
   if k in ('placeholder','aria-label','alt','title','data-q') and v:self.items.append(html.unescape(v.strip()))
 def handle_endtag(self,tag):
  if tag in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,data):
  if not self.skip:self.items.append(html.unescape(data.strip()))
r=Reader();r.feed((ROOT/'index.html').read_text(encoding='utf-8'))
# Extract probable UI strings from JavaScript literals, including dynamically generated status labels.
# Avoid translating code, URLs, selectors, keys, HTML templates, and large prompts.
js_re=re.compile(r"(?P<q>['\"])(?P<v>(?:\\.|(?!\1).)*?)(?P=q)",re.S)
items=list(r.items)
for file in (ROOT/'assets/js').glob('*.js'):
 if file.name in ('28-multilingual.js','29-static-catalog.js'):continue
 source=file.read_text(encoding='utf-8')
 for match in js_re.finditer(source):
  v=match.group('v').replace('\\n',' ').strip()
  if len(v)<5 or len(v)>280 or not re.search(r'[A-Za-z]{3}',v):continue
  if any(z in v for z in ('<','>','${','{','}','/api/','http','querySelector','document.','window.','--','\\','=', '#')):continue
  if not ((' ' in v) or v.endswith(('…','!','?'))):continue
  items.append(v)
items=sorted({re.sub(r'\s+',' ',x).strip() for x in items if x and re.search(r'[A-Za-z]',x) and len(x)<=900 and not re.fullmatch(r'[0-9\s\-.,/:+]+',x)})
# Existing catalog and core are merged; never overwrite good human-reviewed translations.
source=(ROOT/'assets/js/29-static-catalog.js').read_text(encoding='utf-8')
old=json.loads(source[source.index('{'):source.rindex('}')+1]);catalog=dict(old)
core_source=(ROOT/'assets/js/28-multilingual.js').read_text(encoding='utf-8')
# The core translations remain available at runtime; include their keys for completeness in audit.
core_keys=re.findall(r"^ '((?:[^'\\]|\\.)+)':\{hi:",core_source,re.M)
items=sorted(set(items)|set(core_keys))
# Don't send proper names/venue names to model as translatable interface text.
proper={'Sawan','Pratibha','Swastik Foundation','Ranchi Ring Road','Baghmara, Talcher'}
items=[x for x in items if x not in proper]
async def run():
 for code,label in [('hi','Hindi'),('or','Odia'),('te','Telugu')]:
  missing=[x for x in items if not catalog.get(x,{}).get(code)]
  print(f'{label}: {len(missing)} missing; translating in one-time batches',flush=True)
  for start in range(0,len(missing),12):
   batch=missing[start:start+12]
   msg=[{'role':'system','content':f'You are a professional Indian wedding website localizer. Translate the JSON array into natural {label}. Return ONLY a JSON array of strings in the exact same order. Preserve names, dates, numbers, emojis, symbols, format placeholders and proper nouns. Never omit any item. Use fluent {label} script, not transliteration or English.'},{'role':'user','content':json.dumps(batch,ensure_ascii=False)}]
   answer=(await generate(msg,temperature=0,max_tokens=4500)).strip()
   answer=re.sub(r'^```(?:json)?\s*|\s*```$','',answer)
   translated=json.loads(answer)
   if not isinstance(translated,list) or len(translated)!=len(batch) or any(not isinstance(v,str) or not v.strip() for v in translated):raise RuntimeError('Invalid translation batch '+str(start))
   for a,b in zip(batch,translated):catalog.setdefault(a,{})[code]=b
   (ROOT/'assets/js/29-static-catalog.js').write_text('window.WEDDING_TRANSLATIONS_OFFLINE='+json.dumps(catalog,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
   print(label,start+len(batch),'/',len(missing),flush=True)
 report={'total_extracted':len(items),'missing':{code:[x for x in items if not catalog.get(x,{}).get(code)] for code in ('hi','or','te')}}
 (ROOT/'FULL-TRANSLATION-AUDIT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 print('Coverage:',{k:len(v) for k,v in report['missing'].items()})
 if any(report['missing'].values()):raise SystemExit('ERROR: Translation catalog is incomplete')
if __name__=='__main__':asyncio.run(run())
