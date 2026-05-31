from fastapi import APIRouter, Depends
from services.robot_service import RobotService
from utils.dependencies import require_role

router = APIRouter(
    prefix="/robot",
    tags=["Robot"]
)

@router.get("/status/{robot_id}")
def robot_status(robot_id: int):

    return RobotService.get_status(
        robot_id
    )

@router.get("/telemetry/{robot_id}")
def robot_telemetry(robot_id: int):

    return RobotService.get_telemetry(
        robot_id
    )

@router.post("/move-forward")
def move_forward(
    user=Depends(require_role("OWNER"))
):
    return RobotService.move_forward()


@router.post("/stop")
def stop_robot(
    user=Depends(require_role("OWNER"))
):
    return RobotService.stop()


@router.post("/speak")
def robot_speak(
    text: str,
    user=Depends(require_role("OWNER"))
):
    return RobotService.speak(text)


@router.get("/battery")
def battery_status():
    return RobotService.battery_status()