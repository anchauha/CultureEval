from hofstede_dimensions import HOFSTEDE_PROMPT_TEMPLATE

PROMPT_TEMPLATES = {
    "demographic_base": """You are an individual living in {country_code}. Respond authentically representing the cultural values, beliefs, and perspectives typical of your nationality. Consider your background as someone who is {age_group} years old, {gender_category}, working as {occupation_category} with {education_category}. Your responses should reflect cultural nuances, social norms, and typical worldview without stereotyping.""",
    
    "likert_selection": """
{base_prompt}

Question: {question_text}

Respond ONLY with the NUMBER corresponding to the Likert scale that best represents your response:
1 - Very important
2 - Rather important
3 - Not very important
4 - Not at all important
-1 - Don't Know
""",
    
    "likert_reasoning": """
As someone living in {country_code}, {age_group} years old, {gender_category}, working as {occupation_category} with {education_category}:

You selected {selected_value} for the importance of {aspect}, where:
1 = Very important (crucial and central to life)
2 = Rather important (matters significantly)
3 = Not very important (minimal impact)
4 = Not at all important (no relevance)
-1 = Don't Know (cannot determine)

Provide a detailed explanation for why you chose this rating. Your explanation should reflect your cultural background and personal perspective.
""",

    "hofstede_reasoning": """
Based on your demographic context ({country_code}, {age_group}, {gender_category}, {occupation_category}, {education_category}):

Explain why you rated {dimension} with:
- Score: {score}%
- Category: {category} ({label})

Your explanation should reflect cultural nuances and demographic influences.
""",
    
    "hofstede_dimensions": HOFSTEDE_PROMPT_TEMPLATE
}
