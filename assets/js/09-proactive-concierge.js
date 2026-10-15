/* Proactive bottom concierge: mirrors server-controlled profile stages. */
(()=>{'use strict';
const t={en:{title:'Your Wedding Concierge',yes:"Yes, that’s me",no:'Not me',open:'Open conversation',dismiss:'Minimize',answer:'Reply in the Concierge'},hi:{title:'आपका विवाह सहायक',yes:'हाँ, मैं ही हूँ',no:'मैं नहीं हूँ',open:'बातचीत खोलें',dismiss:'छोटा करें',answer:'सहायक को जवाब दें'},or:{title:'ଆପଣଙ୍କ ବିବାହ ସହାୟକ',yes:'ହଁ, ମୁଁ',no:'ମୁଁ ନୁହେଁ',open:'କଥାବାର୍ତ୍ତା ଖୋଲନ୍ତୁ',dismiss:'ଛୋଟ କରନ୍ତୁ',answer:'ଉତ୍ତର ଦିଅନ୍ତୁ'},te:{title:'మీ వివాహ సహాయకుడు',yes:'అవును, నేనే',no:'నేను కాదు',open:'సంభాషణ తెరవండి',dismiss:'చిన్నదిగా చేయండి',answer:'సమాధానం ఇవ్వండి'}};
const el=document.createElement('aside');el.className='concierge-welcome-toast';el.id='concierge-welcome-toast';el.hidden=true;el.setAttribute('role','region');el.setAttribute('aria-label','Wedding Concierge');
el.innerHTML=`<div class="concierge-toast-head"><span aria-hidden="true">✧</span><strong class="concierge-toast-title"></strong><button type="button" class="concierge-welcome-close" aria-label="Minimize">×</button></div><p class="concierge-welcome-message" aria-live="polite"></p><div class="concierge-toast-actions"><button type="button" class="concierge-yes"></button><button type="button" class="concierge-no"></button><button type="button" class="concierge-open"></button></div>`;
document.body.appendChild(el);let stage=null;let dismissed=false;let autoHideTimer=null;
function clearAutoHide(){if(autoHideTimer!==null){clearTimeout(autoHideTimer);autoHideTimer=null;}}
function hideToast(){clearAutoHide();el.hidden=true;}
function scheduleAutoHide(){clearAutoHide();autoHideTimer=setTimeout(()=>{autoHideTimer=null;el.hidden=true;},20000);}
const language=()=>window.weddingLanguage?.get?.()||'en';const words=()=>t[language()]||t.en;
const message=el.querySelector('.concierge-welcome-message');const yes=el.querySelector('.concierge-yes'),no=el.querySelector('.concierge-no'),open=el.querySelector('.concierge-open');
function refresh(){const w=words();el.querySelector('.concierge-toast-title').textContent=w.title;yes.textContent=w.yes;no.textContent=w.no;open.textContent=stage==='question'?w.answer:w.open;el.querySelector('.concierge-welcome-close').setAttribute('aria-label',w.dismiss);}
function show(detail){stage=detail.status;dismissed=false;message.textContent=detail.message||'';refresh();yes.hidden=stage!=='confirm';no.hidden=stage!=='confirm';open.hidden=stage==='confirm';el.hidden=false;scheduleAutoHide();}
function goChat(){hideToast();document.getElementById('concierge')?.scrollIntoView({behavior:'smooth',block:'start'});setTimeout(()=>document.getElementById('ai-question')?.focus({preventScroll:true}),350);}
async function respond(answer){hideToast();if(typeof window.weddingProfileAsk!=='function')return;yes.disabled=no.disabled=true;try{await window.weddingProfileAsk(answer)}finally{yes.disabled=no.disabled=false;}}
yes.addEventListener('click',()=>respond('yes'));no.addEventListener('click',()=>respond('no'));open.addEventListener('click',goChat);
el.querySelector('.concierge-welcome-close').addEventListener('click',()=>{dismissed=true;hideToast();});
window.addEventListener('wedding:profile-stage',e=>{const d=e.detail||{};if(d.status==='confirm'||d.status==='question'||d.status==='ready'||d.status==='ambiguous')show(d);else{stage=null;hideToast();}});
window.addEventListener('wedding:language-change',refresh);
window.weddingOpenConcierge=goChat;
})();
