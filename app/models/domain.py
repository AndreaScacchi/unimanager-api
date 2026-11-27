from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    
    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": "role",
    }
    
    
class Student(User):
    __tablename__ = "students"
    
    id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    matricola: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    enrollment_year: Mapped[int] = mapped_column(Integer, nullable=False)
    
    enrollments: Mapped[list["Enrollment"]] = relationship(
        back_populates="student",
        cascade="all, delete-orphan",
    )
    
    __mapper_args__ = {
        "polymorphic_identity": "student",
    }
    

class Professor(User):
    __tablename__ = "professors"
    
    id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    department: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    
    courses: Mapped[list["Course"]] = relationship(
        back_populates="professor",
    )
    
    __mapper_args__ = {
        "polymorphic_identity": "professor",
    }
    

class Course(Base):
    __tablename__ = "courses"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    cfu: Mapped[int] = mapped_column(Integer, nullable=False)
    max_students: Mapped[int] = mapped_column(Integer, nullable=False)
    professor_id: Mapped[int] = mapped_column(ForeignKey("professors.id", ondelete="RESTRICT"), nullable=False)
    
    professor: Mapped["Professor"] = relationship(
        back_populates="courses",
    )
    
    enrollments: Mapped[list["Enrollment"]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan",
    )
    
    __table_args__ = (
        CheckConstraint("cfu > 0", name="ck_course_cfu_positive"),
        CheckConstraint("max_students > 0", name="ck_course_max_students_positive"),
    )
    
    
class Enrollment(Base):
    __tablename__ = "enrollments"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    grade: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None)
    enrolled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    student: Mapped["Student"] = relationship(back_populates="enrollments")
    course: Mapped["Course"] = relationship(back_populates="enrollments")
    
    __table_args__ = (
        UniqueConstraint("student_id", "course_id", name="uq_student_course_enrollment"),
        CheckConstraint("grade IS NULL OR (grade >= 18 AND grade <= 31)", name="ck_enrollment_grade_range"),
    )
    