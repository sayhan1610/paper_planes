#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python is not installed. Please install Python 3.11.6 or higher."
    exit
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null
then
    echo "Pip is not installed. Installing pip..."
    python3 -m ensurepip --upgrade
fi

# Install dependencies
pip3 install -r requirements.txt

# Run the game
python3 brick.py
