function openModal(){

    document
        .getElementById(
            "modal"
        )
        .style.display =
        "flex";
}


function closeModal(){

    document
        .getElementById(
            "modal"
        )
        .style.display =
        "none";
}


/* ==========================
   CREATE REMINDER
========================== */

async function createReminder(){

    try{

        const remindAt =
            document
            .getElementById(
                "remindAt"
            )
            .value
            .replace(
                "T",
                " "
            );

        const payload = {

            title:
                document
                .getElementById(
                    "title"
                )
                .value,

            message:
                document
                .getElementById(
                    "message"
                )
                .value,

            remind_at:
                remindAt,

            priority:
                document
                .getElementById(
                    "priority"
                )
                .value
        };

        await apiRequest(
            "POST",
            "/reminder/",
            null,
            payload
        );

        closeModal();

        loadReminders();

    }

    catch(error){

        console.error(
            error
        );

        alert(
            "Failed to create reminder"
        );
    }
}

// ==========================
// RENDER REMINDERS
// ==========================
async function renderReminders(reminders) {

    const container =
        document.getElementById("remindersContainer");

    if (!container) return;

    container.innerHTML = "";

    reminders.forEach(reminder => {

        container.innerHTML += `
            <div class="reminder-card">
                <h3>${reminder.title}</h3>
                <p>${reminder.description}</p>
                <small>${reminder.reminder_time}</small>
            </div>
        `;
    });
}

/* ==========================
   LOAD REMINDERS
========================== */

async function loadReminders(){

    try{

        const reminders =
            await apiRequest(
                "GET",
                `/reminder/${USER_ID}`
            );

        renderReminders(
            reminders
        );

    }

    catch(error){

        console.error(
            error
        );
    }
}


/* ==========================
   DONE
========================== */

async function completeReminder(
    reminderId
){

    try{

        await apiRequest(
            "PUT",
            `/reminder/done/${USER_ID}/${reminderId}`
        );

        loadReminders();

    }

    catch(error){

        console.error(
            error
        );
    }
}


/* ==========================
   DELETE
========================== */

async function deleteReminder(
    reminderId
){

    try{

        await apiRequest(
            "DELETE",
            `/reminder/${USER_ID}/${reminderId}`
        );

        loadReminders();

    }

    catch(error){

        console.error(
            error
        );
    }
}


/* ==========================
   SNOOZE
========================== */

async function snoozeReminder(
    reminderId
){

    try{

        await apiRequest(
            "PUT",
            `/reminder/snooze/${USER_ID}/${reminderId}`
        );

        loadReminders();

    }

    catch(error){

        console.error(
            error
        );
    }
}