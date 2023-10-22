#!/bin/bash

# List of required packages
packages=("python-chess" "python-chess-variant")

# Function to install packages
install_packages() {
    for package in "${packages[@]}"; do
        pip3 install "$package"
        if [ $? -eq 0 ]; then
            echo "Successfully installed $package"
        else
            echo "Failed to install $package"
            exit 1
        fi
    done
}

# Check if pip is installed
if command -v pip3 &> /dev/null; then
    echo "Installing required Python packages..."
    install_packages
    echo "Installation completed."
else
    echo "pip is not installed. Please install pip3 and try again."
    exit 1
fi
