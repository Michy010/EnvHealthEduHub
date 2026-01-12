
// Password visibility toggle
const toggleRegPassword = document.getElementById('toggleRegPassword');
const regPasswordInput = document.getElementById('regPassword');
const toggleConfirmPassword = document.getElementById('toggleConfirmPassword');
const confirmPasswordInput = document.getElementById('confirmPassword');

toggleRegPassword.addEventListener('click', function() {
    const type = regPasswordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    regPasswordInput.setAttribute('type', type);
    this.innerHTML = type === 'password' ? '<i class="far fa-eye"></i>' : '<i class="far fa-eye-slash"></i>';
});

toggleConfirmPassword.addEventListener('click', function() {
    const type = confirmPasswordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    confirmPasswordInput.setAttribute('type', type);
    this.innerHTML = type === 'password' ? '<i class="far fa-eye"></i>' : '<i class="far fa-eye-slash"></i>';
});

// Password strength checker
regPasswordInput.addEventListener('input', function() {
    const password = this.value;
    const strengthFill = document.getElementById('strengthFill');
    const strengthText = document.getElementById('strengthText');
    
    let strength = 0;
    let text = 'Weak';
    
    if (password.length >= 8) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;
    
    // Update strength indicator
    strengthFill.className = 'strength-fill';
    
    if (password.length === 0) {
        strengthFill.style.width = '0';
        strengthText.textContent = 'None';
    } else if (strength <= 1) {
        strengthFill.classList.add('weak');
        strengthText.textContent = 'Weak';
    } else if (strength <= 3) {
        strengthFill.classList.add('medium');
        strengthText.textContent = 'Medium';
    } else {
        strengthFill.classList.add('strong');
        strengthText.textContent = 'Strong';
    }
    
    // Check password match
    checkPasswordMatch();
});

// Password confirmation check
confirmPasswordInput.addEventListener('input', checkPasswordMatch);

function checkPasswordMatch() {
    const password = regPasswordInput.value;
    const confirmPassword = confirmPasswordInput.value;
    const matchIndicator = document.getElementById('passwordMatch');
    
    if (confirmPassword.length === 0) {
        matchIndicator.style.display = 'none';
        return;
    }
    
    matchIndicator.style.display = 'block';
    
    if (password === confirmPassword) {
        matchIndicator.innerHTML = '<i class="fas fa-check-circle" style="color: #28a745;"></i> Passwords match';
        matchIndicator.style.color = '#28a745';
    } else {
        matchIndicator.innerHTML = '<i class="fas fa-times-circle" style="color: #dc3545;"></i> Passwords do not match';
        matchIndicator.style.color = '#dc3545';
    }
}

// Google Registration Simulation
const googleRegister = document.getElementById('googleRegister');
googleRegister.addEventListener('click', function() {
    this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Connecting to Google...';
    this.disabled = true;
    
    // Simulate Google authentication process
    setTimeout(() => {
        window.location.href = `http://127.0.0.1:8000/accounts/google/login`
        this.innerHTML = '<i class="fab fa-google"></i> Sign up with Google';
        this.disabled = false;
    }, 1500);
});

// Form submission
// const registerForm = document.getElementById('registerForm');
// registerForm.addEventListener('submit', function(e) {
//     e.preventDefault();
    
//     const firstName = document.getElementById('first_name').value;
//     const lastName = document.getElementById('last_name').value;
//     const email = document.getElementById('email').value;
//     const password = document.getElementById('password').value;
//     const confirmPassword = document.getElementById('confirmPassword').value;
//     const educationLevel = document.getElementById('educationLevel').value;
//     const agreeTerms = document.getElementById('agreeTerms').checked;
    
//     const submitBtn = this.querySelector('.btn-submit');
//     const originalContent = submitBtn.innerHTML;
    
    // Validation
    // if (!firstName || !lastName || !email || !password || !confirmPassword || !educationLevel) {
    //     alert('Please fill in all required fields.');
    //     return;
    // }
    
    // if (password !== confirmPassword) {
    //     alert('Passwords do not match. Please check and try again.');
    //     return;
    // }
    
    // if (password.length < 8) {
    //     alert('Password must be at least 8 characters long.');
    //     return;
    // }
    
    // if (!agreeTerms) {
    //     alert('You must agree to the Terms of Service and Privacy Policy.');
    //     return;
    // }
    
    // Show loading state
    // submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating Account...';
    // submitBtn.disabled = true;
    
    // Simulate API call
    // setTimeout(() => {
        // Simulate successful registration
        // alert(`Welcome ${firstName} ${lastName}! Your account has been created successfully. Check your email to verify your account.`);
        
        // In real app: window.location.href = 'dashboard.html';
        
        // Reset form
        // registerForm.reset();
        // document.getElementById('strengthFill').style.width = '0';
        // document.getElementById('strengthText').textContent = 'Weak';
        // document.getElementById('passwordMatch').style.display = 'none';
        
        // Reset button
//         submitBtn.innerHTML = originalContent;
//         submitBtn.disabled = false;
//     }, 2000);
// });

const form = document.getElementById('registerForm');

function getCsrfToken() {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith('csrftoken=')) {
            return cookie.split('=')[1];
        }
    }
    return null;
}

form.addEventListener('submit', (e) => {
    e.preventDefault();

    const formData = new FormData(form);

    fetch('/registretion/register/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCsrfToken(),
        },
        body: formData
    })
    .then(res => res.json())
    .then(results => {
        const errorBlock = document.getElementById('error-block');
        if(results.success) {
            errorBlock.innerHTML = `${results.message}`;
            errorBlock.style.display = 'flex';
            errorBlock.style.color = 'green'

            setTimeout(() => {
                window.location.href = `http://127.0.0.1:8000/registretion/login/`;
            }, 2000);
        }else{
            errorBlock.innerHTML = `${results.message}`;
            errorBlock.style.display = 'flex';
        }
    })
    .catch(err => {
        const errorBlock = document.getElementById('error-block');
        errorBlock.innerHTML = `<p>${err}</p>`;
        errorBlock.style.display = 'flex';

    });
});

// Auto-focus first input
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('firstName').focus();
});
