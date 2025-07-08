// Add any custom JavaScript functionality here
document.addEventListener('DOMContentLoaded', function() {
    // Example: Add confirmation before deleting an employee
    const deleteButtons = document.querySelectorAll('.delete-employee');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this employee?')) {
                e.preventDefault();
            }
        });
    });
});