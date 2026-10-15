/* Show visitor's self-entered first name after the envelope opens. */
(()=>{
 const target=document.getElementById('wedding-personal-welcome');
 if(!target)return;
 function render(){
   let name='';try{name=sessionStorage.getItem('wedding-visitor-preferred-name-v1')||'';}catch{}
   name=name.trim().split(/\s+/)[0];
   if(!name || !/^[\p{L}'-]{2,40}$/u.test(name)){target.hidden=true;return;}
   target.textContent=`Welcome ${name} 🌸`;
   target.hidden=false;
 }
 render();
 document.getElementById('wedding-entry-form')?.addEventListener('submit',()=>{
   setTimeout(render,250);
   setTimeout(render,1000);
 });
 window.addEventListener('storage',render);
 window.addEventListener('wedding:visitor-name',render);
})();
