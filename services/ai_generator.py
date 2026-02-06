"""
LEPT AI Reviewer - AI Question Generation Service
"""

import json
from typing import List, Dict, Optional
import streamlit as st

from config.settings import QUESTIONS_PER_BATCH, EXAM_CATEGORIES, SPECIALIZATIONS


def get_openai_client():
    """Get OpenAI client instance."""
    try:
        from openai import OpenAI
        api_key = st.secrets.get("openai", {}).get("api_key", "")
        if not api_key or api_key == "sk-your-openai-api-key":
            return None
        return OpenAI(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize OpenAI client: {str(e)}")
        return None


def generate_questions(
    exam_type: str,
    specialization: Optional[str],
    difficulty: str,
    document_text: str,
    num_questions: int = QUESTIONS_PER_BATCH
) -> List[Dict]:
    """
    Generate exam questions using OpenAI based on document content.
    
    Args:
        exam_type: Type of exam (general_education, professional_education, specialization)
        specialization: Specific subject area (if exam_type is specialization)
        difficulty: Difficulty level (Easy, Medium, Hard)
        document_text: Text extracted from reviewer documents
        num_questions: Number of questions to generate
    
    Returns:
        List of question dictionaries
    """
    client = get_openai_client()
    if client is None:
        st.error("OpenAI API key not configured. Please check your secrets.")
        return []
    
    # Build the prompt
    exam_name = EXAM_CATEGORIES.get(exam_type, exam_type)
    subject_context = ""
    if exam_type == "specialization" and specialization:
        subject_context = f"Specialization Subject: {specialization}\n"
    
    # Truncate document text if too long
    from services.document_processor import truncate_text_for_ai
    truncated_text = truncate_text_for_ai(document_text, max_chars=12000)
    
    prompt = f"""You are an expert exam question generator for the Philippine Licensure Examination for Professional Teachers (LEPT).

Generate {num_questions} multiple-choice questions based on the following context:

Exam Type: {exam_name}
{subject_context}Difficulty Level: {difficulty}

REFERENCE MATERIAL:
{truncated_text}

REQUIREMENTS:
1. Each question must be directly based on the reference material provided
2. Questions should be appropriate for the {difficulty} difficulty level:
   - Easy: Basic recall and understanding
   - Medium: Application and analysis
   - Hard: Synthesis, evaluation, and complex problem-solving
3. Each question must have exactly 4 options (A, B, C, D)
4. Only ONE option should be correct
5. Include a brief explanation for the correct answer
6. Questions should be relevant to Philippine education context

RESPONSE FORMAT:
Return a JSON array with this exact structure:
[
  {{
    "question": "The question text here?",
    "options": {{
      "A": "First option",
      "B": "Second option",
      "C": "Third option",
      "D": "Fourth option"
    }},
    "correct_answer": "A",
    "explanation": "Brief explanation why A is correct..."
  }}
]

Generate exactly {num_questions} questions. Return ONLY the JSON array, no other text."""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert LEPT exam question generator. Always respond with valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        # Parse the response
        response_text = response.choices[0].message.content.strip()
        
        # Try to extract JSON from the response
        questions = parse_questions_response(response_text)
        
        if not questions:
            st.error("Failed to parse AI response. Please try again.")
            return []
        
        # Validate and clean questions
        validated_questions = validate_questions(questions)
        
        return validated_questions
        
    except Exception as e:
        st.error(f"Error generating questions: {str(e)}")
        return []


def parse_questions_response(response_text: str) -> List[Dict]:
    """
    Parse the AI response to extract questions.
    
    Args:
        response_text: Raw response from OpenAI
    
    Returns:
        List of question dictionaries
    """
    try:
        # Try direct JSON parse first
        questions = json.loads(response_text)
        if isinstance(questions, list):
            return questions
    except json.JSONDecodeError:
        pass
    
    # Try to find JSON array in the response
    try:
        start_idx = response_text.find('[')
        end_idx = response_text.rfind(']') + 1
        
        if start_idx != -1 and end_idx > start_idx:
            json_str = response_text[start_idx:end_idx]
            questions = json.loads(json_str)
            if isinstance(questions, list):
                return questions
    except json.JSONDecodeError:
        pass
    
    return []


def validate_questions(questions: List[Dict]) -> List[Dict]:
    """
    Validate and clean question data.
    
    Args:
        questions: List of question dictionaries
    
    Returns:
        List of validated question dictionaries
    """
    validated = []
    
    for q in questions:
        if not isinstance(q, dict):
            continue
        
        # Check required fields
        if "question" not in q or not q["question"]:
            continue
        
        if "options" not in q or not isinstance(q["options"], dict):
            continue
        
        # Validate options
        options = q["options"]
        required_keys = {"A", "B", "C", "D"}
        if not required_keys.issubset(set(options.keys())):
            continue
        
        # Validate correct answer
        correct = q.get("correct_answer", "").upper()
        if correct not in required_keys:
            continue
        
        # Build validated question
        validated_q = {
            "question": str(q["question"]).strip(),
            "options": {
                "A": str(options.get("A", "")).strip(),
                "B": str(options.get("B", "")).strip(),
                "C": str(options.get("C", "")).strip(),
                "D": str(options.get("D", "")).strip()
            },
            "correct_answer": correct,
            "explanation": str(q.get("explanation", "No explanation provided.")).strip()
        }
        
        # Skip if any option is empty
        if any(not v for v in validated_q["options"].values()):
            continue
        
        validated.append(validated_q)
    
    return validated


def generate_sample_questions(exam_type: str, specialization: Optional[str], difficulty: str) -> List[Dict]:
    """
    Generate sample questions without document context (for demo/testing).
    Note: This should only be used when no documents are available.
    
    Args:
        exam_type: Type of exam
        specialization: Specific subject area
        difficulty: Difficulty level
    
    Returns:
        List of sample question dictionaries
    """
    client = get_openai_client()
    if client is None:
        return []
    
    exam_name = EXAM_CATEGORIES.get(exam_type, exam_type)
    subject_context = ""
    if exam_type == "specialization" and specialization:
        subject_context = f"for the subject of {specialization}"
    
    prompt = f"""Generate 5 multiple-choice questions for the Philippine LEPT exam.

Exam Type: {exam_name} {subject_context}
Difficulty: {difficulty}

Requirements:
1. Questions should be relevant to Philippine education
2. Each question has 4 options (A, B, C, D)
3. Include correct answer and explanation

Return ONLY a JSON array:
[{{"question": "...", "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}}, "correct_answer": "A", "explanation": "..."}}]"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert LEPT exam question generator. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=3000
        )
        
        response_text = response.choices[0].message.content.strip()
        questions = parse_questions_response(response_text)
        return validate_questions(questions)
        
    except Exception as e:
        st.error(f"Error generating questions: {str(e)}")
        return []
