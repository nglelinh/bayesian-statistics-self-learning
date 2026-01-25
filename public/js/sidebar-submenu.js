/**
 * Sidebar submenu toggle functionality
 * Author: Nguyen Le Linh
 * Date: 2026-01-24
 */

(function() {
  'use strict';

  // Wait for DOM to be ready
  document.addEventListener('DOMContentLoaded', function() {
    initializeSubmenu();
  });

  function initializeSubmenu() {
    // Get all chapter headers
    const chapterHeaders = document.querySelectorAll('.sidebar-chapter-header');
    
    if (chapterHeaders.length === 0) {
      return; // No chapters found
    }

    // Add click handlers to all chapter headers
    chapterHeaders.forEach(function(header) {
      header.addEventListener('click', function(e) {
        // Prevent default link behavior when clicking arrow
        const target = e.target;
        if (target.classList.contains('dropdown-arrow') || 
            target.closest('.dropdown-arrow')) {
          e.preventDefault();
        }

        toggleSubmenu(header);
      });
    });

    // Auto-expand current chapter
    autoExpandCurrentChapter();

    // Add keyboard navigation
    addKeyboardNavigation(chapterHeaders);
  }

  function toggleSubmenu(header) {
    const chapterNum = header.getAttribute('data-chapter');
    const submenu = document.getElementById('submenu-' + chapterNum);
    
    if (!submenu) {
      return;
    }

    // Toggle open class
    const isOpen = submenu.classList.contains('open');
    
    if (isOpen) {
      // Close submenu
      submenu.classList.remove('open');
      header.classList.remove('expanded');
    } else {
      // Open submenu
      submenu.classList.add('open');
      header.classList.add('expanded');
    }

    // Save state to localStorage
    saveSubmenuState(chapterNum, !isOpen);
  }

  function autoExpandCurrentChapter() {
    // Find current page's chapter
    const currentLessonItem = document.querySelector('.sidebar-lesson-item.active');
    
    if (currentLessonItem) {
      // Find parent submenu
      const parentSubmenu = currentLessonItem.closest('.sidebar-lessons-submenu');
      if (parentSubmenu) {
        const chapterNum = parentSubmenu.id.replace('submenu-', '');
        const chapterHeader = document.querySelector('[data-chapter="' + chapterNum + '"]');
        
        if (chapterHeader) {
          // Open this submenu
          parentSubmenu.classList.add('open');
          chapterHeader.classList.add('expanded');
          chapterHeader.classList.add('current-chapter');
          
          // Save state
          saveSubmenuState(chapterNum, true);
        }
      }
    } else {
      // Restore saved states from localStorage
      restoreSubmenuStates();
    }
  }

  function saveSubmenuState(chapterNum, isOpen) {
    try {
      const states = getSubmenuStates();
      states[chapterNum] = isOpen;
      localStorage.setItem('sidebar-submenu-states', JSON.stringify(states));
    } catch (e) {
      // localStorage might not be available
      console.warn('Could not save submenu state:', e);
    }
  }

  function getSubmenuStates() {
    try {
      const saved = localStorage.getItem('sidebar-submenu-states');
      return saved ? JSON.parse(saved) : {};
    } catch (e) {
      return {};
    }
  }

  function restoreSubmenuStates() {
    const states = getSubmenuStates();
    
    Object.keys(states).forEach(function(chapterNum) {
      if (states[chapterNum]) {
        const submenu = document.getElementById('submenu-' + chapterNum);
        const header = document.querySelector('[data-chapter="' + chapterNum + '"]');
        
        if (submenu && header) {
          submenu.classList.add('open');
          header.classList.add('expanded');
        }
      }
    });
  }

  function addKeyboardNavigation(headers) {
    headers.forEach(function(header) {
      // Make it focusable
      header.setAttribute('tabindex', '0');
      
      // Handle keyboard events
      header.addEventListener('keydown', function(e) {
        // Enter or Space to toggle
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          toggleSubmenu(header);
        }
        
        // Arrow keys for navigation
        if (e.key === 'ArrowRight') {
          // Open submenu
          const chapterNum = header.getAttribute('data-chapter');
          const submenu = document.getElementById('submenu-' + chapterNum);
          if (submenu && !submenu.classList.contains('open')) {
            toggleSubmenu(header);
          }
        }
        
        if (e.key === 'ArrowLeft') {
          // Close submenu
          const chapterNum = header.getAttribute('data-chapter');
          const submenu = document.getElementById('submenu-' + chapterNum);
          if (submenu && submenu.classList.contains('open')) {
            toggleSubmenu(header);
          }
        }
      });
    });
  }

  // Add collapse all / expand all functionality
  function addCollapseExpandAll() {
    const sidebar = document.querySelector('.sidebar-nav');
    if (!sidebar) return;

    // Create buttons container
    const buttonsDiv = document.createElement('div');
    buttonsDiv.className = 'submenu-controls';
    buttonsDiv.style.cssText = 'padding: 0.5rem 0; margin: 0.5rem 0; border-top: 1px solid #e5e5e5;';

    // Expand all button
    const expandBtn = document.createElement('button');
    expandBtn.textContent = 'Expand All';
    expandBtn.className = 'submenu-control-btn';
    expandBtn.onclick = function() {
      document.querySelectorAll('.sidebar-lessons-submenu').forEach(function(submenu) {
        submenu.classList.add('open');
      });
      document.querySelectorAll('.sidebar-chapter-header').forEach(function(header) {
        header.classList.add('expanded');
      });
    };

    // Collapse all button
    const collapseBtn = document.createElement('button');
    collapseBtn.textContent = 'Collapse All';
    collapseBtn.className = 'submenu-control-btn';
    collapseBtn.onclick = function() {
      document.querySelectorAll('.sidebar-lessons-submenu').forEach(function(submenu) {
        submenu.classList.remove('open');
      });
      document.querySelectorAll('.sidebar-chapter-header').forEach(function(header) {
        header.classList.remove('expanded');
      });
    };

    buttonsDiv.appendChild(expandBtn);
    buttonsDiv.appendChild(collapseBtn);

    // Insert before version info
    const versionSpan = sidebar.querySelector('span.sidebar-nav-item');
    if (versionSpan) {
      sidebar.insertBefore(buttonsDiv, versionSpan);
    }
  }

  // Optional: Add collapse/expand all buttons
  // Uncomment if you want this feature
  // document.addEventListener('DOMContentLoaded', addCollapseExpandAll);

})();
