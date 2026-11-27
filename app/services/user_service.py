from sqlalchemy.orm import Session

from app.models.domain import Professor, Student
from app.repositories.user_repository import UserRepository
from app.schemas.api_schemas import ProfessorCreate, StudentCreate
from app.services.exceptions import EntityAlreadyExistsError, EntityNotFoundError


class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        
    # --- STUDENT OPERATIONS --- #
    def register_student(self, student_data: StudentCreate) -> Student:
        if self.user_repo.get_user_by_email(student_data.email):
            raise EntityAlreadyExistsError(f"Email '{student_data.email}' già registrata nel sistema.")
        
        if self.user_repo.get_student_by_matricola(student_data.matricola):
            raise EntityAlreadyExistsError(f"Matricola '{student_data.matricola}' già assegnata a uno studente.")
        
        return self.user_repo.create_student(student_data)
    
    def get_student(self, student_id: int) -> Student:
        student = self.user_repo.get_student_by_id(student_id)
        if not student:
            raise EntityNotFoundError(f"Studente con ID '{student_id}' non trovato.")
        return student
    
    def list_students(self, skip: int = 0, limit: int = 100) -> list[Student]:
        return self.user_repo.get_all_students(skip=skip, limit=limit)
    
    # --- PROFESSOR OPERATIONS --- #
    def register_professor(self, professor_data: ProfessorCreate) -> Professor:
        if self.user_repo.get_user_by_email(professor_data.email):
            raise EntityAlreadyExistsError(f"Email '{professor_data.email}' già registrata nel sistema.")
        
        return self.user_repo.create_professor(professor_data)
    
    def get_professor(self, professor_id: int) -> Professor:
        professor = self.user_repo.get_professor_by_id(professor_id)
        if not professor:
            raise EntityNotFoundError(f"Docente con ID '{professor_id}' non trovato.")
        return professor
    
    def list_professors(self, skip: int = 0, limit: int = 100) -> list[Professor]:
        return self.user_repo.get_all_professors(skip=skip, limit=limit)