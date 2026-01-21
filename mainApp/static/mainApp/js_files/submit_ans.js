// Updated submit_ans.js with proper URL and JSON handling
document.addEventListener('DOMContentLoaded', function() {
    // Function to toggle reply forms
    window.toggleReplyForm = function(formId) {
        const form = document.getElementById(formId);
        if (form) {
            form.style.display = form.style.display === 'none' ? 'block' : 'none';
            if (form.style.display === 'block') {
                const textarea = form.querySelector('textarea');
                if (textarea) textarea.focus();
            }
        }
    };
    
    // Add event listeners to all reply submit buttons
    document.querySelectorAll('.reply-form .btn-primary, .nested-reply-form .btn-primary').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const replyForm = this.closest('.reply-form, .nested-reply-form');
            const textarea = replyForm.querySelector('textarea');
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            // Get question ID and parent ID from data attributes
            const questionId = textarea.dataset.questionId || 
                              replyForm.querySelector('input[type="hidden"]')?.value;
            const parentId = textarea.dataset.answerId || 
                           replyForm.querySelector('[name="parent_id"]')?.value || 
                           replyForm.querySelector('[name="answerID"]')?.value;
            
            if (!textarea) {
                console.error('Textarea not found');
                return;
            }
            
            const reply = textarea.value.trim();
            
            if (!reply) {
                alert('Please write an answer before submitting.');
                return;
            }
            
            if (!questionId) {
                console.error('Question ID not found');
                return;
            }
            
            // Submit the answer
            const formData = new FormData();
            formData.append('reply', reply);
            formData.append('question', questionId);
            formData.append('csrfmiddlewaretoken', csrfToken);
            
            if (parentId) {
                formData.append('parent_id', parentId);
            }
            
            // IMPORTANT: Use the correct URL - check your urls.py
            fetch('/reply_qn/', {  // Changed from '/reply-question/'
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                console.log('Success:', data);
                if (data.success) {
                    // Clear textarea and hide form
                    textarea.value = '';
                    if (replyForm.id.includes('nestedReplyForm')) {
                        toggleReplyForm(replyForm.id);
                    } else if (replyForm.id.includes('replyForm')) {
                        toggleReplyForm(replyForm.id);
                    }
                    // Reload to show new reply
                    setTimeout(() => {
                        window.location.reload();
                    }, 500);
                } else {
                    alert(data.message || 'Error submitting reply.');
                }
            })
            .catch(err => {
                console.error('Error:', err);
                alert('An error occurred. Please try again.');
            });
        });
    });
    
    // Add event listener for Enter key in textareas
    document.querySelectorAll('.reply-form textarea, .nested-reply-form textarea').forEach(textarea => {
        textarea.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && e.ctrlKey) {
                e.preventDefault();
                const submitBtn = this.closest('.reply-form, .nested-reply-form').querySelector('.btn-primary');
                if (submitBtn) {
                    submitBtn.click();
                }
            }
        });
    });
    
    // Rate answer functionality
    window.rateAnswer = function(answerId, type) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        fetch('/rate-answer/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                answer_id: answerId,
                type: type
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update vote counts
                const upvoteSpan = document.getElementById(`upvotes-${answerId}`);
                const downvoteSpan = document.getElementById(`downvotes-${answerId}`);
                
                if (upvoteSpan && data.upvotes !== undefined) {
                    upvoteSpan.textContent = data.upvotes;
                }
                if (downvoteSpan && data.downvotes !== undefined) {
                    downvoteSpan.textContent = data.downvotes;
                }
                
                // Update button styles based on user's vote
                updateVoteButtonStyles(answerId, data.user_vote);
                
            } else {
                alert(data.message || 'Error rating answer.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    };
    
    // Update vote button styles based on user's vote
    function updateVoteButtonStyles(answerId, userVote) {
        const answerElement = document.getElementById(`answer-${answerId}`);
        if (!answerElement) return;
        
        const upvoteBtn = answerElement.querySelector('.action-btn:nth-child(1)');
        const downvoteBtn = answerElement.querySelector('.action-btn:nth-child(2)');
        
        // Reset all buttons
        if (upvoteBtn) {
            upvoteBtn.classList.remove('active', 'upvote');
            upvoteBtn.style.color = '';
            upvoteBtn.style.borderColor = '';
        }
        if (downvoteBtn) {
            downvoteBtn.classList.remove('active', 'downvote');
            downvoteBtn.style.color = '';
            downvoteBtn.style.borderColor = '';
        }
        
        // Set active state based on user's vote
        if (userVote === 'up' && upvoteBtn) {
            upvoteBtn.classList.add('active', 'upvote');
            upvoteBtn.style.color = 'var(--success-color)';
            upvoteBtn.style.borderColor = 'var(--success-color)';
        } else if (userVote === 'down' && downvoteBtn) {
            downvoteBtn.classList.add('active', 'downvote');
            downvoteBtn.style.color = 'var(--danger-color)';
            downvoteBtn.style.borderColor = 'var(--danger-color)';
        }
    }
});