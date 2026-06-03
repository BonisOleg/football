const initTournamentChoice = () => {
  const choiceRoot = document.querySelector('[data-tournament-choice]');
  const tournamentInput = document.getElementById('id_tournament');
  if (!choiceRoot || !tournamentInput) return;

  const setTheme = (theme) => {
    if (theme) document.body.className = `page ${theme}`;
  };

  choiceRoot.querySelectorAll('.choice-btn').forEach((btn) => {
    btn.replaceWith(btn.cloneNode(true));
  });

  choiceRoot.querySelectorAll('.choice-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      choiceRoot.querySelectorAll('.choice-btn').forEach((b) => b.classList.remove('is-selected'));
      btn.classList.add('is-selected');
      tournamentInput.value = btn.dataset.tournamentId;
      setTheme(btn.dataset.theme);
    });
  });

  const selected = choiceRoot.querySelector('.choice-btn.is-selected');
  if (selected) {
    tournamentInput.value = selected.dataset.tournamentId;
    setTheme(selected.dataset.theme);
  }
};

initTournamentChoice();

document.body.addEventListener('htmx:afterSwap', (e) => {
  if (e.detail.target?.id === 'apply-result') {
    if (e.detail.target.querySelector('.apply-success')) {
      document.getElementById('apply-section')?.scrollIntoView({ behavior: 'smooth' });
    } else {
      initTournamentChoice();
    }
  }
});
