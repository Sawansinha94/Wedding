/* Wedding calendar actions: Android -> Google Calendar, iOS -> calendar-import ICS. */
(() => {
  'use strict';
  // Times are India Standard Time. End times are provisional because the invitation says "onwards".
  const events = {
    lagan: {title:'Lagan Ceremony — Sawan & Pratibha', start:'2026-11-20T16:00:00+05:30', description:'Lagan Sagai: formal invitation exchange and traditional rituals. Dress code: Saffron & Traditional Ethnic.'},
    haldi: {title:'Haldi Ceremony — Sawan & Pratibha', start:'2026-11-22T18:00:00+05:30', description:'Haldi Ubtan: turmeric blessings, music and celebration. Dress code: Golden Yellow Festive Attire.'},
    wedding: {title:'Wedding Ceremony — Sawan & Pratibha', start:'2026-11-24T19:00:00+05:30', location:'Swastik Foundation, Ranchi Ring Road, Ranchi, Jharkhand', description:'Shubh Vivah: wedding ceremony from 7:00 PM onwards. Dress code: Royal Festive Attire.'},
    reception: {title:'Reception & Blessings — Sawan & Pratibha', start:'2026-11-27T19:00:00+05:30', location:'Our Residence, Baghmara, Talcher, Odisha', description:'Reception and blessings from 7:00 PM onwards. Dress code: Festive Elegance.'}
  };
  const two = n => String(n).padStart(2,'0');
  const utc = date => `${date.getUTCFullYear()}${two(date.getUTCMonth()+1)}${two(date.getUTCDate())}T${two(date.getUTCHours())}${two(date.getUTCMinutes())}${two(date.getUTCSeconds())}Z`;
  const escapeICS = s => String(s||'').replace(/\\/g,'\\\\').replace(/\n/g,'\\n').replace(/,/g,'\\,').replace(/;/g,'\\;');
  const eventTimes = e => {const start = new Date(e.start); return {start,end:new Date(start.getTime()+2*60*60*1000)};};
  function ics(e,key){
    const {start,end}=eventTimes(e);
    const lines=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Sawan Pratibha Wedding//Calendar Invitation//EN','CALSCALE:GREGORIAN','METHOD:PUBLISH','BEGIN:VEVENT',`UID:${key}-2026@sawan-pratibha-wedding`,`DTSTAMP:${utc(new Date())}`,`DTSTART:${utc(start)}`,`DTEND:${utc(end)}`,`SUMMARY:${escapeICS(e.title)}`,`DESCRIPTION:${escapeICS(e.description+' Start time is confirmed; event end time is provisional.')}`];
    if(e.location)lines.push(`LOCATION:${escapeICS(e.location)}`);
    lines.push('END:VEVENT','END:VCALENDAR','');return lines.join('\r\n');
  }
  function downloadICS(e,key){
    const blob=new Blob([ics(e,key)],{type:'text/calendar;charset=utf-8'});
    const url=URL.createObjectURL(blob),a=document.createElement('a');
    a.href=url;a.download=`sawan-pratibha-${key}.ics`;document.body.appendChild(a);a.click();a.remove();
    setTimeout(()=>URL.revokeObjectURL(url),30000);
  }
  function googleUrl(e){
    const {start,end}=eventTimes(e);
    const params=new URLSearchParams({action:'TEMPLATE',text:e.title,dates:`${utc(start)}/${utc(end)}`,details:e.description+' Start time is confirmed; end time is provisional.',ctz:'Asia/Kolkata'});
    if(e.location)params.set('location',e.location);
    return `https://calendar.google.com/calendar/render?${params.toString()}`;
  }
  function isIOS(){return /iPad|iPhone|iPod/i.test(navigator.userAgent) || (navigator.platform==='MacIntel' && navigator.maxTouchPoints>1);}
  document.addEventListener('click',event=>{
    const button=event.target.closest('[data-calendar-event]');if(!button)return;
    const key=button.dataset.calendarEvent,e=events[key];if(!e)return;
    // iOS Calendar imports .ics; Android opens Google Calendar's prefilled event editor.
    // On other devices Google Calendar is the default, with an ICS fallback in documentation.
    if(isIOS())downloadICS(e,key);
    else window.open(googleUrl(e),'_blank','noopener,noreferrer');
  });
})();
