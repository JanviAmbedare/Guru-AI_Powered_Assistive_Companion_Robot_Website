document
.getElementById(
    "profileBtn"
)
?.addEventListener(
    "click",
    () => {

        const dropdown =
            document.getElementById(
                "profileDropdown"
            );

        dropdown.style.display =
            dropdown.style.display ===
            "block"
            ? "none"
            : "block";
    }
);


async function loadProfile(){

    try{

        const [
            profile,
            media,
            training
        ] = await Promise.all([

            apiRequest(
                "GET",
                `/api/profile/${USER_ID}`
            ),

            apiRequest(
                "GET",
                `/status/${USER_ID}`
            ),

            apiRequest(
                "GET",
                `/training/status/${USER_ID}`
            )
        ]);

        document.getElementById(
            "profileName"
        ).innerText =
            profile.name || "-";

        document.getElementById(
            "profileEmail"
        ).innerText =
            profile.email || "-";

        document.getElementById(
            "faceTrainProfile"
        ).innerText =
            training.face_status;

        document.getElementById(
            "voiceTrainProfile"
        ).innerText =
            training.voice_status;

    }

    catch(error){

        console.error(
            error
        );
    }
}


async function retrainModels(){

    try{

        await apiRequest(
            "POST",
            `/api/profile/${USER_ID}/retrain`
        );

        alert(
            "Retraining requested"
        );

    }

    catch(error){

        console.error(
            error
        );
    }
}

document.addEventListener(
    "DOMContentLoaded",
    () => {

        loadProfile();

    }
);