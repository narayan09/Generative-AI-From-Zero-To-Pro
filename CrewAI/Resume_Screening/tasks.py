"""
CrewAI Task definitions for the Resume Screening System
Each task is assigned to an agent and defines what to work on
"""

from crewai import Task
from textwrap import dedent


def create_resume_parsing_task(agent, resume_text: str) -> Task:
    """
    TASK 1: Parse Resume
    Agent 1 extracts structured data from raw resume text
    """
    return Task(
        description=dedent(f"""
            Parse the following resume and extract all relevant information:
            
            RESUME TEXT:
            {resume_text}
            
            Please extract and organize:
            1. **Contact Information**: Name, email, phone, location
            2. **Professional Summary**: Brief overview if present
            3. **Work Experience**: 
               - Job titles and companies
               - Employment dates (start and end)
               - Key achievements and responsibilities
               - Technologies and tools used
            4. **Technical Skills**: Programming languages, frameworks, tools
            5. **Soft Skills**: Communication, leadership, teamwork, etc.
            6. **Education**: 
               - Degrees obtained
               - University/Institution
               - Graduation year
               - GPA if mentioned
            7. **Certifications**: Professional certifications and licenses
            8. **Years of Experience**: Calculate total based on work history
            
            Provide the output as structured data with clear sections.
            Ensure accuracy and completeness.
        """),
        expected_output=dedent("""
            Structured resume data including:
            - Full name and contact details
            - Years of total experience (number)
            - Detailed work history with job titles, companies, and dates
            - Complete list of technical and soft skills
            - Education history with institutions and graduation years
            - Any professional certifications or licenses
            - Professional summary if available
        """),
        agent=agent
    )


def create_requirement_matching_task(agent, parsed_resume: str, job_requirements: str) -> Task:
    """
    TASK 2: Match Requirements
    Agent 2 compares candidate profile against job requirements
    """
    return Task(
        description=dedent(f"""
            Compare the candidate's profile with job requirements and calculate match score.
            
            CANDIDATE PROFILE:
            {parsed_resume}
            
            JOB REQUIREMENTS:
            {job_requirements}
            
            Please analyze:
            1. **Skill Matching**:
               - List all required skills
               - Mark which are matched (✓) and which are missing (✗)
               - Calculate match percentage
               - Identify critical gaps vs. nice-to-have gaps
            
            2. **Experience Evaluation**:
               - Does candidate have required years of experience?
               - Is the experience directly relevant?
               - Does candidate exceed requirements?
            
            3. **Education Assessment**:
               - Does candidate meet education requirements?
               - Are qualifications appropriate for the level?
            
            4. **Overall Fit Score**: Calculate 0-100 based on:
               - Skill match (40% weight)
               - Experience fit (35% weight)
               - Education fit (15% weight)
               - Additional qualifications (10% weight)
            
            Provide specific feedback on strengths and gaps.
        """),
        expected_output=dedent("""
            Comprehensive requirement matching analysis including:
            - List of matched skills with checkmarks
            - List of missing skills with priority levels
            - Skill match percentage (0-100%)
            - Experience fit assessment (STRONG/MEETS/BELOW)
            - Education fit assessment (EXCEEDS/MEETS/BELOW)
            - Overall match score (0-100)
            - Key strengths in required areas
            - Critical skill gaps that need addressing
            - Nice-to-have qualifications status
        """),
        agent=agent
    )


def create_cultural_fit_task(agent, candidate_profile: str, company_culture: str) -> Task:
    """
    TASK 3: Assess Cultural Fit
    Agent 3 evaluates candidate's cultural fit and team compatibility
    """
    return Task(
        description=dedent(f"""
            Assess the candidate's cultural fit and team compatibility.
            
            CANDIDATE PROFILE:
            {candidate_profile}
            
            COMPANY/TEAM CULTURE:
            {company_culture}
            
            Please evaluate:
            1. **Career Stability**:
               - Check for job hopping (frequent short-term positions)
               - Assess career progression pattern
               - Identify any career gaps
               - Is there a coherent career narrative?
            
            2. **Growth Trajectory**:
               - Is candidate showing career growth?
               - Have responsibilities increased over time?
               - Has compensation/title progressed appropriately?
               - Learning and skill development visible?
            
            3. **Leadership Experience**:
               - Does candidate have team lead/management experience?
               - Have they grown others' careers?
               - Evidence of mentoring?
            
            4. **Work Environment Fit**:
               - Startup experience (if relevant)?
               - Large company experience?
               - Remote work experience?
               - Fast-paced vs. structured environments?
               - Evidence of adaptability?
            
            5. **Team Compatibility**:
               - Collaboration and communication skills evident?
               - Problem-solving approach visible?
               - Willingness to learn and adapt?
               - References to teamwork and group projects?
            
            6. **Cultural Alignment**: 
               - Values alignment with company culture
               - Work style compatibility
               - Team dynamics fit
            
            Provide cultural fit score (0-100).
        """),
        expected_output=dedent("""
            Cultural fit analysis including:
            - Career stability assessment (Stable/Variable/Concerning)
            - Growth trajectory evaluation (Strong/Moderate/Weak)
            - Leadership experience status (Yes/Limited/No)
            - Startup experience assessment (Yes/Some/No)
            - Remote work capability (Proven/Some/Unknown)
            - Team fit assessment (STRONG/MODERATE/WEAK)
            - Cultural fit score (0-100)
            - Key cultural strengths
            - Potential cultural misalignments
            - Adaptation needs for this role
        """),
        agent=agent
    )


def create_ranking_task(agent, all_analysis: str) -> Task:
    """
    TASK 4: Final Ranking
    Agent 4 consolidates all findings and creates final ranking
    """
    return Task(
        description=dedent(f"""
            Consolidate all analysis and create final ranking with recommendations.
            
            COMPLETE CANDIDATE ANALYSIS:
            {all_analysis}
            
            Please provide:
            1. **Overall Score Calculation** (0-100):
               - Skill match (40%)
               - Experience fit (25%)
               - Cultural fit (20%)
               - Education (10%)
               - Other factors (5%)
            
            2. **Candidate Ranking**:
               - Overall final score
               - Recommendation level (TOP PRIORITY / INTERVIEW / HOLD / REJECT)
            
            3. **Key Strengths** (3-5 points):
               - Most relevant qualifications
               - Unique advantages
               - Standout accomplishments
               - Why this candidate is special
            
            4. **Improvement Areas** (2-3 points):
               - Skill gaps
               - Experience gaps
               - Areas for on-the-job training
               - Development needs
            
            5. **Interview Focus Areas** (4-5 points):
               - Key topics to explore
               - Red flags to investigate
               - Strength areas to dig deeper
               - Behavioral questions to ask
            
            6. **Red Flags Assessment**:
               - Any concerning patterns?
               - Unexplained gaps in resume?
               - Career instability?
               - Skill mismatches that are concerning?
            
            7. **Interview Preparation Notes**:
               - Background briefing for interviewer
               - Key questions to ask
               - How to assess cultural fit in interview
               - Role-specific assessment criteria
            
            Generate actionable insights for the hiring team.
        """),
        expected_output=dedent("""
            Complete ranking and recommendation report including:
            - Overall final score (0-100)
            - Recommendation (TOP PRIORITY / INTERVIEW / HOLD / REJECT)
            - 3-5 key strengths with specific examples
            - 2-3 improvement areas that need attention
            - 4-5 interview focus areas with specific questions
            - Red flags (if any) or "None" if clean profile
            - Detailed interview preparation notes for hiring manager
            - Success prediction (High/Medium/Low likelihood)
            - Next steps recommendation
        """),
        agent=agent
    )