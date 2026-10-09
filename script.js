const button = document.getElementById("menuButton");
const menu = document.getElementById("menu");

button.addEventListener("click", function() {
    menu.textContent = "☕ 本日のおすすめ：カフェラテ 500円";
});


const contactForm = document.getElementById("contactForm");

contactForm.addEventListener("submit", function(event) {
    event.preventDefault();

    const name = document.getElementById("name").value;
    const message = document.getElementById("message").value;

    fetch("/api/contact", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        name: name,
        message: message
    })
})
.then(response => response.json())
.then(data => {
    document.getElementById("result").textContent = data.message;
});

});