let form = document.getElementById("login-form")

form.addEventListener('submit', (e) => {
    // When we entered incorrect data, the page will not reload
    e.preventDefault()

    let formData = {
        "username": form.username.value,
        "password": form.password.value     
    }
    
    // POST to API
    fetch('http://127.0.0.1:8000/api/users/token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // Whithout Authorization token, because we 
            // take token from Lokal storage at browser
        },

        // 
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        // data.access get a token 
        console.log("DATA: ", data.access)
        // if true put/save this token into Lokal browser storage 
        if (data.access) {
            localStorage.setItem('token', data.access)
            // Then redirect to 'project-list.html'
            window.location = 'file:///C:/Users/User/Desktop/Django%20Projects/frontend/projects-list.html'
        } else {
            alert("Username OR password did not work")
        }
    })
})