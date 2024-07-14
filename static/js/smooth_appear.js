const body = document.querySelector("body");
const album = document.querySelector(".album");
album.classList.add("album--loaded");
setTimeout(() => {
    album.classList.add("album--parallax");
}, 1200);

// https://css-tricks.com/animated-intro-rxjs/
function smoothParallax() {
    const body = document.querySelector("body");
    const clientHeight = window.innerHeight;
    const bodyDims = {
        w: body.getBoundingClientRect().width,
        h: body.getBoundingClientRect().height
    };
    const limit = {
        x: 25,
        y: 25
    };
    // console.clear();
}

smoothParallax();