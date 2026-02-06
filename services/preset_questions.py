"""
LEPT AI Reviewer - Preset Questions Database
Default questions for FREE users based on 2026 PRC LEPT Competencies
Questions are aligned to specific exam configurations
"""

import random
from typing import List, Dict

# ============== GENERAL EDUCATION (GenEd) QUESTIONS ==============
# Covers: English, Filipino, Mathematics, Science, Social Studies fundamentals
# These are foundational subject questions for ALL education levels

GENERAL_EDUCATION_QUESTIONS = {
    "easy": [
        {
            "question": "Which of the following sentences is grammatically correct?",
            "options": {
                "A": "The children plays in the park.",
                "B": "The children play in the park.",
                "C": "The children playing in the park.",
                "D": "The children is playing in the park."
            },
            "correct_answer": "B",
            "explanation": "The subject 'children' is plural, so it requires the plural verb 'play' without the 's'."
        },
        {
            "question": "Ano ang kahulugan ng salitang 'mahinahon'?",
            "options": {
                "A": "Magaspang",
                "B": "Maingay",
                "C": "Payapa at kalmado",
                "D": "Mabilis"
            },
            "correct_answer": "C",
            "explanation": "Ang 'mahinahon' ay nangangahulugang payapa, kalmado, at hindi nagmamadali."
        },
        {
            "question": "What is the value of x if 2x + 5 = 15?",
            "options": {
                "A": "5",
                "B": "10",
                "C": "7",
                "D": "3"
            },
            "correct_answer": "A",
            "explanation": "2x + 5 = 15; 2x = 15 - 5; 2x = 10; x = 5"
        },
        {
            "question": "Which planet is known as the 'Red Planet'?",
            "options": {
                "A": "Venus",
                "B": "Jupiter",
                "C": "Mars",
                "D": "Saturn"
            },
            "correct_answer": "C",
            "explanation": "Mars is called the 'Red Planet' because of its reddish appearance due to iron oxide (rust) on its surface."
        },
        {
            "question": "Who is considered the 'Father of the Filipino Nation'?",
            "options": {
                "A": "Jose Rizal",
                "B": "Andres Bonifacio",
                "C": "Emilio Aguinaldo",
                "D": "Apolinario Mabini"
            },
            "correct_answer": "B",
            "explanation": "Andres Bonifacio is considered the 'Father of the Filipino Nation' for founding the Katipunan and leading the revolution against Spain."
        },
        {
            "question": "What is the correct spelling?",
            "options": {
                "A": "Accomodate",
                "B": "Accommodate",
                "C": "Acommodate",
                "D": "Acomodate"
            },
            "correct_answer": "B",
            "explanation": "The correct spelling is 'accommodate' with double 'c' and double 'm'."
        },
        {
            "question": "What is 25% of 200?",
            "options": {
                "A": "25",
                "B": "50",
                "C": "75",
                "D": "100"
            },
            "correct_answer": "B",
            "explanation": "25% of 200 = 0.25 × 200 = 50"
        },
        {
            "question": "What is the process by which plants make their own food?",
            "options": {
                "A": "Respiration",
                "B": "Transpiration",
                "C": "Photosynthesis",
                "D": "Fermentation"
            },
            "correct_answer": "C",
            "explanation": "Photosynthesis is the process where plants use sunlight, water, and carbon dioxide to produce glucose and oxygen."
        },
        {
            "question": "What is the largest organ of the human body?",
            "options": {
                "A": "Heart",
                "B": "Liver",
                "C": "Skin",
                "D": "Brain"
            },
            "correct_answer": "C",
            "explanation": "The skin is the largest organ of the human body, covering approximately 20 square feet in adults."
        },
        {
            "question": "What is the capital city of the Philippines?",
            "options": {
                "A": "Cebu City",
                "B": "Davao City",
                "C": "Manila",
                "D": "Quezon City"
            },
            "correct_answer": "C",
            "explanation": "Manila is the capital city of the Philippines, though Quezon City is the most populous city in Metro Manila."
        },
        {
            "question": "What is the Filipino word for 'thank you'?",
            "options": {
                "A": "Paalam",
                "B": "Salamat",
                "C": "Kumusta",
                "D": "Maganda"
            },
            "correct_answer": "B",
            "explanation": "Salamat is the Filipino word for 'thank you'."
        },
        {
            "question": "How many sides does a hexagon have?",
            "options": {
                "A": "5",
                "B": "6",
                "C": "7",
                "D": "8"
            },
            "correct_answer": "B",
            "explanation": "A hexagon has 6 sides. The prefix 'hexa-' means six."
        }
    ],
    "medium": [
        {
            "question": "Which literary device is used in 'The wind whispered through the trees'?",
            "options": {
                "A": "Simile",
                "B": "Metaphor",
                "C": "Personification",
                "D": "Hyperbole"
            },
            "correct_answer": "C",
            "explanation": "Personification gives human qualities to non-human things. Here, the wind is given the human ability to whisper."
        },
        {
            "question": "Ano ang uri ng pangungusap: 'Kumain ka na ba?'",
            "options": {
                "A": "Pasalaysay",
                "B": "Patanong",
                "C": "Pautos",
                "D": "Padamdam"
            },
            "correct_answer": "B",
            "explanation": "Ang pangungusap na 'Kumain ka na ba?' ay patanong dahil nagtatanong ito at nagtatapos sa tandang pananong."
        },
        {
            "question": "If a triangle has angles of 45° and 90°, what is the third angle?",
            "options": {
                "A": "35°",
                "B": "45°",
                "C": "55°",
                "D": "65°"
            },
            "correct_answer": "B",
            "explanation": "The sum of angles in a triangle is 180°. So, 180° - 45° - 90° = 45°"
        },
        {
            "question": "The Philippine Constitution grants sovereignty to whom?",
            "options": {
                "A": "The President",
                "B": "The Congress",
                "C": "The Filipino People",
                "D": "The Supreme Court"
            },
            "correct_answer": "C",
            "explanation": "Article II, Section 1 of the 1987 Constitution states that sovereignty resides in the people."
        },
        {
            "question": "Which sentence uses the correct subject-verb agreement?",
            "options": {
                "A": "Neither the teacher nor the students was present.",
                "B": "Neither the teacher nor the students were present.",
                "C": "Neither the teacher nor the students is present.",
                "D": "Neither the teacher nor the students are present."
            },
            "correct_answer": "B",
            "explanation": "When using 'neither...nor', the verb agrees with the nearer subject. 'Students' is plural, so 'were' is correct."
        },
        {
            "question": "Solve: If 3(x - 2) = 12, what is x?",
            "options": {
                "A": "4",
                "B": "5",
                "C": "6",
                "D": "7"
            },
            "correct_answer": "C",
            "explanation": "3(x - 2) = 12; x - 2 = 4; x = 6"
        },
        {
            "question": "What is the main function of the respiratory system?",
            "options": {
                "A": "To digest food",
                "B": "To exchange oxygen and carbon dioxide",
                "C": "To pump blood",
                "D": "To filter waste"
            },
            "correct_answer": "B",
            "explanation": "The respiratory system's main function is to facilitate gas exchange - taking in oxygen and expelling carbon dioxide."
        },
        {
            "question": "Who wrote the Philippine National Anthem 'Lupang Hinirang'?",
            "options": {
                "A": "Jose Palma",
                "B": "Julian Felipe",
                "C": "Both A and B",
                "D": "Andres Bonifacio"
            },
            "correct_answer": "C",
            "explanation": "Julian Felipe composed the music, while Jose Palma wrote the Spanish lyrics which were later translated to Filipino."
        },
        {
            "question": "What fraction is equivalent to 0.75?",
            "options": {
                "A": "1/2",
                "B": "2/3",
                "C": "3/4",
                "D": "4/5"
            },
            "correct_answer": "C",
            "explanation": "0.75 = 75/100 = 3/4 when simplified."
        },
        {
            "question": "Ano ang kasingkahulugan ng salitang 'maganda'?",
            "options": {
                "A": "Pangit",
                "B": "Marilag",
                "C": "Mabaho",
                "D": "Maliit"
            },
            "correct_answer": "B",
            "explanation": "Ang 'marilag' ay kasingkahulugan ng 'maganda' na nangangahulugang may kagandahan."
        }
    ],
    "hard": [
        {
            "question": "Which of the following best exemplifies the concept of 'irony' in literature?",
            "options": {
                "A": "A fire station burning down",
                "B": "A sad person crying",
                "C": "A happy person smiling",
                "D": "A student studying hard"
            },
            "correct_answer": "A",
            "explanation": "Irony involves a contrast between expectation and reality. A fire station, meant to fight fires, burning down is ironic."
        },
        {
            "question": "What is the derivative of f(x) = 3x² + 2x - 5?",
            "options": {
                "A": "6x + 2",
                "B": "3x + 2",
                "C": "6x - 5",
                "D": "6x² + 2"
            },
            "correct_answer": "A",
            "explanation": "Using the power rule: d/dx(3x²) = 6x, d/dx(2x) = 2, d/dx(-5) = 0. So f'(x) = 6x + 2"
        },
        {
            "question": "Which principle explains why ice floats on water?",
            "options": {
                "A": "Archimedes' Principle",
                "B": "Pascal's Principle",
                "C": "Bernoulli's Principle",
                "D": "Newton's Third Law"
            },
            "correct_answer": "A",
            "explanation": "Archimedes' Principle states that buoyant force equals the weight of displaced fluid. Ice is less dense than water, so it floats."
        },
        {
            "question": "The Comprehensive Agrarian Reform Program (CARP) was enacted under which President?",
            "options": {
                "A": "Ferdinand Marcos",
                "B": "Corazon Aquino",
                "C": "Fidel Ramos",
                "D": "Joseph Estrada"
            },
            "correct_answer": "B",
            "explanation": "CARP was enacted in 1988 under President Corazon Aquino through Republic Act 6657."
        },
        {
            "question": "Ano ang tayutay na ginamit sa 'Ang kanyang mga mata ay parang bituin'?",
            "options": {
                "A": "Metapora",
                "B": "Pagtutulad (Simile)",
                "C": "Personipikasyon",
                "D": "Hayperbole"
            },
            "correct_answer": "B",
            "explanation": "Ang pagtutulad (simile) ay gumagamit ng 'parang', 'tulad ng', o 'gaya ng' upang ihambing ang dalawang bagay."
        },
        {
            "question": "What is the speed of light in a vacuum?",
            "options": {
                "A": "3 × 10⁶ m/s",
                "B": "3 × 10⁸ m/s",
                "C": "3 × 10¹⁰ m/s",
                "D": "3 × 10⁴ m/s"
            },
            "correct_answer": "B",
            "explanation": "The speed of light in a vacuum is approximately 3 × 10⁸ meters per second (about 300,000 km/s)."
        },
        {
            "question": "What is the significance of EDSA Revolution in Philippine history?",
            "options": {
                "A": "It ended Spanish colonization",
                "B": "It peacefully overthrew the Marcos dictatorship",
                "C": "It declared Philippine independence",
                "D": "It ended Japanese occupation"
            },
            "correct_answer": "B",
            "explanation": "The 1986 EDSA People Power Revolution peacefully ended the 21-year rule of Ferdinand Marcos through non-violent mass protests."
        },
        {
            "question": "In the expression log₁₀(1000), what is the value?",
            "options": {
                "A": "2",
                "B": "3",
                "C": "4",
                "D": "10"
            },
            "correct_answer": "B",
            "explanation": "log₁₀(1000) = 3 because 10³ = 1000."
        }
    ]
}

# ============== PROFESSIONAL EDUCATION (ProfEd) QUESTIONS ==============
# Covers: Teaching principles, child development, curriculum, assessment
# These apply to ALL specializations - about HOW to teach, not WHAT to teach

PROFESSIONAL_EDUCATION_QUESTIONS = {
    "easy": [
        {
            "question": "Who is known as the 'Father of Modern Education'?",
            "options": {
                "A": "John Dewey",
                "B": "Jean Piaget",
                "C": "B.F. Skinner",
                "D": "Maria Montessori"
            },
            "correct_answer": "A",
            "explanation": "John Dewey is considered the 'Father of Modern Education' for his progressive educational philosophy emphasizing experiential learning."
        },
        {
            "question": "Which of the following is a characteristic of child-centered education?",
            "options": {
                "A": "Teacher lectures while students listen",
                "B": "Students actively participate in learning",
                "C": "Emphasis on memorization",
                "D": "Strict discipline and rules"
            },
            "correct_answer": "B",
            "explanation": "Child-centered education focuses on the needs and interests of students, encouraging active participation."
        },
        {
            "question": "What does IEP stand for in special education?",
            "options": {
                "A": "Individual Education Plan",
                "B": "Inclusive Education Program",
                "C": "Integrated Educational Process",
                "D": "Individual Evaluation Protocol"
            },
            "correct_answer": "A",
            "explanation": "IEP stands for Individual Education Plan, a document developed for each student with special needs."
        },
        {
            "question": "According to Piaget, at what stage do children develop abstract thinking?",
            "options": {
                "A": "Sensorimotor",
                "B": "Preoperational",
                "C": "Concrete Operational",
                "D": "Formal Operational"
            },
            "correct_answer": "D",
            "explanation": "The Formal Operational stage (ages 12+) is when children develop abstract and hypothetical thinking."
        },
        {
            "question": "What type of assessment is given at the end of a lesson to measure learning?",
            "options": {
                "A": "Diagnostic Assessment",
                "B": "Formative Assessment",
                "C": "Summative Assessment",
                "D": "Placement Assessment"
            },
            "correct_answer": "C",
            "explanation": "Summative assessment is conducted at the end of instruction to evaluate student learning."
        },
        {
            "question": "Which learning theory emphasizes reinforcement and punishment?",
            "options": {
                "A": "Constructivism",
                "B": "Behaviorism",
                "C": "Cognitivism",
                "D": "Humanism"
            },
            "correct_answer": "B",
            "explanation": "Behaviorism, developed by B.F. Skinner, focuses on observable behaviors and uses reinforcement/punishment."
        },
        {
            "question": "What is the K to 12 program in the Philippines?",
            "options": {
                "A": "A feeding program",
                "B": "An enhanced basic education curriculum",
                "C": "A scholarship program",
                "D": "A teacher training program"
            },
            "correct_answer": "B",
            "explanation": "K to 12 refers to the enhanced basic education curriculum covering Kindergarten and 12 years of basic education."
        },
        {
            "question": "What is the primary purpose of lesson planning?",
            "options": {
                "A": "To impress the principal",
                "B": "To guide instruction and ensure learning objectives are met",
                "C": "To satisfy DepEd requirements",
                "D": "To keep students busy"
            },
            "correct_answer": "B",
            "explanation": "Lesson planning guides instruction and ensures that learning objectives are systematically achieved."
        },
        {
            "question": "What is the role of a teacher as a facilitator?",
            "options": {
                "A": "To lecture and give all the answers",
                "B": "To guide students in discovering knowledge themselves",
                "C": "To punish students who make mistakes",
                "D": "To grade papers only"
            },
            "correct_answer": "B",
            "explanation": "As a facilitator, the teacher guides and supports students in constructing their own understanding."
        },
        {
            "question": "What is formative assessment?",
            "options": {
                "A": "Assessment at the end of a semester",
                "B": "Assessment during instruction to monitor learning",
                "C": "Assessment before instruction begins",
                "D": "Assessment for college admission"
            },
            "correct_answer": "B",
            "explanation": "Formative assessment is ongoing assessment during instruction that helps teachers monitor student progress and adjust teaching."
        },
        {
            "question": "What does DepEd stand for?",
            "options": {
                "A": "Department of Educational Development",
                "B": "Department of Education",
                "C": "Division of Education",
                "D": "Department of Educational Design"
            },
            "correct_answer": "B",
            "explanation": "DepEd stands for Department of Education, the executive department of the Philippine government responsible for education."
        },
        {
            "question": "What is the main goal of inclusive education?",
            "options": {
                "A": "To separate students with disabilities",
                "B": "To provide equal education opportunities for all learners",
                "C": "To focus only on gifted students",
                "D": "To exclude difficult students"
            },
            "correct_answer": "B",
            "explanation": "Inclusive education aims to provide equal educational opportunities for all learners regardless of abilities or backgrounds."
        }
    ],
    "medium": [
        {
            "question": "According to Vygotsky, what is the Zone of Proximal Development (ZPD)?",
            "options": {
                "A": "What a child can do independently",
                "B": "What a child cannot do at all",
                "C": "The gap between what a child can do alone and with guidance",
                "D": "The physical space for learning"
            },
            "correct_answer": "C",
            "explanation": "ZPD is the difference between what a learner can do without help and what they can achieve with guidance."
        },
        {
            "question": "Which of the following best describes 'scaffolding' in teaching?",
            "options": {
                "A": "Building physical structures in classrooms",
                "B": "Providing temporary support that is gradually removed",
                "C": "Punishing students for mistakes",
                "D": "Giving students complete freedom"
            },
            "correct_answer": "B",
            "explanation": "Scaffolding is a teaching method where support is provided and gradually withdrawn as the learner gains competence."
        },
        {
            "question": "Bloom's Taxonomy lists cognitive levels. Which is the highest level?",
            "options": {
                "A": "Knowledge",
                "B": "Application",
                "C": "Analysis",
                "D": "Evaluation/Creating"
            },
            "correct_answer": "D",
            "explanation": "In the revised Bloom's Taxonomy, 'Creating' is the highest level, followed by Evaluating, Analyzing, Applying, Understanding, and Remembering."
        },
        {
            "question": "What is differentiated instruction?",
            "options": {
                "A": "Teaching all students the same way",
                "B": "Adjusting teaching to meet individual student needs",
                "C": "Separating students by ability",
                "D": "Using only one teaching method"
            },
            "correct_answer": "B",
            "explanation": "Differentiated instruction involves tailoring teaching to meet the diverse needs of learners in the classroom."
        },
        {
            "question": "Which Republic Act is known as the 'Magna Carta for Public School Teachers'?",
            "options": {
                "A": "RA 4670",
                "B": "RA 7836",
                "C": "RA 9155",
                "D": "RA 10533"
            },
            "correct_answer": "A",
            "explanation": "RA 4670 is the Magna Carta for Public School Teachers, which provides rights and benefits to teachers."
        },
        {
            "question": "What is the primary purpose of a rubric in assessment?",
            "options": {
                "A": "To confuse students",
                "B": "To provide clear criteria for evaluation",
                "C": "To make grading faster",
                "D": "To replace tests"
            },
            "correct_answer": "B",
            "explanation": "Rubrics provide clear, consistent criteria for evaluating student work, making assessment more transparent and fair."
        },
        {
            "question": "According to Gardner's Multiple Intelligences, how many types of intelligence are there?",
            "options": {
                "A": "5",
                "B": "7",
                "C": "8",
                "D": "10"
            },
            "correct_answer": "C",
            "explanation": "Howard Gardner originally proposed 7 intelligences and later added an 8th (Naturalistic Intelligence)."
        },
        {
            "question": "What teaching strategy involves students teaching other students?",
            "options": {
                "A": "Direct instruction",
                "B": "Peer tutoring",
                "C": "Lecture method",
                "D": "Drill and practice"
            },
            "correct_answer": "B",
            "explanation": "Peer tutoring involves students helping teach and support each other's learning."
        },
        {
            "question": "What is cooperative learning?",
            "options": {
                "A": "Students work individually on tasks",
                "B": "Students work in groups to achieve common goals",
                "C": "Teacher lectures while students listen",
                "D": "Competition among students"
            },
            "correct_answer": "B",
            "explanation": "Cooperative learning involves students working together in small groups to accomplish shared learning goals."
        },
        {
            "question": "What is the purpose of diagnostic assessment?",
            "options": {
                "A": "To grade students at the end of the year",
                "B": "To identify students' prior knowledge and learning gaps",
                "C": "To punish poor performers",
                "D": "To rank students"
            },
            "correct_answer": "B",
            "explanation": "Diagnostic assessment is conducted before instruction to determine students' existing knowledge, skills, and learning needs."
        },
        {
            "question": "Which Republic Act is known as the 'Enhanced Basic Education Act of 2013'?",
            "options": {
                "A": "RA 7836",
                "B": "RA 9155",
                "C": "RA 10533",
                "D": "RA 4670"
            },
            "correct_answer": "C",
            "explanation": "RA 10533, the Enhanced Basic Education Act of 2013, mandates the K to 12 Basic Education Program."
        },
        {
            "question": "What is authentic assessment?",
            "options": {
                "A": "Multiple choice tests only",
                "B": "Assessment that measures real-world application of knowledge",
                "C": "Memorization tests",
                "D": "Standardized testing"
            },
            "correct_answer": "B",
            "explanation": "Authentic assessment evaluates students' abilities to apply knowledge and skills in real-world situations."
        }
    ],
    "hard": [
        {
            "question": "Which educational philosophy believes that education should focus on the whole child?",
            "options": {
                "A": "Essentialism",
                "B": "Perennialism",
                "C": "Progressivism",
                "D": "Existentialism"
            },
            "correct_answer": "C",
            "explanation": "Progressivism, influenced by John Dewey, emphasizes educating the whole child including social and emotional development."
        },
        {
            "question": "What is the main principle of Universal Design for Learning (UDL)?",
            "options": {
                "A": "One-size-fits-all approach",
                "B": "Multiple means of engagement, representation, and expression",
                "C": "Focus only on students with disabilities",
                "D": "Using technology exclusively"
            },
            "correct_answer": "B",
            "explanation": "UDL provides multiple means of engagement, representation, and action/expression to address learner variability."
        },
        {
            "question": "According to Erikson's psychosocial theory, what is the crisis faced by adolescents?",
            "options": {
                "A": "Trust vs. Mistrust",
                "B": "Initiative vs. Guilt",
                "C": "Identity vs. Role Confusion",
                "D": "Integrity vs. Despair"
            },
            "correct_answer": "C",
            "explanation": "Adolescents (12-18 years) face the crisis of Identity vs. Role Confusion as they develop a sense of self."
        },
        {
            "question": "Which of the following is NOT a principle of constructivism?",
            "options": {
                "A": "Learning is an active process",
                "B": "Knowledge is constructed by the learner",
                "C": "Learning is passive absorption of information",
                "D": "Prior knowledge affects new learning"
            },
            "correct_answer": "C",
            "explanation": "Constructivism views learning as active, not passive. Learners construct knowledge through experiences."
        },
        {
            "question": "What is the Philippine Professional Standards for Teachers (PPST)?",
            "options": {
                "A": "A salary grading system",
                "B": "A framework defining teacher quality",
                "C": "A building code for schools",
                "D": "A retirement plan"
            },
            "correct_answer": "B",
            "explanation": "PPST defines the competencies expected of effective teachers across different career stages."
        },
        {
            "question": "Kohlberg's theory of moral development includes how many stages?",
            "options": {
                "A": "4",
                "B": "5",
                "C": "6",
                "D": "8"
            },
            "correct_answer": "C",
            "explanation": "Kohlberg proposed 6 stages of moral development grouped into 3 levels: pre-conventional, conventional, and post-conventional."
        },
        {
            "question": "What is the Code of Ethics for Professional Teachers in the Philippines?",
            "options": {
                "A": "RA 7836",
                "B": "RA 4670",
                "C": "RA 9155",
                "D": "Board Resolution No. 435"
            },
            "correct_answer": "A",
            "explanation": "RA 7836, the Philippine Teachers Professionalization Act of 1994, includes the Code of Ethics for Professional Teachers."
        },
        {
            "question": "What is Bandura's Social Learning Theory primarily about?",
            "options": {
                "A": "Learning through operant conditioning",
                "B": "Learning through observation and modeling",
                "C": "Learning through classical conditioning",
                "D": "Learning through punishment only"
            },
            "correct_answer": "B",
            "explanation": "Bandura's Social Learning Theory emphasizes that people learn by observing and imitating others' behaviors."
        },
        {
            "question": "What is the theory of Meaningful Learning associated with David Ausubel?",
            "options": {
                "A": "Learning through rote memorization",
                "B": "Connecting new information to existing knowledge structures",
                "C": "Learning through trial and error",
                "D": "Learning only through direct experience"
            },
            "correct_answer": "B",
            "explanation": "Ausubel's Meaningful Learning Theory states that new learning is most effective when connected to relevant prior knowledge."
        },
        {
            "question": "What are the domains in PPST?",
            "options": {
                "A": "5 domains",
                "B": "6 domains",
                "C": "7 domains",
                "D": "8 domains"
            },
            "correct_answer": "C",
            "explanation": "PPST has 7 domains: Content Knowledge, Learning Environment, Diversity of Learners, Curriculum and Planning, Assessment and Reporting, Community Linkages, and Personal Growth."
        }
    ]
}

# ============== SPECIALIZATION-SPECIFIC CONTENT QUESTIONS ==============
# These are SUBJECT CONTENT questions, not teaching methodology questions

SPECIALIZATION_CONTENT_QUESTIONS = {
    "Science": {
        "easy": [
            {
                "question": "What is the basic unit of life?",
                "options": {"A": "Atom", "B": "Cell", "C": "Molecule", "D": "Organ"},
                "correct_answer": "B",
                "explanation": "The cell is the basic structural and functional unit of all living organisms."
            },
            {
                "question": "What type of energy does the sun provide?",
                "options": {"A": "Mechanical energy", "B": "Chemical energy", "C": "Solar/Radiant energy", "D": "Nuclear energy"},
                "correct_answer": "C",
                "explanation": "The sun provides solar or radiant energy through electromagnetic radiation."
            },
            {
                "question": "What is the chemical symbol for water?",
                "options": {"A": "H2O", "B": "CO2", "C": "NaCl", "D": "O2"},
                "correct_answer": "A",
                "explanation": "Water is composed of two hydrogen atoms and one oxygen atom, hence H2O."
            },
            {
                "question": "Which planet is closest to the sun?",
                "options": {"A": "Venus", "B": "Earth", "C": "Mercury", "D": "Mars"},
                "correct_answer": "C",
                "explanation": "Mercury is the closest planet to the sun in our solar system."
            },
            {
                "question": "What is the function of the heart?",
                "options": {"A": "To digest food", "B": "To pump blood", "C": "To filter waste", "D": "To produce hormones"},
                "correct_answer": "B",
                "explanation": "The heart's primary function is to pump blood throughout the body."
            }
        ],
        "medium": [
            {
                "question": "What is the law of conservation of mass?",
                "options": {"A": "Mass can be created", "B": "Mass can be destroyed", "C": "Mass is neither created nor destroyed in a chemical reaction", "D": "Mass always increases"},
                "correct_answer": "C",
                "explanation": "The law of conservation of mass states that mass cannot be created or destroyed in a chemical reaction."
            },
            {
                "question": "What organelle is responsible for cellular respiration?",
                "options": {"A": "Nucleus", "B": "Ribosome", "C": "Mitochondria", "D": "Golgi body"},
                "correct_answer": "C",
                "explanation": "Mitochondria are the 'powerhouses' of the cell, responsible for cellular respiration and ATP production."
            },
            {
                "question": "What is Newton's First Law of Motion?",
                "options": {"A": "F = ma", "B": "For every action, there is an equal and opposite reaction", "C": "An object at rest stays at rest unless acted upon by a force", "D": "Energy cannot be created or destroyed"},
                "correct_answer": "C",
                "explanation": "Newton's First Law (Law of Inertia) states that an object will remain at rest or in uniform motion unless acted upon by an external force."
            },
            {
                "question": "What is the pH of a neutral solution?",
                "options": {"A": "0", "B": "7", "C": "14", "D": "1"},
                "correct_answer": "B",
                "explanation": "A neutral solution has a pH of 7. Below 7 is acidic, above 7 is basic."
            },
            {
                "question": "What type of bond is formed when electrons are shared between atoms?",
                "options": {"A": "Ionic bond", "B": "Covalent bond", "C": "Metallic bond", "D": "Hydrogen bond"},
                "correct_answer": "B",
                "explanation": "Covalent bonds are formed when atoms share electrons."
            }
        ],
        "hard": [
            {
                "question": "What is the function of mRNA in protein synthesis?",
                "options": {"A": "To store genetic information", "B": "To carry genetic instructions from DNA to ribosomes", "C": "To transport amino acids", "D": "To form ribosomes"},
                "correct_answer": "B",
                "explanation": "mRNA (messenger RNA) carries genetic instructions from DNA in the nucleus to ribosomes for protein synthesis."
            },
            {
                "question": "What is the relationship between wavelength and frequency of electromagnetic waves?",
                "options": {"A": "Directly proportional", "B": "Inversely proportional", "C": "No relationship", "D": "Equal"},
                "correct_answer": "B",
                "explanation": "Wavelength and frequency are inversely proportional. As wavelength increases, frequency decreases (c = λf)."
            },
            {
                "question": "What is the process of cell division that produces gametes?",
                "options": {"A": "Mitosis", "B": "Meiosis", "C": "Binary fission", "D": "Cytokinesis"},
                "correct_answer": "B",
                "explanation": "Meiosis is the cell division process that produces gametes (sex cells) with half the chromosome number."
            }
        ]
    },
    "Mathematics": {
        "easy": [
            {
                "question": "What is the formula for the area of a rectangle?",
                "options": {"A": "A = πr²", "B": "A = length × width", "C": "A = ½bh", "D": "A = s²"},
                "correct_answer": "B",
                "explanation": "The area of a rectangle is calculated by multiplying its length by its width."
            },
            {
                "question": "What is the value of π (pi) approximately equal to?",
                "options": {"A": "3.14", "B": "2.71", "C": "1.41", "D": "1.73"},
                "correct_answer": "A",
                "explanation": "Pi (π) is approximately equal to 3.14159, commonly rounded to 3.14."
            },
            {
                "question": "What is 15% of 80?",
                "options": {"A": "10", "B": "12", "C": "15", "D": "8"},
                "correct_answer": "B",
                "explanation": "15% of 80 = 0.15 × 80 = 12"
            },
            {
                "question": "What is the next number in the sequence: 2, 4, 8, 16, ___?",
                "options": {"A": "20", "B": "24", "C": "32", "D": "18"},
                "correct_answer": "C",
                "explanation": "This is a geometric sequence where each number is multiplied by 2. 16 × 2 = 32."
            }
        ],
        "medium": [
            {
                "question": "What is the Pythagorean theorem?",
                "options": {"A": "a + b = c", "B": "a² + b² = c²", "C": "a × b = c", "D": "a - b = c"},
                "correct_answer": "B",
                "explanation": "The Pythagorean theorem states that in a right triangle, a² + b² = c², where c is the hypotenuse."
            },
            {
                "question": "What is the slope-intercept form of a linear equation?",
                "options": {"A": "ax + by = c", "B": "y = mx + b", "C": "y - y₁ = m(x - x₁)", "D": "(y₂-y₁)/(x₂-x₁)"},
                "correct_answer": "B",
                "explanation": "The slope-intercept form is y = mx + b, where m is the slope and b is the y-intercept."
            },
            {
                "question": "What is the quadratic formula?",
                "options": {"A": "x = -b/2a", "B": "x = (-b ± √(b²-4ac))/2a", "C": "x = b² - 4ac", "D": "x = a + b + c"},
                "correct_answer": "B",
                "explanation": "The quadratic formula x = (-b ± √(b²-4ac))/2a is used to solve quadratic equations ax² + bx + c = 0."
            },
            {
                "question": "What is the sum of interior angles of a triangle?",
                "options": {"A": "90°", "B": "180°", "C": "270°", "D": "360°"},
                "correct_answer": "B",
                "explanation": "The sum of interior angles of any triangle is always 180 degrees."
            }
        ],
        "hard": [
            {
                "question": "What is the derivative of sin(x)?",
                "options": {"A": "-sin(x)", "B": "cos(x)", "C": "-cos(x)", "D": "tan(x)"},
                "correct_answer": "B",
                "explanation": "The derivative of sin(x) is cos(x). This is a fundamental calculus identity."
            },
            {
                "question": "What is the integral of 2x?",
                "options": {"A": "x²", "B": "x² + C", "C": "2", "D": "2x² + C"},
                "correct_answer": "B",
                "explanation": "The integral of 2x is x² + C, where C is the constant of integration."
            },
            {
                "question": "In a geometric sequence, if a₁ = 3 and r = 2, what is a₅?",
                "options": {"A": "24", "B": "48", "C": "96", "D": "15"},
                "correct_answer": "B",
                "explanation": "For a geometric sequence, aₙ = a₁ × r^(n-1). So a₅ = 3 × 2⁴ = 3 × 16 = 48."
            }
        ]
    },
    "English": {
        "easy": [
            {
                "question": "What is a noun?",
                "options": {"A": "An action word", "B": "A describing word", "C": "A naming word for person, place, thing, or idea", "D": "A connecting word"},
                "correct_answer": "C",
                "explanation": "A noun is a word that names a person, place, thing, or idea."
            },
            {
                "question": "Which sentence is in passive voice?",
                "options": {"A": "The cat chased the mouse.", "B": "The mouse was chased by the cat.", "C": "She runs every morning.", "D": "They built a house."},
                "correct_answer": "B",
                "explanation": "In passive voice, the subject receives the action. 'The mouse was chased by the cat' is passive."
            },
            {
                "question": "What is the plural of 'child'?",
                "options": {"A": "Childs", "B": "Children", "C": "Childes", "D": "Child's"},
                "correct_answer": "B",
                "explanation": "'Child' has an irregular plural form: 'children'."
            }
        ],
        "medium": [
            {
                "question": "What literary period does William Shakespeare belong to?",
                "options": {"A": "Victorian Era", "B": "Elizabethan Era", "C": "Romantic Period", "D": "Modern Period"},
                "correct_answer": "B",
                "explanation": "Shakespeare wrote during the Elizabethan Era (1558-1603), named after Queen Elizabeth I."
            },
            {
                "question": "What is the difference between denotation and connotation?",
                "options": {"A": "Denotation is emotional; connotation is literal", "B": "Denotation is literal meaning; connotation is associated/emotional meaning", "C": "They are the same", "D": "Connotation is found in dictionaries"},
                "correct_answer": "B",
                "explanation": "Denotation is the literal dictionary meaning, while connotation includes emotional or cultural associations."
            },
            {
                "question": "What is an oxymoron?",
                "options": {"A": "Comparing unlike things using 'like' or 'as'", "B": "Exaggeration for effect", "C": "Combining contradictory terms", "D": "Repeating initial sounds"},
                "correct_answer": "C",
                "explanation": "An oxymoron combines two contradictory terms, such as 'jumbo shrimp' or 'deafening silence'."
            }
        ],
        "hard": [
            {
                "question": "Which literary movement emphasized emotion and individualism over reason?",
                "options": {"A": "Neoclassicism", "B": "Romanticism", "C": "Realism", "D": "Modernism"},
                "correct_answer": "B",
                "explanation": "Romanticism (late 18th-19th century) emphasized emotion, imagination, and individualism over rationalism."
            },
            {
                "question": "What is the term for a word that sounds like what it describes?",
                "options": {"A": "Alliteration", "B": "Onomatopoeia", "C": "Assonance", "D": "Consonance"},
                "correct_answer": "B",
                "explanation": "Onomatopoeia refers to words that imitate sounds, like 'buzz', 'hiss', or 'splash'."
            }
        ]
    },
    "Filipino": {
        "easy": [
            {
                "question": "Ano ang pangunahing layunin ng panitikang Filipino?",
                "options": {"A": "Maglibang lamang", "B": "Magpahayag ng damdamin at kaisipan", "C": "Kumita ng pera", "D": "Maging sikat"},
                "correct_answer": "B",
                "explanation": "Ang panitikan ay nagsisilbing daluyan ng pagpapahayag ng damdamin, kaisipan, at karanasan."
            },
            {
                "question": "Ano ang tawag sa salitang may magkaparehong baybay ngunit magkaiba ang kahulugan?",
                "options": {"A": "Magkasingkahulugan", "B": "Magkasalungat", "C": "Homonym", "D": "Antonym"},
                "correct_answer": "C",
                "explanation": "Ang homonym ay mga salitang magkapareho ang baybay ngunit magkaiba ang kahulugan."
            }
        ],
        "medium": [
            {
                "question": "Sino ang itinuturing na 'Ama ng Wikang Pambansa'?",
                "options": {"A": "Jose Rizal", "B": "Manuel L. Quezon", "C": "Andres Bonifacio", "D": "Marcelo H. del Pilar"},
                "correct_answer": "B",
                "explanation": "Si Manuel L. Quezon ang itinuturing na 'Ama ng Wikang Pambansa' dahil sa kanyang pagsisikap na magkaroon ng pambansang wika."
            },
            {
                "question": "Ano ang tawag sa tayutay na nagbibigay ng katangiang pantao sa bagay na walang buhay?",
                "options": {"A": "Pagtutulad", "B": "Metapora", "C": "Personipikasyon", "D": "Hayperbole"},
                "correct_answer": "C",
                "explanation": "Ang personipikasyon ay nagbibigay ng katangiang pantao sa mga bagay na walang buhay."
            }
        ],
        "hard": [
            {
                "question": "Ano ang pinakamahalagang akda ni Jose Rizal na nagpagising sa kamalayan ng mga Pilipino?",
                "options": {"A": "Florante at Laura", "B": "Noli Me Tangere", "C": "El Filibusterismo", "D": "Parehong B at C"},
                "correct_answer": "D",
                "explanation": "Ang Noli Me Tangere at El Filibusterismo ni Rizal ay parehong nagpagising sa kamalayan ng mga Pilipino laban sa pang-aapi ng mga Kastila."
            }
        ]
    },
    "Social Studies": {
        "easy": [
            {
                "question": "What are the three branches of the Philippine government?",
                "options": {"A": "Executive, Legislative, Judicial", "B": "President, Senate, Court", "C": "National, Local, Federal", "D": "Barangay, Municipal, Provincial"},
                "correct_answer": "A",
                "explanation": "The three branches are Executive (implements laws), Legislative (makes laws), and Judicial (interprets laws)."
            },
            {
                "question": "Who was the first President of the Philippines?",
                "options": {"A": "Manuel L. Quezon", "B": "Emilio Aguinaldo", "C": "Jose Rizal", "D": "Sergio Osmeña"},
                "correct_answer": "B",
                "explanation": "Emilio Aguinaldo was the first President of the Philippines, serving from 1899-1901."
            }
        ],
        "medium": [
            {
                "question": "What economic system allows private ownership and free markets?",
                "options": {"A": "Communism", "B": "Socialism", "C": "Capitalism", "D": "Feudalism"},
                "correct_answer": "C",
                "explanation": "Capitalism is characterized by private ownership of the means of production and free market competition."
            },
            {
                "question": "What is the significance of the Treaty of Paris (1898)?",
                "options": {"A": "It granted Philippine independence", "B": "Spain ceded the Philippines to the United States", "C": "It ended World War II", "D": "It established the Philippine Republic"},
                "correct_answer": "B",
                "explanation": "The Treaty of Paris ended the Spanish-American War, with Spain ceding the Philippines to the US for $20 million."
            }
        ],
        "hard": [
            {
                "question": "What does ASEAN stand for?",
                "options": {"A": "Asian Social and Economic Alliance Network", "B": "Association of Southeast Asian Nations", "C": "Allied States of East Asian Nations", "D": "Asian Security and Economic Agreement Network"},
                "correct_answer": "B",
                "explanation": "ASEAN stands for Association of Southeast Asian Nations, founded in 1967."
            }
        ]
    },
    "Values Education": {
        "easy": [
            {
                "question": "What Filipino value emphasizes respect for elders?",
                "options": {"A": "Bayanihan", "B": "Pagmamano", "C": "Pakikisama", "D": "Utang na loob"},
                "correct_answer": "B",
                "explanation": "Pagmamano (blessing from elders) is a Filipino gesture showing respect for older people."
            },
            {
                "question": "What is the meaning of 'bayanihan'?",
                "options": {"A": "Individual achievement", "B": "Community cooperation and helping neighbors", "C": "Government assistance", "D": "Religious devotion"},
                "correct_answer": "B",
                "explanation": "Bayanihan refers to the Filipino spirit of communal unity and cooperation."
            }
        ],
        "medium": [
            {
                "question": "According to Kohlberg, at which level do people follow rules to gain approval?",
                "options": {"A": "Pre-conventional level", "B": "Conventional level", "C": "Post-conventional level", "D": "Universal level"},
                "correct_answer": "B",
                "explanation": "At the conventional level, individuals follow rules to maintain social order and gain approval from others."
            }
        ],
        "hard": [
            {
                "question": "What is the highest level in Maslow's hierarchy of needs?",
                "options": {"A": "Safety needs", "B": "Belongingness", "C": "Esteem", "D": "Self-actualization"},
                "correct_answer": "D",
                "explanation": "Self-actualization is the highest level, representing the need to fulfill one's potential."
            }
        ]
    },
    "Physical Education (PE)": {
        "easy": [
            {
                "question": "What is the primary benefit of regular physical activity?",
                "options": {"A": "Improved physical and mental health", "B": "Becoming famous", "C": "Avoiding homework", "D": "Staying indoors"},
                "correct_answer": "A",
                "explanation": "Regular physical activity improves cardiovascular health, strength, flexibility, and mental well-being."
            }
        ],
        "medium": [
            {
                "question": "What are the components of health-related fitness?",
                "options": {"A": "Speed, agility, power", "B": "Cardiovascular endurance, muscular strength, flexibility, body composition, muscular endurance", "C": "Balance, coordination, reaction time", "D": "Running, jumping, throwing"},
                "correct_answer": "B",
                "explanation": "Health-related fitness includes cardiovascular endurance, muscular strength, muscular endurance, flexibility, and body composition."
            },
            {
                "question": "What is the FITT principle?",
                "options": {"A": "Fast, Intense, Tough, Tiring", "B": "Frequency, Intensity, Time, Type", "C": "Fun, Interesting, Thrilling, Therapeutic", "D": "Fit, Important, Trendy, Tested"},
                "correct_answer": "B",
                "explanation": "FITT stands for Frequency, Intensity, Time, and Type - key principles for exercise programs."
            }
        ],
        "hard": [
            {
                "question": "What is the target heart rate zone for moderate exercise?",
                "options": {"A": "50-70% of maximum heart rate", "B": "70-85% of maximum heart rate", "C": "85-95% of maximum heart rate", "D": "30-50% of maximum heart rate"},
                "correct_answer": "A",
                "explanation": "Moderate exercise is typically performed at 50-70% of maximum heart rate."
            }
        ]
    },
    "Technology and Livelihood Education (TLE)": {
        "easy": [
            {
                "question": "What is the primary goal of TLE education?",
                "options": {"A": "Academic excellence only", "B": "Developing practical and vocational skills", "C": "Sports training", "D": "Art appreciation"},
                "correct_answer": "B",
                "explanation": "TLE aims to develop practical, vocational, and entrepreneurial skills for livelihood."
            }
        ],
        "medium": [
            {
                "question": "What does TESDA stand for?",
                "options": {"A": "Technical Education and Skills Development Authority", "B": "Teacher Education Standards Development Agency", "C": "Technology and Engineering Skills Department Authority", "D": "Training and Employment Services Development Authority"},
                "correct_answer": "A",
                "explanation": "TESDA stands for Technical Education and Skills Development Authority."
            }
        ],
        "hard": [
            {
                "question": "What is the purpose of a business plan in entrepreneurship?",
                "options": {"A": "To impress friends", "B": "To serve as a roadmap for business operations and secure funding", "C": "To fulfill government requirements only", "D": "To avoid paying taxes"},
                "correct_answer": "B",
                "explanation": "A business plan serves as a strategic roadmap for business operations and is essential for securing funding."
            }
        ]
    },
    "Culture and Arts Education": {
        "easy": [
            {
                "question": "What is the national dance of the Philippines?",
                "options": {"A": "Tinikling", "B": "Carinosa", "C": "Pandanggo sa Ilaw", "D": "Maglalatik"},
                "correct_answer": "A",
                "explanation": "Tinikling is considered the national dance of the Philippines."
            }
        ],
        "medium": [
            {
                "question": "Who painted the famous 'Spoliarium'?",
                "options": {"A": "Fernando Amorsolo", "B": "Juan Luna", "C": "Damian Domingo", "D": "Felix Resurreccion Hidalgo"},
                "correct_answer": "B",
                "explanation": "Juan Luna painted the famous 'Spoliarium' which won the gold medal at the Madrid Exposition in 1884."
            }
        ],
        "hard": [
            {
                "question": "What artistic movement influenced Juan Luna's 'Spoliarium'?",
                "options": {"A": "Impressionism", "B": "Romanticism and Realism", "C": "Cubism", "D": "Abstract Expressionism"},
                "correct_answer": "B",
                "explanation": "Luna's 'Spoliarium' was influenced by Romanticism and Realism."
            }
        ]
    },
    "Early Childhood Education (ECE)": {
        "easy": [
            {
                "question": "What is the recommended age range for Early Childhood Education?",
                "options": {"A": "0-3 years", "B": "0-8 years", "C": "3-6 years", "D": "6-12 years"},
                "correct_answer": "B",
                "explanation": "ECE typically covers children from birth to 8 years old."
            }
        ],
        "medium": [
            {
                "question": "What is the primary focus of the Montessori method?",
                "options": {"A": "Teacher-directed learning", "B": "Child-led learning with prepared environment", "C": "Memorization and drills", "D": "Competitive activities"},
                "correct_answer": "B",
                "explanation": "Montessori emphasizes child-led learning in a carefully prepared environment."
            }
        ],
        "hard": [
            {
                "question": "What does the Reggio Emilia approach consider as the 'third teacher'?",
                "options": {"A": "The parent", "B": "Technology", "C": "The environment", "D": "Textbooks"},
                "correct_answer": "C",
                "explanation": "In Reggio Emilia, the environment is considered the 'third teacher'."
            }
        ]
    },
    "Special Needs Education (SNE)": {
        "easy": [
            {
                "question": "What does SPED stand for?",
                "options": {"A": "Special Physical Education Department", "B": "Special Education", "C": "Standard Pedagogy and Education", "D": "Student Performance Evaluation Data"},
                "correct_answer": "B",
                "explanation": "SPED stands for Special Education."
            }
        ],
        "medium": [
            {
                "question": "What is the main goal of inclusive education?",
                "options": {"A": "Separating students with disabilities", "B": "Including all students in regular classrooms", "C": "Creating special schools only", "D": "Limiting enrollment"},
                "correct_answer": "B",
                "explanation": "Inclusive education aims to include all learners, including those with disabilities, in regular classrooms."
            }
        ],
        "hard": [
            {
                "question": "What is Applied Behavior Analysis (ABA) primarily used for?",
                "options": {"A": "Teaching mathematics", "B": "Intervention for autism spectrum disorder", "C": "Physical therapy", "D": "Speech therapy only"},
                "correct_answer": "B",
                "explanation": "ABA is an evidence-based intervention commonly used for children with autism spectrum disorder."
            }
        ]
    },
    "General Education": {
        "easy": [
            {
                "question": "What is the spiral approach in curriculum?",
                "options": {"A": "Teaching topics once and moving on", "B": "Revisiting topics with increasing complexity", "C": "Teaching in circles", "D": "Random topic selection"},
                "correct_answer": "B",
                "explanation": "The spiral approach revisits topics repeatedly with greater depth each time."
            }
        ],
        "medium": [
            {
                "question": "What is thematic instruction?",
                "options": {"A": "Teaching subjects separately", "B": "Integrating subjects around a central theme", "C": "Using textbooks only", "D": "Focusing on one subject"},
                "correct_answer": "B",
                "explanation": "Thematic instruction integrates multiple subjects around a central theme."
            }
        ],
        "hard": [
            {
                "question": "According to MTB-MLE policy, what is the medium of instruction for K-3?",
                "options": {"A": "English only", "B": "Filipino only", "C": "Mother Tongue", "D": "Any foreign language"},
                "correct_answer": "C",
                "explanation": "MTB-MLE uses the learner's mother tongue as the primary medium of instruction for K-3."
            }
        ]
    }
}


def get_aligned_preset_questions(
    education_level: str,
    exam_component: str,
    specialization: str,
    difficulty: str = "Medium",
    num_questions: int = 5
) -> List[Dict]:
    """
    Get preset questions that are properly aligned to the exam configuration.
    
    - General Education: Returns GenEd questions (foundational subjects)
    - Professional Education: Returns ProfEd questions (teaching methodology)
    - Specialization: Returns subject-specific content questions
    
    Args:
        education_level: 'elementary' or 'secondary'
        exam_component: 'general_education', 'professional_education', or 'specialization'
        specialization: The user's selected specialization
        difficulty: 'Easy', 'Medium', or 'Hard'
        num_questions: Number of questions to return
    
    Returns:
        List of question dictionaries aligned to the configuration
    """
    difficulty_key = difficulty.lower()
    questions = []
    
    if exam_component == "general_education":
        # Return General Education questions (foundational subjects)
        question_pool = GENERAL_EDUCATION_QUESTIONS.get(difficulty_key, [])
        
    elif exam_component == "professional_education":
        # Return Professional Education questions (teaching methodology)
        question_pool = PROFESSIONAL_EDUCATION_QUESTIONS.get(difficulty_key, [])
        
    elif exam_component == "specialization":
        # Return specialization-specific content questions
        spec_questions = SPECIALIZATION_CONTENT_QUESTIONS.get(specialization, {})
        question_pool = spec_questions.get(difficulty_key, [])
        
        # If no questions for this specialization, try to find related
        if not question_pool:
            # Map similar specializations
            spec_mapping = {
                "Technical-Vocational Teacher Education (TVTE)": "Technology and Livelihood Education (TLE)",
            }
            mapped_spec = spec_mapping.get(specialization, specialization)
            spec_questions = SPECIALIZATION_CONTENT_QUESTIONS.get(mapped_spec, {})
            question_pool = spec_questions.get(difficulty_key, [])
    else:
        question_pool = []
    
    # If not enough questions at specified difficulty, add from other difficulties
    all_questions = list(question_pool)
    
    if len(all_questions) < num_questions:
        if exam_component == "general_education":
            source = GENERAL_EDUCATION_QUESTIONS
        elif exam_component == "professional_education":
            source = PROFESSIONAL_EDUCATION_QUESTIONS
        elif exam_component == "specialization":
            source = SPECIALIZATION_CONTENT_QUESTIONS.get(specialization, {})
        else:
            source = {}
        
        for diff in ["easy", "medium", "hard"]:
            if diff != difficulty_key:
                additional = source.get(diff, [])
                all_questions.extend(additional)
    
    # Shuffle and select
    if all_questions:
        random.shuffle(all_questions)
        questions = all_questions[:num_questions]
    
    return questions


# Keep backward compatibility
def get_preset_questions(
    education_level: str,
    exam_component: str,
    specialization: str = None,
    difficulty: str = "Medium",
    num_questions: int = 5
) -> List[Dict]:
    """Backward compatible function - redirects to aligned function."""
    return get_aligned_preset_questions(
        education_level=education_level,
        exam_component=exam_component,
        specialization=specialization or "General Education",
        difficulty=difficulty,
        num_questions=num_questions
    )


def get_mixed_preset_questions(
    education_level: str,
    specialization: str = None,
    difficulty: str = "Medium",
    num_questions: int = 5
) -> List[Dict]:
    """
    Get a mix of preset questions from all exam components based on weight distribution.
    GenEd: 20%, ProfEd: 40%, Specialization: 40%
    """
    gened_count = max(1, int(num_questions * 0.2))
    profed_count = max(1, int(num_questions * 0.4))
    spec_count = num_questions - gened_count - profed_count
    
    questions = []
    
    questions.extend(get_aligned_preset_questions(education_level, "general_education", specialization, difficulty, gened_count))
    questions.extend(get_aligned_preset_questions(education_level, "professional_education", specialization, difficulty, profed_count))
    if specialization:
        questions.extend(get_aligned_preset_questions(education_level, "specialization", specialization, difficulty, spec_count))
    
    random.shuffle(questions)
    return questions
