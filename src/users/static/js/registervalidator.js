try{

    document.querySelector('[name=username]').addEventListener('input', event=>{
        let password = document.activeElement
        let passwordLength = password.value.length
        if(passwordLength == 0){
            password.classList.remove('is-valid')
        }else{
            password.classList.add('is-valid')
        }
    })
}catch{}

try{

    document.querySelector('[name=email]').addEventListener('input', event=>{
        let password = document.activeElement
        let passwordValue = password.value
        let passwordLength = passwordValue.length
        if(passwordLength == 0){
            password.classList.remove('is-valid')
            password.classList.remove('is-invalid')
        }else if(passwordValue.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')){
            password.classList.remove('is-invalid')
            password.classList.add('is-valid')
        }else if(!passwordValue.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')){
            password.classList.remove('is-valid')
            password.classList.add('is-invalid')
            document.querySelector('[name=email]').querySelector('[class=invalid-feedback]').innerText = 'لطفا یک ایمیل معتبر وارد کنید'
        }
    })
}catch{}


try{

    document.querySelector('[name=password1]').addEventListener('input', event=>{
        let password = document.activeElement
        let passwordLength = password.value.length
        let lowerCasePassword = password.value.toLowerCase()
        let passwordHasNumber = password.value.search('[0-9]{1,}')
        if(passwordLength == 0){
            password.classList.remove('is-invalid')
            password.classList.remove('is-valid')
        }else if(passwordLength < 8 || password.value === lowerCasePassword || !passwordHasNumber < 0){
            password.classList.add('is-invalid')
            password.classList.remove('is-valid')
        }else if(passwordLength >= 8 && password.value !== lowerCasePassword && passwordHasNumber > 0){
            password.classList.remove('is-invalid')
            password.classList.add('is-valid')
        }
    })
}catch{}

try{

    document.querySelector('[name=password2]').addEventListener('input', event=>{
        let password1 = document.querySelector('[name=password1]').value
        let password2 = document.activeElement
        let password2Value = password2.value
        let password2Length = password2Value.length
        if(password2Length == 0){
            password2.classList.remove('is-invalid')
            password2.classList.remove('is-valid')
        }else if(password1 !== password2Value){
            password2.classList.add('is-invalid')
            password2.classList.remove('is-valid')
        }else if(password1 === password2Value){
            password2.classList.remove('is-invalid')
            password2.classList.add('is-valid')
        }
    })
}catch{}