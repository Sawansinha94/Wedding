
// Automatic, lightweight rose-petal animation. No button or visitor action required.
const reducedPetalMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
function addRosePetal() {
  if (document.hidden || reducedPetalMotion.matches) return;
  const petal = document.createElement('span');
  petal.className = 'petal';
  petal.textContent = ['🌸', '🌺', '🌸', '🌸', '🩷'][Math.floor(Math.random() * 5)];
  petal.style.left = `${Math.random() * 100}vw`;
  petal.style.setProperty('--duration', `${6 + Math.random() * 5}s`);
  petal.style.setProperty('--drift', `${Math.random() * 260 - 130}px`);
  petal.style.setProperty('--size', `${13 + Math.random() * 12}px`);
  petal.style.opacity = '0.75';
  document.body.appendChild(petal);
  petal.addEventListener('animationend', () => petal.remove(), { once: true });
}
if (!reducedPetalMotion.matches) {
  for (let i = 0; i < 8; i++) setTimeout(addRosePetal, i * 240);
}
if (!window.__weddingPetalInterval) window.__weddingPetalInterval = setInterval(addRosePetal, 1200);
// Background music is OFF until the visitor explicitly turns it on.
const weddingAudio = new Audio('images/wedding-background.mp3');
weddingAudio.loop = true;
weddingAudio.preload = 'none';
weddingAudio.volume = 0.5;
const musicToggle = document.getElementById('wedding-music-toggle');
function stopWeddingMusic() { weddingAudio.pause(); updateMusicToggle(); }
function updateMusicToggle() {
  const playing = !weddingAudio.paused;
  musicToggle?.setAttribute('aria-pressed', String(playing));
  musicToggle?.setAttribute('aria-label', playing ? 'Pause wedding background music' : 'Play wedding background music');
  musicToggle?.classList.toggle('is-playing', playing);
}
window.stopWeddingMusic = stopWeddingMusic;
musicToggle?.addEventListener('click', async () => {
  if (!weddingAudio.paused) { stopWeddingMusic(); return; }
  try { await weddingAudio.play(); } catch (_) { /* User can retry if playback is blocked. */ }
  updateMusicToggle();
});
weddingAudio.addEventListener('ended', updateMusicToggle);
updateMusicToggle();
weddingAudio.play().then(updateMusicToggle).catch(updateMusicToggle);
function startWeddingMusicOnInteraction(event) {
  if (musicToggle?.contains(event.target)) return;
  weddingAudio.play().then(() => {
    updateMusicToggle();
    document.removeEventListener('pointerdown', startWeddingMusicOnInteraction);
    document.removeEventListener('keydown', startWeddingMusicOnInteraction);
  }).catch(updateMusicToggle);
}
document.addEventListener('pointerdown', startWeddingMusicOnInteraction);
document.addEventListener('keydown', startWeddingMusicOnInteraction);
