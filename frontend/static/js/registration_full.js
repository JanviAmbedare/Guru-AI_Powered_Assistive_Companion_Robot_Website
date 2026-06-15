const USER_ID =
    window.location.pathname
    .split("/")
    .pop();

    const uploadBtn =
    document.getElementById(
        "uploadBtn"
    );

const uploadStatus =
    document.getElementById(
        "uploadStatus"
    );

const continueBtn =
    document.getElementById(
        "continueBtn"
    );

uploadBtn.addEventListener(
    "click",
    uploadMedia
);

async function uploadMedia() {

    const faces =
        await getFaces();

    const voices =
        await getVoices();

    const formData =
        new FormData();

    faces.forEach(
        (blob, index) => {

            formData.append(
                "face_files",
                blob,
                `face_${index}.jpg`
            );
        }
    );

    voices.forEach(
        (blob, index) => {

            formData.append(
                "voice_files",
                blob,
                `voice_${index}.webm`
            );
        }
    );

    uploadStatus.innerHTML =
        "☁️ Uploading...";

    const response =
        await fetch(

            `${API_BASE_URL}/upload-media/${USER_ID}`,

            {
                method:"POST",
                body:formData
            }
        );

    const data =
        await response.json();

    if(data.status === "success") {

    uploadStatus.innerHTML =
        "✅ Uploaded";

    await clearMedia();

    await loadMediaStatus();

    await loadTrainingStatus();
}
}

async function loadMediaStatus() {

    const response =
        await fetch(
            `${API_BASE_URL}/api/media/status/${USER_ID}`
        );

    const data =
        await response.json();

    document.getElementById(
        "faceUploadStatus"
    ).innerText =
        data.face_uploaded
        ? `✅ ${data.face_count} uploaded`
        : "❌ Not uploaded";

    document.getElementById(
        "voiceUploadStatus"
    ).innerText =
        data.voice_uploaded
        ? `✅ ${data.voice_count} uploaded`
        : "❌ Not uploaded";
}


async function loadTrainingStatus(){

    try{

        const response =
            await fetch(
                `${API_BASE_URL}/training/status/${USER_ID}`
            );

        const data =
            await response.json();

        document.getElementById(
            "faceTrainStatus"
        ).innerText =
            data.face_status;

        document.getElementById(
            "voiceTrainStatus"
        ).innerText =
            data.voice_status;
            if(
                data.face_status === "completed" &&
                data.voice_status === "completed"
                ){
                    continueBtn.disabled = false;
                }
            }

    catch(error){

        console.error(
            "Training status error",
            error
        );
    }
}

// uploadBtn.addEventListener(
//     "click",
//     async () => {

//         uploadStatus.innerHTML =
//             "☁️ Uploading...";

//         try {

//             const formData =
//                 new FormData();

//             const result =
//                 await fetch(

//                     `/upload-media/${USER_ID}`,

//                     {
//                         method:"POST",
//                         body:formData
//                     }
//                 );

//             const data =
//                 await result.json();

//             if(
//                 data.status === "success"
//             ){

//                 uploadCompleted =
//                     true;

//                 uploadStatus.innerHTML =
//                     "✅ Uploaded";

//                 checkReady();

//             }

//             else{

//                 uploadStatus.innerHTML =
//                     "❌ Upload Failed";
//             }

//         }

//         catch(error){

//             uploadStatus.innerHTML =
//                 "❌ Upload Failed";
//         }
//     }
// );


continueBtn.addEventListener(
    "click",
    () => {

        window.location.href =
            "/";
    }
);

document.addEventListener(
    "DOMContentLoaded",
    () => {

        loadMediaStatus();

        loadTrainingStatus();

        setInterval(
            loadTrainingStatus,
            5000
        );
    }
);