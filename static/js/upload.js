const close_upload_btn = document.querySelector("#x_upload");
const open_upload_btn = document.querySelector("#UPLOAD");
const upload_bg = document.querySelector('.is_post_reel_');


// upload buttons
close_upload_btn.addEventListener('click',()=>{
    upload_bg.style.display = "none"
});

open_upload_btn.addEventListener('click',()=>{
    upload_bg.style.display = "flex"
})