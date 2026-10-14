
// Insert selected emoji at the current cursor, respecting textarea maxlength.
(()=>{
 const emojiList=['❤️','💕','💖','💗','💞','💘','🥰','😍','😘','😊','🤗','🙏','🙌','👏','🎉','🎊','🥳','💐','🌹','🌸','🌺','🌷','🪷','✨','🌟','💫','🕊️','💍','👰','🤵','🥂','🎁','🪔','🧿','💛','🫶','☺️','🌼','🎶','💌'];
 for(const [fieldId,label] of [['wish-output','Add emojis to your wedding wish'],['message','Add emojis to your RSVP wish']]){
  const field=document.getElementById(fieldId);if(!field)continue;
  const wrap=document.createElement('div');wrap.className='emoji-tools';
  const trigger=document.createElement('button');trigger.type='button';trigger.className='emoji-trigger';trigger.textContent='😊 Add Emoji';trigger.setAttribute('aria-label',label);trigger.setAttribute('aria-expanded','false');
  const hint=document.createElement('span');hint.className='emoji-hint';hint.textContent='Make your wishes more expressive';
  const picker=document.createElement('div');picker.className='emoji-picker';picker.setAttribute('role','group');picker.setAttribute('aria-label','Choose an emoji');
  emojiList.forEach(emoji=>{const choice=document.createElement('button');choice.type='button';choice.className='emoji-choice';choice.textContent=emoji;choice.setAttribute('aria-label','Insert '+emoji);choice.addEventListener('click',()=>{
   const start=field.selectionStart??field.value.length,end=field.selectionEnd??start;
   const next=field.value.slice(0,start)+emoji+field.value.slice(end);
   if(field.maxLength>=0 && next.length>field.maxLength)return;
   field.value=next;field.focus();field.setSelectionRange(start+emoji.length,start+emoji.length);field.dispatchEvent(new Event('input',{bubbles:true}));
  });picker.appendChild(choice)});
  trigger.addEventListener('click',()=>{const open=picker.classList.toggle('is-open');trigger.setAttribute('aria-expanded',String(open))});
  wrap.append(trigger,hint,picker);field.insertAdjacentElement('afterend',wrap);
 }
})();
