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
                {
                    user_id: USER_ID,
                    message: message
                }
            );

        showAlertToast(
            "🚨 Emergency alert sent"
        );

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