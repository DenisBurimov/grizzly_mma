document.addEventListener('DOMContentLoaded', function() {
    let copy_login = document.querySelector('#copy_login');
    let login_input = document.querySelector('#login_input').value;
    let copy_password = document.querySelector('#copy_password');
    let password_input = document.querySelector('#password_input').value;

    copy_login.addEventListener('click', function() {
        navigator.clipboard.writeText(login_input)
        alert(`The login ${login_input} is copied!`)
    });

    copy_password.addEventListener('click', function() {
        navigator.clipboard.writeText(password_input)
        alert(`The password ${password_input} is copied!`)
    });
});