MODEL_SPECIFIC_PATTERNS = {
    "qwen2.5:7b": {
        "dimension_patterns": [
            r'(?:Power[_ ]Distance).*?(\d+)%.*?([1-5])',
            r'(?:Uncertainty[_ ]Avoidance).*?(\d+)%.*?([1-5])',
            r'(?:Individualism[_ ]Collectivism).*?(\d+)%.*?([1-5])',
            r'(?:Masculinity[_ ]Femininity).*?(\d+)%.*?([1-5])',
            r'(?:Long[_ ]Short[_ ]Term[_ ]Orientation).*?(\d+)%.*?([1-5])',
            r'(?:Indulgence[_ ]Restraint).*?(\d+)%.*?([1-5])'
        ]
    },
    "gemma2:9b": {
        "dimension_patterns": [
            r'(?:Power[_ ]Distance).*?(\d+)%.*?([1-5])',
            r'(?:Uncertainty[_ ]Avoidance).*?(\d+)%.*?([1-5])',
            r'(?:Individualism[_ ]Collectivism).*?(\d+)%.*?([1-5])',
            r'(?:Masculinity[_ ]Femininity).*?(\d+)%.*?([1-5])',
            r'(?:Long[_ ]Short[_ ]Term[_ ]Orientation).*?(\d+)%.*?([1-5])',
            r'(?:Indulgence[_ ]Restraint).*?(\d+)%.*?([1-5])'
        ]
    }
}