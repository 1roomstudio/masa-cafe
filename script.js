const button = document.getElementById("menuButton");
const menu = document.getElementById("menu");

button.addEventListener("click", function() {
    menu.textContent = "☕ 本日のおすすめ：カフェラテ 500円";
});