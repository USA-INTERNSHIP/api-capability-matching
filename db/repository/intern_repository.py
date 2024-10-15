from fastapi import HTTPException
from sqlalchemy.orm import Session
from db.models.intern_model import Intern  # Replace with the correct import for your intern model
from schemas.intern_schema import InternSchema  # Replace with the correct import for your intern schema


def get_intern_dto(intern: Intern):
    return {
        "id": intern.id,
        "name": intern.name,
        "email": intern.email,
        "mobileNo": intern.mobileNo,
        "skills": intern.skills,
        "status": intern.status
    }


def retrieve_intern_profile(intern_id: int, db: Session):
    intern = db.query(Intern).filter(Intern.id == intern_id).first()
    if intern:
        return {"status": "success", "data": get_intern_dto(intern)}
    else:
        raise HTTPException(status_code=404, detail="Intern not found")


def update_intern_profile(intern_id: int, intern_data: InternSchema, db: Session):
    try:
        intern = db.query(Intern).filter(Intern.id == intern_id).first()
        if not intern:
            raise HTTPException(status_code=404, detail="Intern not found")

        if intern_data.name is not None:
            intern.name = intern_data.name
        if intern_data.email is not None:
            intern.email = intern_data.email
        if intern_data.mobileNo is not None:
            intern.mobileNo = intern_data.mobileNo
        if intern_data.skills is not None:
            intern.skills = intern_data.skills
        if intern_data.status is not None:
            intern.status = intern_data.status

        db.commit()
        db.refresh(intern)
        return {"status": "success", "data": get_intern_dto(intern)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def search_interns_logic(query: str, db: Session):
    try:
        interns = db.query(Intern).filter(
            (Intern.name.like(f"%{query}%")) |
            (Intern.email.like(f"%{query}%"))
        ).all()

        return {
            "status": "success",
            "data": [get_intern_dto(intern) for intern in interns]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Placeholder functions for future implementation
def review_applications_logic():
    return None


def respond_to_applications_logic():
    return None


def post_review_logic():
    return None


def read_reviews_logic():
    return None
