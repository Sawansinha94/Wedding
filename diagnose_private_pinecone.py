"""Owner-only private Pinecone diagnostic; never expose as an HTTP endpoint."""
import os,sys,json
from dotenv import load_dotenv
load_dotenv()
from pinecone import Pinecone
key=os.getenv('PINECONE_API_KEY');host=os.getenv('PINECONE_PRIVATE_INDEX_HOST');ns=os.getenv('PINECONE_PRIVATE_NAMESPACE','wedding-private-profiles')
if not key or not host:sys.exit('Configure PINECONE_API_KEY and PINECONE_PRIVATE_INDEX_HOST')
index=Pinecone(api_key=key).Index(host=host)
print('Index stats:',index.describe_index_stats())
print('Namespace:',ns)
if len(sys.argv)>1:
 query=sys.argv[1]
 result=index.search(namespace=ns,query={'inputs':{'text':query},'top_k':5},fields=['name','relation'])
 hits=result.get('result',{}).get('hits',[]) if isinstance(result,dict) else result.result.hits
 for hit in hits:
  data=hit if isinstance(hit,dict) else hit.to_dict()
  print(data.get('_id') or data.get('id'),data.get('fields',{}).get('name'),'score',data.get('_score'))
