let emotionChart = null;
let intentChart = null;


/* ==========================
   DASHBOARD LOADER
========================== */

async function loadDashboard() {

    try {

        const [
            analytics,
            latestEmotion,
            robotStatus,
            emotionHistory
        ] = await Promise.all([

            apiRequest(
                "GET",
                `/analytics/conversations/${USER_ID}`
            ),

            apiRequest(
                "GET",
                `/emotion/latest/${USER_ID}`
            ),

            apiRequest(
                "GET",
                `/robot/status/${ROBOT_ID}`
            ),

            apiRequest(
                "GET",
                `/emotion/history/${USER_ID}`
            )
        ]);

        updateCounters(
            analytics,
            latestEmotion,
            robotStatus
        );

        updateIntentChart(
            analytics
        );

        updateEmotionChart(
            emotionHistory
        );

        addActivity(
            `Dashboard refreshed`
        );

    }

    catch(error){

        console.error(
            "Dashboard Error:",
            error
        );
    }
}


/* ==========================
   COUNTERS
========================== */

function updateCounters(
    analytics,
    emotion,
    robot
){

    document.getElementById(
        "conversationCount"
    ).innerText =
        analytics.total_interactions || 0;
    
    document.getElementById(
        "batteryLevel"
    ).innerText =
        `${robot?.battery_level ?? "Offline"}`;

    document.getElementById(
        "cpuTemp"
    ).innerText =
        `${robot?.temperature ?? "--"}°C`;

    document.getElementById(
        "topEmotion"
    ).innerText =
        emotion.emotion || "Unknown";
}


/* ==========================
   INTENT CHART
========================== */

function updateIntentChart(
    analytics
){

    const ctx =
        document.getElementById(
            "intentChart"
        );

    if(!intentChart){

        intentChart =
            new Chart(ctx,{
                type:"bar",

                data:{
                    labels:[],
                    datasets:[{
                        label:
                            "Intent Count",
                        data:[]
                    }]
                }
            });
    }

    intentChart.data.labels =
        analytics.top_intents.map(
            i => i.intent
        );

    intentChart.data.datasets[0].data =
        analytics.top_intents.map(
            i => i.count
        );

    intentChart.update();
}


/* ==========================
   EMOTION CHART
========================== */

function updateEmotionChart(
    emotions
){

    const ctx =
        document.getElementById(
            "emotionChart"
        );

    if(!emotionChart){

        emotionChart =
            new Chart(ctx,{
                type:"line",

                data:{
                    labels:[],
                    datasets:[{
                        label:
                            "Emotion Confidence",
                        data:[]
                    }]
                }
            });
    }

    emotionChart.data.labels =
        emotions.map(
            e =>
            new Date(
                e.created_at
            ).toLocaleDateString()
        );

    emotionChart.data.datasets[0].data =
        emotions.map(
            e => e.confidence
        );

    emotionChart.update();
}


/* ==========================
   ACTIVITY LOG
========================== */

function addActivity(
    message
){

    const activityLog =
        document.getElementById(
            "activityLog"
        );

    const item =
        document.createElement(
            "div"
        );

    item.className =
        "activity-item";

    item.innerHTML = `

        <div>
            ${message}
        </div>

        <div class="activity-time">
            ${new Date()
                .toLocaleTimeString()}
        </div>
    `;

    activityLog.prepend(item);

    while(
        activityLog.children.length > 15
    ){
        activityLog.removeChild(
            activityLog.lastChild
        );
    }
}


/* ==========================
   START
========================== */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        loadDashboard();

        setInterval(
            loadDashboard,
            10000
        );
    }
);