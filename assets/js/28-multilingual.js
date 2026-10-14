/* Global language state, entry selection, header switching and DOM localization.
 * UI strings are translated exclusively from bundled offline dictionaries.
 * User content (chat, wishes, RSVP, inputs) is deliberately excluded.
 */
(()=>{
'use strict';
const supported=['en','hi','or','te'],key='wedding-language-v1';
const labels={en:'English',hi:'हिन्दी',or:'ଓଡ଼ିଆ',te:'తెలుగు'};
const core={
 'Choose your language':{hi:'अपनी भाषा चुनें',or:'ଆପଣଙ୍କ ଭାଷା ବାଛନ୍ତୁ',te:'మీ భాషను ఎంచుకోండి'},
 'A CELEBRATION OF LOVE':{hi:'प्रेम का उत्सव',or:'ପ୍ରେମର ଉତ୍ସବ',te:'ప్రేమ వేడుక'},
 'Welcome to the Wedding 🌸':{hi:'शादी में आपका स्वागत है 🌸',or:'ବିବାହକୁ ସ୍ୱାଗତ 🌸',te:'వివాహానికి స్వాగతం 🌸'},
 'With love, Sawan & Pratibha invite you to open your wedding invitation.':{hi:'सावन और प्रतिभा स्नेहपूर्वक आपको अपना विवाह निमंत्रण खोलने के लिए आमंत्रित करते हैं।',or:'ସାୱନ ଓ ପ୍ରତିଭା ସ୍ନେହର ସହିତ ଆପଣଙ୍କୁ ବିବାହ ନିମନ୍ତ୍ରଣ ଖୋଲିବାକୁ ଆମନ୍ତ୍ରଣ କରୁଛନ୍ତି।',te:'సావన్ మరియు ప్రతిభ ప్రేమతో తమ వివాహ ఆహ్వానాన్ని తెరవమని మిమ్మల్ని ఆహ్వానిస్తున్నారు.'},
 'What is your first name? (Optional)':{hi:'आपका पहला नाम क्या है? (वैकल्पिक)',or:'ଆପଣଙ୍କ ପ୍ରଥମ ନାମ କ’ଣ? (ଇଚ୍ଛାଧୀନ)',te:'మీ మొదటి పేరు ఏమిటి? (ఐచ్ఛికం)'},
 'Your first name (optional)':{hi:'आपका पहला नाम (वैकल्पिक)',or:'ଆପଣଙ୍କ ପ୍ରଥମ ନାମ (ଇଚ୍ଛାଧୀନ)',te:'మీ మొదటి పేరు (ఐచ్ఛికం)'},
 '✉ Open My Invitation':{hi:'✉ मेरा निमंत्रण खोलें',or:'✉ ମୋ ନିମନ୍ତ୍ରଣ ଖୋଲନ୍ତୁ',te:'✉ నా ఆహ్వానాన్ని తెరవండి'},
 
 '⌨ Text chat':{hi:'⌨ लिखकर बातचीत',or:'⌨ ଲେଖି କଥାହୁଅନ୍ତୁ',te:'⌨ టైప్ చేసి మాట్లాడండి'},
 '🎙 Talk with us':{hi:'🎙 हमसे बात करें',or:'🎙 ଆମ ସହ କଥାହୁଅନ୍ତୁ',te:'🎙 మాతో మాట్లాడండి'},
 'Start conversation':{hi:'बात शुरू करें',or:'କଥା ଆରମ୍ଭ କରନ୍ତୁ',te:'సంభాషణ ప్రారంభించండి'},
 'End conversation':{hi:'बात समाप्त करें',or:'କଥା ଶେଷ କରନ୍ତୁ',te:'సంభాషణ ముగించండి'},
 'Wedding date':{hi:'शादी की तारीख',or:'ବିବାହ ତାରିଖ',te:'పెళ్లి తేదీ'},
 'Venue':{hi:'स्थान',or:'ସ୍ଥାନ',te:'వేదిక'},
 'Reception':{hi:'स्वागत समारोह',or:'ସ୍ୱାଗତ ସମାରୋହ',te:'రిసెప్షన్'},
 'Call family':{hi:'परिवार को कॉल करें',or:'ପରିବାରକୁ ଫୋନ୍ କରନ୍ତୁ',te:'కుటుంబానికి కాల్ చేయండి'},
 'Our Story':{hi:'हमारी कहानी',or:'ଆମ କାହାଣୀ',te:'మా కథ'},
 'Our Families':{hi:'हमारे परिवार',or:'ଆମ ପରିବାର',te:'మా కుటుంబాలు'},
 'Our Journey':{hi:'हमारी यात्रा',or:'ଆମ ଯାତ୍ରା',te:'మా ప్రయాణం'},
 'Ceremonies':{hi:'समारोह',or:'ଉତ୍ସବ',te:'వేడుకలు'},
 'Venues':{hi:'आयोजन स्थल',or:'ସ୍ଥାନ',te:'వేదికలు'},
 'Wedding Wishes':{hi:'शुभकामनाएँ',or:'ଶୁଭେଚ୍ଛା',te:'వివాహ శుభాకాంక్షలు'},
 'Contact':{hi:'संपर्क',or:'ଯୋଗାଯୋଗ',te:'సంప్రదించండి'},
 'Your Wedding Concierge':{hi:'आपका विवाह सहायक',or:'ଆପଣଙ୍କ ବିବାହ ସହାୟକ',te:'మీ వివాహ సహాయకుడు'},
 'Home':{hi:'मुखपृष्ठ',or:'ମୁଖ୍ୟ ପୃଷ୍ଠା',te:'హోమ్'},
 'Events':{hi:'कार्यक्रम',or:'କାର୍ଯ୍ୟକ୍ରମ',te:'కార్యక్రమాలు'},
 'Language':{hi:'भाषा',or:'ଭାଷା',te:'భాష'},
 'Kindly RSVP':{hi:'कृपया अपनी उपस्थिति बताएँ',or:'ଦୟାକରି ଆପଣଙ୍କ ଉପସ୍ଥିତି ଜଣାନ୍ତୁ',te:'దయచేసి మీ హాజరును తెలియజేయండి'},
 'Send My RSVP ✉':{hi:'मेरी पुष्टि भेजें ✉',or:'ମୋ ଉତ୍ତର ପଠାନ୍ତୁ ✉',te:'నా సమాధానాన్ని పంపండి ✉'},
 'Send ↗':{hi:'भेजें ↗',or:'ପଠାନ୍ତୁ ↗',te:'పంపండి ↗'},
 'Our Blessings':{hi:'हमारे आशीर्वाद',or:'ଆମ ଆଶୀର୍ବାଦ',te:'మా ఆశీస్సులు'},
 'The Wedding Of':{hi:'शुभ विवाह',or:'ଶୁଭ ବିବାହ',te:'శుభ వివాహం'}
};
const offlineCatalog=window.WEDDING_TRANSLATIONS_OFFLINE||{};
const excluded='#ai-chat,#wish-feed,[contenteditable],[data-no-translate]';
let lang='en',generation=0,pending=false,observer=null;const cache={hi:new Map(),or:new Map(),te:new Map()};

function readSaved(){try{return localStorage.getItem(key)||'en'}catch{return 'en'}}
function save(v){try{localStorage.setItem(key,v)}catch{}}
function shouldSkip(el){return !el||!!el.closest(excluded)||['SCRIPT','STYLE','NOSCRIPT','SVG','TEXTAREA'].includes(el.tagName)}
function original(node,attr){if(!node.__weddingOriginal)node.__weddingOriginal={};if(!(attr in node.__weddingOriginal))node.__weddingOriginal[attr]=attr==='text'?node.nodeValue:node.getAttribute(attr);return node.__weddingOriginal[attr]}
function collect(){const items=[];const walk=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
while(n=walk.nextNode()){if(!n.nodeValue.trim()||shouldSkip(n.parentElement)||n.parentElement?.closest('select')?.hasAttribute('data-no-translate'))continue;const raw=original(n,'text'),v=raw.trim();if(v&&v.length<901&&/[A-Za-z]/.test(v)&&!/^([\d\s.,:/+–—-]+)$/.test(v))items.push({node:n,attr:'text',raw,v});}
for(const el of document.querySelectorAll('input[placeholder],textarea[placeholder],button[aria-label],a[aria-label],img[alt],iframe[title],[data-i18n-placeholder]')){if(shouldSkip(el))continue;for(const attr of ['placeholder','aria-label','alt','title']){if(!el.hasAttribute(attr))continue;const raw=original(el,attr),v=(raw||'').trim();if(v&&/[A-Za-z]/.test(v)&&v.length<901)items.push({node:el,attr,raw,v});}}
return items;}
function setItem(item,v){if(item.attr==='text'){if(item.node.isConnected)item.node.nodeValue=item.raw.replace(item.v,v)}else if(item.node.isConnected)item.node.setAttribute(item.attr,v)}
function dynamicWelcome(value,language){
  // Only the greeting is translated; the guest's name is preserved verbatim.
  const m=value.match(/^Welcome(?:,|\s+)(.+?)(\s*🌸)?$/i);
  if(!m)return null;
  const prefix={hi:'स्वागत है',or:'ସ୍ୱାଗତ',te:'స్వాగతం'}[language];
  const guest=m[1].trim(); // Visitor name is the sole runtime-transliterated value; no network request.
  return prefix?`${prefix}, ${guest}${m[2]||''}`:null;
}
function localizeNow(items){for(const it of items){if(lang==='en'){setItem(it,it.v);continue}const val=core[it.v]?.[lang]||offlineCatalog[it.v]?.[lang]||dynamicWelcome(it.v,lang);if(val)setItem(it,val);else setItem(it,it.v)}}
function translateMissing(items){
  // No runtime translation requests. Missing strings are reported for the build audit.
  const missing=[...new Set(items.map(x=>x.v).filter(v=>lang!=='en'&&!core[v]?.[lang]&&!offlineCatalog[v]?.[lang]))];
  if(missing.length && window.WEDDING_TRANSLATION_DEBUG) console.warn('Missing bundled translations',lang,missing);
}
function syncControls(){document.documentElement.lang=lang;window.dispatchEvent(new Event('wedding:language-change'));document.querySelectorAll('.entry-lang').forEach(b=>{const on=b.dataset.lang===lang;b.classList.toggle('active',on);b.setAttribute('aria-pressed',String(on))});const select=document.getElementById('site-language');if(select)select.value=lang;for(const id of ['ai-lang','wish-lang','rsvp-wish-language']){const el=document.getElementById(id);if(el&&el.querySelector('option[value="'+lang+'"]'))el.value=lang;}}
function apply(v){
  lang=supported.includes(v)?v:'en';save(lang);generation++;
  // Disconnect while we write DOM nodes; otherwise our own translations
  // and UI refreshes can trigger an endless MutationObserver feedback loop.
  if(observer)observer.disconnect();
  try {syncControls();const items=collect();localizeNow(items);translateMissing(items);}
  finally {if(observer)observer.observe(document.body,{subtree:true,childList:true});}
}
function schedule(){if(pending)return;pending=true;setTimeout(()=>{pending=false;apply(lang)},50)}
window.weddingLanguage={get:()=>lang,set:apply,t:(v)=>lang==='en'?v:(core[v]?.[lang]||offlineCatalog[v]?.[lang]||v),coverage:()=>{const items=collect();return {total:items.length,translated:items.filter(x=>!!(core[x.v]?.[lang]||offlineCatalog[x.v]?.[lang])).length,language:lang}}};
function init(){lang=supported.includes(readSaved())?readSaved():'en';document.querySelectorAll('.entry-lang').forEach(b=>b.addEventListener('click',()=>apply(b.dataset.lang)));document.getElementById('site-language')?.addEventListener('change',e=>apply(e.target.value));apply(lang);
// Only react to newly added meaningful UI content, not decorative petals,
// counters, empty wrappers, or nodes inside excluded live chat regions.
observer=new MutationObserver(mutations=>{
  for(const m of mutations){
    for(const n of m.addedNodes){
      if(n.nodeType!==1 && n.nodeType!==3)continue;
      const el=n.nodeType===1?n:n.parentElement;
      if(!el || el.closest?.(excluded) || el.closest?.('.petal,.rose-petal,.floating-petal'))continue;
      if(n.nodeType===3 && !/[A-Za-z]{2,}/.test(n.nodeValue||''))continue;
      if(n.nodeType===1){
        if(el.matches?.('.petal,.rose-petal,.floating-petal'))continue;
        if(!/[A-Za-z]{2,}/.test((el.textContent||'').slice(0,200)))continue;
      }
      schedule();return;
    }
  }
});observer.observe(document.body,{subtree:true,childList:true});}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
