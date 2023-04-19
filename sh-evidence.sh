#!/bin/sh

# Read command from the piped input
CMD=$(cat)

# Create sh-evidence folder in the user's Documents folder
EVIDENCE_DIR="$HOME/Documents/sh-evidence"
mkdir -p "$EVIDENCE_DIR"

# Extract the command used without parameters
LAST_CMD="$(echo "$CMD" | awk '{print $1}')"

# Define the log file and screenshot file names
DATE_SUFFIX="$(date +%Y%m%d%H%M%S)"
LOGFILE="$EVIDENCE_DIR/${LAST_CMD}_${DATE_SUFFIX}.log"
IMAGE="$EVIDENCE_DIR/${LAST_CMD}_${DATE_SUFFIX}.png"

# Detect the OS and adjust the script command accordingly
OS="$(uname)"
if [[ "$OS" == "Darwin" ]]; then
    echo "\$ $CMD" > "$LOGFILE"
    $CMD | tee -a "$LOGFILE" 2>&1
elif [[ "$OS" == "Linux" ]]; then
    echo "\$ $CMD" | tee -a "$LOGFILE"
    script -c "$CMD" -q "$LOGFILE"
else
    echo "Unsupported operating system"
    exit 1
fi

# Set the Python command based on the OS
if [[ "$OS" == "Darwin" ]] || [[ "$OS" == "Linux" ]]; then
    PYTHON_CMD="python3"
elif [[ "$OS" == "MINGW"* ]] || [[ "$OS" == "MSYS"* ]] || [[ "$OS" == "CYGWIN"* ]]; then
    PYTHON_CMD="python"
else
    echo "Unsupported operating system"
    exit 1
fi

# Generate an image from the log file using the Python script
$PYTHON_CMD text_to_image.py "$LOGFILE" "$IMAGE" --drop-shadow
