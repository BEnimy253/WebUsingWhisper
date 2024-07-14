// Lấy phần tử HTML cần thiết
const playButton = document.getElementById('play-button');
const translateButton = document.getElementById('translate-button');
const currentTimeLabel = document.getElementById('current-time');
const timeSlider = document.getElementById('time-slider');
const durationLabel = document.getElementById('duration');
const dynamicContentElements = document.getElementsByClassName('content');
const textMElements = document.getElementsByClassName('textM');
const audioBut = document.getElementById('audioM');
const originalTextM = [];
const originalDynamicContent = [];

// Lấy các nút bấm
const button1 = document.getElementById('button1');
const button2 = document.getElementById('button2');
const button3 = document.getElementById('button3');

// Lấy phần tử hình ảnh và âm thanh
const image = document.getElementById('image');
const audio = new Audio();
audio.src = '../static/audios/CMNQ.mp3';
// Lưu âm thanh gốc
const originalAudioSrc = audio.src;

// Lưu nội dung ban đầu của các phần tử có lớp "textM" và "dynamic-content"
function push_innerHTML(orig_text_obj, text_obj) {
    for (let i = 0; i < orig_text_obj.length; i++) {
        text_obj.push(orig_text_obj[i].innerHTML)
    }
}

push_innerHTML(textMElements, originalTextM)
push_innerHTML(dynamicContentElements, originalDynamicContent)

function choose_audio(button, name, audio_src, new_text, new_content) {
    button.addEventListener('click', function () {
        audioBut.innerText = name
        for (let i = 0; i < textMElements.length; i++) {
            textMElements[i].innerHTML = new_text;
        }
        for (let i = 0; i < dynamicContentElements.length; i++) {
            dynamicContentElements[i].innerHTML = new_content;
        }
        audio.src = audio_src;
    });
}

choose_audio(button1, "Audio 1", originalAudioSrc, "Văn bản mới 1", "Nội dung mới 1")
choose_audio(button2, "Audio 2", originalAudioSrc, "Văn bản mới 2", "Nội dung mới 2")
choose_audio(button3, "Audio 3", originalAudioSrc, "Văn bản mới 3", "Nội dung mới 3")

// Xử lý sự kiện khi nút play được nhấn
playButton.addEventListener('click', function () {
    if (audio.paused) {
        audio.play();
        playButton.innerHTML = '<i class="fas fa-pause"></i>';
    } else {
        audio.pause();
        playButton.innerHTML = '<i class="fas fa-play"></i>';
    }
});

// Xử lý sự kiện khi trạng thái phát/tạm dừng của audio thay đổi
audio.addEventListener('playing', function () {
    playButton.innerHTML = '<i class="fas fa-pause"></i>';
});

audio.addEventListener('pause', function () {
    playButton.innerHTML = '<i class="fas fa-play"></i>';
});

// Xử lý sự kiện khi thanh thời gian được di chuyển
timeSlider.addEventListener('input', function () {
    audio.currentTime = timeSlider.value;
});

// Xử lý sự kiện khi audio đã tải xong metadata
audio.addEventListener('loadedmetadata', function () {
    const duration = audio.duration;
    timeSlider.max = duration;
    timeSlider.step = 0.01;
    durationLabel.innerText = formatTime(duration);
});

// Cập nhật hiển thị thời gian hiện tại và thanh thời gian
audio.addEventListener('timeupdate', function () {
    const currentTime = audio.currentTime;
    currentTimeLabel.innerText = formatTime(currentTime);
    timeSlider.value = currentTime;
});

translateButton.addEventListener('click', function () {
    let coDon = document.getElementById("coDon");
    coDon.classList.toggle('colDon');
    coDon.classList.toggle('colHai');
});
translateButton.addEventListener('click', function () {
    let chiaHai = document.getElementById("chiaHai");
    chiaHai.classList.toggle('conHai');
    chiaHai.classList.toggle('');
});
translateButton.addEventListener('click', function () {
    let Doiclass = document.getElementById("Doiclass");
    Doiclass.classList.toggle('albumHai');
    Doiclass.classList.toggle('');
});

// Hàm định dạng thời gian (mm:ss)
function formatTime(time) {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${padZero(minutes)}:${padZero(seconds)}`;
}

// Hàm thêm số 0 vào đầu nếu số chỉ có 1 chữ số
function padZero(num) {
    return num.toString().padStart(2, '0');
}
