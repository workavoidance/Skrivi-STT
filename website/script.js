(() => {
  const button = document.querySelector('.language-switch');
  if (!button) return;

  // Carry language between pages in URLs, without cookies or browser storage.
  const setLanguage = (language) => {
    const norwegian = language !== 'en';
    const code = norwegian ? 'nb' : 'en';
    document.documentElement.lang = code;
    document.querySelectorAll('[data-nb][data-en]').forEach((element) => {
      element.textContent = element.dataset[code];
    });
    document.querySelectorAll('[data-aria-nb][data-aria-en]').forEach((element) => {
      element.setAttribute('aria-label', norwegian ? element.dataset.ariaNb : element.dataset.ariaEn);
    });
    document.querySelectorAll('[data-alt-nb][data-alt-en]').forEach((element) => {
      element.setAttribute('alt', norwegian ? element.dataset.altNb : element.dataset.altEn);
    });
    document.querySelectorAll('[data-src-nb][data-src-en]').forEach((element) => {
      element.setAttribute('src', norwegian ? element.dataset.srcNb : element.dataset.srcEn);
    });
    document.querySelectorAll('[data-href-nb][data-href-en]').forEach((element) => {
      element.href = norwegian ? element.dataset.hrefNb : element.dataset.hrefEn;
    });
    const description = document.querySelector('meta[name="description"]');
    if (description?.dataset.descriptionNb && description.dataset.descriptionEn) {
      description.content = norwegian ? description.dataset.descriptionNb : description.dataset.descriptionEn;
    }
    document.querySelectorAll('a[href]').forEach((link) => {
      const url = new URL(link.getAttribute('href'), window.location.href);
      if (url.origin !== window.location.origin || !['http:', 'https:', 'file:'].includes(url.protocol)) return;
      if (norwegian) url.searchParams.delete('lang');
      else url.searchParams.set('lang', 'en');
      link.href = url.href;
    });
    button.textContent = norwegian ? 'EN' : 'NO';
    button.setAttribute('aria-label', norwegian ? 'Switch to English' : 'Bytt til norsk');
    button.setAttribute('aria-pressed', norwegian ? 'false' : 'true');
  };
  button.addEventListener('click', () => {
    const language = document.documentElement.lang === 'nb' ? 'en' : 'nb';
    const url = new URL(window.location.href);
    if (language === 'en') url.searchParams.set('lang', 'en');
    else url.searchParams.delete('lang');
    history.replaceState(null, '', url);
    setLanguage(language);
  });
  window.addEventListener('popstate', () => {
    setLanguage(new URLSearchParams(window.location.search).get('lang'));
  });
  setLanguage(new URLSearchParams(window.location.search).get('lang'));
})();
