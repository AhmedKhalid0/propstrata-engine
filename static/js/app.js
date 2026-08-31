/**
 * PropStrata Engine Interactive Client Controller
 */

function toggleLanguage() {
    const currentDir = document.documentElement.getAttribute('dir');
    const label = document.getElementById('lang-label');

    if (currentDir === 'rtl') {
        document.documentElement.setAttribute('dir', 'ltr');
        document.documentElement.setAttribute('lang', 'en');
        if (label) label.textContent = 'العربية (RTL)';
        localStorage.setItem('propstrata_lang', 'en');
    } else {
        document.documentElement.setAttribute('dir', 'rtl');
        document.documentElement.setAttribute('lang', 'ar');
        if (label) label.textContent = 'English (LTR)';
        localStorage.setItem('propstrata_lang', 'ar');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Restore language preference
    const savedLang = localStorage.getItem('propstrata_lang');
    if (savedLang === 'ar') {
        document.documentElement.setAttribute('dir', 'rtl');
        document.documentElement.setAttribute('lang', 'ar');
        const label = document.getElementById('lang-label');
        if (label) label.textContent = 'English (LTR)';
    }
});
