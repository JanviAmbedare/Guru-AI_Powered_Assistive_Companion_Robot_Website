console.log(
    "🚨 alerts.js loaded"
);


// =========================
// ELEMENTS
// =========================

const modal =
    document.getElementById("modal");

const openEmergencyBtn =
    document.getElementById(
        "openEmergencyBtn"
    );

const closeModalBtn =
    document.getElementById(
        "closeModalBtn"
    );

const sendEmergencyBtn =
    document.getElementById(
        "sendEmergencyBtn"
    );


// =========================
// OPEN MODAL
// =========================

if(openEmergencyBtn){

    openEmergencyBtn
    .addEventListener(

        "click",

        () => {

            modal.style.display =
                "flex";
        }
    );
}


// =========================
// CLOSE MODAL
// =========================

if(closeModalBtn){

    closeModalBtn
    .addEventListener(

        "click",

        () => {

            modal.style.display =
                "none";
        }
    );
}


// =========================
// SEND EMERGENCY
// =========================

if(sendEmergencyBtn){

    sendEmergencyBtn
    .addEventListener(

        "click",

        async () => {

            try{

                const message =

                    document
                    .getElementById(
                        "emergencyMessage"
                    )
                    .value;

                const response =
                    await fetch(

                    "/trigger-emergency",

                    {
                        method:"POST",

                        headers:{
                            "Content-Type":
                            "application/json"
                        },

                        body: JSON.stringify({
                            message
                        })
                    }
                );

                const result =
                    await response.json();

                console.log(result);

                if(result.status === "success"){

                    showNotification(

                        "Emergency Alert",

                        message

                    );

                    modal.style.display =
                        "none";
                }

            }

            catch(error){

                console.log(
                    error
                );
            }
        }
    );
}


// =========================
// ACKNOWLEDGE ALERT
// =========================

document
.querySelectorAll(".ack-btn")
.forEach((button) => {

    button.addEventListener(

        "click",

        async () => {

            const alertId =

                button.dataset.alertId;

            try{

                await fetch(

                    `/ack-alert/${alertId}`,

                    {
                        method:"PUT"
                    }
                );

                location.reload();

            }

            catch(error){

                console.log(error);
            }
        }
    );
});


// =========================
// LIVE ALERTS
// =========================

let shownAlerts = new Set();


async function fetchLiveAlerts(){

    try{

        const response = await fetch(

            `/api/live-alerts/${USER_ID}`

        );

        const alerts =
            await response.json();

        alerts.forEach(async (alert) => {

            if(

                alert.status === "ACTIVE"

                &&

                !shownAlerts.has(alert.id)

            ){

                shownAlerts.add(alert.id);

                showNotification(

                    alert.title,

                    alert.message

                );

                await fetch(

                    `/ack-alert/${alert.id}`,

                    {
                        method:"PUT"
                    }
                );
            }
        });

    }

    catch(error){

        console.log(error);
    }
}


fetchLiveAlerts();

setInterval(
    fetchLiveAlerts,
    10000
);