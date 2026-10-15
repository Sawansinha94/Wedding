"""Edit profiles and run to upload consented family details to your Pinecone integrated-embedding index."""
import os
from pinecone import Pinecone
from dotenv import load_dotenv
load_dotenv()
profiles=[
 {"_id":"groom-sawan","name":"Sawan","side":"groom","relation":"Groom; son of Late Shri Santosh Prasad and Smt. Asha Sinha","text":"Sawan is the groom. Son of Late Shri Santosh Prasad and Smt. Asha Sinha."},
 {"_id":"bride-pratibha","name":"Pratibha","side":"bride","relation":"Bride; daughter of Shri Pradeep Kumar and Smt. Swarnlata Kumari","text":"Pratibha is the bride. Daughter of Shri Pradeep Kumar and Smt. Swarnlata Kumari."},
 {"_id":"groom-mother","name":"Smt. Asha Sinha","side":"groom","relation":"Groom's mother","text":"Smt. Asha Sinha is the groom Sawan's mother."},
 {"_id":"groom-uncle","name":"Mr. Ajeet Kumar Sinha","side":"groom","relation":"Groom's uncle","text":"Mr. Ajeet Kumar Sinha is the groom Sawan's uncle."},
 {"_id":"groom-brother","name":"Mr. Aswini Sinha","side":"groom","relation":"Groom's brother","text":"Mr. Aswini Sinha is the groom Sawan's brother."},
 {"_id":"bride-father","name":"Shri Pradeep Kumar","side":"bride","relation":"Bride's father","text":"Shri Pradeep Kumar is the bride Pratibha's father."},
 {"_id":"bride-mother","name":"Smt. Swarnlata Kumari","side":"bride","relation":"Bride's mother","text":"Smt. Swarnlata Kumari is the bride Pratibha's mother."},
]
if __name__=='__main__':
    pc=Pinecone(api_key=os.environ['PINECONE_API_KEY'])
    index=pc.Index(host=os.environ['PINECONE_INDEX_HOST'])
    index.upsert_records(namespace=os.getenv('PINECONE_NAMESPACE','wedding-family'), records=profiles)
    print(f'Uploaded {len(profiles)} family profiles. Add consented ages, traits and biographies to enrich answers.')
