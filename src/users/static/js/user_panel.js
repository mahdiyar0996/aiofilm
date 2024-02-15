function userBar(){
    const modal = document.querySelector('#userModal')
    const tag = document.querySelector('#user-bar').cloneNode(true)
    const container = document.querySelector('#container-content')
    container.style.opacity = 0.3
    document.body.classList.add('overflow-hidden')
    if(modal.children.length == 0){
        tag.classList.remove('d-none')
        tag.style.width = '60%'
        modal.appendChild(tag)
        modal.classList.remove('d-none')
        modal.classList.add('bg-dark')
        modal.style.width = '100vw'
        modal.style.position = 'fixed'
        modal.style.zIndex = 999;
    }else{
        tag.classList.add('d-none')
        modal.classList.add('d-none')
        const modalChild = modal.children[1]
        modal.removeChild(modalChild)
    }
}

try{
    document.querySelector("#userModal").addEventListener('click', event=>{
        try{
            
                const body = document.body
                body.querySelector('#container-content').style.opacity = ''
                console.log(body)
                if(body.classList.contains('overflow-hidden')){
                    body.classList.remove('overflow-hidden')
                    const modal = document.querySelector('#userModal')
                    if(modal.classList.contains('overflow-auto')){
                        const tag = document.querySelector('#user-bar')
                        modal.removeChild(tag)
                        tag.classList.add('d-none')
                        tag.classList.remove('w-100')
                        modal.classList.add('d-none')
                        modal.classList.remove('bg-dark')
                        modal.style.width = '0vw'
                        modal.style.position = ''
                        modal.style.zIndex = '';
                    }
                }
            
        }catch{}
    })
}catch{}

try{

    document.querySelector('#file').addEventListener('change', event=>{
        const tag = event.target
        const parentTag = event.target.parentElement
        let fileText = parentTag.querySelector('p')
        console.log(fileText)
        fileText.innerText = tag.value.split('\\').pop()
        
    })
}catch{}


try{
    document.querySelector('#password1').addEventListener('input', event=>{
        console.log(event)
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
    document.querySelector('#password2').addEventListener('input', event=>{
        let password1 = document.querySelector('#password1').value
        let password2 = event.target
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


try{
    const packageBoxTags = document.querySelectorAll('.package-box-link')
    for(let tag of packageBoxTags){
        tag.addEventListener('click', event=>{
            const tag = event.target
            event.preventDefault()
        })
    }
}catch{}

try{
    const packageTags = document.querySelectorAll('.package-box-bg')
    for(let tag of packageTags){
        tag.addEventListener('click',event=>{
            const tagList = tag.parentElement.children
            for(let tag of tagList){
                if(tag.classList.contains('bg-darkyellow')){
                    tag.classList.remove('bg-darkyellow')
                    tag.classList.add('bg-hover-darkyellow')
                }
            }
            if(tag.classList.contains('bg-hover-darkyellow')){
                tag.classList.remove('bg-hover-darkyellow')
                tag.classList.add('bg-darkyellow')
                const gateway = document.querySelector('#gateways').children
                for(let tag of gateway){
                    if(tag.classList.contains('bg-darkyellow')){
                        const packageList = document.querySelectorAll('.package-box-bg')
                        getPayment(packageList)
                    }
                }
            }
        })
    }
}catch{}


// try{
const GatewayTags = document.querySelectorAll('.gateway-bg')
for(let tag of GatewayTags){
    tag.addEventListener('click',event=>{
        event.preventDefault()
        const tagList = tag.parentElement.children
        for(let tag of tagList){
            if(tag.classList.contains('bg-darkyellow')){
                tag.classList.remove('bg-darkyellow')
                tag.classList.add('bg-hover-darkyellow')
            }
        }
        if(tag.classList.contains('bg-hover-darkyellow')){
            tag.classList.remove('bg-hover-darkyellow')
            tag.classList.add('bg-darkyellow')
            const packageTags = document.querySelectorAll('.package-box-bg')
            getPayment(packageTags)
        }
    })
}
// }catch{}


function getPayment(tagList){
    for(let package of tagList){
        if(package.classList.contains('bg-darkyellow')){
            let packageDays = package.querySelector('#day').innerText
            let packagePrice = package.querySelector('#price').innerText.split(' ')[0].replace(',', '')
            let packageDiscount = package.querySelector('#discount')
            if(packageDiscount){
                packageDiscount = packageDiscount.innerText.split(' ')[0].replace(',', '')
            }else{
                packageDiscount = packagePrice
            }
            let payment = document.querySelector('#payment-details')
            payment.classList.remove('d-none')
            let paymentList = payment.children[0].children
            paymentList[1].innerText = `${packageDays} (${packagePrice} تومان)`
            paymentList[3].innerText = `${packagePrice - packageDiscount} تومان`
            paymentList[5].innerText = `${packageDiscount} تومان`
        }
    }
}


function userModal(){
    userBar = document.querySelector('#user-modal')
    if(userBar.classList.contains('d-none')){
        userBar.classList.remove('d-none')
    }
    else{
        userBar.classList.add('d-none')
    }
}


function userModalClose(){
    userBar = document.querySelector('#user-modal')
    if(userBar.classList.contains('d-none')){
        userBar.classList.remove('d-none')
    }
    else{
        userBar.classList.add('d-none')
    }
}