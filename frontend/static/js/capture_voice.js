const mic =
    document.getElementById("mic");

const countText =
    document.getElementById("count");

const progress =
    document.getElementById("progress");

const statusText =
    document.getElementById("status");

let mediaRecorder;

let audioChunks = [];

let samples = [];

const MAX_SAMPLES = 15;

const voicePrompt =
    document.getElementById("voicePrompt");

const SAMPLE_PHRASES = [

    "Hello Guru, how are you today?",

    "Please remind me to take my medicine at 8 PM.",

    "What is the weather forecast for today?",

    "Set an alarm for six o'clock tomorrow morning.",

    "Call my emergency contact if I need help.",

    "Open my daily schedule and read it aloud.",

    "I would like to listen to some relaxing music.",

    "Please tell me the current time and date.",

    "Navigate me safely to the living room.",

    "Turn on the lights in my bedroom.",

    "Read my latest notifications and messages.",

    "Start a video call with my family members.",

    "Help me find my glasses and water bottle.",

    "Thank you Guru for assisting me every day.",

    "My voice is being registered for secure authentication."

];
// =========================
// 🎤 RECORD SAMPLE
// =========================

async function recordSample(){

    if(samples.length >= MAX_SAMPLES){

        statusText.innerHTML =
            "✅ All samples collected";

        return;
    }

    try{

        const stream =
            await navigator.mediaDevices.getUserMedia({
                audio:true
            });

        mediaRecorder =
            new MediaRecorder(stream);

        audioChunks = [];

        mic.classList.add("recording");

        statusText.innerHTML =
            "🎤 Recording...";

        mediaRecorder.ondataavailable = e => {

            audioChunks.push(e.data);

        };

        mediaRecorder.onstop = async () => {

            mic.classList.remove("recording");

            const audioBlob =
                new Blob(audioChunks, {
                    type:"audio/webm"
                });

            samples.push(audioBlob);

            await saveVoice(audioBlob);
            updatePrompt();
            updateUI();

            // AUTO UPLOAD
            if(samples.length >= MAX_SAMPLES){

                sessionStorage.setItem(
                    "voiceCount",
                    samples.length
                );

                window.voiceSamples =
                    samples;

                window.location.href =
                    `/registration-complete/${USER_ID}`;
            }

        };

        mediaRecorder.start();

        // 3 sec recording
        setTimeout(() => {

            mediaRecorder.stop();

            stream.getTracks().forEach(track => {
                track.stop();
            });

        }, 3000);

    }

    catch(error){

        console.error(error);

        statusText.innerHTML =
            "❌ Microphone permission denied";

        statusText.className = "error";
    }
}


// =========================
// 📊 UPDATE UI
// =========================

function updateUI(){

    countText.innerHTML =
        samples.length;

    const percentage =
        (samples.length / MAX_SAMPLES) * 100;

    progress.style.width =
        percentage + "%";

    statusText.innerHTML =
        `✅ Sample ${samples.length} recorded`;
    updatePrompt();
}

// =========================
// 🔄 UPDATE PROMPT
// =========================
function updatePrompt(){

    if(samples.length < SAMPLE_PHRASES.length){

        voicePrompt.innerHTML =
            SAMPLE_PHRASES[samples.length];

    }
    else{

        voicePrompt.innerHTML =
            "✅ All voice samples collected";

    }
}

document.addEventListener("DOMContentLoaded", () => {

    updatePrompt();

});
// =========================
// ☁️ UPLOAD VOICE DATA
// =========================

// async function uploadVoices(){

//     statusText.innerHTML =
//         "☁️ Uploading voice samples...";

//     const formData = new FormData();

//     samples.forEach((blob, index) => {

//         formData.append(
//             "files",
//             blob,
//             `voice_${index}.webm`
//         );

//     });

//     // IMPORTANT
//     formData.append(
//         "media_role",
//         "raw"
//     );

//     try{

//         const result =
//             await uploadVoiceData(
//                 USER_ID,
//                 formData
//             );

//         console.log(result);

//         if(result.status === "success"){

//             statusText.innerHTML =
//                 "✅ Voice registration completed";

//             statusText.className =
//                 "success";

//             setTimeout(() => {

//                 window.location.href = "/";

//             }, 2000);

//         }

//         else{

//             statusText.innerHTML =
//                 "❌ Upload failed";

//             statusText.className =
//                 "error";
//         }

//     }

//     catch(error){

//         console.error(error);

//         statusText.innerHTML =
//             "❌ Network/server error";

//         statusText.className =
//             "error";
//     }
// }