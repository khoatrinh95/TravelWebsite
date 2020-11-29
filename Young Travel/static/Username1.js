function username1() {
    const reg = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{5,}$/;
    const username = document.getElementById("username").value;
    if (!reg.test(username)) {
        alert("Username must contain at least 5 characters and a number and no special character")
    }
}

function comment1(){
    const reg = /[a-zA-Z0-9]{3,}/;
    const comment = document.getElementById("comment").value;
    if (!reg.test(comment)) {
        alert("Comment must contain at least 3 characters")
    }
}