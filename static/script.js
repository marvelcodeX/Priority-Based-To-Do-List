document.addEventListener('DOMContentLoaded', () => {
  // Confirm before deleting
  document.querySelectorAll('.delete-link').forEach(link => {
    link.addEventListener('click', (e) => {
      if (!confirm('Are you sure you want to delete this task?')) {
        e.preventDefault();
      }
    });
  });

  // Optional: Priority-based styling
  document.querySelectorAll('.task-item').forEach(item => {
    const priority = item.getAttribute('data-priority');
    if (priority === 'High') {
      item.style.borderLeft = '6px solid red';
    } else if (priority === 'Medium') {
      item.style.borderLeft = '6px solid orange';
    } else {
      item.style.borderLeft = '6px solid green';
    }
  });
});