// =========================
// 🌐 BASE CONFIG
// =========================

const BASE_URL =
    window.API_BASE_URL ||
    "https://guru-ai-powered-assistive-companion-kpna.onrender.com";

const DEFAULT_TIMEOUT = 20000;


// =========================
// 🌐 COMMON API ENGINE
// =========================

async function apiRequest(
    method,
    endpoint,
    token = null,
    data = null,
    params = null
) {

    try {

        let url =
            `${BASE_URL}${endpoint}`;

        // =========================
        // 🔍 QUERY PARAMS
        // =========================

        if (params) {

            const query =
                new URLSearchParams(params)
                    .toString();

            url += `?${query}`;
        }

        // =========================
        // 🔐 HEADERS
        // =========================

        const headers = {
            "Content-Type":
                "application/json"
        };

        if (token) {

            headers[
                "Authorization"
            ] = `Bearer ${token}`;
        }

        // =========================
        // ⏳ REQUEST TIMEOUT
        // =========================

        const controller =
            new AbortController();

        const timeoutId =
            setTimeout(
                () => controller.abort(),
                DEFAULT_TIMEOUT
            );

        // =========================
        // 📡 FETCH REQUEST
        // =========================

        const response =
            await fetch(url, {
                method,
                headers,
                credentials: "include",
                signal: controller.signal,
                body: data
                    ? JSON.stringify(data)
                    : null
            });

        clearTimeout(timeoutId);

        console.log(
            `🌐 ${method} ${url}`
        );

        console.log(
            "📡 STATUS:",
            response.status
        );

        // =========================
        // ✅ JSON RESPONSE
        // =========================

        const contentType =
            response.headers.get(
                "content-type"
            );

        if (
            contentType &&
            contentType.includes(
                "application/json"
            )
        ) {

            return await response.json();
        }

        // =========================
        // ❌ RAW RESPONSE
        // =========================

        return {
            status: "error",
            message:
                await response.text()
        };

    } catch (error) {

        console.error(
            "API ERROR:",
            error
        );

        // =========================
        // ⏳ TIMEOUT
        // =========================

        if (
            error.name === "AbortError"
        ) {

            return {
                status: "error",
                message:
                    "Request timeout"
            };
        }

        // =========================
        // ❌ NETWORK ERROR
        // =========================

        return {
            status: "error",
            message: error.message
        };
    }
}


// =====================================================
// 🔐 AUTH APIs
// =====================================================

async function signupUser(data) {

    return await apiRequest(
        "POST",
        "/auth/register",
        null,
        data
    );
}
async function handleSignup() {

    const formData = {

        username:
            document.querySelector(
                '[name="name"]'
            ).value,

        password:
            document.querySelector(
                '[name="password"]'
            ).value,

        role:
            document.querySelector(
                '[name="role"]'
            ).value,

        disability_type:
            document.querySelector(
                '[name="disability_type"]'
            ).value,

        language_pref:
            document.querySelector(
                '[name="language_pref"]'
            ).value
    };

    const result =
        await signupUser(formData);

    const errorBox =
        document.getElementById(
            "signupError"
        );

    if (
        result.detail ===
        "Username already exists"
    ) {

        errorBox.innerText =
            "❌ Username already exists";

        errorBox.style.display =
            "block";

        return;
    }

    window.location.href =
        result.redirect_url;
}
async function loginUser(data) {

    return await apiRequest(
        "POST",
        "/auth/login",
        null,
        data
    );
}


// =====================================================
// 👤 USER APIs
// =====================================================

async function getUsers(token) {

    return await apiRequest(
        "GET",
        "/dashboard/users",
        token
    );
}

async function getProfile(
    userId,
    token
) {

    return await apiRequest(
        "GET",
        `/profile/${userId}`,
        token
    );
}


// =====================================================
// 💬 CHAT APIs
// =====================================================

async function sendChat(
    data,
    token
) {

    return await apiRequest(
        "POST",
        "/chat/",
        token,
        data
    );
}

async function getChat(
    userId,
    token
) {

    return await apiRequest(
        "GET",
        `/memory/conversation/${userId}`,
        token
    );
}


// =====================================================
// 🧠 MEMORY APIs
// =====================================================

async function getConversation(
    userId,
    token
) {

    return await apiRequest(
        "GET",
        `/memory/conversation/${userId}`,
        token
    );
}

async function searchMemory(
    userId,
    query,
    token
) {

    return await apiRequest(
        "GET",
        `/memory/search/${userId}`,
        token,
        null,
        {
            query
        }
    );
}

async function getMemorySummary(
    userId,
    token
) {

    return await apiRequest(
        "GET",
        `/memory/summary/${userId}`,
        token
    );
}


// =====================================================
// ⏰ REMINDER APIs
// =====================================================

async function getReminders(
    userId,
    token
) {

    return await apiRequest(
        "GET",
        `/reminder/${userId}`,
        token
    );
}

async function createReminder(
    data,
    token
) {

    return await apiRequest(
        "POST",
        "/reminder/",
        token,
        data
    );
}

async function markReminderDone(
    userId,
    reminderId,
    token
) {

    return await apiRequest(
        "PUT",
        `/reminder/done/${userId}/${reminderId}`,
        token
    );
}

async function deleteReminder(
    userId,
    reminderId,
    token
) {

    return await apiRequest(
        "DELETE",
        `/reminder/${userId}/${reminderId}`,
        token
    );
}


// =====================================================
// 🚨 ALERT APIs
// =====================================================

async function getAlerts(
    userId,
    token
) {

    return await apiRequest(
        "GET",
        `/alerts/${userId}`,
        token
    );
}

async function sendEmergencyAlert(
    userId,
    message,
    token
) {

    return await apiRequest(
        "POST",
        "/alerts/emergency",
        token,
        null,
        {
            user_id: userId,
            message
        }
    );
}

async function acknowledgeAlert(
    alertId,
    token
) {

    return await apiRequest(
        "PUT",
        `/alerts/acknowledge/${alertId}`,
        token
    );
}


// =====================================================
// 🤖 ROBOT APIs
// =====================================================

async function getRobotStatus(
    token
) {

    return await apiRequest(
        "GET",
        "/robot/status",
        token
    );
}

async function sendRobotCommand(
    data,
    token
) {

    return await apiRequest(
        "POST",
        "/robot/command",
        token,
        data
    );
}


// =====================================================
// 📊 ANALYTICS APIs
// =====================================================

async function getUsageStats(
    userId,
    token
) {

    return await apiRequest(
        "GET",
        `/analytics/${userId}`,
        token
    );
}

async function getLogs(
    userId,
    token
) {

    return await apiRequest(
        "GET",
        `/logs/${userId}`,
        token
    );
}


// =====================================================
// ❤️ HEALTH CHECK
// =====================================================

async function healthCheck() {

    return await apiRequest(
        "GET",
        "/health"
    );
}

// =====================================================
// 📤 MEDIA UPLOAD APIs
// =====================================================
async function uploadAllMedia(
    userId,
    formData
){

    const response =
        await fetch(

            `${BASE_URL}/registration/upload-all/${userId}`,

            {
                method:"POST",
                body:formData
            }
        );

    return await response.json();
}
// =====================================
// FACE MODEL TRAINING
// =====================================
// async function trainFaceModel(
//     userId
// ){

//     return await apiRequest(

//         "POST",

//         `/training/face/${userId}`
//     );
// }

// // =====================================
// // VOICE MODEL TRAINING
// // =====================================
// async function trainVoiceModel(
//     userId
// ){

//     return await apiRequest(

//         "POST",

//         `/training/voice/${userId}`
//     );
// }
// =====================================
// FACE UPLOAD
// =====================================

// async function uploadFaceData(
//     userId,
//     formData
// ){

//     const response = await fetch(

//         `${BASE_URL}/register/face/${userId}`,

//         {
//             method: "POST",

//             body: formData
//         }
//     );

//     return await response.json();
// }



// // =====================================
// // VOICE UPLOAD
// // =====================================

// async function uploadVoiceData(
//     userId,
//     formData
// ){

//     const response = await fetch(

//         `${BASE_URL}/register/voice/${userId}`,

//         {
//             method: "POST",

//             body: formData
//         }
//     );

//     return await response.json();
// }