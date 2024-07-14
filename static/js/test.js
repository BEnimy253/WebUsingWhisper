const muteButton = document.getElementById('mute-button');
muteButton.addEventListener('click', function () {
    let coDon = document.getElementById("coDon");
    coDon.classList.toggle('colDon');
    coDon.classList.toggle('colHai');
});
muteButton.addEventListener('click', function () {
    let chiaHai = document.getElementById("chiaHai");
    chiaHai.classList.toggle('conHai');
    chiaHai.classList.toggle('');
});
muteButton.addEventListener('click', function () {
    let Doiclass = document.getElementById("Doiclass");
    Doiclass.classList.toggle('albumHai');
    Doiclass.classList.toggle('');
});