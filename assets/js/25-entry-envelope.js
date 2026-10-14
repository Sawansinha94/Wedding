/* Optional welcome: open automatically after 20 seconds of no typing. */
(()=>{
 const gate=document.getElementById('wedding-entry');
 const form=document.getElementById('wedding-entry-form');
 const input=document.getElementById('wedding-entry-name');
 const status=document.getElementById('wedding-entry-error');
 if(!gate||!form||!input)return;
 const button=form.querySelector('button');
 const key='wedding-entry-complete-v1';
 let timer=null,opening=false,typingStarted=false;
 let known=false;try{known=sessionStorage.getItem(key)==='yes'}catch{}
 function openInvitation(){
   if(opening)return;
   opening=true;
   if(timer!==null)clearTimeout(timer);
   try{sessionStorage.setItem(key,'yes')}catch{}
   gate.classList.add('wedding-opening');
   setTimeout(()=>{gate.hidden=true;document.documentElement.classList.remove('wedding-gated');},850);
 }
 if(known){gate.hidden=true;document.documentElement.classList.remove('wedding-gated');return;}
 gate.hidden=false;document.documentElement.classList.add('wedding-gated');
 // Start counting on page load; typing cancels the countdown permanently for this visit.
 timer=setTimeout(()=>{if(!typingStarted)openInvitation()},20000);
 input.addEventListener('input',()=>{if(!typingStarted){typingStarted=true;if(timer!==null)clearTimeout(timer);timer=null;}});
 form.addEventListener('submit',async e=>{
   e.preventDefault();if(opening)return;
   const name=input.value.trim().replace(/\s+/g,' ');
   // Name is optional; empty submission opens immediately, without identity matching.
   if(!name){openInvitation();return;}
   if(name.length<2||name.length>80||!/^[\p{L} .'-]+$/u.test(name)||name.split(' ').length>2){status.textContent='Please enter a valid first name, or leave it blank to continue.';return;}
   button.disabled=true;status.textContent='Opening your invitation…';
   window.weddingSetVisitorName?.(name,'welcome');
   try{sessionStorage.setItem('wedding-visitor-preferred-name-v1',name)}catch{}
   window.dispatchEvent(new CustomEvent('wedding:visitor-name',{detail:{name,source:'welcome'}}));
   openInvitation();
   // Optional analytics must never prevent a guest entering the site.
   if(window.weddingSessionId){fetch('/api/telemetry/visitor-name',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session_id:window.weddingSessionId,first_name:name})}).catch(()=>{});}
   button.disabled=false;
 });
})();
