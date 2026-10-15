/* Prefill RSVP and Wishes from the name entered at the invitation envelope. */
(()=>{
  const KEY='wedding-visitor-preferred-name-v1';
  const fields=['guest','wish-from'];
  function prefill(name){
    const clean=String(name||'').trim();
    if(!clean)return;
    for(const id of fields){
      const field=document.getElementById(id);
      if(field && (!field.value.trim() || field.dataset.weddingAutofilled==='true')){
        field.value=clean;
        field.dataset.weddingAutofilled='true';
        field.dispatchEvent(new Event('input',{bubbles:true}));
      }
    }
  }
  try{prefill(sessionStorage.getItem(KEY))}catch{}
  window.addEventListener('wedding:visitor-name',e=>prefill(e.detail?.name));
  for(const id of fields){
    document.getElementById(id)?.addEventListener('input',e=>{
      if(e.isTrusted)e.currentTarget.dataset.weddingAutofilled='false';
    });
  }
})();
