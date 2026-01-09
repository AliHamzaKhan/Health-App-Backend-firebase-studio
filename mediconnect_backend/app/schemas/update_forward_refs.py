from .appointment import Appointment
from .consultation import Consultation
from .doctor import Doctor
from .notification import Notification
from .patient import Patient
from .review import Review
from .schedule import Schedule


def update_forward_refs():
    Doctor.model_rebuild()
    Patient.model_rebuild()
    Appointment.model_rebuild()
