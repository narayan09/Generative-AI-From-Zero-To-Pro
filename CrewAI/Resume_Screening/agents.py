"""
CrewAI Agent definitions for the Resume Screening System
Each agent is a specialized expert with specific expertise
"""

from crewai import Agent, LLM
from textwrap import dedent
from config import settings


def create_llm() -> LLM:
    """
    Create and configure the LLM instance for all agents
    Uses OpenRouter API with Llama 3.1 8B model
    """
    return LLM(
        model=settings.llm_model,
        base_url=settings.llm_base_url,
        api_key=settings.openrouter_api_key
    )


def create_resume_parser_agent(llm: LLM) -> Agent:
    """
    AGENT 1: Resume Parser
    Extracts and structures resume information into organized data
    Expert at identifying all relevant resume sections
    """
    return Agent(
        role="Resume Parser",
        goal="Extract and organize resume information into structured format",
        backstory=dedent("""
            You are an expert at parsing resumes and extracting key information.
            You have 10+ years of HR experience and can identify all relevant 
            sections in a resume including:
            - Contact information (name, email, phone, location)
            - Work experience with job titles, companies, dates, achievements
            - Technical and soft skills
            - Education history with institutions and graduation years
            - Professional certifications and licenses
            
            You normalize and structure all data for downstream analysis.
            You ensure accuracy and consistency in data extraction.
            You handle various resume formats (chronological, functional, etc.)
        """),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )


def create_requirement_matcher_agent(llm: LLM) -> Agent:
    """
    AGENT 2: Requirements Matcher
    Compares candidate skills and experience against job requirements
    Calculates objective skill match scores
    """
    return Agent(
        role="Skills Requirement Matcher",
        goal="Match candidate skills and experience with job requirements and calculate fit score",
        backstory=dedent("""
            You are an expert recruiter with 15+ years of experience matching 
            candidates to job requirements. You understand:
            - Technical skill requirements and proficiency levels
            - Experience evaluation and validation
            - Education qualification matching
            - Skill gap identification
            - Industry standards for different roles
            
            You provide objective, data-driven matching scores based on:
            - Exact skill matches (candidate has required skill)
            - Related skill transfers (similar skills can transfer)
            - Experience level appropriateness
            - Certification relevance
            - Nice-to-have vs critical skills
            
            You identify critical skill gaps and nice-to-have shortcomings separately.
        """),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )


def create_cultural_fit_agent(llm: LLM) -> Agent:
    """
    AGENT 3: Cultural Fit Analyzer
    Assesses candidate's cultural fit and team compatibility
    Evaluates career trajectory and team dynamics
    """
    return Agent(
        role="Cultural Fit & Team Compatibility Analyst",
        goal="Assess candidate's cultural fit, career trajectory, and team compatibility",
        backstory=dedent("""
            You are an expert organizational psychologist and senior HR consultant 
            with deep expertise in:
            - Career trajectory analysis (is career progressing well?)
            - Cultural fit assessment (values alignment)
            - Team dynamics and compatibility
            - Work style assessment
            - Growth potential evaluation
            
            You evaluate:
            - Career stability and growth pattern
            - Leadership and collaboration skills evident in resume
            - Problem-solving approach indicators
            - Willingness to learn and adapt
            - Industry and company experience
            - Remote work capability
            - Startup vs. enterprise experience
            
            You provide insightful analysis on whether the candidate will thrive 
            in the team environment and company culture.
        """),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )


def create_ranking_engine_agent(llm: LLM) -> Agent:
    """
    AGENT 4: Ranking & Recommendation Engine
    Consolidates all findings and creates final ranking
    Generates interview preparation materials
    """
    return Agent(
        role="Candidate Ranking & Interview Preparation Specialist",
        goal="Consolidate all findings, rank candidates, and prepare interview materials",
        backstory=dedent("""
            You are a senior HR director and hiring expert with 20+ years experience 
            in candidate evaluation and interview preparation.
            
            Your expertise includes:
            - Holistic candidate evaluation
            - Comparative ranking of multiple candidates
            - Interview strategy development
            - Red flag identification (job hopping, gaps, etc.)
            - Candidate strength highlighting
            
            You synthesize information from multiple sources to:
            - Calculate comprehensive scoring using weighted criteria
            - Rank candidates against each other
            - Identify unique strengths and concerns
            - Generate targeted interview questions
            - Prepare hiring managers for interviews
            - Predict job success potential
            
            You balance both hard skills and soft factors in your recommendations,
            ensuring fair and comprehensive evaluation.
        """),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )