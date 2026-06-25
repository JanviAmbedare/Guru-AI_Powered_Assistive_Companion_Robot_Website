/* =====================================
   LOAD USER ALERTS
===================================== */

async function loadAlerts() {

    try {

        return await apiRequest(
            "GET",
            `/alerts/${USER_ID}`
        );

    } catch (error) {

        console.error(
            "Failed to load alerts",
            error
        );

        return [];
    }
}
async function renderAlerts() {

    const alerts = await loadAlerts();

    const container =
        document.getElementById(
            "alertsContainer"
        );

    container.innerHTML = "";

    alerts.forEach(alert => {

        container.innerHTML += `

        <div class="alert-card ${alert.severity.toLowerCase()}">

            <div class="header">

                <h3>${alert.title}</h3>

                <span>${alert.severity}</span>

            </div>

            <p>${alert.message}</p>

            <div class="meta">

                <span>${alert.type}</span>

                <span>${alert.source}</span>

            </div>

            <div class="meta">

                <span>${alert.created_at}</span>

                <span>${alert.status}</span>

            </div>

            ${
                alert.status === "ACTIVE"
                ?

                `
                <button
                    class="ack-btn"
                    onclick="acknowledge(${alert.id})">

                    ✅ Acknowledge

                </button>

                <button
                    class="resolve-btn"
                    onclick="resolve(${alert.id})">

                    ✔ Resolve

                </button>
                `

                :

                `<span class="resolved">✔ ${alert.status}</span>`

            }

        </div>

        `;

    });

}

/* =====================================
   EMERGENCY ALERT
===================================== */

async function sendEmergencyAlert(
    message = "Emergency assistance required"
) {

    try {

        const response =
            await apiRequest(
            "POST",
            "/alerts/emergency",
            null,
            null,
            {
                user_id: USER_ID,
                message: message
            }
        );

        showAlertToast(
            "🚨 Emergency alert sent"
        );

        renderAlerts();

        return response;


    } catch (error) {

        console.error(error);

        showAlertToast(
            "❌ Emergency alert failed"
        );
    }
}


/* =====================================
   CRITICAL ALERT
===================================== */

async function sendCriticalAlert(
    message
) {

    return await apiRequest(
        "POST",
        "/alerts/critical",
        null,
        {
            user_id: USER_ID,
            message: message
        }
    );
}


/* =====================================
   INFO ALERT
===================================== */

async function sendInfoAlert(
    message
) {

    return await apiRequest(
        "POST",
        "/alerts/info",
        null,
        {
            user_id: USER_ID,
            message: message
        }
    );
}


/* =====================================
   ACKNOWLEDGE ALERT
===================================== */

async function acknowledgeAlert(
    alertId
) {

    return await apiRequest(
        "PUT",
        `/alerts/acknowledge/${alertId}`
    );
}

async function acknowledge(id){

    await acknowledgeAlert(id);

    showAlertToast(
        "Alert Acknowledged"
    );

    renderAlerts();

}
/* =====================================
   RESOLVE ALERT
===================================== */

async function resolveAlert(
    alertId
) {

    return await apiRequest(
        "PUT",
        `/alerts/resolve/${alertId}`
    );
}
async function resolve(id){

    await resolveAlert(id);

    showAlertToast(
        "Alert Resolved"
    );

    renderAlerts();

}

/* =====================================
   ALERT ANALYTICS
===================================== */

async function getAlertAnalytics() {

    return await apiRequest(
        "GET",
        `/alerts/analytics/${USER_ID}`
    );
}


/* =====================================
   SIMPLE ALERT TOAST
===================================== */

function showAlertToast(
    message
) {

    const toast =
        document.createElement(
            "div"
        );

    toast.innerText =
        message;

    toast.style.position =
        "fixed";

    toast.style.top =
        "20px";

    toast.style.right =
        "20px";

    toast.style.background =
        "#ef4444";

    toast.style.color =
        "white";

    toast.style.padding =
        "12px 18px";

    toast.style.borderRadius =
        "10px";

    toast.style.zIndex =
        "9999";

    document.body.appendChild(
        toast
    );

    setTimeout(() => {

        toast.remove();

    }, 3000);
}

document.addEventListener("DOMContentLoaded", () => {

    const btn = document.getElementById("emergencyBtn");

    if (btn) {

        btn.addEventListener("click", async () => {

            await sendEmergencyAlert();

            await renderAlerts();

        });

    }

});

// setInterval(
//     renderAlerts,
//     5000
// );