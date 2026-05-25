// =========================
// 🔔 INIT NOTIFICATIONS
// =========================

async function initNotifications(){

    if(!("Notification" in window)){

        console.log(
            "Notifications unsupported"
        );

        return;
    }

    if(Notification.permission
        !== "granted"){

        await Notification
            .requestPermission();
    }

    console.log(
        "🔔 Notifications ready"
    );
}


// =========================
// 🔔 SHOW POPUP
// =========================

function showNotification(
    title,
    body
){

    console.log(
        "🔔 SHOW:",
        title,
        body
    );

    if(Notification.permission
        === "granted"){

        new Notification(

            title,

            {
                body: body
            }
        );
    }
}


initNotifications();