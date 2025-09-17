const close_set_btn = document.querySelector("#x_set");
const open_set_btn = document.querySelector("#bt_set");
const setting_bg = document.querySelector('.settings_xts');

close_set_btn.addEventListener('click',()=>{
    setting_bg.style.display = "none"
});

open_set_btn.addEventListener('click',()=>{
    setting_bg.style.display = "flex"
})