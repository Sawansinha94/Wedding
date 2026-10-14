
const facts = { wedding: { en: 'The wedding is on Tuesday, 24 November 2026, from 7:00 PM at Swastik Foundation, Ranchi Ring Road, Ranchi, Jharkhand.', hi: 'शादी मंगलवार, 24 नवंबर 2026 को शाम 7 बजे से स्वस्तिक फाउंडेशन, रांची रिंग रोड, रांची, झारखंड में है।', or: 'ବିବାହ ମଙ୍ଗଳବାର, ୨୪ ନଭେମ୍ବର ୨୦୨୬ ସନ୍ଧ୍ୟା ୭ଟାରୁ ସ୍ୱସ୍ତିକ ଫାଉଣ୍ଡେସନ୍, ରାଞ୍ଚି ରିଙ୍ଗ ରୋଡ୍, ରାଞ୍ଚି, ଝାଡ଼ଖଣ୍ଡରେ ହେବ।' }, reception: { en: 'The reception and blessings ceremony is on Friday, 27 November 2026, at our residence in Baghmara, Talcher, Odisha. The reception starts at 1:00 PM onwards.', hi: 'रिसेप्शन और आशीर्वाद समारोह शुक्रवार, 27 नवंबर 2026 को बाघमारा, तालचेर, ओडिशा स्थित हमारे निवास पर है। समारोह दोपहर 1 बजे से शुरू होगा।', or: 'ରିସେପ୍ସନ୍ ଓ ଆଶୀର୍ବାଦ ସମାରୋହ ଶୁକ୍ରବାର, ୨୭ ନଭେମ୍ବର ୨୦୨୬ରେ ବାଘମରା, ତାଳଚେର, ଓଡ଼ିଶାରେ ଆମ ବାସଭବନରେ ହେବ। ସମାରୋହ ଦିନ ୧ଟାରୁ ଆରମ୍ଭ ହେବ।' }, contacts: { en: 'For help, call Smt. Asha Sinha (mother): +91 93371 82996; Mr. Ajeet Kumar Sinha (uncle): +91 70166 11280; or Mr. Aswini Sinha (brother): +91 70089 06695. Tap their Call buttons in Family Contacts.', hi: 'मदद के लिए माता श्रीमती आशा सिन्हा: +91 93371 82996, चाचा श्री अजीत कुमार सिन्हा: +91 70166 11280, या भाई अश्विनी सिन्हा: +91 70089 06695 पर कॉल करें।', or: 'ସହାୟତା ପାଇଁ ମାଆ ଆଶା ସିହ୍ନା: +91 93371 82996, ଦାଦା ଅଜିତ କୁମାର ସିହ୍ନା: +91 70166 11280, କିମ୍ବା ଭାଇ ଅଶ୍ୱିନୀ ସିହ୍ନା: +91 70089 06695 ଙ୍କୁ ଫୋନ୍ କରନ୍ତୁ।' }, couple: { en: 'Sawan, son of Late Shri Santosh Prasad and Smt. Asha Sinha, is marrying Pratibha, daughter of Shri Pradeep Kumar and Smt. Swarnlata Kumari.', hi: 'स्वर्गीय श्री संतोष प्रसाद और श्रीमती आशा सिन्हा के पुत्र सावन का विवाह श्री प्रदीप कुमार और श्रीमती स्वर्णलता कुमारी की पुत्री प्रतिभा से हो रहा है।', or: 'ସ୍ୱର୍ଗତ ଶ୍ରୀ ସନ୍ତୋଷ ପ୍ରସାଦ ଓ ଶ୍ରୀମତୀ ଆଶା ସିହ୍ନାଙ୍କ ପୁଅ ସାୱନଙ୍କ ବିବାହ ଶ୍ରୀ ପ୍ରଦୀପ କୁମାର ଓ ଶ୍ରୀମତୀ ସ୍ୱର୍ଣ୍ଣଲତା କୁମାରୀଙ୍କ ଝିଅ ପ୍ରତିଭାଙ୍କ ସହ ହେଉଛି।' }, other: { en: 'I can help with wedding dates, reception, venue directions and family contacts. For other details, please call the family.', hi: 'मैं शादी की तारीख, रिसेप्शन, स्थान और परिवार के संपर्क की जानकारी दे सकता हूँ। अन्य जानकारी के लिए परिवार को कॉल करें।', or: 'ମୁଁ ବିବାହ ତାରିଖ, ରିସେପ୍ସନ୍, ସ୍ଥାନ ଓ ପରିବାର ସମ୍ପର୍କରେ ସାହାଯ୍ୟ କରିପାରିବି। ଅନ୍ୟ ସୂଚନା ପାଇଁ ପରିବାରକୁ ଫୋନ୍ କରନ୍ତୁ।' } };
function offlineAnswer(q, lang) { const s = q.toLowerCase(); let k = /reception|blessing|रिसेप्शन|स्वागत|ରିସେପ୍ସନ|ଆଶୀର୍ବାଦ/.test(s) ? 'reception' : /call|contact|phone|mother|uncle|brother|number|कॉल|फोन|माँ|भाई|संपर्क|ଫୋନ|ମାଆ|ଭାଇ|ଯୋଗାଯୋଗ/.test(s) ? 'contacts' : /bride|groom|parents|who is|दूल्ह|दुल्ह|माता पिता|ବର|କନ୍ୟା/.test(s) ? 'couple' : /wedding|marriage|date|time|venue|where|location|direction|शादी|विवाह|कहाँ|कब|स्थान|समय|ବିବାହ|କେଉଁଠ|କେବେ|ସ୍ଥାନ/.test(s) ? 'wedding' : 'other'; return facts[k][lang] || facts[k].en }
async function requestAI(endpoint, data) { const controller = new AbortController(); const timer = setTimeout(() => controller.abort("AI response exceeded 60 seconds"), 60000); try { const r = await fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data), signal: controller.signal }); if (!r.ok) throw Error('Service unavailable'); return await r.json() } finally { clearTimeout(timer) } }
const conciergeHistory = [];
const VISITOR_NAME_KEY = 'wedding-visitor-preferred-name-v1';
function weddingVisitorName() { try { return sessionStorage.getItem(VISITOR_NAME_KEY) || '' } catch (e) { return '' } }
function weddingSetVisitorName(name, source) { if (!name || !name.trim()) return; try { sessionStorage.setItem(VISITOR_NAME_KEY, name.trim().slice(0, 80)); if (source === 'rsvp' || source === 'wish') sessionStorage.setItem('wedding-visitor-name-source-v1', source); else sessionStorage.removeItem('wedding-visitor-name-source-v1') } catch (e) { } }
window.weddingSetVisitorName = weddingSetVisitorName;
let weddingFamilyConfirmation = '';
let weddingVerificationToken = '';
let weddingIdentityQuestionToken = '';
// A visitor-supplied name is a display preference, never identity authentication.
// Dedicated WebRTC speech-to-speech conversation. No browser TTS or speech recognition.
const voicePanel = document.getElementById('concierge-voice-panel');
const voiceStart = document.getElementById('voice-start');
const voiceStop = document.getElementById('voice-stop');
const voiceState = document.getElementById('voice-state');
const voiceOrb = document.getElementById('voice-orb');
let voiceActive = false, voiceSpeaking = false, voiceRequestPending = false, voiceRecorder = null, voiceStream = null, voicePlayer = null, voiceHistory = [];
function voiceStatus(s) { voiceState.textContent = s; voiceOrb.classList.toggle('listening', s === 'Listening…'); voiceOrb.classList.toggle('speaking', s === 'Speaking…'); document.body.classList.toggle('wedding-voice-active', !voicePanel.hidden) }
function stopVoice() { voiceActive = false; voiceRequestPending = false; if (voiceRecorder?.state === 'recording') voiceRecorder.stop(); voiceStream?.getTracks().forEach(t => t.stop()); voicePlayer?.pause(); browserRecognizer?.abort(); browserRecognizer = null; voiceRecorder = null; voiceStream = null; voiceStart.disabled = false; voiceStop.disabled = true; voiceStatus('Conversation ended.'); document.body.classList.toggle('wedding-voice-active', !voicePanel.hidden); }
function speakReply() { return Promise.resolve() }
function currentVoiceLanguage() { return document.getElementById('ai-lang')?.value || window.weddingCurrentLanguage || 'en' }
let browserRecognizer = null;
function browserVoiceFallback() {
  const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!Recognition) { voiceStatus('Voice recognition is unavailable in this browser. Try Chrome or use text input.'); voiceActive = false; voiceStart.disabled = false; voiceStop.disabled = true; return }
  voiceStream?.getTracks().forEach(track => track.stop()); voiceStream = null;
  voiceStatus('Listening…');
  const rec = new Recognition(); browserRecognizer = rec;
  rec.lang = ({ en: 'en-IN', hi: 'hi-IN', or: 'or-IN', te: 'te-IN' })[currentVoiceLanguage()] || 'en-IN';
  rec.continuous = false; rec.interimResults = false;
  rec.onresult = async (event) => {
    const utterance = event.results?.[0]?.[0]?.transcript?.trim(); if (!utterance || !voiceActive) return;
    voiceStatus('Thinking…');
    try {
      const data = await requestAI('/api/concierge', { question: utterance, language: currentVoiceLanguage(), visitor_name: weddingVisitorName(), verification_token: weddingVerificationToken, history: voiceHistory.slice(-8) });
      const answer = data.answer || 'Sorry, please try again.';
      voiceHistory.push({ role: 'user', content: utterance }, { role: 'assistant', content: answer });
      bubble('user', utterance); bubble('assistant', answer);
      voiceStatus('Speaking…');
      // Prefer the server's Indian neural TTS. Browser speech is a last-resort fallback.
      try {
        const audioResponse = await fetch('/api/voice/speak', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ language: currentVoiceLanguage(), text: answer }) });
        if (!audioResponse.ok) { let detail = 'HTTP ' + audioResponse.status; try { const err = await audioResponse.json(); detail = err.detail || detail } catch (_) { } throw new Error(detail) }
        const audioUrl = URL.createObjectURL(await audioResponse.blob());
        voicePlayer = new Audio(audioUrl);
        await voicePlayer.play();
        await new Promise(resolve => { voicePlayer.onended = resolve; voicePlayer.onerror = resolve });
        URL.revokeObjectURL(audioUrl);
        voicePlayer = null;
        if (voiceActive) browserVoiceFallback();
      } catch (ttsError) {
        console.error('Indian neural voice failed; browser speech deliberately disabled', ttsError);
        voiceStatus('Neural speech failed: ' + (ttsError.message || 'unknown error') + '. Run backend voice diagnostics.');
        voiceActive = false; voiceStart.disabled = false; voiceStop.disabled = true;
      }
    } catch (e) { voiceStatus('AI service unavailable: ' + (e?.name === 'AbortError' ? 'AI response timed out after 30 seconds. Please retry.' : e.message)); voiceActive = false; voiceStart.disabled = false; voiceStop.disabled = true }
  };
  rec.onerror = e => { if (!voiceActive) return; if (e.error === 'no-speech') { browserVoiceFallback(); return } voiceStatus('Microphone: ' + e.error); voiceActive = false; voiceStart.disabled = false; voiceStop.disabled = true };
  rec.onend = () => { };
  try { rec.start() } catch (e) { voiceStatus('Microphone start failed: ' + e.message); voiceActive = false; voiceStart.disabled = false; voiceStop.disabled = true }
}
async function startRealtimeVoice() {
  if (voiceActive) return; voiceActive = true; voiceStart.disabled = true; voiceStop.disabled = false; voiceHistory = []; window.stopWeddingMusic?.();
  if (window.SpeechRecognition || window.webkitSpeechRecognition) { browserVoiceFallback(); return }
  try { voiceStream = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: true, noiseSuppression: true } }); voiceStatus('Listening…'); await voiceLoop() } catch (e) { console.error(e); stopVoice(); voiceStatus('Microphone unavailable. Allow microphone access and use HTTPS or localhost. ' + (e?.message || '')) }
}
async function voiceLoop() {
  if (!voiceActive) return; let chunks = []; let recorder; try { recorder = new MediaRecorder(voiceStream, { mimeType: MediaRecorder.isTypeSupported('audio/webm') ? 'audio/webm' : undefined }); voiceRecorder = recorder; } catch (e) { stopVoice(); voiceStatus('Recording unsupported'); return }
  recorder.ondataavailable = e => { if (e.data.size) chunks.push(e.data) };
  recorder.onstop = async () => {
    if (!voiceActive) return; const blob = new Blob(chunks, { type: recorder.mimeType || 'audio/webm' }); const fd = new FormData(); fd.append('audio', blob, 'voice.webm'); fd.append('language', currentVoiceLanguage()); fd.append('history', JSON.stringify(voiceHistory.slice(-8))); voiceStatus('Thinking…');
    try { const res = await fetch('/api/voice/turn', { method: 'POST', body: fd }); if (!res.ok) { if (res.status === 422) { voiceStatus('Listening…'); return voiceLoop() } throw Error('Speech service ' + res.status) } const data = await res.json(); voiceHistory.push({ role: 'user', content: data.transcript }, { role: 'assistant', content: data.reply }); voiceStatus('Speaking…'); const audio = await fetch('/api/voice/speak', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ language: currentVoiceLanguage(), text: data.reply }) }); if (!audio.ok) throw Error('Voice generation ' + audio.status); const url = URL.createObjectURL(await audio.blob()); voicePlayer = new Audio(url); await voicePlayer.play(); await new Promise(resolve => { voicePlayer.onended = resolve; voicePlayer.onerror = resolve }); URL.revokeObjectURL(url) } catch (e) { console.error(e); voiceStatus('Voice request failed: ' + (e?.message || 'check server settings')); await new Promise(r => setTimeout(r, 1500)) } if (voiceActive) { voiceStatus('Listening…'); voiceLoop() }
  };
  recorder.start(); setTimeout(() => { if (voiceActive && recorder.state === 'recording') recorder.stop() }, 4500);
}
document.getElementById('concierge-talk-mode').addEventListener('click', () => {
  voicePanel.hidden = !voicePanel.hidden;
  document.getElementById('concierge-talk-mode').setAttribute('aria-pressed', String(!voicePanel.hidden));
  voicePanel.setAttribute('aria-label', 'Wedding voice conversation');
  if (voicePanel.hidden) stopVoice();
  document.getElementById('concierge-talk-mode').classList.toggle('active', !voicePanel.hidden); document.body.classList.toggle('wedding-voice-active', !voicePanel.hidden);
  voiceStatus(voicePanel.hidden ? 'Conversation ended.' : 'Tap Start conversation to begin.');
});
document.getElementById('voice-close')?.addEventListener('click', () => { stopVoice(); voicePanel.hidden = true; document.body.classList.remove('wedding-voice-active'); document.getElementById('concierge-talk-mode')?.classList.remove('active'); document.getElementById('concierge-talk-mode')?.setAttribute('aria-pressed', 'false'); });
voiceStart.addEventListener('click', startRealtimeVoice); voiceStop.addEventListener('click', stopVoice); window.addEventListener('pagehide', stopVoice);
document.getElementById('ai-lang').addEventListener('change', () => { if (voiceActive) { stopVoice(); voiceStatus('Language changed. Start a new voice conversation.') } });
const chat = document.getElementById('ai-chat'); function bubble(role, t) { const el = document.createElement('div'); el.className = 'bubble ' + role; el.textContent = t; chat.appendChild(el); chat.scrollTop = chat.scrollHeight } async function askCore(q) {
  q = q.trim(); if (!q) return; const intro = q.match(/^(?:hi[,! ]+)?(?:my name is|i am|i'm|call me)\s+([\p{L} .'-]{2,70})[.!]?$/iu); if (intro) weddingSetVisitorName(intro[1]); if (weddingIdentityQuestionToken) {
    bubble('user', q); document.getElementById('ai-question').value = '';
    try {
      const result = await requestAI('/api/concierge/verify/answer', { token: weddingIdentityQuestionToken, answer: q });
      weddingIdentityQuestionToken = '';
      if (result.status === 'question') {
        weddingIdentityQuestionToken = result.token;
        bubble('assistant', result.question);
      } else if (result.status === 'verified') {
        weddingVerificationToken = result.verified_token;
        const text = [result.special_message, result.greeting].filter(Boolean).join('\n\n');
        bubble('assistant', text); speakReply(text, document.getElementById('ai-lang').value);
      } else bubble('assistant', result.message || 'We can still chat about the wedding!');
    } catch (e) { weddingIdentityQuestionToken = ''; bubble('assistant', 'The check is unavailable. We can still talk about the wedding!'); }
    return;
  }
  const pending = window.weddingPendingFamily;
  const affirmative = /^(yes|yes that's me|yes that is me|yes i am|correct|haan|ha|ji haan|जी हाँ|ହଁ)$/i.test(q.trim());
  const negative = /^(no|nope|not me|no i am not|nah|नहीं|ନା)$/i.test(q.trim());
  if (pending && (affirmative || negative)) {
    const chatLang = document.getElementById('ai-lang').value;
    bubble('user', q); document.getElementById('ai-question').value = '';
    conciergeHistory.push({ role: 'user', content: q });
    window.weddingPendingFamily = null;
    window.weddingLogAction?.(negative ? 'family_declined' : 'family_confirmed', pending.id);
    if (negative) { const text = 'Thank you for clarifying! How can I help you with the wedding?'; bubble('assistant', text); conciergeHistory.push({ role: 'assistant', content: text }); return; }
    const confirmedName = weddingVisitorName();
    if (!confirmedName) { bubble('assistant', 'Please tell me your name so I can check the family greeting.'); return; }
    const send = document.getElementById('ai-send'); send.disabled = true;
    try {
      const data = await requestAI('/api/concierge/verify/start', { name: confirmedName, profile_id: pending.id, confirmed: true });
      if (data.status === 'question') {
        weddingIdentityQuestionToken = data.token;
        const text = 'So lovely to meet you! May I ask a quick question to make sure I am greeting the right person? 🌸\n\n' + data.question;
        bubble('assistant', text); speakReply(text, chatLang);
      } else bubble('assistant', data.message || 'We can still chat about the wedding!');
    } catch (e) { bubble('assistant', 'I could not start the family check right now. We can still chat about the wedding!'); }
    finally { send.disabled = false; }
    return;
  }
  const lang = document.getElementById('ai-lang').value; const btn = document.getElementById('ai-send'); bubble('user', q); document.getElementById('ai-question').value = ''; btn.disabled = true; const status = document.getElementById('ai-chat-status'); try { const r = await requestAI('/api/concierge', { question: q, language: lang, history: conciergeHistory, visitor_name: weddingVisitorName(), family_confirmation: weddingFamilyConfirmation, verification_token: weddingVerificationToken }); bubble('assistant', r.answer); window.weddingPendingFamily = null; conciergeHistory.push({ role: 'user', content: q }, { role: 'assistant', content: r.answer }); if (conciergeHistory.length > 20) conciergeHistory.splice(0, conciergeHistory.length - 20); speakReply(r.answer, lang); status.textContent = r.searched_family ? 'Family knowledge checked.' : 'Answered using wedding knowledge.' } catch (e) { const fallback = /\b(wedding date|venue|reception|contact|address|shaadi|शादी|विवाह)\b/i.test(q) ? offlineAnswer(q, lang) : 'The concierge could not connect to its AI service. Your profile question was not answered. Please retry; the site administrator should inspect the /api/concierge response and backend logs.'; bubble('assistant', fallback); conciergeHistory.push({ role: 'user', content: q }, { role: 'assistant', content: fallback }); status.textContent = 'Concierge API error — profile answer unavailable.'; console.error('Concierge request failed', e) } finally { btn.disabled = false }
}

// Profile recognition begins as soon as the guest supplies a preferred name.
let profileFlow = null, profileFlowName = '', profileFlowBusy = false;
async function startProfileFlow(name) {
  name = (name || '').trim(); if (!name || profileFlowBusy || name === profileFlowName) return;
  profileFlowBusy = true; profileFlowName = name; profileFlow = null; weddingVerificationToken = '';
  try {
    const data = await requestAI('/api/profile/start', { name });
    if (data.status === 'confirm') {
      profileFlow = { status: 'confirm', token: data.token };
      bubble('assistant', data.message + ' Please reply Yes or No.');
      window.dispatchEvent(new CustomEvent('wedding:profile-stage', { detail: { status: 'confirm', message: data.message, name: data.name } }));
    }
    if (data.status === 'ambiguous') {
      const names = (data.candidates || []).map(x => x.name); window.weddingAmbiguousNames = names;
      const text = data.message + ' ' + names.join(' / ');
      bubble('assistant', text);
      window.dispatchEvent(new CustomEvent('wedding:profile-stage', { detail: { status: 'ambiguous', message: text, candidates: names } }));
    }
    if (data.status === 'unmatched') window.dispatchEvent(new CustomEvent('wedding:profile-stage', { detail: { status: 'ready', message: data.message } }));
    window.weddingLogAction?.('profile_match_status', data.status);
  } catch (e) { console.warn('Profile recognition unavailable', e); }
  finally { profileFlowBusy = false; }
}
async function ask(q) {
  q = (q || '').trim(); if (!q) return;
  if (!profileFlow && profileFlowName && q && q !== profileFlowName) {
    // A name selection from an ambiguous shortlist restarts the confirmation flow.
    if (window.weddingAmbiguousNames?.some(n => n.toLowerCase() === q.toLowerCase())) {
      window.weddingAmbiguousNames = []; profileFlowName = ''; await startProfileFlow(q); return;
    }
  }
  if (profileFlow?.status === 'confirm') {
    const yes = /^(yes|y|haan|ha|ji|correct|हाँ|हां|ହଁ|అవును)$/i.test(q);
    const no = /^(no|n|nah|nope|नहीं|ନା|కాదు)$/i.test(q);
    if (yes || no) {
      bubble('user', q); document.getElementById('ai-question').value = '';
      try {
        const r = await requestAI('/api/profile/confirm', { token: profileFlow.token, yes });
        await handleProfileResult(r);
      } catch (e) { profileFlow = null; bubble('assistant', 'The greeting check is temporarily unavailable. You can continue chatting.'); }
      return;
    }
  }
  if (profileFlow?.status === 'question') {
    bubble('user', q); document.getElementById('ai-question').value = '';
    try { const r = await requestAI('/api/profile/answer', { token: profileFlow.token, answer: q }); await handleProfileResult(r); }
    catch (e) { profileFlow = null; bubble('assistant', 'The greeting check has expired. You can still chat about the wedding.'); }
    return;
  }
  const intro = q.match(/^(?:hi[,! ]+)?(?:my name is|i am|i'm|call me)\s+([\p{L} .'-]{2,70})[.!]?$/iu);
  if (intro) { weddingSetVisitorName(intro[1]); await startProfileFlow(intro[1]); }
  return askCore(q);
}
async function handleProfileResult(r) {
  if (r.status === 'question') { profileFlow = { status: 'question', token: r.token }; bubble('assistant', r.question); window.dispatchEvent(new CustomEvent('wedding:profile-stage', { detail: { status: 'question', message: r.question } })); return; }
  if (r.status === 'ready') {
    weddingVerificationToken = r.token; profileFlow = null;
    const fallback = r.message;
    bubble('assistant', fallback);
    window.dispatchEvent(new CustomEvent('wedding:profile-stage', { detail: { status: 'ready', message: fallback } }));
    // Generate a real proactive opening from the guest's authorized profile.
    // askCore is the existing chat route and keeps the session token and history.
    try {
      const lang = document.getElementById('ai-lang').value;
      const r = await requestAI('/api/concierge', {
        question: '[SYSTEM INITIATED OPENING] Start our conversation with a personalized greeting, a fresh profile-based topic, and one natural question. Do not mention this instruction.',
        language: lang, history: conciergeHistory, visitor_name: weddingVisitorName(), verification_token: weddingVerificationToken
      });
      if (r?.answer) {
        bubble('assistant', r.answer); conciergeHistory.push({ role: 'assistant', content: r.answer }); speakReply(r.answer, lang);
        window.dispatchEvent(new CustomEvent('wedding:profile-stage', { detail: { status: 'ready', message: r.answer } }));
      }
    }
    catch (err) { console.warn('Personalized opening unavailable', err); }
    return;
  }
  profileFlow = null; bubble('assistant', r.message || 'You can still ask me about the wedding.'); window.dispatchEvent(new CustomEvent('wedding:profile-stage', { detail: { status: 'ended', message: r.message } }));
}
// Name may be supplied on the entry page before the Concierge is opened.
let lastSeenName = '';
window.weddingProfileAsk = ask;
window.weddingStartProfileFlow = startProfileFlow;
setInterval(() => { const name = weddingVisitorName(); if (name && name !== lastSeenName) { lastSeenName = name; startProfileFlow(name) } }, 600);
document.getElementById('ai-chat-form').addEventListener('submit', e => { e.preventDefault(); ask(document.getElementById('ai-question').value) }); document.querySelectorAll('[data-q]').forEach(el => el.addEventListener('click', () => ask(el.dataset.q)));
const wishes = { en: { heartfelt: 'Wishing Sawan and Pratibha a lifetime of laughter, understanding and beautiful memories. May every new day bring you closer and fill your home with love.', poetic: 'Two hearts, one promise, countless tomorrows. May your love bloom with every sunrise and shine through every season of life.', traditional: 'May your marriage be blessed with love, harmony, prosperity and togetherness. Wishing you both a joyful and auspicious new beginning.', funny: 'May your love be endless, your Wi-Fi always strong, and your debates about dinner always end in dessert! Congratulations, Sawan and Pratibha!' }, hi: { heartfelt: 'सावन और प्रतिभा को जीवनभर प्रेम, खुशियों और साथ का आशीर्वाद। आपका हर नया दिन सुंदर यादों और मुस्कान से भरा हो।', poetic: 'दो दिल, एक वादा, और अनगिनत खूबसूरत कल। आपका प्यार हर मौसम में यूँ ही खिलता रहे।', traditional: 'सावन और प्रतिभा का दांपत्य जीवन प्रेम, सौहार्द, समृद्धि और मंगलमय खुशियों से भरा रहे। हार्दिक शुभकामनाएँ!', funny: 'आपका प्यार हमेशा बना रहे, वाई-फाई तेज रहे और खाने का फैसला हमेशा मुस्कुराकर हो! शादी की ढेर सारी बधाई!' }, or: { heartfelt: 'ସାୱନ ଓ ପ୍ରତିଭାଙ୍କୁ ସାରା ଜୀବନ ପ୍ରେମ, ଖୁସି ଓ ସୁନ୍ଦର ସ୍ମୃତିର ଶୁଭେଚ୍ଛା। ଆପଣଙ୍କ ପ୍ରତ୍ୟେକ ଦିନ ଆନନ୍ଦମୟ ହେଉ।', poetic: 'ଦୁଇଟି ହୃଦୟ, ଗୋଟିଏ ପ୍ରତିଜ୍ଞା, ଅସଂଖ୍ୟ ସୁନ୍ଦର ଆସନ୍ତାକାଲି। ଆପଣଙ୍କ ପ୍ରେମ ସଦା ଫୁଲିଫଳି ରହୁ।', traditional: 'ସାୱନ ଓ ପ୍ରତିଭାଙ୍କ ଦାମ୍ପତ୍ୟ ଜୀବନ ପ୍ରେମ, ସୁଖ, ଶାନ୍ତି ଓ ସମୃଦ୍ଧିରେ ପୂର୍ଣ୍ଣ ହେଉ। ହାର୍ଦ୍ଦିକ ଶୁଭେଚ୍ଛା!', funny: 'ଆପଣଙ୍କ ପ୍ରେମ ଅସୀମ ରହୁ, ୱାଇ-ଫାଇ ସବୁବେଳେ ଭଲ ଚାଲୁ, ଆଉ ଖାଇବା ବାଛିବାରେ ସବୁବେଳେ ହସ ରହୁ! ବିବାହର ଶୁଭେଚ୍ଛା!' } };
// RSVP wish composer: use the same server-side OpenRouter endpoint as Wedding Wishes.
// Never submit automatically: the guest can edit or remove the suggestion.
document.getElementById('rsvp-generate-wish').addEventListener('click', async () => {
  const button = document.getElementById('rsvp-generate-wish');
  const status = document.getElementById('rsvp-wish-status');
  const message = document.getElementById('message');
  const language = document.getElementById('rsvp-wish-language').value;
  const tone = document.getElementById('rsvp-wish-tone').value;
  const name = document.getElementById('guest').value.trim();
  button.disabled = true; button.textContent = 'Creating your wish…'; status.classList.remove('is-ready');
  try {
    const result = await requestAI('/api/wish', { name, tone, language });
    if (!result.wish) throw Error('Empty wish');
    message.value = result.wish.slice(0, 1200);
    status.textContent = 'Your wish is ready! You can edit it before sending your RSVP.';
  } catch (error) {
    message.value = (wishes[language]?.[tone] || wishes.en.heartfelt).slice(0, 1200);
    status.textContent = 'A wedding wish suggestion is ready. Edit it as you like.';
  } finally { button.disabled = false; button.textContent = '✨ Generate a Wedding Wish'; status.classList.add('is-ready'); message.dispatchEvent(new Event('input', { bubbles: true })); message.focus(); }
});
document.getElementById('wish-generate').addEventListener('click', async () => { const name = document.getElementById('wish-from').value.trim(), tone = document.getElementById('wish-tone').value, language = document.getElementById('wish-lang').value; const btn = document.getElementById('wish-generate'), status = document.getElementById('wish-status'); btn.disabled = true; try { const r = await requestAI('/api/wish', { name, tone, language }); document.getElementById('wish-output').value = r.wish; status.textContent = r.mode === 'ai' ? 'Your personalized wish is ready.' : 'Your wish is ready.' } catch (e) { document.getElementById('wish-output').value = wishes[language][tone] + (name ? '\n— ' + name : ''); status.textContent = 'Created from wedding wish templates.' } finally { btn.disabled = false; document.getElementById('wish-output').dispatchEvent(new Event('input', { bubbles: true })); } });
document.getElementById('wish-copy').addEventListener('click', async () => { const value = document.getElementById('wish-output').value; if (!value) return; try { await navigator.clipboard.writeText(value); document.getElementById('wish-status').textContent = 'Wish copied!' } catch (e) { document.getElementById('wish-output').select(); document.getElementById('wish-status').textContent = 'Select and copy the wish above.' } });
document.getElementById('wish-rsvp').addEventListener('click', () => { const value = document.getElementById('wish-output').value; if (!value) return; document.getElementById('message').value = value; document.getElementById('message').dispatchEvent(new Event('input', { bubbles: true })); location.hash = '#rsvp' });
