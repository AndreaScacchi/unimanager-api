from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# --- STUDENT SCHEMAS --- #
class StudentCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=150, examples=["Mario Rossi"])
    matricola: str = Field(..., min_length=4, max_length=20, examples=["MAT2026001"])
    enrollment_year: int = Field(..., ge=1990, le=2100, examples=[2026])
    

class StudentResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    matricola: str
    enrollment_year: int
    
    model_config = ConfigDict(from_attributes=True)
    
    
# --- PROFESSOR SCHEMAS --- #
class ProfessorCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=150, examples=["Prof.ssa Elena Bianchi"])
    department: str = Field(..., min_length=2, max_length=100, examples=["Informatica"])
    title: str = Field(..., min_length=2, max_length=100, examples=["Professore Ordinario"])
    

class ProfessorResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    roel: str
    department: str
    title: str
    
    model_config = ConfigDict(from_attributes=True)
    
    
# --- COURSE SCHEMAS --- #
class CourseCreate(BaseModel):
    code: str = Field(..., min_length=2, max_length=20, examples=["INF-101"])
    title: str = Field(..., min_length=3, max_length=150, examples=["Algoritmi e Strutture Dati"])
    cfu: int = Field(..., gt=0, le=30, examples=[9])
    max_students: int = Field(..., gt=0, le=1000, examples=[120])
    professor_id: int = Field(..., gt=0, examples=[1])
    
    
class CourseResponse(BaseModel):
    id: int
    code: str
    title: str
    cfu: int
    max_students: int
    professor_id: int
    
    model_config = ConfigDict(from_attributes=True)
    
    
# --- ENROLLMENT & GRADE SCHEMAS --- #
class EnrollmentCreate(BaseModel):
    student_id: int = Field(..., gt=0, examples=[2])
    course_id: int = Field(..., gt=0, examples=[1])
    
    
class GradeUpdate(BaseModel):
    grade: Annotated[
        int,
        Field(ge=18, le=31, description="Voto da 18 a 30 (31 corrisponde a 30 e lode)", examples=[28]),
    ]
    

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    grade: int | None
    enrolled_at: datetime
    
    model_config = ConfigDict(from_attributes=True)