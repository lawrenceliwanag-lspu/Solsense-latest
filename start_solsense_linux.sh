#!/bin/bash
# SolSense Launcher - Auto-install dependencies and run application
# ============================================================

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo ""
    echo "========================================"
    echo "  $1"
    echo "========================================"
    echo ""
}

# Clear screen and show header
clear
print_header "SolSense GeoTIFF Viewer Launcher"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed!"
    echo "Please install Python 3.8 or higher:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip python3-tk"
    echo "  Fedora/RHEL:   sudo dnf install python3 python3-pip python3-tkinter"
    echo "  Arch:          sudo pacman -S python python-pip tk"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

print_success "Python found:"
python3 --version
echo ""

# Check if pip is available
if ! python3 -m pip --version &> /dev/null; then
    print_error "pip is not available!"
    echo "Please install pip:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-pip"
    echo "  Fedora/RHEL:   sudo dnf install python3-pip"
    echo "  Arch:          sudo pacman -S python-pip"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

print_success "pip found:"
python3 -m pip --version
echo ""

# Check for tkinter
if ! python3 -c "import tkinter" &> /dev/null; then
    print_warning "tkinter is not installed!"
    echo "tkinter is required for the GUI. Installing..."
    echo "You may need to enter your password for sudo access."
    echo ""
    
    # Detect distribution and install tkinter
    if [ -f /etc/debian_version ]; then
        sudo apt-get update && sudo apt-get install -y python3-tk
    elif [ -f /etc/redhat-release ]; then
        sudo dnf install -y python3-tkinter
    elif [ -f /etc/arch-release ]; then
        sudo pacman -S --noconfirm tk
    else
        print_error "Could not detect Linux distribution."
        echo "Please manually install tkinter for your distribution."
        read -p "Press Enter to continue anyway..."
    fi
    echo ""
fi

# Create a flag file to track if dependencies were installed
FLAG_FILE="/tmp/solsense_deps_installed_$(whoami).flag"

# Check if this is the first run or dependencies need installation
if [ ! -f "$FLAG_FILE" ]; then
    print_header "Installing Required Dependencies"
    print_info "This may take a few minutes on first run..."
    echo ""
    
    # Check if we need to install system dependencies for GDAL
    print_info "Checking system dependencies for GDAL/rasterio..."
    if command -v apt-get &> /dev/null; then
        print_info "Detected Debian/Ubuntu system"
        echo "Some packages may require system libraries."
        echo "If rasterio fails, run:"
        echo "  sudo apt-get install gdal-bin libgdal-dev"
    elif command -v dnf &> /dev/null; then
        print_info "Detected Fedora/RHEL system"
        echo "If rasterio fails, run:"
        echo "  sudo dnf install gdal gdal-devel"
    elif command -v pacman &> /dev/null; then
        print_info "Detected Arch system"
        echo "If rasterio fails, run:"
        echo "  sudo pacman -S gdal"
    fi
    echo ""
    
    # Upgrade pip first
    print_info "[1/7] Upgrading pip..."
    python3 -m pip install --upgrade pip --quiet --user
    
    # Install numpy first (required by many other packages)
    print_info "[2/7] Installing numpy..."
    python3 -m pip install numpy --quiet --user
    
    # Install matplotlib
    print_info "[3/7] Installing matplotlib..."
    python3 -m pip install matplotlib --quiet --user
    
    # Install Pillow
    print_info "[4/7] Installing Pillow..."
    python3 -m pip install Pillow --quiet --user
    
    # Install requests
    print_info "[5/7] Installing requests..."
    python3 -m pip install requests --quiet --user
    
    # Install psutil
    print_info "[6/7] Installing psutil..."
    python3 -m pip install psutil --quiet --user
    
    # Install rasterio (may take longer)
    print_info "[7/7] Installing rasterio (this may take a while)..."
    python3 -m pip install rasterio --user 2>&1 | grep -i "error" && {
        echo ""
        print_warning "rasterio installation encountered issues!"
        echo ""
        echo "GDAL/rasterio may require system libraries."
        echo "Try installing system dependencies:"
        echo ""
        echo "  Ubuntu/Debian:"
        echo "    sudo apt-get install gdal-bin libgdal-dev python3-gdal"
        echo ""
        echo "  Fedora/RHEL:"
        echo "    sudo dnf install gdal gdal-devel python3-gdal"
        echo ""
        echo "  Arch:"
        echo "    sudo pacman -S gdal python-gdal"
        echo ""
        echo "Alternative: Use conda instead of pip:"
        echo "  conda install -c conda-forge rasterio gdal"
        echo ""
        read -p "Press Enter to continue anyway..."
    } || {
        # Create flag file to skip installation next time
        touch "$FLAG_FILE"
        echo ""
        print_success "All dependencies installed successfully!"
    }
    
    echo ""
    print_header "Installation Complete"
    echo ""
else
    print_success "Dependencies already installed (skipping installation)"
    echo "    To force reinstall, delete: $FLAG_FILE"
    echo ""
fi

# Check if main.py exists
if [ ! -f "main.py" ]; then
    print_error "main.py not found in current directory!"
    echo "Please ensure you're running this script from the SolSense directory."
    echo ""
    echo "Current directory: $(pwd)"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Launch the application
print_header "Starting SolSense Application"

print_info "The application window will open shortly..."
print_info "This terminal will close automatically."
echo ""

# Launch the application in background and detach from terminal
python3 main.py &> /dev/null &

# Wait briefly to check if it started successfully
sleep 2

# Check if the process is still running
if pgrep -f "python3 main.py" > /dev/null; then
    print_success "Application launched successfully!"
    echo ""
    # Exit the script (terminal will close)
    exit 0
else
    print_error "Application failed to start!"
    echo ""
    echo "Common issues:"
    echo "  1. Missing tkinter: sudo apt-get install python3-tk"
    echo "  2. GDAL not installed: Install system GDAL packages"
    echo "  3. Missing resource files: Check resources/ folder"
    echo "  4. Permission issues: Check file permissions"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi