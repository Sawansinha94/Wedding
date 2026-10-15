
(function(){
 const feed=document.getElementById('wish-feed');
 const status=document.getElementById('feed-status');
 const publish=document.getElementById('wish-publish');
 const output=document.getElementById('wish-output');
 const nameInput=document.getElementById('wish-from');
 const publishStatus=document.getElementById('publish-status');
 let serverItems=[];
 let pending=[];
 let latestIds=new Set();
 let initialized=false;
 function entry(item,isNew){
   const card=document.createElement('article');card.className='wish-entry'+(isNew?' wish-new':'');
   const by=document.createElement('strong');by.textContent=item.name;
   const when=document.createElement('time');const d=new Date(item.created_at);when.textContent=Number.isNaN(d.getTime())?'Just now':d.toLocaleDateString(undefined,{day:'numeric',month:'short',year:'numeric'});
   const quote=document.createElement('blockquote');quote.textContent=item.message;
   card.append(when,by,quote);
   if(Number.isInteger(Number(item.id)) && !String(item.id).startsWith('temp-') && !String(item.id).startsWith('local-')) {
     const replies=document.createElement('div');replies.className='wish-replies';
     (item.replies||[]).forEach(reply=>{const r=document.createElement('p');const author=document.createElement('strong');author.textContent=reply.name+': ';r.append(author,document.createTextNode(reply.message));replies.append(r)});
     const toggle=document.createElement('button');toggle.type='button';toggle.className='wish-reply-toggle';toggle.textContent='↩ Reply / Comment';
     const form=document.createElement('form');form.className='wish-reply-form';form.hidden=true;
     const responder=document.createElement('input');responder.placeholder='Your name';responder.required=true;responder.maxLength=80;responder.setAttribute('aria-label','Your name');
     const comment=document.createElement('textarea');comment.placeholder='Write your reply or comment';comment.required=true;comment.maxLength=1000;comment.setAttribute('aria-label','Your comment');
     const send=document.createElement('button');send.type='submit';send.textContent='Post reply';
     const msg=document.createElement('small');msg.setAttribute('role','status');
     form.append(responder,comment,send,msg);
     toggle.addEventListener('click',()=>{form.hidden=!form.hidden;if(!form.hidden)responder.focus()});
     form.addEventListener('submit',async e=>{e.preventDefault();const name=responder.value.trim(),message=comment.value.trim();if(!name||!message){msg.textContent='Please enter your name and comment.';return}send.disabled=true;msg.textContent='Posting…';try{const response=await fetch('/api/wishes/'+encodeURIComponent(item.id)+'/replies',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,message})});if(!response.ok)throw Error('Could not save reply');msg.textContent='Reply posted';await refresh()}catch(err){msg.textContent='Unable to post. Please try again.'}finally{send.disabled=false}});
     card.append(replies,toggle,form);
   }
   return card;
 }
 function render(){
   const combined=[...pending,...serverItems];
   const seen=new Set();const items=combined.filter(item=>{const key=item.id||item.name+'|'+item.message+'|'+item.created_at;if(seen.has(key))return false;seen.add(key);return true}).slice(0,40);
   const nextIds=new Set(items.map(x=>String(x.id)));
   const frag=document.createDocumentFragment();
   if(!items.length){const empty=document.createElement('p');empty.className='wish-empty';empty.textContent='Be the first to share a blessing!';frag.append(empty)}
   else items.forEach((item,index)=>frag.append(entry(item,initialized && index===0 && !latestIds.has(String(item.id)))));
   feed.replaceChildren(frag);latestIds=nextIds;initialized=true;
 }
 async function refresh(){
   if(location.protocol==='file:'){
     status.textContent='Please run the FastAPI server. Wishes are saved only to Neon PostgreSQL.';
     return;
   }
   try{
     const r=await fetch('/api/wishes',{cache:'no-store'});
     if(!r.ok)throw Error('Neon wishes unavailable (HTTP '+r.status+')');
     const data=await r.json();serverItems=Array.isArray(data.wishes)?data.wishes:[];
     pending=pending.filter(x=>!serverItems.some(y=>y.id===x.id));
     render();status.textContent='';
   }catch(e){
     status.textContent='Unable to load wishes from Neon. Please try again later.';
   }
 }
 publish.addEventListener('click',async()=>{
   const name=nameInput.value.trim();const message=output.value.trim();
   if(!name){publishStatus.textContent='Please enter your name before publishing.';nameInput.focus();return}if(!message){publishStatus.textContent='Please enter a wish before publishing.';output.focus();return}
   if(message.length>1200){publishStatus.textContent='Please keep your wish within 1200 characters.';return}
   const optimistic={id:'temp-'+Date.now(),name,message,created_at:new Date().toISOString()};
   pending.unshift(optimistic);render();feed.scrollTop=0;
   publish.disabled=true;publishStatus.textContent='Saving your wish to Neon…';
   try{
     if(location.protocol==='file:')throw Error('local');
     const r=await fetch('/api/wishes',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,message})});
     if(!r.ok){const detail=await r.json().catch(()=>({}));throw Error(detail.detail||'Server unavailable')}
     const saved=await r.json();
     pending=pending.filter(x=>x.id!==optimistic.id);
     if(saved.wish){serverItems=[saved.wish,...serverItems.filter(x=>x.id!==saved.wish.id)]}
     render();
     publishStatus.textContent='Published! Your blessing is now visible to other visitors.';if(window.weddingSetVisitorName)window.weddingSetVisitorName(name,'wish');
     output.value='';await refresh();
   }catch(e){
     pending=pending.filter(x=>x.id!==optimistic.id);
     render();
     publishStatus.textContent='Not published: Neon did not confirm the save. Please try again. '+(e.message||'');
   }finally{publish.disabled=false}
 });
 refresh();setInterval(()=>{if(!document.hidden)refresh()},12000);
})();
