"""
Configuration for the Sleep Quality Dashboard
"""

# Color scheme
COLOR_MAP = {
    "Very Bad": "#E63946",
    "Pretty Bad": "#F4A261",
    "Quite Good": "#A8DADC",
    "Very Good": "#1D3557"
}

# Mapping numeric class -> text
SLEEP_CLASSES = {
    1: "Very Bad",
    2: "Pretty Bad",
    3: "Quite Good",
    4: "Very Good"
}

# Question types with appropriate response options
QUESTION_TYPES = {
    # Numeric questions (age, hours, etc.)
    "numeric": {
        "widget": "number_input",
        "defaults": {"min_value": 0, "max_value": 100, "step": 1}
    },

    # Custom range for height
    "height": {
        "widget": "number_input",
        "defaults": {"min_value": 140, "max_value": 220, "step": 1}
    },

    # Custom range for weight
    "weight": {
        "widget": "number_input",
        "defaults": {"min_value": 40, "max_value": 150, "step": 1}
    },

    # Custom range for minutes
    "minutes": {
        "widget": "number_input",
        "defaults": {"min_value": 0, "max_value": 180, "step": 1}
    },

    # Custom range for sleep hours
    "sleep_hours": {
        "widget": "number_input",
        "defaults": {"min_value": 0, "max_value": 12, "step": 0.5}
    },

    # Yes/No questions
    "yes_no": {
        "widget": "radio",
        "options": ["Yes", "No"],
        "values": {"Yes": 1, "No": 0}
    },

    # Frequency questions with clear distinctions
    "frequency": {
        "widget": "selectbox",
        "options": [
            "Never",
            "Rarely (< once/week)",
            "Sometimes (1-2 times/week)",
            "Often (≥3 times/week)"
        ],
        "values": {
            "Never": 0,
            "Rarely (< once/week)": 1,
            "Sometimes (1-2 times/week)": 2,
            "Often (≥3 times/week)": 3
        }
    },

    # Energy level scale
    "energy_level": {
        "widget": "slider",
        "options": [1, 2, 3, 4, 5],
        "labels": {
            1: "Very Low",
            2: "Low",
            3: "Moderate",
            4: "High",
            5: "Very High"
        },
        "values": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}
    },

    # Sleep quality ratings
    "sleep_quality": {
        "widget": "selectbox",
        "options": ["Very Good", "Quite Good", "Pretty Bad", "Very Bad"],
        "values": {"Very Good": 4, "Quite Good": 3, "Pretty Bad": 2, "Very Bad": 1}
    },

    # General health ratings
    "health": {
        "widget": "selectbox",
        "options": ["Perfect", "Very Good", "Good", "Average", "Poor"],
        "values": {"Perfect": 5, "Very Good": 4, "Good": 3, "Average": 2, "Poor": 1}
    },

    # Agreement level
    "agreement": {
        "widget": "selectbox",
        "options": ["Never", "Rarely", "Sometimes", "Often", "Always"],
        "values": {"Never": 1, "Rarely": 2, "Sometimes": 3, "Often": 4, "Always": 5}
    },

    # Activities limitation
    "limitation": {
        "widget": "selectbox",
        "options": [
            "No simple movements do not limit me",
            "Yes simple gestures limit me"
        ],
        "values": {
            "No simple movements do not limit me": 0,
            "Yes simple gestures limit me": 1
        }
    },

    # Movement level
    "movement": {
        "widget": "selectbox",
        "options": [
            "I did my movements at the level I wanted",
            "I couldn't do my movements at the level I wanted"
        ],
        "values": {
            "I did my movements at the level I wanted": 1,
            "I couldn't do my movements at the level I wanted": 0
        }
    },

    # Restriction level
    "restriction": {
        "widget": "selectbox",
        "options": [
            "My movement and work are not restricted",
            "My movement and work are restricted"
        ],
        "values": {
            "My movement and work are not restricted": 0,
            "My movement and work are restricted": 1
        }
    },

    # Achievement level
    "achievement": {
    "widget": "selectbox",
    "options": [
        "No, my emotional state did not cause problems at work",
        "Yes, emotional stress interfered with my work"
    ],
    "values": {
        "No, my emotional state did not cause problems at work": 0,
        "Yes, emotional stress interfered with my work": 1
    }
    },

    # Interruption level
    "interruption": {
        "widget": "selectbox",
        "options": [
            "Never",
            "A little bit",
            "Partially",
            "Quite a lot"
        ],
        "values": {
            "Never": 0,
            "A little bit": 1,
            "Partially": 2,
            "Quite a lot": 3
        }
    },

    # Feeling frequency
    "feeling_frequency": {
        "widget": "selectbox",
        "options": [
            "Never",
            "Very few",
            "Sometimes",
            "Majority",
            "Almost always"
        ],
        "values": {
            "Never": 0,
            "Very few": 1,
            "Sometimes": 2,
            "Majority": 3,
            "Almost always": 4
        }
    },

    # Problem extent
    "problem_extent": {
        "widget": "selectbox",
        "options": [
            "Never posed a problem",
            "Only very few problems created",
            "To some extent it created a problem",
            "It created a huge problem"
        ],
        "values": {
            "Never posed a problem": 0,
            "Only very few problems created": 1,
            "To some extent it created a problem": 2,
            "It created a huge problem": 3
        }
    },

    # Time input
    "time": {
        "widget": "number_input",
        "defaults": {"min_value": 0, "max_value": 24, "step": 1}
    }
}

# Key factors for simplified prediction (simple tab)
KEY_FACTORS = [
    {
        "id": "33",
        "column": "33. What is the weekly frequency of days in the last month when you could not fall asleep within 30 minutes?",
        "question": "How often did you have difficulty falling asleep within 30 minutes?",
        "type": "frequency",
        "category": "Sleep"
    },
    {
        "id": "26",
        "column": "26. I feel full of energy",
        "question": "Energy level",
        "type": "energy_level",
        "category": "Emotional"
    },
    {
        "id": "41",
        "column": "41. What is the weekly frequency of other reasons (hearing a noise, waking up suddenly, etc.) at night in the last month?",
        "question": "How often did noise wake you up?",
        "type": "frequency",
        "category": "Environment"
    },
    {
        "id": "16",
        "column": "16. Do you think your diet is adequate and balanced?",
        "question": "Do you think your diet is adequate and balanced?",
        "type": "yes_no",
        "category": "Health"
    },
    {
        "id": "10",
        "column": "10. How many hours of practical sports lessons (athletics, swimming, orienteering and pentathlon) do you have per week?",
        "question": "Hours of physical activity per week",
        "type": "numeric",
        "category": "Activity"
    },
    {
        "id": "37",
        "column": "37. What is the weekly frequency of nights in the last month when you were extremely cold at night?",
        "question": "How often did you feel extremely cold at night?",
        "type": "frequency",
        "category": "Environment"
    },
    {
        "id": "38",
        "column": "38. What is the weekly frequency of nights in the last month when you felt extremely hot at night?",
        "question": "How often did you feel extremely hot at night?",
        "type": "frequency",
        "category": "Environment"
    },
    {
        "id": "44",
        "column": "44. How often did you take sleeping pills (prescription and over-the-counter) to help you sleep last month?",
        "question": "How often did you take sleeping medication?",
        "type": "frequency",
        "category": "Medication"
    },
    {
        "id": "25",
        "column": "25. I feel peaceful and calm",
        "question": "Level of calmness and peace",
        "type": "energy_level",  # Using energy_level widget but with different context
        "category": "Emotional"
    },
    {
        "id": "27",
        "column": "27. I feel devastated and finished",
        "question": "Level of exhaustion",
        "type": "energy_level",  # Using energy_level widget but with different context
        "category": "Emotional"
    }
]

# Complete list of all 52 questions for the advanced mode
ALL_QUESTIONS = [
    {
        "id": "1",
        "column": "1. Height (in cm)",
        "question": "Height (in cm)",
        "type": "height",  # Changed from numeric to custom height type
        "category": "Demographics"
    },
    {
        "id": "2",
        "column": "2. Age?",
        "question": "Age",
        "type": "numeric",
        "category": "Demographics"
    },
    {
        "id": "3",
        "column": "3. Body weight (in kg)",
        "question": "Body weight (in kg)",
        "type": "weight",  # Changed from numeric to custom weight type
        "category": "Demographics"
    },
    {
        "id": "5",
        "column": "5. Do you smoke?",
        "question": "Do you smoke?",
        "type": "yes_no",
        "category": "Health"
    },
    {
        "id": "6",
        "column": "6. Do you drink alcohol?",
        "question": "Do you drink alcohol?",
        "type": "yes_no",
        "category": "Health"
    },
    {
        "id": "7",
        "column": "7. Have you received a diagnosis of 'STRESS FRACTURE' from a medical specialist as a result of a health complaint you have experienced since you started university/college?",
        "question": "Have you received a diagnosis of 'STRESS FRACTURE'?",
        "type": "yes_no",
        "category": "Health"
    },
    {
        "id": "8",
        "column": "8. Since you started university/college, have you been diagnosed with a 'dislocated shoulder' by a medical specialist as a result of a health complaint during classes or training?",
        "question": "Have you been diagnosed with a 'dislocated shoulder'?",
        "type": "yes_no",
        "category": "Health"
    },
    {
        "id": "9",
        "column": "9. Since you started university/college, have you been diagnosed with 'LUMBAR HIT' by a medical specialist as a result of a health complaint during classes or training?",
        "question": "Have you been diagnosed with 'LUMBAR HIT'?",
        "type": "yes_no",
        "category": "Health"
    },
    {
        "id": "10",
        "column": "10. How many hours of practical sports lessons (athletics, swimming, orienteering and pentathlon) do you have per week?",
        "question": "Hours of practical sports lessons per week",
        "type": "numeric",
        "category": "Activity"
    },
    {
        "id": "11",
        "column": "11. How many hours per week in total do you have applied martial arts (wrestling, kickboxing, arm defense and intervention techniques) classes?",
        "question": "Hours of martial arts per week",
        "type": "numeric",
        "category": "Activity"
    },
    {
        "id": "12",
        "column": "12. How many hours of practical military training do you have per week?",
        "question": "Hours of military training per week",
        "type": "numeric",
        "category": "Activity"
    },
    {
        "id": "13",
        "column": "13. Do you take part in any school teams?",
        "question": "Do you take part in any school teams?",
        "type": "yes_no",
        "category": "Activity"
    },
    {
        "id": "14",
        "column": "14. If you are a member of the school team, HOW MANY DAYS a week do you train?",
        "question": "Days per week of team training",
        "type": "numeric",
        "category": "Activity"
    },
    {
        "id": "15",
        "column": "15. If you are a member of the school team, HOW MANY HOURS a day do you train?",
        "question": "Hours per day of team training",
        "type": "numeric",
        "category": "Activity"
    },
    {
        "id": "16",
        "column": "16. Do you think your diet is adequate and balanced?",
        "question": "Do you think your diet is adequate and balanced?",
        "type": "yes_no",
        "category": "Health"
    },
    {
        "id": "17",
        "column": "17. How is your health in general?",
        "question": "How is your health in general?",
        "type": "health",
        "category": "Health"
    },
    {
        "id": "18",
        "column": "18. The following questions are about activities you do during an ordinary day. Simple movements, pulling and pushing a table, moderate activities (such as bowling or playing golf). Does your health limit these activities? If yes, how much? (Check one box in each row)",
        "question": "Does your health limit simple movements?",
        "type": "limitation",
        "category": "Health"
    },
    {
        "id": "19",
        "column": "19. To climb a ladder with many steps (climb)",
        "question": "Does your health limit climbing a ladder with many steps?",
        "type": "limitation",
        "category": "Health"
    },
    {
        "id": "20",
        "column": "20. In the past 4 weeks, have you experienced any of the following problems with your daily activities and work because of your physical health?",
        "question": "Problems with daily activities due to physical health",
        "type": "movement",
        "category": "Health"
    },
    {
        "id": "21",
        "column": "21. In the past 4 weeks, have you experienced any of the following problems with your daily activities and work because of your physical health?",
        "question": "Restriction in movement and work due to physical health",
        "type": "restriction",
        "category": "Health"
    },
    {
        "id": "22",
        "column": "22. In the past 4 weeks, have you experienced any of the following problems due to emotional reasons (depression or extreme stress)?",
        "question": "Problems due to emotional reasons",
        "type": "achievement",
        "category": "Emotional"
    },
    {
        "id": "23",
        "column": "23. In the last 4 weeks, has your normal work been interrupted because of pain (housework or normal work) (Please select only one option)?",
        "question": "Work interruption due to pain",
        "type": "interruption",
        "category": "Health"
    },
    {
        "id": "25",
        "column": "25. I feel peaceful and calm",
        "question": "How often do you feel peaceful and calm?",
        "type": "feeling_frequency",
        "category": "Emotional"
    },
    {
        "id": "26",
        "column": "26. I feel full of energy",
        "question": "How often do you feel full of energy?",
        "type": "feeling_frequency",
        "category": "Emotional"
    },
    {
        "id": "27",
        "column": "27. I feel devastated and finished",
        "question": "How often do you feel devastated and finished?",
        "type": "feeling_frequency",
        "category": "Emotional"
    },
    {
        "id": "28",
        "column": "28. My health has limited or affected my daily life (such as visiting friends and close relatives)",
        "question": "Has your health limited your social life?",
        "type": "feeling_frequency",
        "category": "Health"
    },
    {
        "id": "29",
        "column": "29. What time did you usually go to bed at night last month? (At what time?)",
        "question": "What time did you usually go to bed? (hour 0-24)",
        "type": "time",
        "category": "Sleep"
    },
    {
        "id": "30",
        "column": "30. How long (minutes) did it usually take you to fall asleep at night last month?",
        "question": "How long did it take to fall asleep? (minutes)",
        "type": "minutes",  # Changed from numeric to custom minutes type
        "category": "Sleep"
    },
    {
        "id": "31",
        "column": "31. What time did you usually get up in the morning last month? (What time?)",
        "question": "What time did you usually get up? (hour 0-24)",
        "type": "time",
        "category": "Sleep"
    },
    {
        "id": "32",
        "column": "32. How many hours did you sleep at night last month?",
        "question": "How many hours did you sleep at night?",
        "type": "sleep_hours",  # Changed from numeric to custom sleep_hours type
        "category": "Sleep"
    },
    {
        "id": "33",
        "column": "33. What is the weekly frequency of days in the last month when you could not fall asleep within 30 minutes?",
        "question": "How often could you not fall asleep within 30 minutes?",
        "type": "frequency",
        "category": "Sleep"
    },
    {
        "id": "34",
        "column": "34. What is the weekly frequency of days in the last month when you woke up in the middle of the night and early in the morning?",
        "question": "How often did you wake up in the middle of the night?",
        "type": "frequency",
        "category": "Sleep"
    },
    {
        "id": "35",
        "column": "35. What is the weekly frequency of the nights you went to the toilet in the last month?",
        "question": "How often did you go to the toilet at night?",
        "type": "frequency",
        "category": "Sleep"
    },
    {
        "id": "36",
        "column": "36. What is the weekly frequency of nights in the last month when you could not breathe easily at night?",
        "question": "How often could you not breathe easily at night?",
        "type": "frequency",
        "category": "Sleep"
    },
    {
        "id": "37",
        "column": "37. What is the weekly frequency of nights in the last month when you were extremely cold at night?",
        "question": "How often were you extremely cold at night?",
        "type": "frequency",
        "category": "Environment"
    },
    {
        "id": "38",
        "column": "38. What is the weekly frequency of nights in the last month when you felt extremely hot at night?",
        "question": "How often did you feel extremely hot at night?",
        "type": "frequency",
        "category": "Environment"
    },
    {
        "id": "39",
        "column": "39. What is the weekly frequency of nights in the past month when you had bad dreams?",
        "question": "How often did you have bad dreams?",
        "type": "frequency",
        "category": "Sleep"
    },
    {
        "id": "40",
        "column": "40. What is the weekly frequency of nights in the last month when you had night pain?",
        "question": "How often did you have night pain?",
        "type": "frequency",
        "category": "Health"
    },
    {
        "id": "41",
        "column": "41. What is the weekly frequency of other reasons (hearing a noise, waking up suddenly, etc.) at night in the last month?",
        "question": "How often did noise or other factors wake you up?",
        "type": "frequency",
        "category": "Environment"
    },
    {
        "id": "42",
        "column": "42. In the last month, what is your weekly frequency of coughing at night and snoring loudly?",
        "question": "How often did you cough or snore at night?",
        "type": "frequency",
        "category": "Health"
    },
    {
        "id": "43",
        "column": "43. How would you rate your sleep quality as a whole in the last month?",
        "question": "How would you rate your sleep quality overall?",
        "type": "sleep_quality",
        "category": "Sleep"
    },
    {
        "id": "44",
        "column": "44. How often did you take sleeping pills (prescription and over-the-counter) to help you sleep last month?",
        "question": "How often did you take sleeping pills?",
        "type": "frequency",
        "category": "Medication"
    },
    {
        "id": "45",
        "column": "45. In the last month, how often have you struggled to stay awake while driving, eating or during a social activity?",
        "question": "How often did you struggle to stay awake during activities?",
        "type": "frequency",
        "category": "Sleep"
    },
    {
        "id": "46",
        "column": "46. Last month, to what extent did this make it a problem for you to do your work with enough enthusiasm?",
        "question": "Did sleepiness affect your work enthusiasm?",
        "type": "problem_extent",
        "category": "Sleep"
    },
    {
        "id": "48",
        "column": "48. According to your bed partner or roommate, how often have you experienced loud snoring in the last 1 month?",
        "question": "How often did your roommate report you snoring loudly?",
        "type": "frequency",
        "category": "Sleep"
    },
    {
        "id": "49",
        "column": "49. According to your bed partner or roommate, how often have you experienced long intervals between breathing in and out of sleep in the last 1 month?",
        "question": "How often did your roommate report breathing pauses?",
        "type": "frequency",
        "category": "Sleep"
    },
    {
        "id": "50",
        "column": "50. According to your bed partner or roommate, how often have you experienced twitching or jumping of the legs while sleeping in the last 1 month?",
        "question": "How often did your roommate report leg movements?",
        "type": "frequency",
        "category": "Sleep"
    },
    {
        "id": "51",
        "column": "51. According to your bed partner or roommate, how often in the last 1 month have you experienced incoherence or confusion during sleep?",
        "question": "How often did your roommate report confusion during sleep?",
        "type": "frequency",
        "category": "Sleep"
    },
    {
        "id": "52",
        "column": "52. According to your bed partner or roommate, how often have you experienced other disturbances (waking up screaming, etc.) in the last 1 month?",
        "question": "How often did your roommate report other disturbances?",
        "type": "frequency",
        "category": "Sleep"
    }
]

# Factor categories for organizing questions
FACTOR_CATEGORIES = [
    {"id": "demographic", "name": "Demographics", "keywords": ["height", "age", "weight", "classroom"]},
    {"id": "sleep", "name": "Sleep", "keywords": ["sleep", "night", "bed", "wake", "dream", "fall asleep"]},
    {"id": "environment", "name": "Environment", "keywords": ["cold", "hot", "noise", "temperature"]},
    {"id": "health", "name": "Health", "keywords": ["health", "diet", "smoke", "alcohol"]},
    {"id": "activity", "name": "Activity", "keywords": ["sport", "training", "martial", "military"]},
    {"id": "emotional", "name": "Emotional", "keywords": ["feel", "peaceful", "calm", "energy", "devastated"]}
]