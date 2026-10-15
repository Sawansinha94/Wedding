// Rephrase only when the visitor has written at least five characters.
(() => {
  const configs=[
    {button:'wish-rephrase',field:'wish-output',status:'wish-status',lang:'wish-lang',tone:'wish-tone'},
    {button:'rsvp-rephrase',field:'message',status:'rsvp-wish-status',lang:'rsvp-wish-language',tone:'rsvp-wish-tone'}
  ];
  for(const cfg of configs){
    const button=document.getElementById(cfg.button);
    const field=document.getElementById(cfg.field);
    const status=document.getElementById(cfg.status);
    if(!button||!field||!status) continue;
    const sync=()=>{
      const eligible=field.value.trim().length>=5;
      button.hidden=!eligible;
      button.setAttribute('aria-hidden',String(!eligible));
      button.disabled=!eligible||button.dataset.busy==='true';
    };
    field.addEventListener('input',sync);
    field.addEventListener('change',sync);
    // Other modules can generate text programmatically; observe their input changes.
    field.addEventListener('wedding:text-updated',sync);
    sync();
    button.addEventListener('click',async()=>{
      const original=field.value.trim();
      if(original.length<5){sync();return;}
      button.dataset.busy='true';button.disabled=true;
      const old=button.textContent;button.textContent='Rephrasing…';
      try{
        const res=await fetch('/api/wish/rephrase',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:original,language:document.getElementById(cfg.lang)?.value||'en',tone:document.getElementById(cfg.tone)?.value||'heartfelt'})});
        if(!res.ok)throw new Error('Rephrasing unavailable');
        const data=await res.json();
        if(!data.text?.trim())throw new Error('No rewritten text');
        // Do not overwrite text that the visitor changed while the request was running.
        if(field.value.trim()!==original){status.textContent='Your message changed while rephrasing. Your edits were kept.';return;}
        field.value=data.text.trim().slice(0,Number(field.maxLength)>0?field.maxLength:1200);
        field.dispatchEvent(new Event('input',{bubbles:true}));
        status.textContent='Rephrased your message. Please review or edit before submitting.';
      }catch(e){status.textContent='Rephrasing is unavailable right now. Your original message is unchanged.';}
      finally{delete button.dataset.busy;button.textContent=old;sync();}
    });
  }
})();
