document.querySelector('.product-box').addEventListener('mouseenter', event=>{
    const tag = event.target
    const productName = tag.querySelector('.product-name-box')
    console.log(productName)
    productName.classList.remove('d-none')
})

document.querySelector('.product-box').addEventListener('mouseleave', event=>{
    const tag = event.target
    const productName = tag.querySelector('.product-name-box')
    console.log(productName)
    productName.classList.add('d-none')
})