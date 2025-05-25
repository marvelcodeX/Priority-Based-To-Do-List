document.addEventListener('DOMContentLoaded', () => {
  // Confirm before deleting
  document.querySelectorAll('.delete-task').forEach(link => {
    link.addEventListener('click', (e) => {
      if (!confirm('Are you sure you want to delete this task?')) {
        e.preventDefault();
      }
    });
  });

  // Confirm before toggling task completion
  document.querySelectorAll('.toggle-complete').forEach(link => {
    link.addEventListener('click', (e) => {
      const icon = link.textContent.trim();
      const isCompleting = icon === '✔️';
      const message = isCompleting
        ? 'Are you sure you want to mark this task as complete?'
        : 'Are you sure you want to mark this task as incomplete?';
      if (!confirm(message)) {
        e.preventDefault();
      }
    });
  });

  // Dismiss reminder banner with fade out
  const dismissButton = document.querySelector('.dismiss-reminder');
  if (dismissButton) {
    dismissButton.addEventListener('click', () => {
      const banner = document.querySelector('.reminder-banner');
      if (banner) {
        banner.classList.add('hide');
        banner.addEventListener('animationend', () => banner.remove());
      }
    });
  }

  // Apply saved theme preference or system default
  const currentTheme = localStorage.getItem('theme');
  if (currentTheme === 'dark') {
    document.body.classList.add('dark-mode');
  } else if (currentTheme === 'light') {
    document.body.classList.remove('dark-mode');
  } else {
    // No preference saved, check system preference
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      document.body.classList.add('dark-mode');
    }
  }

  // Theme toggle button
  const themeToggleBtn = document.getElementById('theme-toggle-btn');
  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const isDark = document.body.classList.toggle('dark-mode');
      if (isDark) {
        localStorage.setItem('theme', 'dark');
      } else {
        localStorage.setItem('theme', 'light');
      }
    });
  }
});
