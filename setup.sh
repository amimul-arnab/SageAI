#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 Setting up SageAI Dataset Generator...${NC}"

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.9+ and try again.${NC}"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${BLUE}Upgrading pip...${NC}"
pip install --upgrade pip

# Install requirements
echo -e "${BLUE}Installing requirements...${NC}"
pip install -r requirements.txt

# Create necessary directories
echo -e "${BLUE}Creating necessary directories...${NC}"
mkdir -p uploads output

# Create cache directory for models
echo -e "${BLUE}Setting up model cache...${NC}"
mkdir -p ~/.cache/gpt4all

# Create run script
echo -e "${BLUE}Creating run script...${NC}"
cat > run.sh << 'EOL'
#!/bin/bash
source venv/bin/activate
python src/main.py
EOL

chmod +x run.sh

# Success message
echo -e "${GREEN}✅ Setup complete!${NC}"
echo -e "${GREEN}To run the application:${NC}"
echo -e "${BLUE}Simply type: ${NC}./run.sh"

# Make setup.sh executable
chmod +x setup.sh