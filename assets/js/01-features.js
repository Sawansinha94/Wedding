
const weddingTime=new Date('2026-11-24T19:00:00+05:30').getTime();function updateCountdown(){const remaining=Math.max(0,weddingTime-Date.now());const vals=[Math.floor(remaining/86400000),Math.floor(remaining/3600000)%24,Math.floor(remaining/60000)%60,Math.floor(remaining/1000)%60];['days','hours','minutes','seconds'].forEach((id,i)=>document.getElementById(id).textContent=String(vals[i]).padStart(2,'0'))}updateCountdown();setInterval(updateCountdown,1000);
const rsvpForm=document.getElementById('rsvp-form');
rsvpForm.addEventListener('submit',async event=>{
  event.preventDefault();
  const button=rsvpForm.querySelector('button[type="submit"]');
  const confirmation=document.getElementById('rsvp-success');
  const error=document.getElementById('rsvp-error');
  confirmation.hidden=true; confirmation.classList.remove('is-visible');
  error.hidden=true;
  const data={name:document.getElementById('guest').value.trim(),attendance:document.getElementById('attending').value,event:document.getElementById('event').value,guests:Number(document.getElementById('guests').value),message:document.getElementById('message').value};
  if(!data.name || !data.attendance || !Number.isInteger(data.guests) || data.guests<1 || data.guests>20){error.textContent='Please enter a name, attendance choice, and valid guest count.';error.hidden=false;return;}
  button.disabled=true;button.textContent='Saving your RSVP…';
  try{
    const response=await fetch('/api/rsvp',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
    if(!response.ok)throw new Error('The RSVP could not be saved. Please try again.');
    const result=await response.json();
    if(!result.ok)throw new Error('The RSVP could not be confirmed.');
    if(window.weddingSetVisitorName)window.weddingSetVisitorName(data.name,'rsvp');
    rsvpForm.reset();
    confirmation.hidden=false;
    requestAnimationFrame(()=>confirmation.classList.add('is-visible'));
    confirmation.scrollIntoView({behavior:'smooth',block:'nearest'});
  }catch(err){error.textContent='Unable to save your RSVP. Please check your connection and try again. The confirmation animation will appear only after saving succeeds.';error.hidden=false;}
  finally{button.disabled=false;button.textContent='Send My RSVP ✉';}
});
