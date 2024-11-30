#!/bin/bash
# Set the base directory where Ollama is installed
OLLAMA_BASE_DIR="/N/scratch/ankichau/CultureEval"

Environment=OLLAMA_MODELS="/N/scratch/ankichau/CultureEval/.ollama"
export OLLAMA_MODELS="/N/scratch/ankichau/CultureEval/.ollama"

# Define the model to download
MODEL_NAME="qwen2.5:7b"



# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to start Ollama server
start_ollama_server() {
    echo "Starting Ollama server..."
    
    # Change to the Ollama base directory
    cd "$OLLAMA_BASE_DIR" || exit 1
    
    # Make ollama executable if not already
    chmod +x bin/ollama
    
    # Start Ollama server in the background
    bin/ollama serve &
    
    # Wait a moment to ensure the server starts
    sleep 3
    
    # Check if the server is running
    if pgrep -f "ollama serve" > /dev/null; then
        echo "Ollama server started successfully."
    else
        echo "Failed to start Ollama server."
        exit 1
    fi
}


# Function to download Ollama model
download_ollama_model() {
    echo "Downloading Ollama model: $MODEL_NAME"
    
    # Change to the Ollama base directory
    cd "$OLLAMA_BASE_DIR" || exit 1
    
    # Download the specified model
    bin/ollama pull "$MODEL_NAME"
}

# Function to run Python script
run_python_script() {
    local script_path="$1"
    # Run the Python script
    echo "Running Python script: $script_path"
    python3 "$script_path"
}

# Main script execution
main() {

    # Start Ollama server
    start_ollama_server

    # Download the specified model first
    download_ollama_model

    # Replace 'your_script.py' with the path to your actual Python script
    local python_script="executables/python_script.py"
    
    # Run Python script
    run_python_script "$python_script"
}

# Error handling
set -e
trap 'echo "Error: Script failed at line $LINENO"; exit 1' ERR

# Execute main function
main

# Optional: Cleanup function to stop Ollama server when script completes
cleanup() {
    echo "Stopping Ollama server..."
    pkill -f "ollama serve"
}
trap cleanup EXIT