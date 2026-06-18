document.addEventListener(
    "DOMContentLoaded",
    async () => {

        await loadDashboard();

    }
);

let emotionChart = null;

const USER_ID =
    window.USER_ID ||
    localStorage.getItem("user_id");
    
/* ==========================
   LOAD ALL DATA
========================== */

async function loadDashboard(){

    try{

        const [
            conversations,
            analytics,
            emotions,
            latestEmotion
        ] = await Promise.all([

            apiRequest(
                "GET",
                `/conversations/${USER_ID}`
            ),

            apiRequest(
                "GET",
                `/analytics/conversations/${USER_ID}`
            ),

            apiRequest(
                "GET",
                `/emotion/history/${USER_ID}`
            ),

            apiRequest(
                "GET",
                `/emotion/latest/${USER_ID}`
            )
        ]);

        populateConversationList(
            conversations.history || []
        );

        populateAnalytics(
            analytics
        );

        populateEmotionChart(
            emotions
        );

        populateLatestEmotion(
            latestEmotion
        );

    }

    catch(error){

        console.error(
            "Memory load error:",
            error
        );
    }
}

function populateConversationList(
    conversations
){

    const memoryList =
        document.getElementById(
            "memoryList"
        );

    memoryList.innerHTML = "";

    conversations.forEach(
        (item,index) => {

            const div =
                document.createElement(
                    "div"
                );

            div.className =
                "memory-item";

            div.innerHTML = `

                <strong>
                    ${item.intent || "General"}
                </strong>

                <p>
                    ${item.user_input || ""}
                </p>

            `;

            div.onclick =
                () =>
                showMemoryDetails(
                    item
                );

            memoryList.appendChild(
                div
            );
        }
    );
}

function showMemoryDetails(
    memory
){

    document.getElementById(
        "memoryContent"
    ).innerHTML = `

        <h4>User</h4>

        <p>
            ${memory.user_input}
        </p>

        <h4>Response</h4>

        <p>
            ${memory.response_text}
        </p>

        <h4>Intent</h4>

        <p>
            ${memory.intent}
        </p>

        <h4>Emotion</h4>

        <p>
            ${memory.emotion}
        </p>

    `;
}

function populateAnalytics(
    analytics
){

    document.getElementById(
        "memoryCount"
    ).innerText =
        analytics.total_interactions || 0;
}

function populateLatestEmotion(
    emotion
){

    document.getElementById(
        "latestEmotion"
    ).innerText =
        emotion.emotion || "Unknown";
}

function populateEmotionChart(
    emotions
){

    const ctx =
        document.getElementById(
            "emotionChart"
        );

    const labels =
        emotions.map(
            e => e.created_at
        );

    const values =
        emotions.map(
            e => e.confidence
        );

    if(emotionChart){

        emotionChart.destroy();
    }

    emotionChart =
        new Chart(ctx,{

            type:"line",

            data:{

                labels,

                datasets:[{

                    label:
                        "Emotion Confidence",

                    data:values,

                    borderColor:
                        "#38bdf8",

                    tension:0.3
                }]
            }
        });
}