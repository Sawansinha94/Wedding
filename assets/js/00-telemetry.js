/* Session-scoped, minimal event logging. Never captures text inputs or keystrokes. */
(() => {
  'use strict';
  let sid=null;
  try { sid=sessionStorage.getItem('wedding-tab-session-id-v1'); } catch {}
  if(!sid && window.crypto && crypto.randomUUID){
    sid=crypto.randomUUID();
    try { sessionStorage.setItem('wedding-tab-session-id-v1',sid); } catch {}
  }
  if(!sid)return;
  window.weddingSessionId=sid;
  const nativeFetch=window.fetch.bind(window);
  window.fetch=(input,init={})=>{
    const url=typeof input==='string'?input:input.url;
    const sameOrigin=new URL(url,location.href).origin===location.origin;
    if(!sameOrigin)return nativeFetch(input,init);
    const headers=new Headers(init.headers || (typeof input!=='string'?input.headers:undefined));
    headers.set('X-Wedding-Session',sid);
    return nativeFetch(input,{...init,headers});
  };
  const send=(endpoint,body)=>nativeFetch(endpoint,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({...body,session_id:sid}),keepalive:true}).catch(()=>{});
  const device=/iPhone|iPad|iPod/i.test(navigator.userAgent)?'ios':/Android/i.test(navigator.userAgent)?'android':'desktop';
  const ua=navigator.userAgent||'';
  const browser=/Edg\//.test(ua)?'Edge':/CriOS\//.test(ua)?'Chrome iOS':/FxiOS\//.test(ua)?'Firefox iOS':/Chrome\//.test(ua)?'Chrome':/Firefox\//.test(ua)?'Firefox':/Safari\//.test(ua)?'Safari':'Other';
  const os=/iPhone|iPad|iPod/.test(ua)?'iOS/iPadOS':/Android/.test(ua)?'Android':/Windows/.test(ua)?'Windows':/Mac OS X|Macintosh/.test(ua)?'macOS':/Linux/.test(ua)?'Linux':'Unknown';
  const sendVisit=()=>send('/api/telemetry/visit',{
    page_path:location.pathname,referrer:document.referrer,device_type:device,
    browser_name:browser,operating_system:os,device_model:'',
    screen_width:screen.width,screen_height:screen.height,
    viewport_width:innerWidth,viewport_height:innerHeight,
    language:navigator.language||'',timezone:Intl.DateTimeFormat().resolvedOptions().timeZone||''
  });
  sendVisit();
  window.weddingLogAction=(action,context='')=>send('/api/telemetry/action',{action,context:String(context).slice(0,160)});
  document.addEventListener('change',e=>{if(e.target.id==='concierge-speak')window.weddingLogAction('concierge_voice_toggle',e.target.checked?'on':'off');});
  document.addEventListener('click',e=>{
    const calendar=e.target.closest('[data-calendar-event]');
    if(calendar)window.weddingLogAction('calendar_open',calendar.dataset.calendarEvent);
    const music=e.target.closest('#wedding-music-toggle');
    if(music)window.weddingLogAction('music_toggle',music.getAttribute('aria-pressed')==='true'?'turn_off':'turn_on');
    const mic=e.target.closest('#concierge-mic');
    if(mic)window.weddingLogAction('concierge_microphone');
    const copy=e.target.closest('#wish-copy');
    if(copy)window.weddingLogAction('wish_copied');
    const nav=e.target.closest('a[href^="#"]');
    if(nav)window.weddingLogAction('navigation',nav.getAttribute('href'));
    const call=e.target.closest('a[href^="tel:"]');
    if(call)window.weddingLogAction('contact_call','family-contact');
  });
})();
