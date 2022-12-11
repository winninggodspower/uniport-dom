
const MainDisplayImage = document.querySelector('.room-main-display-image');

document.querySelectorAll('.room-display-image').forEach(image => {
    image.addEventListener('click', (e)=>{
        MainDisplayImage.src = image.src;
    })
});