try{

    document.querySelector('#showpassword').addEventListener('click', input=>{
        
        var tag = document.querySelector('[name=password]')
        if(tag.type == 'text'){
            tag.type = 'password'
        }else{
            tag.type = 'text'
        }
        input.preventDefault()
    })
    function modalClose(){
        const tag = document.querySelector('#modal')
        if(!tag.classList.contains('d-none')){
            tag.classList.add('d-none')
        }
    }
}catch{}
