const close_set_btn = document.querySelector("#x_set");
const open_set_btn = document.querySelector("#bt_set");
const setting_bg = document.querySelector('.settings_xts');

close_set_btn.addEventListener('click',()=>{
    setting_bg.style.display = "none"
});

open_set_btn.addEventListener('click',()=>{
    setting_bg.style.display = "flex"
})

document.addEventListener("DOMContentLoaded", function () {
    const subscribeBtn = document.getElementById("subscribe");
    if (subscribeBtn) {
        subscribeBtn.addEventListener("click", function () {
            const username = this.dataset.username;

            fetch(`/follow-toggle/${username}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Tugma textini o‘zgartirish
                    this.textContent = data.is_following ? "Unsubscribe" : "Subscribe";

                    // Followers sonini yangilash
                    const followersCount = document.getElementById("followers-count");
                    if (followersCount) {
                        followersCount.textContent = data.followers_count;
                    }
                }
            })
            .catch(err => console.error("Follow toggle error:", err));
        });
    }
});

// CSRF olish uchun helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

