document.addEventListener('DOMContentLoaded', function() {
    // Add loading state to display buttons when clicked
    const displayButtons = document.querySelectorAll('.small-btn');
    displayButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.textContent = 'Displaying...';
            this.disabled = true;
            this.classList.add('loading');
        });
    });
    
    // Show filename when selected in upload form
    const fileInput = document.getElementById('file');
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            var fileName = e.target.files[0].name;
            document.getElementById('file-name').textContent = fileName;
        });
    }
});