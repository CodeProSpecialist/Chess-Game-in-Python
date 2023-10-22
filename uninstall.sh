#!/bin/bash

# List of installed packages
packages=("python-chess" "python-chess-variant")

# Function to uninstall packages
uninstall_packages() {
    for package in "${packages[@]}"; do
        pip3 uninstall -y "$package"
        if [ $? -eq 0 ]; then
            echo "Successfully uninstalled $package"
        else
            echo "Failed to uninstall $package"
            exit 1
        fi
    done
}

# Check if pip3 is installed
if command -v pip3 &> /dev/null; then
    echo "Uninstalling Python packages..."
    uninstall_packages
    echo "Uninstallation completed."
else
    echo "pip3 is not installed. Please install pip3 and try again."
    exit 1
fi
