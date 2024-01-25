for(let tag of document.querySelectorAll('.product-box')){
    tag.addEventListener('mouseenter', event=>{
        const tag = event.target
        const productName = tag.querySelector('.product-name-box')
        productName.classList.remove('d-none')
    })
}
// document.querySelector('.product-box').addEventListener('mouseenter', event=>{
//     const tag = event.target
//     const productName = tag.querySelectorALL('.product-name-box')
//     for(let item of productName)
//         tag.classList.remove('d-none')
// })


for(let tag of document.querySelectorAll('.product-box')){
    tag.addEventListener('mouseleave', event=>{
        const tag = event.target
        const productName = tag.querySelector('.product-name-box')
        productName.classList.add('d-none')
    })
}
// document.querySelector('.product-box').addEventListener('mouseleave', event=>{
//     const tag = event.target
//     const productName = tag.querySelectorALL('.product-name-box')
//     for(let item of productName)
//         tag.classList.add('d-none')
// })