from fastapi import APIRouter, Depends
from services.robot_service import RobotService
from utils.dependencies import require_role

router = APIRouter(
    prefix="/robot",
    tags=["Robot"]
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