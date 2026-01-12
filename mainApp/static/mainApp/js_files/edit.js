function getCsrfToken () {
    const cookies = document.cookie.split(';')
    for(let i = 0; i < cookies.length; i++) {
       if (cookies[i].trim().startsWith('csrftoken=')) {
        return cookies[i].split('=')[1];
       } 
    }
    return null;
}

const editSubmit = document.getElementById('edit-button');
editSubmit.addEventListener ('click', (e) => {
    e.preventDefault();

    let FirstName = document.getElementById('first_name').value;
    let LastName = document.getElementById('last_name').value;
    let email = document.getElementById('personal-email').value;
    let userId = document.getElementById('userId').value;

    let formData = {
        'first_name': FirstName,
        'last_name': LastName,
        'email': email,
        'userId': userId
    }

    fetch(`/registretion/edit/${userId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCsrfToken(),
            'Content-Type': 'Application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(res => res.json())
    .then(data => {
        let messageBlock = document.getElementById('messageBlock');
        messageBlock.innerHTML = `${data.message}`
    })
    .catch(err => {
        console.log(err.error)
    })
});