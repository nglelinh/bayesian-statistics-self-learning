/**
 * Sidebar submenu toggle.
 * The chapter title navigates. Only the button collapses the lesson list,
 * so a tap on mobile does not leave the page before the submenu can be read.
 * The current chapter is opened in the HTML; this script does not restore
 * an older collapsed state over that.
 */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var toggles = document.querySelectorAll('.sidebar-chapter-toggle');

    toggles.forEach(function (toggle) {
      toggle.addEventListener('click', function () {
        setSubmenuOpen(toggle, toggle.getAttribute('aria-expanded') !== 'true');
      });

      toggle.addEventListener('keydown', function (event) {
        if (event.key === 'ArrowRight') {
          event.preventDefault();
          setSubmenuOpen(toggle, true);
        } else if (event.key === 'ArrowLeft') {
          event.preventDefault();
          setSubmenuOpen(toggle, false);
        }
      });
    });
  });

  function setSubmenuOpen(toggle, open) {
    var submenuId = toggle.getAttribute('aria-controls');
    var submenu = submenuId ? document.getElementById(submenuId) : null;
    if (!submenu) {
      return;
    }

    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    toggle.classList.toggle('expanded', open);
    submenu.classList.toggle('open', open);
  }
})();
