function getCsrfToken () {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
        if (cookies[i].trim().startsWith('csrftoken=')) {
            return cookies[i].split('=')[1]
        }
    }
    return null
}

document
.getElementById('submit_QuestionBtn')
.addEventListener('click', (e) => {
    e.preventDefault()

    let questionTitle = document.getElementById('questionTitle').value
    let category = document.getElementById('questionCategory').value
    let questionDetail = document.getElementById('questionDetails').value
    let questionTag = document.getElementById('questionTags').value

    let formData = new FormData()
    formData.append('question_title', questionTitle)
    formData.append('category', category)
    formData.append('question_tags', questionTag)
    formData.append('question', questionDetail)

    fetch('submit_question/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCsrfToken(),
        },
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        window.location.reload()
    })
    .catch(err => {
        console.error(err)
    })
})