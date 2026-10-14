"""Offline translation coverage audit; no API calls."""
import json,re,html,subprocess
from pathlib import Path
from html.parser import HTMLParser
root=Path(__file__).resolve().parent
class Reader(HTMLParser):
 def __init__(self):super().__init__();self.texts=[];self.skip=0
 def handle_starttag(self,tag,attrs):
  if tag in ('script','style'):self.skip+=1
  for key,value in attrs:
   if key in ('placeholder','aria-label','alt','title') and value and re.search('[A-Za-z]',value):self.texts.append(value.strip())
 def handle_endtag(self,tag):
  if tag in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,data):
  value=html.unescape(data.strip())
  if not self.skip and value and re.search('[A-Za-z]',value):self.texts.append(value)
r=Reader();r.feed((root/'index.html').read_text())
source=(root/'assets/js/29-static-catalog.js').read_text()
catalog=json.loads(source[source.index('{'):source.rindex('}')+1])
all_text=sorted(set(r.texts))
missing={lang:[t for t in all_text if not catalog.get(t,{}).get(lang)] for lang in ('hi','or','te')}
(root/'TRANSLATION-AUDIT.json').write_text(json.dumps({'total_html_strings':len(all_text),'missing_by_language':missing},ensure_ascii=False,indent=2))
for lang,values in missing.items():print(f'{lang}: {len(all_text)-len(values)}/{len(all_text)} catalog entries, {len(values)} missing (some are in the core dictionary)')
