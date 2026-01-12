// Add this to your submit_ans.js file
document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners to all reply submit buttons
    document.querySelectorAll('.reply-form .btn-primary').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const replyForm = this.closest('.reply-form');
            const textarea = replyForm.querySelector('textarea');
            const hiddenInput = replyForm.querySelector('input[type="hidden"]');
            const parentID = replyForm.querySelector('[name=answerID]');
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            if (!textarea || !hiddenInput) {
                console.error('Form elements not found');
                return;
            }
            
            const reply = textarea.value.trim();
            const questionId = hiddenInput.value;
            const parent_id = parentID.value;

            
            if (!reply) {
                alert('Please write an answer before submitting.');
                return;
            }
            
            // Submit the answer
            const formData = new FormData();
            formData.append('reply', reply);
            formData.append('question', questionId);
            formData.append('csrfmiddlewaretoken', csrfToken);
            formData.append('parent_id', parent_id);
            
            fetch('reply_qn/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                    console.log('Success:', data);
                    window.location.reload();
                })
            .catch(err => {
                console.error('Error:', err);
            });
        });
    });
    
    // Function to toggle reply forms
    window.toggleReplyForm = function(formId) {
        const form = document.getElementById(formId);
        if (form) {
            form.style.display = form.style.display === 'none' ? 'block' : 'none';
        }
    };
});