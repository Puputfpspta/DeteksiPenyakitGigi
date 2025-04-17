const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const previewImage = document.getElementById('preview-image');
const captureBtn = document.getElementById('capture-btn');
const upload = document.getElementById('upload');
let stream;

upload.addEventListener('change', function (e) {
  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (event) {
      previewImage.src = event.target.result;
    };
    reader.readAsDataURL(file);
  }
});

function openCamera() {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(s => {
      stream = s;
      video.srcObject = stream;
      video.style.display = 'block';
      captureBtn.style.display = 'inline-block';
    })
    .catch(err => {
      alert('Gagal mengakses kamera: ' + err.message);
    });
}

function capture() {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);

  stream.getTracks().forEach(track => track.stop());
  video.style.display = 'none';
  captureBtn.style.display = 'none';

  const imageData = canvas.toDataURL('image/png');
  previewImage.src = imageData;

  canvas.toBlob(blob => {
    const file = new File([blob], 'capture.png', { type: 'image/png' });
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    upload.files = dataTransfer.files;
  }, 'image/png');
}
