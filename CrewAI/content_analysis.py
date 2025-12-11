"""
Content Marketing Analysis & SEO Optimization System
Multi-Agent CrewAI Application using OpenRouter

This system automates content review, SEO analysis, and optimization 
recommendations for organizations to save time on manual content marketing workflows.
"""

import os
import json
from datetime import datetime
from textwrap import dedent
from crewai import Agent, Task, Process, Crew, LLM


# Set dummy OPENAI_API_KEY (required by CrewAI internally)
os.environ["OPENAI_API_KEY"] = "sk-dummy-key-111"


# ============================================================
# LLM Configuration using OpenRouter
# ============================================================
def create_llm():
    """Create and return configured LLM instance using OpenRouter"""
    llm = LLM(
        model="openrouter/meta-llama/llama-3.1-8b-instruct",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY") 
    )
    return llm


# ============================================================
# AGENT 1: CONTENT ANALYST
# Analyzes content structure, extracts keywords, identifies topics
# ============================================================
def create_content_analyst(llm):
    """Creates Content Analyst Agent"""
    return Agent(
        role="Content Analyst",
        goal="Extract and analyze key information from content including structure, keywords, topics, and readability metrics",
        backstory=dedent("""
            You are an experienced content strategist with deep expertise in:
            - Content structure analysis
            - Keyword extraction and analysis
            - Topic identification
            - Readability assessment
            - Content gap identification
            
            Your goal is to provide comprehensive analysis of any content piece,
            identifying its strengths and areas for improvement. You look at word count,
            reading time, keyword density, and overall content architecture.
        """),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )


# ============================================================
# AGENT 2: SEO OPTIMIZER
# Analyzes and optimizes SEO elements
# ============================================================
def create_seo_optimizer(llm):
    """Creates SEO Optimizer Agent"""
    return Agent(
        role="SEO Optimization Expert",
        goal="Analyze and provide comprehensive SEO recommendations for content optimization",
        backstory=dedent("""
            You are a certified SEO specialist with 10+ years of experience in:
            - On-page SEO optimization
            - Keyword strategy and placement
            - Meta description optimization
            - Heading structure and hierarchy
            - Readability and user engagement
            - Technical SEO basics
            - Image optimization and alt text
            
            You understand Google's ranking factors and provide practical,
            actionable recommendations that directly impact search rankings.
            You balance technical SEO with user experience.
        """),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )


# ============================================================
# AGENT 3: COMPETITOR ANALYST
# Analyzes competitive landscape and identifies gaps
# ============================================================
def create_competitor_analyst(llm):
    """Creates Competitor Analyst Agent"""
    return Agent(
        role="Competitive Intelligence Analyst",
        goal="Analyze competitors and identify content gaps and opportunities",
        backstory=dedent("""
            You are a competitive intelligence expert specialized in:
            - Competitive landscape analysis
            - Content gap identification
            - Market positioning
            - Competitor benchmarking
            - Industry trends analysis
            - Unique selling proposition (USP) identification
            
            You provide insights on how the content compares to competitors,
            what opportunities are being missed, and how to differentiate.
            You focus on actionable competitive advantages.
        """),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )


# ============================================================
# AGENT 4: RECOMMENDATIONS ENGINE
# Consolidates all findings and generates prioritized recommendations
# ============================================================
def create_recommendations_engine(llm):
    """Creates Recommendations Engine Agent"""
    return Agent(
        role="Content Strategy & Recommendations Specialist",
        goal="Consolidate all analysis findings and generate prioritized, actionable recommendations with clear implementation paths",
        backstory=dedent("""
            You are a senior content strategist and project manager who:
            - Synthesizes complex information into clear, actionable steps
            - Prioritizes recommendations by impact and effort
            - Creates detailed implementation roadmaps
            - Understands ROI and business impact
            - Communicates technical concepts clearly
            
            Your strength is taking insights from multiple specialists and
            creating a cohesive strategy with clear priorities and next steps.
            You focus on quick wins, medium-term improvements, and long-term
            strategic enhancements.
        """),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )


# ============================================================
# TASK DEFINITIONS
# ============================================================
def create_tasks(agents):
    """Create all tasks for the multi-agent system"""
    
    content_analyst = agents['content_analyst']
    seo_optimizer = agents['seo_optimizer']
    competitor_analyst = agents['competitor_analyst']
    recommendations_engine = agents['recommendations_engine']
    
    # Task 1: Content Analysis
    content_analysis_task = Task(
        description=dedent("""
            Analyze the provided content and provide detailed analysis covering:
            
            1. **Content Structure Analysis**:
               - Word count and estimated reading time
               - Heading hierarchy (H1, H2, H3 distribution)
               - Paragraph length and density
               - Number of images and multimedia
            
            2. **Topic & Keyword Analysis**:
               - Main topic and sub-topics
               - Target keywords identified
               - Keyword density (if any keywords mentioned)
               - Long-tail keyword opportunities
            
            3. **Content Quality Metrics**:
               - Readability assessment (estimate based on sentence structure)
               - Writing tone and style consistency
               - Content depth and comprehensiveness
               - Unique value proposition clarity
            
            4. **Content Architecture**:
               - Introduction quality
               - Logical flow and transitions
               - Conclusion effectiveness
               - Call-to-action presence
            
            Provide structured analysis in clear bullet points.
            
            Content to analyze:
            {content}
        """),
        expected_output=dedent("""
            Comprehensive content analysis report including:
            - Content metrics (word count, reading time, structure)
            - Identified keywords and topics
            - Readability and quality assessment
            - Content architecture review
            - Key strengths and weaknesses
        """),
        agent=content_analyst
    )
    
    # Task 2: SEO Analysis
    seo_analysis_task = Task(
        description=dedent("""
            Based on the content analysis and original content, perform comprehensive SEO analysis:
            
            1. **Keyword SEO Optimization**:
               - Keyword placement quality (title, headings, first 100 words)
               - Keyword density analysis
               - LSI keywords and semantic variations
               - Keyword relevance to target audience
            
            2. **On-Page SEO Elements**:
               - Title tag optimization (should be 50-60 characters)
               - Meta description optimization (155-160 characters)
               - H1 usage (should be exactly 1 main H1)
               - Heading hierarchy (H2 and H3 structure)
            
            3. **Content Optimization**:
               - Internal linking opportunities
               - External linking quality
               - Image optimization and alt text recommendations
               - Schema markup suggestions
            
            4. **User Experience Factors**:
               - Readability score (Flesch Kincaid scale estimation)
               - Sentence and paragraph length
               - Subheading frequency (every 100-150 words)
               - Mobile-friendly formatting
            
            5. **Technical SEO**:
               - Content freshness
               - URL optimization (if provided)
               - Load time considerations
               - Structured data opportunities
            
            Provide specific, actionable optimization recommendations with impact levels.
            
            Content to analyze:
            {content}
            
            Content Analysis Results:
            {content_analysis}
        """),
        expected_output=dedent("""
            Detailed SEO analysis including:
            - On-page SEO score (0-100)
            - Keyword optimization recommendations
            - Meta description and title suggestions
            - Technical SEO improvements
            - Quick wins and longer-term optimizations
            - Specific implementation guidance
        """),
        agent=seo_optimizer
    )
    
    # Task 3: Competitor Analysis
    competitor_analysis_task = Task(
        description=dedent("""
            Perform competitive analysis based on the content analysis:
            
            1. **Content Gap Analysis**:
               - Identify missing sections or topics
               - Compare depth with competitor standards
               - Find unique positioning opportunities
               - Suggest additional angles or perspectives
            
            2. **Competitive Positioning**:
               - How unique is this content?
               - What competitor advantages exist?
               - What competitive disadvantages?
               - Where can we differentiate?
            
            3. **Market Opportunities**:
               - Underexplored angles in the topic
               - Emerging trends not covered
               - User intent gaps
               - Content format opportunities
            
            4. **Industry Benchmarking**:
               - Content length comparison
               - Update frequency best practices
               - Visual content standards
               - Engagement opportunities
            
            Focus on identifying specific, actionable opportunities where this content
            can gain competitive advantage.
            
            Content Analysis Results:
            {content_analysis}
            
            SEO Analysis Results:
            {seo_analysis}
        """),
        expected_output=dedent("""
            Competitive analysis report including:
            - Content gaps and opportunities
            - Competitive advantages and disadvantages
            - Market positioning recommendations
            - Specific topics to expand or add
            - Unique angles to explore
            - Estimated competitive strength (rating)
        """),
        agent=competitor_analyst
    )
    
    # Task 4: Generate Recommendations
    recommendations_task = Task(
        description=dedent("""
            Consolidate all analysis findings and create a comprehensive, prioritized
            recommendations report:
            
            1. **Synthesize All Findings**:
               - Combine content, SEO, and competitive analyses
               - Identify overlapping recommendations
               - Resolve conflicting priorities
            
            2. **Prioritize Recommendations**:
               - HIGH: Critical issues affecting rankings/engagement
               - MEDIUM: Important improvements with good ROI
               - LOW: Nice-to-have enhancements
            
            3. **Categorize by Type**:
               - Content improvements
               - SEO optimizations
               - Structural changes
               - User experience enhancements
            
            4. **Estimate Impact & Effort**:
               - Expected impact (traffic %, engagement %, rankings)
               - Implementation effort (minutes/hours)
               - Priority scoring (impact vs effort)
            
            5. **Create Implementation Timeline**:
               - Quick wins (do today - 1-2 hours)
               - Medium improvements (this week - 3-5 hours)
               - Strategic updates (this month - 5-8 hours)
            
            6. **Generate Final Report**:
               - Executive summary
               - Detailed recommendations list
               - Implementation roadmap
               - Expected outcomes and metrics
            
            All Analysis Results:
            {content_analysis}
            {seo_analysis}
            {competitor_analysis}
        """),
        expected_output=dedent("""
            Comprehensive recommendations report in JSON format containing:
            - Executive summary with overall SEO/content score
            - Prioritized recommendations list with:
              * Priority level (High/Medium/Low)
              * Category (Content/SEO/UX/Technical)
              * Specific recommendation
              * Expected impact
              * Effort estimation
            - Implementation timeline
            - Quick wins list
            - Expected metrics improvement
            - Success criteria
        """),
        agent=recommendations_engine
    )
    
    return {
        'content_analysis': content_analysis_task,
        'seo_analysis': seo_analysis_task,
        'competitor_analysis': competitor_analysis_task,
        'recommendations': recommendations_task
    }


# ============================================================
# MAIN CONTENT ANALYSIS FUNCTION
# ============================================================
def analyze_content(content, title="Untitled Content"):
    """
    Main function to analyze content using multi-agent system
    
    Args:
        content (str): The content to analyze
        title (str): Title of the content
    
    Returns:
        dict: Comprehensive analysis report
    """
    
    print("\n" + "="*70)
    print("🚀 CONTENT MARKETING ANALYSIS SYSTEM")
    print("="*70)
    print(f"Analyzing: {title}")
    print(f"Content Length: {len(content)} characters")
    print("="*70 + "\n")
    
    # Create LLM
    llm = create_llm()
    
    # Create agents
    agents = {
        'content_analyst': create_content_analyst(llm),
        'seo_optimizer': create_seo_optimizer(llm),
        'competitor_analyst': create_competitor_analyst(llm),
        'recommendations_engine': create_recommendations_engine(llm)
    }
    
    # Create tasks
    tasks = create_tasks(agents)
    
    # Create crew with sequential processing
    crew = Crew(
        agents=list(agents.values()),
        tasks=list(tasks.values()),
        verbose=True,
        process=Process.sequential,
        planning=True,
        planning_llm=llm,
        cache=True
    )
    
    # Prepare inputs for tasks
    inputs = {
        'content': content,
        'title': title,
        'content_analysis': '',  # Will be filled after first task
        'seo_analysis': '',      # Will be filled after second task
        'competitor_analysis': ''  # Will be filled after third task
    }
    
    print("\n📊 Starting Multi-Agent Analysis...\n")
    
    # Execute crew
    result = crew.kickoff(inputs=inputs)
    
    # Parse and format results
    analysis_report = {
        'title': title,
        'analysis_date': datetime.now().isoformat(),
        'content_length': len(content),
        'analysis_result': str(result),
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return analysis_report


# ============================================================
# DEMO: Example Content Analysis
# ============================================================
def run_demo():
    """Run demonstration with sample content"""
    
    sample_content = """
    Getting Started with Artificial Intelligence: A Beginner's Guide
    
    Artificial Intelligence (AI) has become one of the most transformative technologies 
    of our time. From virtual assistants to medical diagnosis, AI is reshaping how we live 
    and work. But what exactly is AI, and how can you get started learning about it?
    
    What is Artificial Intelligence?
    
    AI refers to computer systems designed to perform tasks that typically require human 
    intelligence. These include learning from experience, recognizing patterns, understanding 
    language, and making decisions. AI can be categorized into two main types: Narrow AI 
    (specialized for specific tasks) and General AI (hypothetical AI with human-level intelligence).
    
    Why Learn AI?
    
    The demand for AI skills is skyrocketing. Companies across industries are investing heavily 
    in AI technology. Learning AI opens doors to:
    
    1. Career opportunities in a growing field
    2. Understanding emerging technology
    3. Building innovative applications
    4. Contributing to solve real-world problems
    
    Key Concepts for Beginners
    
    To get started with AI, familiarize yourself with these core concepts:
    
    Machine Learning: Algorithms that learn from data without explicit programming
    Deep Learning: Advanced ML using neural networks
    Natural Language Processing: Teaching computers to understand human language
    Computer Vision: Enabling machines to interpret visual information
    
    Learning Resources
    
    Several excellent platforms offer beginner-friendly AI courses:
    - Online platforms like Coursera and Udemy
    - University programs
    - Self-study with textbooks
    - Hands-on projects with Python
    
    Getting Your Hands Dirty
    
    Theory is important, but practice is essential. Start with Python programming, 
    as it's the de facto language for AI. Build small projects like:
    
    - Sentiment analysis for text
    - Image classification models
    - Chatbots using NLP
    - Recommendation systems
    
    Conclusion
    
    AI is not just for researchers or tech giants. With dedication and the right resources, 
    anyone can learn AI fundamentals and build meaningful applications. Start small, 
    be consistent, and don't be afraid to experiment.
    """
    
    # Run analysis
    report = analyze_content(
        content=sample_content,
        title="Getting Started with AI: A Beginner's Guide"
    )
    
    print("\n" + "="*70)
    print("✅ ANALYSIS COMPLETE")
    print("="*70)
    print("\n📋 Analysis Report:\n")
    print(json.dumps(report, indent=2))
    
    # Save report to file
    report_filename = f"content_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_filename, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Report saved to: {report_filename}")
    
    return report


# ============================================================
# BATCH PROCESSING MODE
# ============================================================
def analyze_multiple_contents(contents_list):
    """
    Analyze multiple content pieces and generate batch report
    
    Args:
        contents_list (list): List of dicts with 'title' and 'content' keys
    
    Returns:
        list: List of analysis reports
    """
    
    print("\n" + "="*70)
    print(f"🔄 BATCH CONTENT ANALYSIS - {len(contents_list)} items")
    print("="*70 + "\n")
    
    reports = []
    
    for idx, item in enumerate(contents_list, 1):
        print(f"\n[{idx}/{len(contents_list)}] Analyzing: {item['title']}")
        report = analyze_content(item['content'], item['title'])
        reports.append(report)
    
    # Generate batch summary
    batch_summary = {
        'batch_date': datetime.now().isoformat(),
        'total_items': len(contents_list),
        'analysis_reports': reports,
        'summary': f"Completed analysis of {len(contents_list)} content pieces"
    }
    
    return batch_summary


# ============================================================
# RUN APPLICATION
# ============================================================
if __name__ == "__main__":
    """
    Execute the content analysis system
    
    Ensure OPENROUTER_API_KEY environment variable is set before running:
    export OPENROUTER_API_KEY="your-key-here"
    """
    
    # Verify API key is set
    if not os.getenv("OPENROUTER_API_KEY"):
        print("❌ Error: OPENROUTER_API_KEY environment variable not set")
        print("Please set it: export OPENROUTER_API_KEY='your-key-here'")
        exit(1)
    
    # Run demonstration
    report = run_demo()
    
    print("\n" + "="*70)
    print("📊 System Status: READY FOR PRODUCTION")
    print("="*70)
    print("\nTo analyze your own content:")
    print("  content = 'Your article text here...'")
    print("  report = analyze_content(content, title='Your Title')")
    print("\nFor batch processing:")
    print("  contents = [{'title': '...', 'content': '...'}, ...]")
    print("  batch_report = analyze_multiple_contents(contents)")
