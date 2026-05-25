function openModal(){

    document
    .getElementById("modal")
    .style.display = "flex";
}


async function createReminder(){
    let remindAt =
    document.getElementById(
        "remindAt"
    ).value;

    remindAt = remindAt.replace("T", " ");
    const data = {

        user_id: USER_ID,

        title:
            document.getElementById(
                "title"
            ).value,

        message:
            document.getElementById(
                "message"
            ).value,

        remind_at: remindAt,

        priority:
            document.getElementById(
                "priority"
            ).value
    };

    const response = await fetch(
        "/create-reminder",
        {
            method:"POST",

            headers:{
                "Content-Type":
                "application/json"
            },

            body: JSON.stringify(data)
        }
    );

    const result =
        await response.json();

    if(result.status === "success"){

        location.reload();
    }
}


async function completeReminder(id){

    await fetch(
        `/complete-reminder/${id}`,
        {
            method:"PUT"
        }
    );

    location.reload();
}


async function deleteReminder(id){

    await fetch(
        `/delete-reminder/${id}`,
        {
            method:"DELETE"
        }
    );

    location.reload();
}

function closeModal(){

    document
    .getElementById("modal")
    .style.display = "none";
}