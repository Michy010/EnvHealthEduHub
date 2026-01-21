// submit_ans.js - UPDATED VERSION
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
    
    // Rate answer functionality ONLY
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