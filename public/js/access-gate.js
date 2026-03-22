(function() {
  'use strict';

  function bytesToHex(bytes) {
    return Array.from(bytes).map(function(byte) {
      return byte.toString(16).padStart(2, '0');
    }).join('');
  }

  function setUnlockedState(isUnlocked) {
    var root = document.documentElement;

    root.classList.toggle('access-gate-locked', !isUnlocked);
    root.classList.toggle('access-gate-unlocked', isUnlocked);
  }

  async function hashPassword(value) {
    var encoder = new TextEncoder();
    var digest = await window.crypto.subtle.digest('SHA-256', encoder.encode(value));
    return bytesToHex(new Uint8Array(digest));
  }

  function focusPasswordInput() {
    var passwordInput = document.getElementById('access-gate-password');

    if (passwordInput) {
      passwordInput.focus();
      passwordInput.select();
    }
  }

  function initAccessGate() {
    var payload = window.__ACCESS_GATE__;
    var gate = document.getElementById('access-gate');
    var form = document.getElementById('access-gate-form');
    var passwordInput = document.getElementById('access-gate-password');
    var errorMessage = document.getElementById('access-gate-error');

    if (!payload || !payload.enabled || !gate || !form || !passwordInput) {
      return;
    }

    if (!window.crypto || !window.crypto.subtle) {
      if (errorMessage) {
        errorMessage.hidden = false;
        errorMessage.textContent = 'This browser does not support the password gate.';
      }
      setUnlockedState(false);
      return;
    }

    try {
      if (window.sessionStorage.getItem(payload.session_key) === payload.password_hash) {
        setUnlockedState(true);
        return;
      }
    } catch (error) {
      setUnlockedState(false);
    }

    setUnlockedState(false);
    focusPasswordInput();

    form.addEventListener('submit', async function(event) {
      event.preventDefault();

      if (errorMessage) {
        errorMessage.hidden = true;
      }

      try {
        var submittedHash = await hashPassword(passwordInput.value);

        if (submittedHash === payload.password_hash) {
          window.sessionStorage.setItem(payload.session_key, payload.password_hash);
          passwordInput.value = '';
          setUnlockedState(true);
          return;
        }
      } catch (error) {
        // Fall through to the generic error state below.
      }

      passwordInput.value = '';
      setUnlockedState(false);

      if (errorMessage) {
        errorMessage.hidden = false;
      }

      focusPasswordInput();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAccessGate);
  } else {
    initAccessGate();
  }
})();
