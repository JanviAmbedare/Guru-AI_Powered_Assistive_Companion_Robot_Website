const chatForm =
    document.getElementById(
        "chatForm"
    );

const messageInput =
    document.getElementById(
        "messageInput"
    );


chatForm.addEventListener(
    "submit",
    async (e) => {

        e.preventDefault();

        const message =
            messageInput.value.trim();

        if(!message){
            return;
        }

        appendUserMessage(
            message
        );

        messageInput.value = "";

        try{

            const response =
                await apiRequest(
                    "POST",
                    "/chat/",
                    null,
                    {
                        user_id: USER_ID,
                        message: message
                    }
                );

            appendBotMessage(
                response.response ||
                "No response received."
            );

        }

        catch(error){

            console.error(error);

            appendBotMessage(
                "Sorry, I couldn't process that request."
            );
        }
    }
);


function appendUserMessage(
    text
){

    const div =
        document.createElement(
            "div"
        );

    div.className =
        "message user";

    div.innerHTML = `
        <div class="bubble">
            ${text}
        </div>
    `;

    chatContainer.appendChild(
        div
    );

    scrollToBottom();
}


function appendBotMessage(
    text
){

    const div =
        document.createElement(
            "div"
        );

    div.className =
        "message bot";

    div.innerHTML = `
        <div class="bubble">
            ${text}
        </div>
    `;

    chatContainer.appendChild(
        div
    );

    scrollToBottom();
}


function quickMessage(
    text
){

    messageInput.value = text;

    chatForm.dispatchEvent(
        new Event(
            "submit",
            {
                cancelable:true,
                bubbles:true
            }
        )
    );
}


function scrollToBottom(){

    chatContainer.scrollTop =
        chatContainer.scrollHeight;
}

document.getElementById(
    "newChatBtn"
)?.addEventListener(
    "click",
    () => {

        document
        .getElementById(
            "chatContainer"
        )
        .innerHTML = "";

    }
);