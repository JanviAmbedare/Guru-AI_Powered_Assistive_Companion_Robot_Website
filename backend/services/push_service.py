from config.settings import settings

#Currently we are only logging push notifications, but this service can be expanded in the future to handle actual push logic if needed
#when we implement push notifications on the frontend, we can use this service to send push notifications from the backend as well
#when we use firebase or other third-party services, we can integrate them here and keep the rest of the codebase clean and decoupled from specific implementations
#This service can also be used to send push notifications for other features in the future, such as alerts, reminders, etc. 
#For now, we will just log the push notifications in the LoggingService, but we can easily expand this in the future to handle actual push logic if needed
#This with use of FCM or other services can be implemented in the future when we want to send push notifications to mobile devices as well, currently we are only targeting web push notifications for browsers, but this can be expanded in the future to target mobile devices as well
#This allow to send notifications even when the user is not actively using the website, as long as they have granted permission for push notifications in their browser. This can help increase engagement and retention by keeping users informed and engaged with the website even when they are not actively using it.
class PushNotificationService:

    @staticmethod
    def send_push(subscription, title, body):

        payload = {
            "title": title,
            "body": body
        }

        try:

            webpush(
                subscription_info=subscription,
                data=str(payload),
                vapid_private_key=settings.VAPID_PRIVATE_KEY,
                vapid_claims={
                    "sub": settings.VAPID_CLAIMS_EMAIL
                }
            )

            return {
                "status": "success"
            }

        except Exception as e:

            return {
                "status": "error",
                "message": str(e)
            }