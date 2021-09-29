const form =document.getElementById('form');
const username=document.getElementById('Username');
const area=document.getElementById('area');

form.addEventListener('Submit', (e)=>({
    e.preventDefault();
    checkInputs();
})

function checkInputs(){
    const usernameValue = username.value.trim();
    const areaValue = area.value.trim();

    if(usernameValue === ''){
        setErrorFor(username, 'Username cannot be blank');
    } else {
        setSuccessFor(username);
    }
}

function setSuccessFor(input){
    const formControl = input.parentElement;
    formControl.className = 'form-control success';
}