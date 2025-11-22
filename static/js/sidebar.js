document.addEventListener('DOMContentLoaded', function () {
    try {
        console.log('[sidebar.js] loaded');
        const toggle = document.getElementById('sidebarToggle');
        const sidebar = document.getElementById('sidebar');

        if (!toggle) console.warn('[sidebar.js] toggle button (#sidebarToggle) not found');
        if (!sidebar) console.warn('[sidebar.js] sidebar element (#sidebar) not found');
        if (!toggle || !sidebar) return;

        // initialize aria-expanded based on current sidebar visibility
        function updateAria() {
            const isHidden = sidebar.classList.contains('hidden');
            toggle.setAttribute('aria-expanded', String(!isHidden));
        }

        // keep aria state correct on resize (do not force-show/hide)
        window.addEventListener('resize', updateAria);
        updateAria();

        // Attach click handler (robust to event binding order)
        const onToggle = function (e) {
            e.preventDefault();

            // Toggle base hidden class
            const isHiddenNow = sidebar.classList.toggle('hidden');

            // Ensure responsive classes reflect the collapsed state so md:block doesn't override hidden
            if (isHiddenNow) {
                // Hiding: add md:hidden, remove md:block
                sidebar.classList.add('md:hidden');
                sidebar.classList.remove('md:block');
            } else {
                // Showing: remove md:hidden, add md:block
                sidebar.classList.remove('md:hidden');
                sidebar.classList.add('md:block');
                // Ensure hidden removed
                sidebar.classList.remove('hidden');
            }

            // compute visible state for aria (use computed style for accuracy)
            const computedHidden = window.getComputedStyle(sidebar).display === 'none';
            toggle.setAttribute('aria-expanded', String(!computedHidden));
            console.log('[sidebar.js] toggled, hidden=', computedHidden);
        };

        // If button exists, use it; otherwise attach delegated handler
        if (toggle) {
            toggle.addEventListener('click', onToggle);
        } else {
            document.addEventListener('click', function (e) {
                if (e.target && (e.target.id === 'sidebarToggle' || e.target.closest('#sidebarToggle'))) {
                    onToggle(e);
                }
            });
        }

    } catch (err) {
        console.error('[sidebar.js] error', err);
    }
});
