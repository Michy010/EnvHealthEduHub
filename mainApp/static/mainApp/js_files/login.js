// Google Sign In Simulation
const googleSignIn = document.getElementById('googleSignIn');
googleSignIn.addEventListener('click', function() {
    this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Redirecting to Google...';
    this.disabled = true;
    
    // Simulate Google authentication process
    setTimeout(() => {
        window.location.href = `http://127.0.0.1:8000/accounts/google/login`
        this.innerHTML = '<i class="fab fa-google"></i> Sign in with Google';
        this.disabled = false;
    }, 1500);
});

// Password visibility toggle
const togglePassword = document.getElementById('togglePassword');
const passwordInput = document.getElementById('password');

togglePassword.addEventListener('click', function () {
    const type = passwordInput.type === 'password' ? 'text' : 'password';
    passwordInput.type = type;
    this.innerHTML = type === 'password'
        ? '<i class="far fa-eye"></i>'
        : '<i class="far fa-eye-slash"></i>';
});

// ===== LOGIN FORM =====
const form = document.getElementById('signInForm');
const messageBlock = document.getElementById('error-block');
const rememberMe = document.getElementById('rememberMe');
const emailInput = document.getElementById('email');

function getCsrfToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith('csrftoken=')) {
            return cookie.split('=')[1];
        }
    }
    return null;
}

// Load remembered email
window.addEventListener('load', () => {
    const savedEmail = localStorage.getItem('envhealth_email');
    if (savedEmail) {
        emailInput.value = savedEmail;
        rememberMe.checked = true;
    }
});

form.addEventListener('submit', function (e) {
    e.preventDefault();

    const formData = new FormData(form);

    fetch('/registretion/login/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCsrfToken(),
        },
        body: formData,
    })
    .then(res => res.json())
    .then(data => {
        messageBlock.style.display = 'flex';
        messageBlock.innerHTML = data.message;

        if (data.success) {
            messageBlock.style.color = 'green';

            // Remember email
            if (rememberMe.checked) {
                localStorage.setItem('envhealth_email', emailInput.value);
            } else {
                localStorage.removeItem('envhealth_email');
            }

            setTimeout(() => {
                window.location.href = '/';
            }, 2000);
        } else {
            messageBlock.style.color = 'red';
        }
    })
    .catch(() => {
        messageBlock.style.display = 'flex';
        messageBlock.style.color = 'red';
        messageBlock.innerHTML = 'Server error. Try again.';
    });
});
