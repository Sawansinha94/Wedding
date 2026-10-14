
/* One-time typing animation when the invitation cards enter the viewport.
   All names stay visible when scripting is disabled or reduced motion is requested. */
(()=>{
  const cards=[...document.querySelectorAll('#our-story .person')];
  if(!cards.length || !('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  const pause=ms=>new Promise(resolve=>setTimeout(resolve,ms));
  async function typeText(el,speed){
    const full=el.textContent;
    el.setAttribute('aria-label',full);
    el.textContent='';
    el.classList.add('type-target','is-typing');
    for(const char of full){el.textContent+=char;await pause(speed)}
    el.classList.remove('is-typing');
  }
  const observer=new IntersectionObserver(entries=>{
    entries.forEach(entry=>{
      if(!entry.isIntersecting)return;
      observer.unobserve(entry.target);
      (async()=>{
        const card=entry.target;
        await typeText(card.querySelector('h3'),105);
        for(const parent of card.querySelectorAll('p strong')){
          await pause(140);
          await typeText(parent,32);
        }
      })();
    });
  },{threshold:.35});
  cards.forEach(card=>observer.observe(card));
})();
