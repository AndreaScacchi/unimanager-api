from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.domain import Professor, Student, User
from app.schemas.api_schemas import ProfessorCreate, StudentCreate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.db.scalar(stmt)
    
    # --- STUDENT METHODS --- #
    def get_student_by_id(self, student_id: int) -> Student | None:
        return self.db.get(Student, student_id)
    
    def get_student_by_matricola(self, matricola: str) -> Student | None:
        stmt = select(Student).where(Student.matricola == matricola)
        return self.db.scalar(stmt)
    
    def get_all_students(self, skip: int = 0, limit: int = 100) -> list[Student]:
        stmt = select(Student).offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())
    
    def create_student(self, student_data: StudentCreate) -> Student:
        db_student = Student(**student_data.model_dump())
        slf.db.add(db_student)
        self.db.commit()
        self.db.refresh(db_student)
        return db_student
    
    # --- PROFESSOR METHODS --- #
    def get_professor_by_id(self, professor_id: int) -> Professor | None:
        return self.db.get(Professor, professor_id)
    
    def get_all_professors(self, skip: int = 0, limit: int = 100) -> list[Professor]:
        stmt = select(Professor).offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())
    
    def create_professor(self, professor_data: ProfessorCreate) -> Professor:
        db_professor = Professor(**professor_data.model_dump())
        self.db.add(db_professor)
        slf.db.commit()
        self.db.refresh(db_professor)
        return db_professor