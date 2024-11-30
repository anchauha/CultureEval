import ollama
import pandas as pd
import csv
import sys
import os
import logging
import argparse
import re
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='survey_generation.log')

# Add config directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))

# Import configurations
from survey_questions import QUESTIONS
from likert_scales import LIKERT_SCALES
from prompt_templates import PROMPT_TEMPLATES
from hofstede_dimensions import HOFSTEDE_DIMENSIONS, generate_dimension_instructions
from model_regex_patterns import MODEL_SPECIFIC_PATTERNS

DEFAULT_DEMOGRAPHIC_CSV_PATH = "demographic_data.csv"

DEFAULT_MODEL_CONFIG = {
    "model_name": "qwen2.5:7b",
    "temperature": 0.3,
    "top_p": 0.8,
    "max_tokens": 200,
    "presence_penalty": 0.1,
    "frequency_penalty": 0.1
}

class OllamaCulturalSurveyManager:
    def __init__(self, model_name="qwen2.5:7b", csv_path=None, model_config=None):
        # Core settings
        self.model_name = model_name
        self.csv_path = csv_path
        self.model_config = model_config or DEFAULT_MODEL_CONFIG
        
        # Load configurations
        self.questions = QUESTIONS
        self.likert_scales = LIKERT_SCALES
        self.hofstede_dimensions = HOFSTEDE_DIMENSIONS
        
        
        # Store template references
        self.base_template = PROMPT_TEMPLATES['demographic_base']
        self.likert_template = PROMPT_TEMPLATES['likert_selection']
        self.reasoning_template = PROMPT_TEMPLATES['likert_reasoning']
        self.hofstede_template = PROMPT_TEMPLATES['hofstede_dimensions']
        self.hofstede_reasoning_template = PROMPT_TEMPLATES['hofstede_reasoning']

        # Pre-generate dimension instructions
        self.dimension_instructions = generate_dimension_instructions()
        
        # Create reusable template formatters
        self.demographic_formatter = lambda row: {
            'country_code': row['country_code'],
            'age_group': row['age_group'],
            'gender_category': row['gender_category'],
            'occupation_category': row['occupation_category'],
            'education_category': row['education_category']
        }
    
    def _create_prompts(self, demographic_context):
        # Format demographic base once
        base_prompt = self.base_template.format(**demographic_context)
        
        # Create all question prompts
        question_prompts = [
            self.likert_template.format(
                base_prompt=base_prompt,
                question_text=question['full_text']
            )
            for question in self.questions
        ]
        
        # Create Hofstede prompt
        hofstede_prompt = self.hofstede_template.format(
            **demographic_context,
            dimension_instructions=self.dimension_instructions
        )
        
        return base_prompt, question_prompts, hofstede_prompt

    def _process_demographic_row(self, row):
        logging.debug(f"Row data received: {row}")
        logging.debug(f"Row data types: {row.dtypes}")
        demographic_context = self.demographic_formatter(row)
        base_prompt, question_prompts, hofstede_prompt = self._create_prompts(demographic_context)
        
        responses = list(demographic_context.values())
        
        # Process questions with pre-formatted prompts
        for idx, prompt in enumerate(question_prompts):
            likert_rating = self._generate_response(prompt).strip()
            
            reasoning = self._generate_response(
                self.reasoning_template.format(
                    **demographic_context,
                    selected_value=likert_rating,
                    aspect=self.questions[idx]['aspect']
                )
            )
            
            responses.extend([likert_rating, reasoning])
        
        # Process Hofstede dimensions
        hofstede_response = self._generate_response(hofstede_prompt)
        hofstede_results = self._parse_hofstede_response(hofstede_response, self.hofstede_dimensions)
        responses.extend(hofstede_results)

        # hofstede_reasonings = []

        # for idx, dimension in enumerate(self.hofstede_dimensions.keys()):
        #     score = hofstede_results[idx]
        #     category = hofstede_results[idx + len(self.hofstede_dimensions)]
        #     label = next(d['label'] for d in self.hofstede_dimensions[dimension]['labels'] if d['value'] == category)
            
        #     reasoning = self._generate_response(
        #         self.hofstede_reasoning_template.format(
        #             **demographic_context,
        #             dimension=dimension.replace('_', ' '),
        #             score=score,
        #             category=category,
        #             label=label
        #         )
        #     )
        #     hofstede_reasonings.append(reasoning)
        
        # responses.extend(hofstede_reasonings)
        return responses

    def generate_cultural_survey_responses(self, output_path='cultural_survey_responses.csv'):
        try:
            df = pd.read_csv(self.csv_path, chunksize=1)
            total_rows = sum(1 for _ in pd.read_csv(self.csv_path))
            logging.info(f"Starting processing of {total_rows} rows")
            
            # Extended headers with prompt columns
            headers = [
                'country_code', 'age_group', 'gender_category', 
                'occupation_category', 'education_category'
            ]

            # Add question prompts and responses
            for q in self.questions:
                headers.extend([
                    f'{q["aspect"]}_Prompt',
                    f'{q["aspect"]}_Importance_Rating',
                    f'{q["aspect"]}_Reasoning_Prompt',
                    f'{q["aspect"]}_Importance_Reasoning'
                ])
            
            # Add Hofstede headers
            headers.extend(['Hofstede_Prompt'])
            headers.extend([
                f'{dim.replace(" ", "_")}_Score' for dim in self.hofstede_dimensions.keys()
            ])
            headers.extend([
                f'{dim.replace(" ", "_")}_Category' for dim in self.hofstede_dimensions.keys()
            ])

            headers.extend([
                f'{dim.replace(" ", "_")}_Reasoning' for dim in self.hofstede_dimensions.keys()
            ])

            with open(output_path, 'w', newline='', encoding='utf-8') as outfile:
                csv_writer = csv.writer(outfile)
                csv_writer.writerow(headers)
            
                with tqdm(total=total_rows, desc="Processing Responses") as pbar:
                    try:
                        for chunk in df:
                            for _, row in chunk.iterrows():
                                demographic_context = self.demographic_formatter(row)
                                base_prompt, question_prompts, hofstede_prompt = self._create_prompts(demographic_context)
                                
                                row_data = list(demographic_context.values())
                                
                                # Process each question with its prompts
                                for idx, prompt in enumerate(question_prompts):
                                    likert_rating = self._generate_response(prompt).strip()
                                    reasoning_prompt = self.reasoning_template.format(
                                        **demographic_context,
                                        selected_value=likert_rating,
                                        aspect=self.questions[idx]['aspect']
                                    )
                                    reasoning = self._generate_response(reasoning_prompt)
                                    
                                    row_data.extend([prompt, likert_rating, reasoning_prompt, reasoning])
                                
                                # Add Hofstede prompt and results
                                hofstede_response = self._generate_response(hofstede_prompt)
                                hofstede_results = self._parse_hofstede_response(hofstede_response, self.hofstede_dimensions)
                                
                                # Generate and add reasonings for each dimension
                                hofstede_reasonings = []
                                for idx, dimension in enumerate(self.hofstede_dimensions.keys()):
                                    score = hofstede_results[idx]
                                    category = hofstede_results[idx + len(self.hofstede_dimensions)]
                                    label = next(d['label'] for d in self.hofstede_dimensions[dimension]['labels'] if d['value'] == category)
                                    
                                    reasoning = self._generate_response(
                                        self.hofstede_reasoning_template.format(
                                            **demographic_context,
                                            dimension=dimension.replace('_', ' '),
                                            score=score,
                                            category=category,
                                            label=label
                                        )
                                    )
                                    hofstede_reasonings.append(reasoning)

                                row_data.extend([hofstede_prompt] + hofstede_results + hofstede_reasonings)
                                csv_writer.writerow(row_data)
                                outfile.flush()
                                pbar.update(1)
                    except KeyboardInterrupt:
                        logging.info("Processing interrupted by user")
                        raise
                    except Exception as e:
                        logging.error(f"Error during row processing: {str(e)}")
                        raise

                logging.info("Survey response generation completed successfully")
                
        except Exception as e:
            logging.error(f"Error generating cultural survey responses: {e}")


    
    def _generate_response(self, prompt):
        try:
            logging.debug(f"Generating response with model: {self.model_name}")
            logging.debug(f"Prompt length: {len(prompt)} characters")
            
            response = ollama.chat(
                model=self.model_name,
                messages=[
                {
                    'role': 'system',
                    'content': '''You are a cultural survey response generator that:
                    - For Likert scales: Responds ONLY with the numerical value (1, 2, 3, 4, or -1)
                    - For explanation: Provides culturally nuanced explanations based on demographic context
                    - For Hofstede dimensions: Outputs clear percentage scores and category labels
                    Your responses must strictly align with the cultural and demographic context provided.'''
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
                options={
                    'temperature': self.model_config['temperature'],
                    'top_p': self.model_config['top_p']
                }
            )
            content = response['message']['content'].strip()
            logging.info("Raw Model Response:")
            logging.info("-" * 50)
            logging.info(content)
            logging.info("-" * 50)

            return content
        
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            return "Model Response Error"

    def _parse_hofstede_response(self, response, hofstede_dimensions):
        logging.info("Raw Hofstede Response:")
        logging.info(response)
        
        # Initialize lists for scores and categories
        all_scores = []
        all_categories = []
        
        # Process each dimension separately to maintain correct order
        # dimension_patterns = [
        #     r'Power Distance Assessment:.*?-\s*(\d+)%.*?-\s*([1-5])',
        #     r'Uncertainty Avoidance Assessment:.*?-\s*(\d+)%.*?-\s*([1-5])',
        #     r'Individualism Collectivism Assessment:.*?-\s*(\d+)%.*?-\s*([1-5])',
        #     r'Masculinity Femininity Assessment:.*?-\s*(\d+)%.*?-\s*([1-5])',
        #     r'Long Short Term Orientation Assessment:.*?-\s*(\d+)%.*?-\s*([1-5])',
        #     r'Indulgence Restraint Assessment:.*?-\s*(\d+)%.*?-\s*([1-5])'
        # ]

        DEFAULT_PATTERNS = [
            r'Power Distance Assessment:.*?-\s*(\d+)%.*?-\s*([1-5])',
            r'Uncertainty Avoidance Assessment:.*?-\s*(\d+)%.*?-\s*([1-5])',
            r'Individualism Collectivism Assessment:.*?-\s*(\d+)%.*?-\s*([1-5])',
            r'Masculinity Femininity Assessment:.*?-\s*(\d+)%.*?-\s*([1-5])',
            r'Long Short Term Orientation Assessment:.*?-\s*(\d+)%.*?-\s*([1-5])',
            r'Indulgence Restraint Assessment:.*?-\s*(\d+)%.*?-\s*([1-5])'
        ]

        patterns = MODEL_SPECIFIC_PATTERNS.get(self.model_name, {}).get('dimension_patterns', DEFAULT_PATTERNS)

        
        # Extract scores and categories for each dimension
        for pattern in patterns:
            match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
            if match:
                score = float(match.group(1))
                category = int(match.group(2))
                all_scores.append(min(max(score, 0), 100))
                all_categories.append(min(max(category, 1), 5))
            else:
                logging.warning(f"No match found for pattern: {pattern}")
                logging.warning(f"Response segment: {response[:200]}...")
                all_scores.append(-5) # Default value for missing hofstede's scores
                all_categories.append(-3) # Default value for missing hofstede's categories
        
        # First add all scores, then all categories
        results = all_scores + all_categories
        
        logging.info(f"Processed scores: {all_scores}")
        logging.info(f"Processed categories: {all_categories}")
        logging.info(f"Final results: {results}")
        
        return results


    def _validate_likert_response(self, response, scale_type="importance"):
        try:
            value = int(response)
            valid_values = [item["value"] for item in self.likert_scales[scale_type]]
            if value not in valid_values:
                logging.warning(f"Invalid Likert response: {value}. Using default value -4.")
                return -4
            return value
        except ValueError:
            logging.warning(f"Non-numeric Likert response: {response}. Using default value -3.")
            return -3


def main():
    parser = argparse.ArgumentParser(description="Generate cultural survey responses.")
    parser.add_argument('--csv_path', type=str, default=DEFAULT_DEMOGRAPHIC_CSV_PATH, 
                       help='Path to the CSV file containing demographic data')
    args = parser.parse_args()

    csv_path = args.csv_path

    try:
        if not os.path.isfile(csv_path):
            logging.error(f"File {csv_path} not found.")
            return

        survey_manager = OllamaCulturalSurveyManager(
            model_name="qwen2.5:7b",
            csv_path=csv_path
        )
        
        survey_manager.generate_cultural_survey_responses(
            output_path='cultural_survey_responses.csv'
        )
        
        logging.info("Cultural survey response generation complete.")
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()