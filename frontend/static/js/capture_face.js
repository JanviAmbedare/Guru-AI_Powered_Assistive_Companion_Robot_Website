const video = document.getElementById("video");

const sampleCountText =
    document.getElementById("sampleCount");

const statusText =
    document.getElementById("statusText");

const progress =
    document.getElementById("progress");

const message =
    document.getElementById("message");

const loader =
    document.getElementById("loader");

let capturedImages = [];

let captureInterval = null;

let stream = null;

let capturing = false;

const MAX_SAMPLES = 60;


// =========================
// 🎥 START CAMERA
// =========================

async function startCamera(){

    try{

        stream = await navigator.mediaDevices.getUserMedia({
            video:{
                    width:1280,
                    height:720,
                    facingMode:"user"
                },
            audio:false
        });

        video.srcObject = stream;
        await video.play();
        message.innerHTML =
            "✅ Camera initialized";

    }

    catch(error){

        console.error(error);

        message.innerHTML =
            "❌ Camera permission denied";

        message.className = "status error";

        alert(
            "Please allow camera permission"
        );
    }
}


// =========================
// 📸 CAPTURE FRAME
// =========================

function captureFrame(){

    const canvas = document.createElement("canvas");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");

    ctx.drawImage(
        video,
        0,
        0,
        canvas.width,
        canvas.height
    );

    canvas.toBlob(blob => {

        capturedImages.push(blob);

        updateUI();

        // AUTO UPLOAD
        if(capturedImages.length >= MAX_SAMPLES){

            stopCapture();

            uploadFaces();
        }

    }, "image/jpeg");

}


// =========================
// 🚀 START CAPTURE
// =========================

async function startCapture(){

    if(capturing) return;

    if(!stream){
        await startCamera();
    }

    capturedImages = [];

    capturing = true;

    message.innerHTML =
        "📸 Capturing facial samples...";

    statusText.innerHTML = "Capturing";

    captureInterval = setInterval(() => {

        if(capturedImages.length < MAX_SAMPLES){

            captureFrame();

        }

    }, 250);

}


// =========================
// ⛔ STOP CAPTURE
// =========================

function stopCapture(){

    capturing = false;

    clearInterval(captureInterval);

    statusText.innerHTML = "Stopped";

    message.innerHTML =
        "⛔ Capture stopped";

}


// =========================
// 📊 UPDATE UI
// =========================

function updateUI(){

    sampleCountText.innerHTML =
        capturedImages.length;

    const percentage =
        (capturedImages.length / MAX_SAMPLES) * 100;

    progress.style.width =
        percentage + "%";

}


// =========================
// ☁️ UPLOAD FACE DATA
// =========================

async function uploadFaces(){

    loader.style.display = "block";

    statusText.innerHTML = "Uploading";

    message.innerHTML =
        "☁️ Uploading facial samples...";

    const formData = new FormData();

    capturedImages.forEach((blob, index) => {

        formData.append(
            "files",
            blob,
            `face_${index}.jpg`
        );

    });

    try{

        const response = await fetch(

            `/register/face/${USER_ID}`,

            {
                method:"POST",
                body: formData
            }
        );

        const result = await response.json();

        loader.style.display = "none";

        console.log(result);

        if(result.status === "success"){

            message.innerHTML =
                "✅ Face registration completed";

            message.className =
                "status success";

            statusText.innerHTML =
                "Completed";

            setTimeout(() => {

                window.location.href =
                    `/capture-voice/${USER_ID}`;

            }, 2000);

        }

        else{

            message.innerHTML =
                "❌ Upload failed";

            message.className =
                "status error";
        }

    }

    catch(error){

        console.error(error);

        loader.style.display = "none";

        message.innerHTML =
            "❌ Network/server error";

        message.className =
            "status error";
    }
}

// =========================
// 🚀 INIT
// =========================

startCamera();