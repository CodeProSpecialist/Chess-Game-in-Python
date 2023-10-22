#!/bin/bash

# Check if pip3 is installed
if command -v pip3 &> /dev/null; then
    echo "pip3 is installed."

    # Install required libraries using pip3
    echo "Installing required libraries using pip3..."
    pip3 install python-chess pygame pillow

    # Check the exit status of the pip3 command
    if [ $? -eq 0 ]; then
        echo "Successfully installed required libraries."
    else
        echo "Failed to install libraries. Please check your Python and pip3 setup."
        exit 1
    fi
else
    echo "pip3 is not installed. Please install pip3 and try again."
    exit 1
fi

