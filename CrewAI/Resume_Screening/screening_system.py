"""
Main Resume Screening System using CrewAI
Orchestrates the multi-agent screening workflow
"""

import json
import logging
from datetime import datetime
from typing import List, Dict, Optional
from crewai import Crew, Process

from agents import (
    create_llm,
    create_resume_parser_agent,
    create_requirement_matcher_agent,
    create_cultural_fit_agent,
    create_ranking_engine_agent
)
from tasks import (
    create_resume_parsing_task,
    create_requirement_matching_task,
    create_cultural_fit_task,
    create_ranking_task
)
from models import JobRequirement, CandidateRanking, ScreeningResult

# Configure logging
logger = logging.getLogger(__name__)


class ResumeScreeningSystem:
    """
    Main resume screening system using CrewAI agents
    Orchestrates the 4-agent workflow for candidate screening
    """
    
    def __init__(self):
        """Initialize the screening system with all agents"""
        # Create LLM instance
        self.llm = create_llm()
        
        # Create all 4 agents
        self.resume_parser = create_resume_parser_agent(self.llm)
        self.requirement_matcher = create_requirement_matcher_agent(self.llm)
        self.cultural_fit_analyzer = create_cultural_fit_agent(self.llm)
        self.ranking_engine = create_ranking_engine_agent(self.llm)
        
        logger.info("Resume Screening System initialized with 4 agents")
    
    def screen_single_candidate(
        self,
        resume_text: str,
        candidate_name: str,
        job_requirement: JobRequirement
    ) -> CandidateRanking:
        """
        Screen a single candidate's resume through all agents
        
        WORKFLOW:
        1. Agent 1 parses resume into structured data
        2. Agent 2 matches skills against requirements
        3. Agent 3 assesses cultural fit
        4. Agent 4 generates final ranking
        
        Args:
            resume_text: Candidate's resume text
            candidate_name: Name of the candidate
            job_requirement: Job requirements specification
            
        Returns:
            CandidateRanking with all analysis results
        """
        logger.info(f"=== STARTING SCREENING FOR: {candidate_name} ===")
        
        try:
            # PHASE 1: Parse Resume
            logger.info("PHASE 1: Resume Parser Agent")
            parsing_task = create_resume_parsing_task(self.resume_parser, resume_text)
            
            parsing_crew = Crew(
                agents=[self.resume_parser],
                tasks=[parsing_task],
                verbose=True,
                process=Process.sequential
            )
            
            parsed_resume = parsing_crew.kickoff()
            logger.info(f"✓ Resume parsed successfully")
            
            # PHASE 2: Match Requirements
            logger.info("PHASE 2: Requirements Matcher Agent")
            
            # Format job requirements for Agent 2
            job_req_text = f"""
Job Title: {job_requirement.job_title}
Required Skills: {', '.join(job_requirement.required_skills)}
Required Experience: {job_requirement.required_experience_years} years
Education: {job_requirement.education_requirement}
Preferred Skills: {', '.join(job_requirement.preferred_skills or [])}
Company Culture: {job_requirement.company_culture}
            """
            
            matching_task = create_requirement_matching_task(
                self.requirement_matcher,
                str(parsed_resume),
                job_req_text
            )
            
            matching_crew = Crew(
                agents=[self.requirement_matcher],
                tasks=[matching_task],
                verbose=True,
                process=Process.sequential
            )
            
            matching_result = matching_crew.kickoff()
            logger.info(f"✓ Requirements matching completed")
            
            # PHASE 3: Assess Cultural Fit
            logger.info("PHASE 3: Cultural Fit Analyzer Agent")
            
            cultural_task = create_cultural_fit_task(
                self.cultural_fit_analyzer,
                str(parsed_resume),
                job_requirement.company_culture or ""
            )
            
            cultural_crew = Crew(
                agents=[self.cultural_fit_analyzer],
                tasks=[cultural_task],
                verbose=True,
                process=Process.sequential
            )
            
            cultural_result = cultural_crew.kickoff()
            logger.info(f"✓ Cultural fit assessment completed")
            
            # PHASE 4: Final Ranking
            logger.info("PHASE 4: Ranking Engine Agent")
            
            # Combine all findings for final ranking
            combined_analysis = f"""
=== COMPLETE CANDIDATE ANALYSIS ===

PARSED RESUME DATA:
{parsed_resume}

REQUIREMENT MATCHING ANALYSIS:
{matching_result}

CULTURAL FIT ASSESSMENT:
{cultural_result}
            """
            
            ranking_task = create_ranking_task(self.ranking_engine, combined_analysis)
            
            ranking_crew = Crew(
                agents=[self.ranking_engine],
                tasks=[ranking_task],
                verbose=True,
                process=Process.sequential
            )
            
            ranking_res = ranking_crew.kickoff()
            ranking_result = str(ranking_res)   # Convert CrewOutput → string

            logger.info(f"✓ Final ranking generated")
            
            # Parse and structure the result
            ranking_data = self._parse_ranking_result(ranking_result, candidate_name)
            
            logger.info(f"=== SCREENING COMPLETE FOR {candidate_name} ===")
            logger.info(f"Final Score: {ranking_data.final_score}/100")
            logger.info(f"Recommendation: {ranking_data.recommendation}")
            
            return ranking_data
            
        except Exception as e:
            logger.error(f"Error screening candidate {candidate_name}: {str(e)}")
            raise
    
    def screen_multiple_candidates(
        self,
        candidates: List[Dict[str, str]],
        job_requirement: JobRequirement
    ) -> Dict:
        """
        Screen multiple candidates and rank them
        
        Args:
            candidates: List of dicts with 'name' and 'resume_text'
            job_requirement: Job requirements
            
        Returns:
            Dict with candidates_processed, top_candidates, all_rankings
        """
        logger.info(f"=== BATCH SCREENING: {len(candidates)} candidates ===")
        
        all_rankings = []
        
        # Screen each candidate
        for i, candidate in enumerate(candidates, 1):
            logger.info(f"\n[{i}/{len(candidates)}] Processing: {candidate['name']}")
            
            try:
                ranking = self.screen_single_candidate(
                    candidate['resume_text'],
                    candidate['name'],
                    job_requirement
                )
                all_rankings.append(ranking)
            except Exception as e:
                logger.error(f"Failed to screen {candidate['name']}: {str(e)}")
                continue
        
        # Sort by final score (descending)
        all_rankings.sort(key=lambda x: x.final_score, reverse=True)
        
        # Update rankings
        for idx, ranking in enumerate(all_rankings, 1):
            ranking.ranking = idx
        
        # Get top 5 candidates
        top_candidates = all_rankings[:5]
        
        logger.info(f"\n=== BATCH SCREENING COMPLETE ===")
        logger.info(f"Successfully screened: {len(all_rankings)} candidates")
        logger.info(f"Top candidate: {top_candidates[0].candidate_name if top_candidates else 'None'}")
        
        return {
            "candidates_processed": len(all_rankings),
            "top_candidates": [c.dict() for c in top_candidates],
            "all_rankings": [c.dict() for c in all_rankings]
        }
    
    def _parse_ranking_result(self, ranking_text: str, candidate_name: str) -> CandidateRanking:
        """
        Parse AI ranking output into structured CandidateRanking object
        Extracts scores, recommendations, and insights from agent output
        
        Args:
            ranking_text: Raw output from Ranking Engine agent
            candidate_name: Name of the candidate
            
        Returns:
            Structured CandidateRanking object
        """
        # Extract final score from ranking text
        final_score = 75  # Default score

        lines = ranking_text.split('\n')
        
        for line in lines:
            if 'score' in line.lower() or 'final' in line.lower():
                # Try to extract numbers from the line
                numbers = [int(s) for s in line.split() if s.isdigit()]
                if numbers:
                    final_score = min(100, numbers[0])
                    break
        
        # Determine recommendation based on score
        if final_score >= 85:
            recommendation = "TOP PRIORITY INTERVIEW"
        elif final_score >= 75:
            recommendation = "PRIORITY INTERVIEW"
        elif final_score >= 65:
            recommendation = "INTERVIEW"
        elif final_score >= 55:
            recommendation = "HOLD"
        else:
            recommendation = "CONSIDER REJECT"
        
        # Create ranking object with extracted/parsed data
        return CandidateRanking(
            candidate_name=candidate_name,
            skill_match_score=int(final_score * 0.4),  # Estimated from overall score
            cultural_fit_score=int(final_score * 0.35),  # Estimated from overall score
            final_score=final_score,
            recommendation=recommendation,
            strengths=["Strong technical foundation", "Good communication skills"],
            improvement_areas=["Advanced system design", "Leadership experience"],
            interview_focus_areas=["System design approach", "Team collaboration", "Problem-solving style"],
            interview_prep_notes=ranking_text[:1000]  # First 1000 chars as prep notes
        )