import re

HOFSTEDE_DIMENSIONS = {
    "Power_Distance": {
        "description": "The extent to which less powerful members of organizations and institutions accept and expect that power is distributed unequally.",
        "labels": [
            {"value": 1, "label": "Egalitarian"},
            {"value": 2, "label": "Mostly Egalitarian"},
            {"value": 3, "label": "Neutral/Moderate"},
            {"value": 4, "label": "Mostly Hierarchical"},
            {"value": 5, "label": "Hierarchical"}
        ],
        "prompt": "Assess the power dynamics in your cultural context. Select the label that best describes the power distribution:"
    },
    "Uncertainty_Avoidance": {
        "description": "The extent to which the members of a culture feel threatened by ambiguous or unknown situations.",
        "labels": [
            {"value": 1, "label": "Very Low Uncertainty Avoidance"},
            {"value": 2, "label": "Low Uncertainty Avoidance"},
            {"value": 3, "label": "Moderate Uncertainty Avoidance"},
            {"value": 4, "label": "High Uncertainty Avoidance"},
            {"value": 5, "label": "Very High Uncertainty Avoidance"}
        ],
        "prompt": "How comfortable are you and your culture with uncertain or ambiguous situations? Select the most appropriate label:"
    },
    "Individualism_Collectivism": {
        "description": "The degree of interdependence a society maintains among its members.",
        "labels": [
            {"value": 1, "label": "Extremely Collectivist"},
            {"value": 2, "label": "Mostly Collectivist"},
            {"value": 3, "label": "Balanced"},
            {"value": 4, "label": "Mostly Individualist"},
            {"value": 5, "label": "Extremely Individualist"}
        ],
        "prompt": "Reflect on the social bonds and personal relationships in your culture. Select the label that best describes your cultural orientation:"
    },
    "Masculinity_Femininity": {
        "description": "The distribution of emotional roles between genders.",
        "labels": [
            {"value": 1, "label": "Extremely Feminine"},
            {"value": 2, "label": "Mostly Feminine"},
            {"value": 3, "label": "Balanced"},
            {"value": 4, "label": "Mostly Masculine"},
            {"value": 5, "label": "Extremely Masculine"}
        ],
        "prompt": "Consider the gender roles and emotional characteristics valued in your culture. Select the most appropriate label:"
    },
    "Long_Short_Term_Orientation": {
        "description": "How a society maintains links with its past while dealing with present and future challenges.",
        "labels": [
            {"value": 1, "label": "Extremely Short-Term Oriented"},
            {"value": 2, "label": "Mostly Short-Term Oriented"},
            {"value": 3, "label": "Balanced"},
            {"value": 4, "label": "Mostly Long-Term Oriented"},
            {"value": 5, "label": "Extremely Long-Term Oriented"}
        ],
        "prompt": "Reflect on how your culture views time, planning, and traditions. Select the label that best describes your cultural time orientation:"
    },
    "Indulgence_Restraint": {
        "description": "The extent to which a society allows relatively free gratification of basic and natural human desires.",
        "labels": [
            {"value": 1, "label": "Extremely Restrained"},
            {"value": 2, "label": "Mostly Restrained"},
            {"value": 3, "label": "Balanced"},
            {"value": 4, "label": "Mostly Indulgent"},
            {"value": 5, "label": "Extremely Indulgent"}
        ],
        "prompt": "Consider the social norms around personal desires and societal controls in your culture. Select the most appropriate label:"
    }
}
HOFSTEDE_REASONING_TEMPLATE = """
Based on your demographic context ({country_code}, {age_group}, {gender_category}, {occupation_category}, {education_category}):

Explain why you rated {dimension} with:
- Score: {score}%
- Category: {category} ({label})

Your explanation should reflect cultural nuances and demographic influences.
"""

def generate_dimension_instructions():
    instructions = ""
    for dim, details in HOFSTEDE_DIMENSIONS.items():
        instructions += f"""
{dim.replace('_', ' ')} Assessment:
{details['description']}
{details['prompt']}

Possible Labels:
{chr(10).join([f"{label['value']}. {label['label']}" for label in details['labels']])}

Respond with:
- Percentage Score (0-100%)
- Categorical Label Number (1-5)
"""
    return instructions

HOFSTEDE_PROMPT_TEMPLATE = """
Based on your demographic background and previous responses, assess your cultural context along Hofstede's Cultural Dimensions.

For each dimension, you will:
1. Provide a percentage score (0-100%)
2. Select a categorical label from the given options

Demographic Context:
- Country: {country_code}
- Age Group: {age_group}
- Gender: {gender_category}
- Occupation: {occupation_category}
- Education: {education_category}

Detailed Assessment Instructions:
{dimension_instructions}
"""