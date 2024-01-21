try{
    document.querySelector('#dropdown-button').addEventListener('click', event=>{
        const tag = document.querySelector('#dropdown-menu')
        if(tag.classList.contains('d-none')){
            tag.classList.remove('d-none')
            tag.style.position = 'fixed'
            tag.style.left = 0
            tag.style.right = 0
            tag.style.top = '95px'
        }else{
            tag.classList.add('d-none')
        }
    })
}catch{}
function dropdown(){
    const navBtn = document.querySelector('#modal')
    const tag = document.querySelector('#dropdown-menu').cloneNode(true)
    if(navBtn.children.length == 1){
        tag.classList.remove('d-none')
        tag.classList.add('h-100')
        navBtn.appendChild(tag)
        navBtn.classList.remove('d-none')
        navBtn.classList.add('bg-dark')
        navBtn.style.height = '100vh'
        navBtn.style.position = 'fixed'
        navBtn.style.zIndex = 999;
    }else{
        tag.classList.add('d-none')
        navBtn.classList.add('d-none')
        const modalChild = navBtn.children[1]
        navBtn.removeChild(modalChild)
    }
}

function searchDropDown(){
    const navBtn = document.querySelector('#modal')
    const tag = document.querySelector('#searchform').cloneNode(true)
    if(navBtn.children.length == 1){
        tag.classList.remove('d-none')
        tag.classList.add('w-50','m-auto', 'text-center')
        navBtn.appendChild(tag)
        navBtn.classList.remove('d-none')
        navBtn.classList.add('bg-dark')
        navBtn.style.height = '100vh'
        navBtn.style.position = 'fixed'
        navBtn.style.zIndex = 999;
    }else{
        tag.classList.add('d-none')
        navBtn.classList.add('d-none')
        const modalChild = navBtn.children[1]
        navBtn.removeChild(modalChild)
    }
}

addEventListener("resize", (event) => {
    if(innerWidth < 768){
        let modal = document.querySelector('#modal')
        console.log(modal)
        if(!modal.classList.contains('d-none')){
            modal.classList.add('d-none')
            // document.querySelector('#dropdown-menu').classList.add('d-none')
        }
    }else if(innerWidth > 768){
        let dropdown = document.querySelector('#dropdown-menu')
        if(!dropdown.classList.contains('d-none')){
            dropdown.classList.add('d-none')
        }
    }     
    
});