const ROBOT_ID = 1;

async function loadRobotStatus(){


try{

    const status =
        await apiRequest(
            "GET",
            `/robot/status/${ROBOT_ID}`
        );

    if(!robot || robot.status === "error"){

    document.getElementById(
        "batteryLevel"
    ).innerText = "Offline";

    document.getElementById(
        "cpuTemp"
    ).innerText = "Offline";

    return;
    }

    document.getElementById(
        "cpuTemp"
    ).innerText =
        `${status.temperature}°C`;

    document.getElementById(
        "robotLocation"
    ).innerText =
        status.location || "Unknown";

    document.getElementById(
        "obstacleStatus"
    ).innerText =
        status.obstacle_detected
        ? "Detected"
        : "Clear";

}

catch(error){

    console.error(
        "Robot status error",
        error
    );
}


}

async function moveForward(){


    await apiRequest(
        "POST",
        "/robot/move-forward"
    );


}

async function stopRobot(){


await apiRequest(
    "POST",
    "/robot/stop"
);


}

document.addEventListener(
"DOMContentLoaded",
() => {


    loadRobotStatus();

    setInterval(
        loadRobotStatus,
        5000
    );

    document
    .getElementById(
        "forwardBtn"
    )
    ?.addEventListener(
        "click",
        moveForward
    );

    document
    .getElementById(
        "stopBtn"
    )
    ?.addEventListener(
        "click",
        stopRobot
    );
}


);
