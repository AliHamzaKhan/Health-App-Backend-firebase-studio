from app.crud.crud_base import CRUDBase
from app.db.base import Subscription
from app.schemas.subscription import SubscriptionCreate, SubscriptionUpdate

class CRUDSubscription(CRUDBase[Subscription, SubscriptionCreate, SubscriptionUpdate]):
    pass

subscription = CRUDSubscription(Subscription)
