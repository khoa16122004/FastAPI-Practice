function take_all_database(event) {
    event.preventDefault();

    // call api
    fetch('http://127.0.0.1:8001/authent', {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('API Response:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


// Sign up
function signup(event) {
    event.preventDefault();
    // Get input value
    var username = document.getElementById("username").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var first_name = document.getElementById("first_name").value;
    var last_name = document.getElementById("last_name").value;

    var Data_request = {
        username: username,
        email: email,
        password: password,
        first_name: first_name,
        last_name: last_name
    };
// gửi request url
    fetch('http://127.0.0.1:8001/auth', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(Data_request)
        })
        .then(response => response.json())
        .then(data => {
            console.log('API Response:', data);
            // Boostrap rasise popups
            $('#successModal').modal('show');

            // Redirect to login page after a delay (e.g., 2000 milliseconds or 2 seconds)
            setTimeout(function () {
                window.location.href = 'login.html'; // Replace 'path_to_login_page' with the actual path
            }, 2000);
        })
        .catch(error => {
            // Boostrap rasise popups
            console.error('Error:', error);
            $('#errorModal').modal('show');
        });
}

// Login
function login(event) {
    event.preventDefault();
    
    var formData = new FormData();
    formData.append("username", document.getElementById("username").value);
    formData.append("password", document.getElementById("password").value);

    fetch('http://127.0.0.1:8001/token', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Invalid credentials');
            }
            return response.json();
        })
        .then(data => {
            console.log('API Response:', data);
            // Boostrap rasise popups
            $('#successModal').modal('show');

            // setTimeout(function () {
            //     window.location.href = 'login.html'; 
            // }, 2000);
        })
        .catch(error => {
            // Boostrap rasise popups
            console.error('Error:', error.message);
            $('#errorModal').modal('show');
        });
}

