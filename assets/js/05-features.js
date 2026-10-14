
/* Progressive enhancement: content remains visible if JavaScript is disabled. */
(()=>{
  if(!('IntersectionObserver' in window)||window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  const sections=[...document.querySelectorAll('main > section, body > section')].filter(el=>el.id!=='home');
  const targets=[];
  const add=(el,variant='',delay=0)=>{
    if(!el||el.classList.contains('scroll-reveal'))return;
    el.classList.add('scroll-reveal');
    if(variant)el.classList.add(variant);
    el.style.setProperty('--reveal-delay',`${Math.min(delay,360)}ms`);
    targets.push(el);
  };
  sections.forEach(section=>{
    add(section.querySelector('.section-heading, .reference-heading'));
    const groups=[
      '.ceremony-card','.venue-card','.journey-location','.journey-art',
      '.journey-steps > *','.timeline-item','.story-card','.couple-story-feature',
      '.family-panel','.contact','.person','.tree-generation',
      '.ai-card','.ai-panel','.rsvp-wrap','.traditional-portrait-card'
    ];
    groups.forEach(selector=>{
      [...section.querySelectorAll(selector)].forEach((el,i)=>add(el,i%2?'reveal-right':'reveal-left',(i%4)*85));
    });
    // Other major section blocks get a soft fade-in, without affecting interactive controls.
    [...section.children].filter(el=>!el.classList.contains('scroll-reveal')&&el.tagName!=='SCRIPT').forEach(el=>{
      if(!el.querySelector('.scroll-reveal'))add(el);
    });
  });
  if(!targets.length)return;
  document.documentElement.classList.add('scroll-motion-ready');
  const observer=new IntersectionObserver(entries=>{
    entries.forEach(entry=>{
      if(entry.isIntersecting){entry.target.classList.add('is-visible');observer.unobserve(entry.target)}
    });
  },{threshold:.08,rootMargin:'0px 0px -35px 0px'});
  targets.forEach(el=>observer.observe(el));
  // Prevent above-the-fold content from flashing hidden during initialization.
  requestAnimationFrame(()=>targets.forEach(el=>{
    if(el.getBoundingClientRect().top < innerHeight*.83)el.classList.add('is-visible');
  }));
})();
