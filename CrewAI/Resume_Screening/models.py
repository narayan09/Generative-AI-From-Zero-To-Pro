"""
Pydantic data models for request/response validation
Defines all data structures used in the system
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class JobRequirement(BaseModel):
    """Job requirement specification for a position"""
    job_title: str  # e.g., "Senior Software Engineer"
    required_skills: List[str]  # List of required skills
    required_experience_years: int  # Years of experience needed
    education_requirement: Optional[str] = "Bachelor's degree"
    preferred_skills: Optional[List[str]] = []
    company_culture: Optional[str] = "Collaborative, innovative, fast-paced"


class ResumeInput(BaseModel):
    """Input data for resume processing"""
    candidate_name: str
    resume_text: str
    resume_source: Optional[str] = "uploaded"


class ParsedResume(BaseModel):
    """Parsed resume with structured data"""
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    summary: Optional[str] = None
    experience_years: int
    work_history: List[dict] = []
    skills: List[str] = []
    education: List[dict] = []
    certifications: List[str] = []


class SkillMatch(BaseModel):
    """Skill matching results"""
    total_required: int
    matched: int
    match_percentage: float
    gaps: List[str]
    experience_fit: str
    match_score: int


class CulturalFit(BaseModel):
    """Cultural fit assessment"""
    career_stability: str
    growth_trajectory: str
    leadership_experience: bool
    startup_experience: bool
    remote_work_experience: bool
    team_fit: str
    cultural_fit_score: int


class CandidateRanking(BaseModel):
    """Final candidate ranking and recommendation"""
    candidate_name: str
    email: Optional[str] = None
    skill_match_score: int
    cultural_fit_score: int
    final_score: int
    ranking: Optional[int] = None
    recommendation: str
    strengths: List[str] = []
    improvement_areas: List[str] = []
    interview_focus_areas: List[str] = []
    red_flags: Optional[List[str]] = []
    interview_prep_notes: str = ""


class ScreeningResult(BaseModel):
    """Complete screening result for multiple candidates"""
    job_requirement: JobRequirement
    candidates_processed: int
    processing_timestamp: datetime
    top_candidates: List[CandidateRanking]
    all_rankings: List[CandidateRanking]
    summary_report: str