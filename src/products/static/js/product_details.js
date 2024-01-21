document.querySelector('#links-button').addEventListener('click', event=>{
    const linksButton = document.querySelector('#button-list')
    for(let i of linksButton.children){
        if(i.classList.contains('bg-warning')){
            i.classList.remove('bg-warning')
        }        
    }
    const linksMenu = document.querySelector('#links-menu')
    linksMenu.classList.remove('d-none')
    const similarMenu = document.querySelector('#similar-menu')
    const CommentMenu = document.querySelector('#comment-menu')
    const menuArray = [similarMenu,CommentMenu]
    for(let i of menuArray){
        if(!i.classList.contains('d-none')){
            i.classList.add('d-none')
        }
    }
    linksButton.querySelector('#links-button').classList.add('bg-warning')
})

document.querySelector('#similar-button').addEventListener('click', event=>{
    const ButtonList = document.querySelector('#button-list')
    const similarMenu = document.querySelector('#similar-menu')
    similarMenu.classList.remove('d-none')
    const linksMenu = document.querySelector('#links-menu')
    const CommentMenu = document.querySelector('#comment-menu')
    const menuArray = [linksMenu,CommentMenu]
    for(let i of menuArray){
        if(!i.classList.contains('d-none')){
            i.classList.add('d-none')
        }
    }
    ButtonList.querySelector('#links-button').classList.add('bg-warning')
    for(let i of ButtonList.children){
        if(i.classList.contains('bg-warning')){
            console.log(i.classList)
            i.classList.remove("bg-warning")
        }
        if(i.id.includes('similar-button')){
        console.log(i.id)
        i.classList.add('bg-warning')
        } 
    }
})

document.querySelector('#comment-button').addEventListener('click', event=>{
    const ButtonList = document.querySelector('#button-list')
    const similarMenu = document.querySelector('#comment-menu')
    similarMenu.classList.remove('d-none')
    const linksMenu = document.querySelector('#links-menu')
    const SimilarMenu = document.querySelector('#similar-menu')
    const menuArray = [linksMenu, SimilarMenu]
    for(let i of menuArray){
        if(!i.classList.contains('d-none')){
            i.classList.add('d-none')
        }
    }
    ButtonList.querySelector('#links-button').classList.add('bg-warning')
    for(let i of ButtonList.children){
        if(i.classList.contains('bg-warning')){
            console.log(i.classList)
            i.classList.remove("bg-warning")
        }
        if(i.id.includes('comment-button')){
        console.log(i.id)
        i.classList.add('bg-warning')
        } 
    }
})



// let border = document.querySelector('#image-border')
// setInterval(()=>{
//     if(border.classList.contains('border-warning')){
//         border.classList.remove('border-warning')
//         border.classList.add('border-primary')
//     }else{
//         border.classList.add('border-warning')
//         border.classList.remove('border-primary')
//     }
// }, 3000)