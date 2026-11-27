from sqlalchemy.orm import Session

from app.models.domain import Course, Enrollment
from app.repositories.academic_repository import AcademicRepository
from app.repositories.user_repository import UserRepository
from app.schemas.api_schemas import CourseCreate, EnrollmentCreate, GradeUpdate
from app.services.exceptions import BusinessRuleViolationError, EntityAlreadyExistsError, EntityNotFoundError


class AcademicService:
    def __init__(self, db: Session):
        self.academic_repo = AcademicRepository(db)
        self.user_repo = UserRepository(db)
        
    # --- COURSE OPERATIONS --- #
    def create_course(self, course_data: CourseCreate) -> Course:
        if self.academic_repo.get_course_by_code(course_data.code):
            raise EntityAlreadyExistsError(f"Codice corso '{course_data.code}' già esistente.")
        
        professor = self.user_repo.get_professor_by_id(course_data.professor_id)
        if not professor:
            raise EntityNotFoundError(f"Docente con ID '{course_data.professor_id}' non trovato.")
        
        return self.academic_repo.create_course(course_data)
    
    def get_course(self, course_id: int) -> Course:
        course = self.academic_repo.get_course_by_id(course_id)
        if not course:
            raise EntityNotFoundError(f"Corso con ID '{course_id}' non trovato.")
        return course
    
    def list_courses(self, skip: int = 0, limit: int = 100) -> list[Course]:
        return self.academic_repo.get_all_courses(skip=skip, limit=limit)
    
    # --- ENROLLMENT & GRADE OPERATIONS --- #
    def enroll_student(self, enrollment_data: EnrollmentCreate) -> Enrollment:
        student = self.user_repo.get_student_by_id(enrollment_data.student_id)
        if not student:
            raise EntityNotFoundError(f"Studente con ID '{enrollment_data.student_id}' non trovato.")
        
        course = self.academic_repo.get_course_by_id(enrollment_data.course_id)
        if not course:
            raise EntityNotFoundError(f"Corso con ID '{enrollment_data.course_id}' non trovato.")
        
        existing = self.academic_repo.get_enrollment(student_id=enrollment_data.student_id, course_id=enrollment_data.course_id,)
        if existing:
            raise EntityAlreadyExistsError("Lo studente risulta già iscritto a questo corso.")
        
        current_enrolled = self.academic_repo.count_course_enrollments(course.id)
        if current_enrolled >= course.max_students:
            raise BusinessRuleViolationError(f"Il corso '{course.title}' ha raggiunto la capienza massima ({course.max_students} studenti).")
        
        return self.academic_repo.create_enrollment(student_id=enrollment_data.student_id, course_id=enrollment_data.course_id)
    
    def assign_grade(self, enrollment_id: int, grade_data: GradeUpdate) -> Enrollment:
        enrollment = self.academic_repo.get_enrollment_by_id(enrollment_id)
        if not enrollment:
            raise EntityNotFoundError(f"Iscrizione con ID '{enrollment_id}' non trovata.")
        
        return self.academic_repo.update_grade(enrollment, grade_data.grade)
    
    def get_student_career(self, student_id: int) -> list[Enrollment]:
        student = self.user_repo.get_student_by_id(student_id)
        if not student:
            raise EntityNotFoundError(f"Studente con ID '{student_id}' non trovato.")
        
        return self.academic_repo.get_student_enrollments(student_id)