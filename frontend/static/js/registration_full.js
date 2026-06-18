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
    console.log("UPLOAD FUNCTION STARTED");
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

    uploadBtn.disabled = true;

    uploadBtn.innerHTML =
        "Uploading...";

    uploadStatus.innerHTML =
        "☁️ Uploading Media";
    
    
    try {
        console.log("Faces Count:", faces.length);
        console.log("Voices Count:", voices.length);
        console.log(
                "Calling:",
                `/upload-media/${USER_ID}`
            );
        const response =
            await fetch(
                `/upload-media/${USER_ID}`,
                {
                    method:"POST",
                    body:formData
                }
            );

        console.log(
            "UPLOAD STATUS:",
            response.status
        );

        const data =
            await response.json();

        if(data.status === "success") {

            uploadStatus.innerHTML =
                "✅ Uploaded";

            uploadBtn.innerHTML =
                "Upload Complete";

            uploadBtn.disabled = true;

            await clearMedia();

            await loadMediaStatus();

            await loadTrainingStatus();
        }
    }
    catch(error){
        console.log("An error occurred while uploading media.");
        console.error(
            "UPLOAD ERROR:",
            error
        );
    }
}

async function loadMediaStatus() {

    try {

        const response =
            await fetch(
                `${API_BASE_URL}/media/status/${USER_ID}`
            );

        console.log(
            "MEDIA STATUS RESPONSE:",
            response.status
        );

        if(!response.ok){

            console.error(
                "Media Status API Failed"
            );

            return;
        }

        const data =
            await response.json();

        console.log(
            "Media Status:",
            data
        );

        if(!data){

            console.error(
                "Media status returned null"
            );

            return;
        }

        document.getElementById(
            "faceUploadStatus"
        ).innerText =

            data.face_uploaded
                ? `✅ ${data.face_count} Uploaded`
                : "⌛ Pending";

        document.getElementById(
            "voiceUploadStatus"
        ).innerText =

            data.voice_uploaded
                ? `✅ ${data.voice_count} Uploaded`
                : "⌛ Pending";

    }
    catch(error){

        console.error(
            "loadMediaStatus Error:",
            error
        );
    }
}
async function loadTrainingStatus(){

    try{

        const response =
            await fetch(
                `${API_BASE_URL}/training/status/${USER_ID}`
            );

        const data =
            await response.json();
        
        const faceProgress =
            data.face_progress || 0;

        document.getElementById(
            "faceUploadPercentage"
        ).innerText =
            `${faceProgress}%`;

        document.getElementById(
            "faceProgressFill"
        ).style.width =
            `${faceProgress}%`;

        document.getElementById(
            "faceCurrentUploadFile"
        ).innerText =
            data.face_current_file ||
            "Waiting...";

        const voiceProgress =
            data.voice_progress || 0;

        document.getElementById(
            "voiceUploadPercentage"
        ).innerText =
            `${voiceProgress}%`;

        document.getElementById(
            "voiceProgressFill"
        ).style.width =
            `${voiceProgress}%`;

        document.getElementById(
            "voiceCurrentUploadFile"
        ).innerText =
            data.voice_current_file ||
            "Waiting...";



        document.getElementById(
            "faceTrainStatus"
        ).innerText =

        `${data.face_status}
        (${data.face_processed_files}/${data.face_total_files})`;


        document.getElementById(
            "voiceTrainStatus"
        ).innerText =

        `${data.voice_status}
        (${data.voice_processed_files}/${data.voice_total_files})`;
            
        const workflow =
            document.getElementById(
                "workflowStatus"
            );

        if (
            faceProgress < 100 ||
            voiceProgress < 100
        ){

            workflow.innerHTML = `
                ✅ Face Capture
                <br>
                ✅ Voice Capture
                <br>
                ⏳ Uploading Media
                <br>
                ⭕ Training Pending
            `;
        }
        else if(
            data.face_status !== "completed" ||
            data.voice_status !== "completed"
        ){

            workflow.innerHTML = `
                ✅ Face Capture
                <br>
                ✅ Voice Capture
                <br>
                ✅ Upload Complete
                <br>
                ⏳ Training Models
            `;
        }
        else{

            workflow.innerHTML = `
                ✅ Face Capture
                <br>
                ✅ Voice Capture
                <br>
                ✅ Upload Complete
                <br>
                ✅ Training Complete
            `;
        }
        }
    catch(error){

        console.error(
            "Training status error",
            error
        );
    }
}



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