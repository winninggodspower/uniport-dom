// LoggedIn variable gotten from html file
LoggedIn

const likeUrlPath = '/like_apartment';
let likebtns = document.querySelectorAll('[data-likebtn]');

likebtns.forEach((btn)=>{
    btn.addEventListener('click', (e)=>{
        if (LoggedIn) {
            fetch(location.origin.concat(likeUrlPath), {
                method: 'POST',
                body: JSON.stringify({
                    'apartment_id': btn.id,
                })
            }).then((res)=>{
                return res.json();
            }).then((data)=>{
                if (data.liked){
                    updateLIkeBtn(btn, data)
                }else{
                    alert('You already liked apartment')
                }
            })
        }else{
            alert('You are not logged in. Please log in to Like Apartment')
        }
    })
})

// function that updates the frontend if request was successful
const updateLIkeBtn = (btn, data)=>{
    if (data.liked) {
        console.log(data);
        document.getElementById(`like-count-${data.apartment_id}`).innerText = data.apartment_like_count
    }
}