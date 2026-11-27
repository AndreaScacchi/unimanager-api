from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.domain import Course, Enrollment
from app.schemas.api_schemas import CourseCreate


class AcademicRepository:
    def __init__(self, db: Session):
        self.db = db
        
    # --- COURSE METHODS --- #
    def get_course_by_id(self, course_id: int) -> Course | None:
        return self.db.get(Course, course_id)
    
    def get_course_by_code(self, code: str) -> Course | None:
        stmt = select(Course).where(Course.code == code)
        return self.db.scalar(stmt)
    
    def get_all_courses(self, skip: int = 0, limit: int = 100) -> list[Course]:
        stmt = select(Course).offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())
    
    def create_course(self, course_data: CourseCreate) -> Course:
        db_course = Course(**course_data.model_dump())
        self.db.add(db_course)
        self.db.commit()
        self.db.refresh(db_course)
        return db_course
    
    # --- ENROLLMENT & GRADE METHODS --- #
    def get_enrollment(self, student_id: int, course_id: int) -> Enrollment | None:
        stmt = select(Enrollment).where(
            Enrollment.student_id == student_id,
            Enrollment.course_id == course_id,
        )
        return self.db.scalar(stmt)
    
    def get_enrollment_by_id(self, enrollment_id: int) -> Enrollment | None:
        return self.db.get(Enrollment, enrollment_id)
    
    def count_course_enrollments(self, course_id: int) -> int:
        stmt = select(func.count(Enrollment.id)).where(Enrollment.course_id == course_id)
        return self.db.scalar(stmt) or 0
    
    def get_student_enrollments(self, student_id: int) -> list[Enrollment]:
        stmt = select(Enrollment).where(Enrollment.student_id == student_id)
        return list(self.db.scalars(stmt).all())
    
    def create_enrollment(self, student_id: int, course_id: int) -> Enrollment:
        db_enrollment = Enrollment(student_id=student_id, course_id=course_id)
        self.db.add(db_enrollment)
        self.db.commit()
        self.db.refresh(db_enrollment)
        return db_enrollment
    
    def update_grade(self, enrollment: Enrollment, grade: int) -> Enrollment:
        enrollment.grade = grade
        self.db.commit()
        self.db.refresh(enrollment)
        return enrollment