from app.crud.crud_base import CRUDBase
from app.schemas.notification import NotificationCreate, NotificationUpdate
from app.db.base import Notification

class CRUDNotification(CRUDBase[Notification, NotificationCreate, NotificationUpdate]):
    pass

crud_notification = CRUDNotification(Notification)
