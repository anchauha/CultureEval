import ollama
import json
import requests

class OllamaInferenceManager:
    def __init__(self, model_name="phi3:14b"):
        """
        Initialize the Ollama Inference Manager
        
        :param model_name: Name of the Ollama model to use
        """
        self.model_name = model_name
        self.base_url = "http://localhost:11434"
        self.validate_model()
    
    def validate_model(self):
        """
        Validate if the specified model is available locally
        """
        try:
            # Use requests to directly query the local Ollama API
            response = requests.get(f"{self.base_url}/api/tags")
            
            if response.status_code != 200:
                raise ValueError("Could not retrieve model list from Ollama")
            
            models = response.json()
            
            # Check if the model exists
            model_exists = any(
                self.model_name in model.get('name', '') 
                for model in models.get('models', [])
            )
            
            if not model_exists:
                raise ValueError(f"Model {self.model_name} not found. Please download it first.")
            
            print(f"Model {self.model_name} validated successfully.")
        
        except Exception as e:
            print(f"Error validating model: {e}")
            raise
    
    def generate_response(self, prompt, stream=False):
        """
        Generate a response using the specified model
        
        :param prompt: User's input prompt
        :param stream: Whether to stream the response
        :return: Model's response
        """
        try:
            # # For non-streaming response
            # if not stream:
            #     response = ollama.chat(
            #         model=self.model_name,
            #         messages=[{'role': 'user', 'content': prompt}]
            #     )
            #     return response['message']['content']
            
            # For streaming response
            def response_generator():
                full_response = ""
                for chunk in ollama.chat(
                    model=self.model_name,
                    messages=[{'role': 'user', 'content': prompt}],
                    stream=True
                ):
                    if 'message' in chunk:
                        content = chunk['message']['content']
                        print(content, end='', flush=True)
                        full_response += content
                        yield content
                return full_response
            
            return response_generator()
        
        except Exception as e:
            print(f"Error generating response: {e}")
            return None
    
    def list_local_models(self):
        """
        List all locally available Ollama models
        """
        try:
            # Use requests to directly query the local Ollama API
            response = requests.get(f"{self.base_url}/api/tags")
            
            if response.status_code != 200:
                raise ValueError("Could not retrieve model list from Ollama")
            
            models = response.json()
            
            print("Available Local Models:")
            for model in models.get('models', []):
                print(f"- {model.get('name', 'Unknown')}")
        
        except Exception as e:
            print(f"Error listing models: {e}")
    
    def save_response_to_file(self, response, filename='model_response.json'):
        """
        Save model response to a JSON file
        
        :param response: Model's response
        :param filename: Output filename
        """
        try:
            # Handle different response types
            if hasattr(response, '__iter__') and not isinstance(response, str):
                # If it's a generator or iterator, collect the full response
                full_response = ''.join(list(response))
                response = full_response
            
            # Ensure response is a string
            if not isinstance(response, str):
                response = str(response)
            
            # Save to file
            with open(filename, 'w') as f:
                json.dump({'response': response}, f, indent=2)
            print(f"Response saved to {filename}")
        except Exception as e:
            print(f"Error saving response: {e}")

def main():
    # Example usage
    try:
        # Initialize inference manager with default or specified model
        inference_manager = OllamaInferenceManager(model_name="phi3:14b")
        
        # List available local models
        inference_manager.list_local_models()
        
        # Generate a non-streaming response
        print("\n--- Non-Streaming Response ---")
        prompt = "Why is the sky blue?"
        response = inference_manager.generate_response(prompt, stream=False)
        
        # Save non-streaming response to file
        if response:
            inference_manager.save_response_to_file(response, 'non_streaming_response.json')
        
        # Generate a streaming response
        print("\n--- Streaming Response ---")
        streaming_response = inference_manager.generate_response(prompt, stream=True)
        
        # Save streaming response to file
        if streaming_response:
            inference_manager.save_response_to_file(streaming_response, 'streaming_response.json')
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()