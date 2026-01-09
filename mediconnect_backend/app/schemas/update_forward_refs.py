
from .appointment import Appointment
from .consultation import Consultation
from .doctor import Doctor
from .notification import Notification
from .patient import Patient
from .review import Review
from .schedule import Schedule


def update_forward_refs():
    Doctor.update_forward_refs(
        Appointment=Appointment, Review=Review, Schedule=Schedule
    )
    Patient.update_forward_refs(
        Appointment=Appointment,
        Review=Review,
        Notification=Notification,
        Consultation=Consultation,
    )
    Appointment.update_forward_refs(
        Doctor=Doctor,
        Patient=Patient,
        Consultation=Consultation,
        Review=Review,
    )
