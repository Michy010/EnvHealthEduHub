// Mobile navigation toggle
const mobileToggle = document.getElementById('mobileToggle');
const navLinks = document.querySelector('.nav-links');
const body = document.body;

mobileToggle.addEventListener('click', () => {
    navLinks.classList.toggle('active');
    body.classList.toggle('nav-active');
    
    // Change icon
    const icon = mobileToggle.querySelector('i');
    if (icon.classList.contains('fa-bars')) {
        icon.classList.remove('fa-bars');
        icon.classList.add('fa-times');
    } else {
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
    }
});
        
// Ask Question Functionality
const quickAskBtn = document.getElementById('quickAskBtn');
const heroAskBtn = document.getElementById('heroAskBtn');
const newQuestionBtn = document.getElementById('newQuestionBtn');
const askQuestionModal = document.getElementById('askQuestionModal');
const closeAskModal = document.getElementById('closeAskModal');
const cancelQuestionBtn = document.getElementById('cancelQuestionBtn');

function openAskQuestionModal() {
    askQuestionModal.classList.add('active');
    body.style.overflow = 'hidden';
}

function closeAskQuestionModal() {
    askQuestionModal.classList.remove('active');
    body.style.overflow = 'auto';
}
        
quickAskBtn.addEventListener('click', openAskQuestionModal);
heroAskBtn.addEventListener('click', openAskQuestionModal);
newQuestionBtn.addEventListener('click', openAskQuestionModal);
closeAskModal.addEventListener('click', closeAskQuestionModal);
cancelQuestionBtn.addEventListener('click', closeAskQuestionModal);
        
// Submit Question
const submitQuestionBtn = document.getElementById('submitQuestionBtn');
submitQuestionBtn.addEventListener('click', function() {
const title = document.getElementById('questionTitle').value;
const category = document.getElementById('questionCategory').value;
const details = document.getElementById('questionDetails').value;

if (!title || !category || !details) {
    alert('Please fill in all required fields');
    return;
}

alert(`Your question "${title}" has been posted successfully!`);
closeAskQuestionModal();
            
// Reset form
document.getElementById('questionTitle').value = '';
document.getElementById('questionCategory').value = '';
document.getElementById('questionDetails').value = '';
document.getElementById('questionTags').value = '';
});
        
// Publish Work Functionality
const quickPublishBtn = document.getElementById('quickPublishBtn');
const heroPublishBtn = document.getElementById('heroPublishBtn');
const publishWorkBtn = document.getElementById('publishWorkBtn');
const saveDraftBtn = document.getElementById('saveDraftBtn');

quickPublishBtn.addEventListener('click', function() {
    document.getElementById('publish').scrollIntoView({ behavior: 'smooth' });
});

heroPublishBtn.addEventListener('click', function() {
    document.getElementById('publish').scrollIntoView({ behavior: 'smooth' });
});

publishWorkBtn.addEventListener('click', function() {
    const title = document.getElementById('workTitle').value;
    const workType = document.getElementById('workType').value;
    const educationLevel = document.getElementById('educationLevel').value;
    const abstract = document.getElementById('workAbstract').value;
    
    if (!title || !workType || !educationLevel || !abstract) {
        alert('Please fill in all required fields marked with *');
        return;
    }
    
    if (abstract.length < 150) {
        alert('Abstract must be at least 150 characters long');
        return;
    }
    
    alert(`Your work "${title}" has been published successfully! It is now available to the community.`);
    
    // Reset form
    document.getElementById('workTitle').value = '';
    document.getElementById('workType').value = '';
    document.getElementById('educationLevel').value = '';
    document.getElementById('workAbstract').value = '';
    document.getElementById('workKeywords').value = '';
    document.getElementById('workFile').value = '';
});

saveDraftBtn.addEventListener('click', function() {
    const title = document.getElementById('workTitle').value;
    
    if (!title) {
        alert('Please at least enter a title to save as draft');
        return;
    }
    
    alert(`Your work "${title}" has been saved as draft. You can continue editing later.`);
});
        
// Answer Rating System
function rateAnswer(button, type) {
    const icon = button.querySelector('i');
    const countSpan = button.querySelector('span');
    let count = parseInt(countSpan.textContent);
    
    // Check if already liked/disliked
    const isLiked = button.classList.contains('liked');
    const isDisliked = button.classList.contains('disliked');
    
    if (type === 'up') {
        if (!isLiked) {
            // Remove any existing dislike from sibling
            const siblingBtn = button.parentElement.querySelector('.action-btn.disliked');
            if (siblingBtn) {
                siblingBtn.classList.remove('disliked');
                const siblingIcon = siblingBtn.querySelector('i');
                const siblingCount = siblingBtn.querySelector('span');
                siblingCount.textContent = parseInt(siblingCount.textContent) - 1;
                siblingIcon.classList.remove('fas');
                siblingIcon.classList.add('far');
            }
            
            // Add like
            button.classList.add('liked');
            button.classList.remove('disliked');
            icon.classList.remove('far');
            icon.classList.add('fas');
            countSpan.textContent = count + 1;
            
            // Show feedback
            showToast('Thanks for liking this answer!', 'success');
        } else {
            // Remove like
            button.classList.remove('liked');
            icon.classList.remove('fas');
            icon.classList.add('far');
            countSpan.textContent = count - 1;
        }
    } else if (type === 'down') {
        if (!isDisliked) {
            // Remove any existing like from sibling
            const siblingBtn = button.parentElement.querySelector('.action-btn.liked');
            if (siblingBtn) {
                siblingBtn.classList.remove('liked');
                const siblingIcon = siblingBtn.querySelector('i');
                const siblingCount = siblingBtn.querySelector('span');
                siblingCount.textContent = parseInt(siblingCount.textContent) - 1;
                siblingIcon.classList.remove('fas');
                siblingIcon.classList.add('far');
            }
            
            // Add dislike
            button.classList.add('disliked');
            button.classList.remove('liked');
            icon.classList.remove('far');
            icon.classList.add('fas');
            countSpan.textContent = count + 1;
            
            // Show feedback
            showToast('You have disliked this answer', 'info');
        } else {
            // Remove dislike
            button.classList.remove('disliked');
            icon.classList.remove('fas');
            icon.classList.add('far');
            countSpan.textContent = count - 1;
        }
    }
}

// Reply form toggle
function toggleReplyForm(formId) {
    const form = document.getElementById(formId);
    if (form.style.display === 'block') {
        form.style.display = 'none';
    } else {
        form.style.display = 'block';
    }
}

// Load more answers simulation
function loadMoreAnswers() {
    showToast('Loading more answers...', 'info');
    setTimeout(() => {
        showToast('More answers loaded successfully!', 'success');
    }, 1000);
}

// Mark all notifications as read
const markAllReadBtn = document.getElementById('markAllReadBtn');
const notificationBadge = document.querySelector('.notification-badge');

markAllReadBtn.addEventListener('click', function(e) {
    e.preventDefault();
    
    // Remove unread class from all notifications
    const unreadNotifications = document.querySelectorAll('.notification-item.unread');
    unreadNotifications.forEach(notification => {
        notification.classList.remove('unread');
    });
    
    // Update notification badge
    notificationBadge.textContent = '0';
    notificationBadge.style.display = 'none';
    
    showToast('All notifications marked as read', 'success');
});

// Level progress animation
function animateLevelProgress() {
    const progressBar = document.getElementById('levelProgress');
    progressBar.style.width = '75%';
}

// Toast notification function
function showToast(message, type) {
    // Create toast element
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background-color: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#17a2b8'};
        color: white;
        border-radius: (--border-radius);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        z-index: 3000;
        transform: translateX(100%);
        opacity: 0;
        transition: all 0.3s ease;
        max-width: 300px;
        `;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    // Animate in
    setTimeout(() => {
        toast.style.transform = 'translateX(0)';
        toast.style.opacity = '1';
    }, 10);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.style.transform = 'translateX(100%)';
        toast.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Animate level progress on page load
    setTimeout(animateLevelProgress, 500);
    
    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });
    
    // Set active navigation on scroll
    window.addEventListener('scroll', function() {
        const sections = document.querySelectorAll('section[id]');
        const navLinks = document.querySelectorAll('.nav-links a');
        
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (scrollY >= (sectionTop - 100)) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            } else if (current === '' && link.getAttribute('href') === '#') {
                link.classList.add('active');
            }
        });
    });
});

