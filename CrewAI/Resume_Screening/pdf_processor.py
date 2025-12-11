"""
PDF processing utilities for resume extraction
Handles PDF text extraction and validation
"""

import PyPDF2
from typing import Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)


def extract_text_from_pdf(file_path: str) -> Optional[str]:
    """
    Extract text from a PDF file
    Reads all pages and combines text
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Extracted text string or None if error
    """
    try:
        text = ""
        
        # Open and read PDF
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Extract text from all pages
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            
            logger.info(f"Successfully extracted {len(text)} characters from {file_path}")
            return text
            
    except Exception as e:
        logger.error(f"Error extracting PDF: {str(e)}")
        return None


def validate_resume_text(text: str) -> bool:
    """
    Validate that extracted text looks like a resume
    Checks for minimum length and common resume keywords
    
    Args:
        text: Extracted resume text
        
    Returns:
        True if valid resume, False otherwise
    """
    # Check minimum length (resume should have substantial content)
    if len(text) < 100:
        logger.warning("Resume text too short (< 100 characters)")
        return False
    
    # Check for common resume keywords
    resume_keywords = ['experience', 'skills', 'education', 'work', 'employment']
    text_lower = text.lower()
    
    # Count how many resume keywords are present
    keyword_count = sum(1 for keyword in resume_keywords if keyword in text_lower)
    
    # Need at least 2 keywords to be a valid resume
    if keyword_count < 2:
        logger.warning("Resume text missing common resume keywords")
        return False
    
    logger.info("Resume text validated successfully")
    return True
