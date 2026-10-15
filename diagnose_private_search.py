"""Read-only Pinecone integrated-embedding diagnostic. No secret values printed."""
import os,sys,json
from dotenv import load_dotenv
from pinecone import Pinecone
load_dotenv()
query=' '.join(sys.argv[1:]).strip() or 'Sailendra Kumar'
host=os.getenv('PINECONE_PRIVATE_INDEX_HOST','').strip()
ns=os.getenv('PINECONE_PRIVATE_NAMESPACE','wedding-private-profiles').strip()
if not host: raise SystemExit('Set PINECONE_PRIVATE_INDEX_HOST')
index=Pinecone(api_key=os.environ['PINECONE_API_KEY']).Index(host=host)
stats=index.describe_index_stats()
raw=stats.to_dict() if hasattr(stats,'to_dict') else stats
print('Namespace:',ns,'stats:',raw.get('namespaces',{}).get(ns))
response=index.search(namespace=ns,query={'inputs':{'text':query},'top_k':5},fields=['name','relation','side'])
d=response.to_dict() if hasattr(response,'to_dict') else response
hits=d.get('result',{}).get('hits',[])
for hit in hits:
 print(json.dumps({'id':hit.get('_id',hit.get('id')),'name':hit.get('fields',{}).get('name'),'score':hit.get('_score',hit.get('score'))},ensure_ascii=False))
