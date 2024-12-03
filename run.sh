#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}Starting SageAI Dataset Generator...${NC}"

# Activate virtual environment
source venv/bin/activate || {
    echo -e "${RED}Failed to activate virtual environment. Run ./setup.sh first${NC}"
    exit 1
}

# Run the application
python src/main.py

# Handle exit
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Application stopped successfully${NC}"
else
    echo -e "${RED}Application exited with an error${NC}"
fi

# Deactivate virtual environment
deactivate