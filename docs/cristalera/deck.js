<script>
(() => {
  const names = {
    motivation: '01 / Motivation',
    bayes: '02 / Bayesian inference & decisions',
    poison: '03 / Poisoning',
    evasion: '04 / Evasion',
    defense: '05 / Bayesian defenses',
    sequential: '06 / Bayesian sequential play',
    llm: '07 / From humans to AI agents',
    conclusions: '08 / Open questions',
    appendix: 'Technical appendix'
  };
  const setup = () => {
    document.querySelectorAll('.reveal .slides section[id]').forEach(s => {
      const name = names[s.id.split('-')[0]];
      if (!name || s.classList.contains('template-slide')) return;
      const kicker = document.createElement('div');
      kicker.className = 'section-kicker';
      kicker.textContent = name;
      s.prepend(kicker);
    });
    const update = () => document.body.classList.toggle('template-active',
      Reveal.getCurrentSlide()?.classList.contains('template-slide'));
    Reveal.on('slidechanged', update);
    update();
  };
  if (typeof Reveal !== 'undefined' && Reveal.isReady()) setup();
  else if (typeof Reveal !== 'undefined') Reveal.on('ready', setup);
  else window.addEventListener('load', () => {
    if (Reveal.isReady()) setup(); else Reveal.on('ready', setup);
  });
})();
</script>
