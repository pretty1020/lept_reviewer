"""
LEPT AI Reviewer - Enhanced AI Question Generation Service
Strictly aligned with PRC LEPT Board Examination format and competencies
"""

import json
from typing import List, Dict, Optional
import streamlit as st

from config.settings import QUESTIONS_PER_BATCH, EXAM_COMPONENTS


# ============== LEPT BOARD EXAM FORMAT SPECIFICATIONS ==============
# Based on actual PRC LEPT examination structure

LEPT_EXAM_FORMAT = """
LEPT BOARD EXAMINATION FORMAT:
- Multiple choice with 4 options (A, B, C, D)
- Single best answer format
- Questions test recall, comprehension, application, and analysis
- Philippine context and K-12 curriculum aligned
- Time-pressured (approximately 1 minute per question)
"""

# ============== GENERAL EDUCATION COMPETENCIES ==============
# These are foundational subject knowledge questions

GENERAL_EDUCATION_COMPETENCIES = {
    "English": {
        "topics": [
            "Subject-verb agreement", "Correct verb tenses", "Pronoun-antecedent agreement",
            "Parallel structure", "Dangling and misplaced modifiers", "Active and passive voice",
            "Direct and indirect speech", "Conditional sentences", "Idiomatic expressions",
            "Context clues and vocabulary", "Main idea and supporting details",
            "Inferences and conclusions", "Author's purpose and tone", "Fact vs opinion",
            "Figurative language (simile, metaphor, personification, hyperbole)",
            "Literary genres and elements", "Reading comprehension passages"
        ],
        "sample_stems": [
            "Which sentence is grammatically correct?",
            "Choose the correct verb form:",
            "What figure of speech is used in the sentence?",
            "The passage mainly discusses...",
            "What can be inferred from the text?"
        ]
    },
    "Filipino": {
        "topics": [
            "Paksa at panaguri", "Mga bahagi ng pananalita", "Kayarian ng pangungusap",
            "Uri ng pangungusap ayon sa gamit at kayarian", "Pagkakasunod-sunod ng pangyayari",
            "Sanhi at bunga", "Pangunahing ideya at mga detalye", "Mga tayutay",
            "Panitikang Filipino (maikling kwento, tula, dula, nobela)",
            "Mga pangunahing manunulat (Rizal, Balagtas, Bonifacio)",
            "Panahon ng panitikan (Pre-kolonyal, Kolonyal, Kontemporaryo)"
        ],
        "sample_stems": [
            "Ano ang paksa ng pangungusap?",
            "Alin ang wastong gamit ng salita?",
            "Anong tayutay ang ginamit sa pangungusap?",
            "Ano ang pangunahing ideya ng talata?"
        ]
    },
    "Mathematics": {
        "topics": [
            "Four fundamental operations", "Fractions, decimals, percentages",
            "Ratio and proportion", "Direct and inverse variation",
            "Algebraic expressions and equations", "Linear equations and inequalities",
            "Word problems", "Number sequences and patterns", "Basic statistics (mean, median, mode)",
            "Probability basics", "Geometry (area, perimeter, volume)",
            "Pythagorean theorem", "Interest (simple and compound)"
        ],
        "sample_stems": [
            "Solve for x:",
            "What is the value of...",
            "If... then what is...",
            "Find the area/perimeter/volume of..."
        ]
    },
    "Science": {
        "topics": [
            "Scientific method steps", "Matter and its properties", "Atomic structure",
            "Elements and compounds", "Chemical reactions", "Force and motion",
            "Newton's Laws", "Energy forms and transformation", "Waves and sound",
            "Light and optics", "Electricity and magnetism", "Cell structure and function",
            "Human body systems", "Ecology and ecosystems", "Earth's layers",
            "Weather and climate", "Solar system"
        ],
        "sample_stems": [
            "Which of the following best describes...",
            "What happens when...",
            "Which process is responsible for...",
            "The function of... is to..."
        ]
    },
    "Social Studies": {
        "topics": [
            "Philippine pre-colonial history", "Spanish colonization (1565-1898)",
            "Philippine Revolution and heroes", "American period", "Japanese occupation",
            "Post-war Philippines", "Martial Law era", "EDSA Revolution",
            "1987 Philippine Constitution", "Three branches of government",
            "Bill of Rights", "Local government structure", "Philippine geography",
            "ASEAN and international relations", "Economic concepts (supply, demand, GDP)",
            "Current Philippine issues"
        ],
        "sample_stems": [
            "Who was responsible for...",
            "What event led to...",
            "According to the Philippine Constitution...",
            "Which of the following is NOT..."
        ]
    }
}

# ============== PROFESSIONAL EDUCATION COMPETENCIES ==============
# These are about HOW to teach, not WHAT to teach

PROFESSIONAL_EDUCATION_COMPETENCIES = {
    "Facilitating Learning": {
        "topics": [
            "Piaget's Cognitive Development (Sensorimotor, Preoperational, Concrete, Formal)",
            "Vygotsky's Zone of Proximal Development and Scaffolding",
            "Erikson's Psychosocial Development stages",
            "Kohlberg's Moral Development (Pre-conventional, Conventional, Post-conventional)",
            "Bandura's Social Learning Theory and Self-efficacy",
            "Bruner's Discovery Learning and spiral curriculum",
            "Gardner's Multiple Intelligences (8 types)",
            "Bloom's Taxonomy (Remember, Understand, Apply, Analyze, Evaluate, Create)",
            "Maslow's Hierarchy of Needs",
            "Learning styles (Visual, Auditory, Kinesthetic)"
        ],
        "sample_stems": [
            "According to Piaget, a child in the concrete operational stage can...",
            "Vygotsky's ZPD refers to...",
            "A teacher using scaffolding would...",
            "Which level of Bloom's Taxonomy is demonstrated when..."
        ]
    },
    "Curriculum Development": {
        "topics": [
            "Tyler's Curriculum Model (Objectives, Content, Methods, Evaluation)",
            "Taba's Grassroots Model", "Subject-centered vs Learner-centered curriculum",
            "K to 12 Curriculum Framework", "Spiral Progression Approach",
            "Outcomes-Based Education (OBE)", "Competency-Based Education",
            "Curriculum alignment (written, taught, tested)",
            "Mother Tongue-Based Multilingual Education (MTB-MLE)",
            "21st Century Skills integration"
        ],
        "sample_stems": [
            "The K to 12 program aims to...",
            "Spiral progression means...",
            "In outcomes-based education, the focus is on..."
        ]
    },
    "Assessment of Learning": {
        "topics": [
            "Formative vs Summative Assessment", "Diagnostic Assessment",
            "Authentic Assessment", "Portfolio Assessment",
            "Performance-Based Assessment", "Rubrics (holistic vs analytic)",
            "Table of Specifications (TOS)", "Test validity and reliability",
            "Item analysis (difficulty index, discrimination index)",
            "Assessment OF, FOR, and AS learning",
            "DepEd grading system (Written Work, Performance Task, Quarterly Assessment)"
        ],
        "sample_stems": [
            "Formative assessment is used to...",
            "A rubric that describes levels of performance is called...",
            "Assessment FOR learning means..."
        ]
    },
    "Educational Technology": {
        "topics": [
            "TPACK Framework (Technology, Pedagogy, Content Knowledge)",
            "SAMR Model (Substitution, Augmentation, Modification, Redefinition)",
            "Blended learning", "Flipped classroom", "Online learning platforms",
            "Educational apps and software", "Digital citizenship",
            "ICT integration in teaching"
        ],
        "sample_stems": [
            "According to the SAMR model, technology at the Modification level...",
            "TPACK stands for..."
        ]
    },
    "Classroom Management": {
        "topics": [
            "Proactive vs reactive management", "Rules and routines",
            "Positive reinforcement", "Behavior modification techniques",
            "Kounin's classroom management (withitness, momentum, smoothness)",
            "Dreikurs' logical consequences", "Assertive discipline (Canter)",
            "Classroom arrangement and environment"
        ],
        "sample_stems": [
            "A teacher who demonstrates 'withitness' is able to...",
            "According to Dreikurs, logical consequences should be..."
        ]
    },
    "Philippine Education Laws": {
        "topics": [
            "RA 4670 - Magna Carta for Public School Teachers (rights, benefits)",
            "RA 7836 - Philippine Teachers Professionalization Act (licensure, CPD)",
            "RA 9155 - Governance of Basic Education Act (school-based management)",
            "RA 10533 - Enhanced Basic Education Act (K to 12)",
            "RA 10627 - Anti-Bullying Act", "RA 7877 - Anti-Sexual Harassment Act",
            "RA 7610 - Child Protection Policy", "Code of Ethics for Professional Teachers",
            "Philippine Professional Standards for Teachers (PPST) - 7 Domains"
        ],
        "sample_stems": [
            "According to RA 4670, teachers are entitled to...",
            "The PPST Domain 1 focuses on...",
            "RA 10533 mandates..."
        ]
    }
}

# ============== SPECIALIZATION COMPETENCIES ==============
# Subject-specific content knowledge

SPECIALIZATION_COMPETENCIES = {
    "English": {
        "focus": "English language, literature, and language teaching methodology",
        "topics": [
            "Advanced grammar and syntax", "Morphology and word formation",
            "Phonetics and phonology", "Semantics and pragmatics",
            "British literature (Shakespeare, Dickens, Austen)",
            "American literature (Twain, Hemingway, Fitzgerald)",
            "World literature and literary movements",
            "Literary criticism approaches", "Creative writing",
            "Second language acquisition theories", "Communicative Language Teaching (CLT)",
            "Grammar-Translation vs Direct Method", "Task-based language teaching",
            "Teaching the four macro skills (Listening, Speaking, Reading, Writing)",
            "Error correction and feedback"
        ]
    },
    "Filipino": {
        "focus": "Filipino language, Philippine literature, and Filipino teaching methodology",
        "topics": [
            "Istruktura ng wikang Filipino", "Morpolohiya at sintaksis",
            "Panitikang Filipino sa iba't ibang panahon",
            "Pre-kolonyal na panitikan (epiko, mito, alamat)",
            "Panitikan sa panahon ng Kastila (Florante at Laura, Noli Me Tangere)",
            "Panitikan sa panahon ng Amerikano at Hapon",
            "Makabagong panitikan at kontemporaryong manunulat",
            "Mga teorya sa pagtuturo ng wika", "Komunikatibong pagtuturo",
            "Pagtataya sa Filipino"
        ]
    },
    "Mathematics": {
        "focus": "Pure mathematics, applied mathematics, and mathematics education",
        "topics": [
            "Real number system and properties", "Algebraic structures (groups, rings, fields)",
            "Linear algebra (matrices, determinants, vectors)",
            "Calculus (limits, derivatives, integrals, applications)",
            "Differential equations", "Number theory",
            "Euclidean and non-Euclidean geometry", "Trigonometry and identities",
            "Analytic geometry (conic sections)", "Statistics and probability theory",
            "Discrete mathematics", "Mathematical proof techniques",
            "Problem-solving strategies (Polya's method)",
            "Mathematics curriculum and instruction", "Manipulatives and visual aids",
            "Technology in mathematics teaching", "Common mathematical misconceptions"
        ],
        "sample_questions": [
            "Find the derivative of f(x) = x³ + 2x² - 5x + 3",
            "Solve the system of linear equations...",
            "What is the integral of...",
            "In a normal distribution with mean μ and standard deviation σ...",
            "The slope of the tangent line to the curve at point P is...",
            "If A is a 3x3 matrix with determinant 5, then det(2A) = ...",
            "The sum of an infinite geometric series with |r| < 1 is..."
        ]
    },
    "Science": {
        "focus": "Natural sciences and science education",
        "topics": [
            "Cell biology and molecular biology", "Genetics and heredity",
            "Evolution and biodiversity", "Ecology and environment",
            "Human anatomy and physiology", "Organic and inorganic chemistry",
            "Stoichiometry and chemical calculations", "Thermodynamics",
            "Classical mechanics", "Electricity and magnetism",
            "Modern physics concepts", "Earth science and geology",
            "Astronomy and astrophysics", "Scientific inquiry and process skills",
            "Laboratory safety and management", "Science curriculum frameworks"
        ]
    },
    "Social Studies": {
        "focus": "History, geography, economics, political science, and social studies education",
        "topics": [
            "Philippine history (comprehensive)", "Asian history and civilizations",
            "World history major events", "Physical geography concepts",
            "Human geography and demography", "Microeconomics and macroeconomics",
            "Philippine economic development", "Political science theories",
            "Philippine government and politics", "International relations",
            "Sociology and anthropology basics", "Teaching strategies for social studies"
        ]
    },
    "Values Education": {
        "focus": "Ethics, values formation, and character education",
        "topics": [
            "Ethical theories (deontology, utilitarianism, virtue ethics)",
            "Filipino values and character", "Values clarification strategies",
            "Moral dilemma discussions", "Character education programs",
            "Peace education", "Human rights education",
            "Citizenship education", "Environmental ethics"
        ]
    },
    "Physical Education (PE)": {
        "focus": "Physical education, sports science, and health",
        "topics": [
            "Exercise physiology", "Kinesiology and biomechanics",
            "Motor learning and development", "Sports psychology",
            "Individual and dual sports rules", "Team sports rules and strategies",
            "Philippine traditional games", "Dance and rhythmic activities",
            "Health-related fitness components", "Skill-related fitness components",
            "FITT principle", "First aid and injury prevention",
            "Physical education curriculum", "Assessment in PE"
        ]
    },
    "Technology and Livelihood Education (TLE)": {
        "focus": "Technical-vocational skills and entrepreneurship",
        "topics": [
            "Entrepreneurship fundamentals", "Business plan development",
            "Marketing basics", "Financial literacy",
            "Home economics (food, clothing, shelter)",
            "Industrial arts", "Information and Communications Technology (ICT)",
            "Agricultural arts", "TESDA competency standards"
        ]
    },
    "Culture and Arts Education": {
        "focus": "Visual arts, music, and Philippine cultural heritage",
        "topics": [
            "Art elements and principles", "Philippine art history",
            "World art movements", "Music theory basics",
            "Philippine music and musicians", "World music traditions",
            "Performing arts", "Art criticism and appreciation",
            "Cultural heritage preservation"
        ]
    },
    "Early Childhood Education (ECE)": {
        "focus": "Early childhood development and education",
        "topics": [
            "Child development 0-8 years", "Play-based learning",
            "Developmentally Appropriate Practice (DAP)",
            "Montessori method", "Reggio Emilia approach",
            "HighScope curriculum", "Early literacy development",
            "Early numeracy development", "Social-emotional development",
            "Parent and family involvement", "Assessment in early childhood"
        ]
    },
    "Special Needs Education (SNE)": {
        "focus": "Special education and inclusive practices",
        "topics": [
            "Categories of exceptionalities", "Intellectual disabilities",
            "Learning disabilities (dyslexia, dyscalculia, dysgraphia)",
            "Autism Spectrum Disorder", "ADHD",
            "Giftedness and talent", "Inclusive education principles",
            "Universal Design for Learning (UDL)", "IEP development",
            "Applied Behavior Analysis (ABA)", "Assistive technology",
            "Transition planning", "RA 7277 - Magna Carta for PWDs"
        ]
    },
    "General Education": {
        "focus": "Elementary education general curriculum",
        "topics": [
            "Integrated curriculum approaches", "Thematic teaching",
            "Multi-grade teaching", "Spiral curriculum implementation",
            "Teaching reading in the content areas", "Math in elementary grades",
            "Science in elementary grades", "Social Studies in elementary grades"
        ]
    }
}


def get_openai_client():
    """Get OpenAI client instance."""
    try:
        from openai import OpenAI
        
        api_key = None
        
        try:
            api_key = st.secrets["openai"]["api_key"]
        except (KeyError, TypeError):
            pass
        
        if not api_key:
            try:
                openai_secrets = st.secrets.get("openai", {})
                if openai_secrets:
                    api_key = openai_secrets.get("api_key", "")
            except Exception:
                pass
        
        if not api_key:
            try:
                api_key = st.secrets.get("OPENAI_API_KEY", "")
            except Exception:
                pass
        
        if not api_key or api_key == "sk-your-openai-api-key":
            return None
            
        return OpenAI(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize OpenAI client: {str(e)}")
        return None


def get_competencies_for_config(exam_component: str, specialization: str) -> Dict:
    """Get specific competencies based on exam configuration."""
    
    if exam_component == "general_education":
        return {
            "description": "General Education covers foundational knowledge in English, Filipino, Mathematics, Science, and Social Studies",
            "competencies": GENERAL_EDUCATION_COMPETENCIES,
            "instruction": "Generate questions covering English, Filipino, Math, Science, and Social Studies fundamentals"
        }
    
    elif exam_component == "professional_education":
        return {
            "description": "Professional Education covers teaching principles, learning theories, curriculum, assessment, and education laws",
            "competencies": PROFESSIONAL_EDUCATION_COMPETENCIES,
            "instruction": "Generate questions about educational theories, classroom management, assessment, and Philippine education laws"
        }
    
    elif exam_component == "specialization":
        spec_data = SPECIALIZATION_COMPETENCIES.get(specialization, {})
        return {
            "description": f"Specialization in {specialization}: {spec_data.get('focus', 'Subject-specific content')}",
            "competencies": {specialization: spec_data},
            "instruction": f"Generate questions ONLY about {specialization}. Do NOT include questions from other subjects."
        }
    
    return {}


def build_topics_list(competencies: Dict) -> str:
    """Build a formatted list of topics from competencies."""
    topics_text = []
    
    for area, data in competencies.items():
        if isinstance(data, dict):
            topics = data.get("topics", [])
            if topics:
                topics_text.append(f"\n{area}:")
                for topic in topics[:15]:  # Limit topics
                    topics_text.append(f"  • {topic}")
    
    return "\n".join(topics_text)


def generate_questions(
    exam_type: str,
    specialization: Optional[str],
    difficulty: str,
    document_text: str,
    num_questions: int = QUESTIONS_PER_BATCH,
    education_level: str = "secondary"
) -> List[Dict]:
    """
    Generate LEPT board exam questions strictly aligned with exam configuration.
    Uses official LEPT competencies and format.
    """
    client = get_openai_client()
    if client is None:
        st.error("OpenAI API key not configured. Please check your secrets.")
        return []
    
    # Get exam component details
    exam_info = EXAM_COMPONENTS.get(exam_type, {})
    exam_name = exam_info.get("name", exam_type)
    
    # Get competencies for this specific configuration
    config_data = get_competencies_for_config(exam_type, specialization or "General Education")
    competencies = config_data.get("competencies", {})
    config_instruction = config_data.get("instruction", "")
    
    # Build topics list
    topics_list = build_topics_list(competencies)
    
    # Education level context
    level_name = "Elementary (BEEd)" if education_level == "elementary" else "Secondary (BSEd)"
    
    # Handle document context
    doc_instruction = ""
    if document_text and len(document_text.strip()) > 200:
        from services.document_processor import truncate_text_for_ai
        truncated = truncate_text_for_ai(document_text, max_chars=6000)
        doc_instruction = f"""
UPLOADED DOCUMENT (Use ONLY if directly relevant to {exam_name}):
{truncated}

CRITICAL: If this document is NOT about {exam_name} or {specialization if specialization else 'the selected component'}, 
COMPLETELY IGNORE IT and generate questions using official LEPT competencies instead.
"""

    # Specialization-specific strict instruction
    spec_strict = ""
    if exam_type == "specialization" and specialization:
        spec_strict = f"""
⚠️ STRICT REQUIREMENT FOR SPECIALIZATION:
You are generating questions for {specialization} SPECIALIZATION.
- Generate ONLY {specialization} content questions
- Do NOT include questions about teaching methods (that's Professional Education)
- Do NOT include questions about other subjects
- Focus on {specialization} subject matter expertise

{"For MATHEMATICS specialization: Generate pure math questions - algebra, calculus, geometry, statistics, number theory, etc." if specialization == "Mathematics" else ""}
{"For ENGLISH specialization: Generate English language and literature questions - grammar, literature, linguistics, etc." if specialization == "English" else ""}
{"For SCIENCE specialization: Generate science content questions - biology, chemistry, physics, earth science, etc." if specialization == "Science" else ""}
{"For FILIPINO specialization: Generate Filipino language and literature questions - gramatika, panitikan, retorika, etc." if specialization == "Filipino" else ""}
"""

    prompt = f"""You are an official question writer for the Philippine Licensure Examination for Professional Teachers (LEPT) administered by the Professional Regulation Commission (PRC).

═══════════════════════════════════════════════════════════
EXAM CONFIGURATION (MUST FOLLOW EXACTLY)
═══════════════════════════════════════════════════════════
• Education Level: {level_name}
• Exam Component: {exam_name}
• Specialization: {specialization if specialization else "N/A"}
• Difficulty: {difficulty}
• Number of Questions: {num_questions}

{spec_strict}

═══════════════════════════════════════════════════════════
{config_instruction}
═══════════════════════════════════════════════════════════

OFFICIAL LEPT COMPETENCIES AND TOPICS:
{topics_list}

{doc_instruction}

═══════════════════════════════════════════════════════════
LEPT BOARD EXAM QUESTION FORMAT
═══════════════════════════════════════════════════════════

Question Format Requirements:
1. Clear, concise question stem (no unnecessary words)
2. Four options (A, B, C, D) - only ONE correct answer
3. Options should be plausible (no obviously wrong answers)
4. Consistent grammatical structure across options
5. Options of similar length
6. Avoid "All of the above" or "None of the above"
7. No negative questions unless necessary (avoid "NOT", "EXCEPT")

Difficulty Guidelines:
• EASY: Direct recall, definitions, basic facts
• MEDIUM: Application, comprehension, comparing concepts
• HARD: Analysis, synthesis, case-based scenarios, problem-solving

═══════════════════════════════════════════════════════════
GENERATE {num_questions} QUESTIONS
═══════════════════════════════════════════════════════════

Return ONLY a valid JSON array:
[
  {{
    "question": "Question text here?",
    "options": {{
      "A": "First option",
      "B": "Second option",
      "C": "Third option",
      "D": "Fourth option"
    }},
    "correct_answer": "B",
    "explanation": "Brief explanation of why B is correct."
  }}
]

Generate exactly {num_questions} questions. Return ONLY valid JSON, no other text."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"""You are an official LEPT board exam question writer for the Philippine PRC.
                    
Your expertise:
- Philippine education system and K-12 curriculum
- LEPT exam format and competencies
- {"General Education subjects (English, Filipino, Math, Science, Social Studies)" if exam_type == "general_education" else ""}
- {"Professional Education (learning theories, curriculum, assessment, education laws)" if exam_type == "professional_education" else ""}
- {f"{specialization} content and pedagogy" if exam_type == "specialization" and specialization else ""}

CRITICAL RULES:
1. Generate questions ONLY for the specified exam component
2. For Specialization: Generate ONLY subject-specific content questions
3. Match the exact difficulty level requested
4. Use official LEPT competencies as reference
5. Follow Philippine education context
6. Return ONLY valid JSON"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        response_text = response.choices[0].message.content.strip()
        questions = parse_questions_response(response_text)
        
        if not questions:
            st.error("Failed to parse AI response. Please try again.")
            return []
        
        validated = validate_questions(questions)
        
        if len(validated) < num_questions:
            st.warning(f"Generated {len(validated)} of {num_questions} questions.")
        
        return validated
        
    except Exception as e:
        st.error(f"Error generating questions: {str(e)}")
        return []


def parse_questions_response(response_text: str) -> List[Dict]:
    """Parse AI response to extract questions."""
    # Try direct JSON parse
    try:
        questions = json.loads(response_text)
        if isinstance(questions, list):
            return questions
    except json.JSONDecodeError:
        pass
    
    # Find JSON array in response
    try:
        start = response_text.find('[')
        end = response_text.rfind(']') + 1
        if start != -1 and end > start:
            json_str = response_text[start:end]
            questions = json.loads(json_str)
            if isinstance(questions, list):
                return questions
    except json.JSONDecodeError:
        pass
    
    # Clean markdown code blocks
    try:
        cleaned = response_text.replace("```json", "").replace("```", "").strip()
        questions = json.loads(cleaned)
        if isinstance(questions, list):
            return questions
    except json.JSONDecodeError:
        pass
    
    return []


def validate_questions(questions: List[Dict]) -> List[Dict]:
    """Validate and clean question data."""
    validated = []
    
    for q in questions:
        if not isinstance(q, dict):
            continue
        
        if not q.get("question"):
            continue
        
        options = q.get("options", {})
        if not isinstance(options, dict):
            continue
        
        required = {"A", "B", "C", "D"}
        if not required.issubset(set(options.keys())):
            continue
        
        correct = str(q.get("correct_answer", "")).upper()
        if correct not in required:
            continue
        
        validated_q = {
            "question": str(q["question"]).strip(),
            "options": {
                "A": str(options.get("A", "")).strip(),
                "B": str(options.get("B", "")).strip(),
                "C": str(options.get("C", "")).strip(),
                "D": str(options.get("D", "")).strip()
            },
            "correct_answer": correct,
            "explanation": str(q.get("explanation", "")).strip() or "See your reviewer for explanation."
        }
        
        # Skip if any option is empty
        if all(validated_q["options"].values()):
            validated.append(validated_q)
    
    return validated


def generate_sample_questions(exam_type: str, specialization: Optional[str], difficulty: str) -> List[Dict]:
    """Generate questions using LEPT competencies (no document)."""
    return generate_questions(
        exam_type=exam_type,
        specialization=specialization,
        difficulty=difficulty,
        document_text="",
        num_questions=QUESTIONS_PER_BATCH
    )
