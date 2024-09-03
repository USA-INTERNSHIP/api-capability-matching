from sqlalchemy.orm import Session
from db.models.hiring_manager_model import HiringManager, Job  # Correct import


def register_hiring_manager_logic(hiring_manager, db: Session):
    # Register a new hiring manager in the database
    pass


def create_profile_logic(profile, db: Session):
    # Create or update the profile of a hiring manager
    pass


def post_job_logic(job, db: Session):
    # Post a new job in the database
    pass


#  other logic functions

# Note for my future understanding : logic for all the functions is yet to be defined as per the requirement
def search_job_logic():
    return None


def search_interns_logic():
    return None


def review_applications_logic():
    return None


def respond_to_interns_logic():
    return None


def post_contract_logic():
    return None


def respond_to_milestones_logic():
    return None


def pay_intern_logic():
    return None


def review_payment_history_logic():
    return None


def post_review_logic():
    return None


def read_reviews_logic():
    return None