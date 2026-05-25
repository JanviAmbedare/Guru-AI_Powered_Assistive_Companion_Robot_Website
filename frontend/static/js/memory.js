const USER_ID = 1;

async function loadMemories(){

    const response = await fetch(`/api/memory/${USER_ID}`);
    const data = await response.json();

    const list = document.getElementById("memoryList");

    list.innerHTML = "";

    document.getElementById("memoryCount").innerText = data.length;

    data.forEach(memory => {

        const div = document.createElement("div");

        div.className = "memory-item";

        div.innerHTML = `
            <h4>${memory.intent}</h4>
            <p>${memory.text}</p>
        `;

        div.onclick = () => showMemory(memory);

        list.appendChild(div);

    });

}

function showMemory(memory){

    document.getElementById("memoryContent").innerHTML = `
        <h4>User Input</h4>
        <p>${memory.text}</p>

        <h4>AI Response</h4>
        <p>${memory.response}</p>

        <h4>Emotion</h4>
        <p>${memory.sentiment}</p>
    `;

    document.getElementById("latestEmotion").innerText =
        memory.sentiment;
}

async function loadEmotionTimeline(){

    const response =
        await fetch(`/api/profile/timeline/${USER_ID}`);

    const data = await response.json();

    const labels = data.map(x => x.day);
    const values = data.map(x => x.total);

    new Chart(
        document.getElementById("emotionChart"),
        {
            type:"line",

            data:{
                labels:labels,

                datasets:[{
                    label:"Emotion Frequency",
                    data:values
                }]
            }
        }
    );
}

async function searchMemory(){

    const query =
        document.getElementById("memorySearch").value;

    const response =
        await fetch(`/api/memory/search/${USER_ID}?q=${query}`);

    const data = await response.json();

    const list = document.getElementById("memoryList");

    list.innerHTML = "";

    data.forEach(item => {

        const memory = item.memory;

        const div = document.createElement("div");

        div.className = "memory-item";

        div.innerHTML = `
            <h4>Similarity:
            ${item.score.toFixed(2)}</h4>

            <p>${memory.summary}</p>
        `;

        list.appendChild(div);

    });

}
async function loadDailySummary(){

    const response =
        await fetch(`/api/memory/daily-summary/${USER_ID}`);

    const data = await response.json();

    document.getElementById("dailySummary").innerHTML = `
        <p>${data.summary}</p>
    `;
}
async function loadEmotionPrediction(){

    const response =
        await fetch(`/api/memory/emotion-predict/${USER_ID}`);

    const data = await response.json();

    document.getElementById(
        "emotionPrediction"
    ).innerHTML = `
        ${data.prediction}
        (${data.risk_level})
    `;
}
loadMemories();
loadEmotionTimeline();
loadDailySummary();
loadEmotionPrediction();