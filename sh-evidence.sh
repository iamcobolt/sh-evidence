#!/bin/sh

# sh-evidence: A command-line utility for capturing shell command output and generating screenshots
#
# This script captures the output of executed shell commands, saves it to a log file,
# and generates a screenshot of the captured output.
#
# Usage: <your_command> | sh-evidence [options]
#
# Options:
#   --drop-shadow: Add a drop shadow to the generated screenshot
#
# Configuration:
#   The script uses a configuration file located at ~/.sh-evidence.conf
#   If the file doesn't exist, it will be created with default settings.
#
# The log file and screenshot are saved in the directory specified in the configuration.
#
# For more information, see the README.md file in the project repository.

# Configuration and first run

# Path to the configuration file
CONFIG_FILE="$HOME/.sh-evidence.conf"

# Default configuration settings
FONT="DejaVuSansMono.ttf"
PADDING="20,20,20,20"
DROP_SHADOW="false"
EVIDENCE_DIR="$HOME/Documents/sh-evidence"

# Function to check if the --drop-shadow flag is used
# Returns "true" if the flag is present, "false" otherwise
function has_drop_shadow {
  if [[ "$*" == *"--drop-shadow"* ]]; then
    echo "true"
  else
    echo "false"
  fi
}

# Function to create the configuration file with default settings
create_config_file() {
    echo "FONT=$FONT" > $CONFIG_FILE
    echo "PADDING=$PADDING" >> $CONFIG_FILE
    echo "DROP_SHADOW=$DROP_SHADOW" >> $CONFIG_FILE
    echo "EVIDENCE_DIR=$EVIDENCE_DIR" >> $CONFIG_FILE
    mkdir -p "$EVIDENCE_DIR"
}

# Function to load the configuration from the config file
# If a setting is not defined in the config file, it uses the default value
# Returns a JSON-like string with the configuration
load_config() {
    config_file="$HOME/.sh-evidence.conf"
    if [ -f "$config_file" ]; then
        . "$config_file"
    fi

    # Set default values if not defined in the config file
    : "${FONT:=DejaVuSansMono.ttf}"
    : "${PADDING:=50}"
    : "${DROP_SHADOW:=0}"

    config="{"
    config="$config\"font\": \"$FONT\","
    config="$config\"padding\": $PADDING,"
    config="$config\"drop_shadow\": $DROP_SHADOW"
    config="$config}"

    echo "$config"
}

# Check if the config file exists, create it if it doesn't
if [ ! -f "$CONFIG_FILE" ]; then
    create_config_file
else
    config="$(load_config)"
fi

# Determine the appropriate Python command based on the operating system
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PYTHON_CMD="python3"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PYTHON_CMD="python3"
elif [[ "$OSTYPE" == "cygwin" ]]; then
    PYTHON_CMD="python"
elif [[ "$OSTYPE" == "msys" ]]; then
    PYTHON_CMD="python"
elif [[ "$OSTYPE" == "win32" ]]; then
    PYTHON_CMD="python"
else
    echo "Unsupported platform: $OSTYPE"
    exit 1
fi

# Application Functionality

# Read the command from the piped input
CMD=$(cat)

# Extract the first word of the command (the command name without parameters)
LAST_CMD="$(echo "$CMD" | awk '{print $1}')"

# Define the log file and screenshot file names with a timestamp
DATE_SUFFIX="$(date +%Y%m%d%H%M%S)"
LOGFILE="$EVIDENCE_DIR/${LAST_CMD}_${DATE_SUFFIX}.log"
IMAGE="$EVIDENCE_DIR/${LAST_CMD}_${DATE_SUFFIX}.png"

# Execute the command and save its output to the log file
# The approach differs slightly between macOS and Linux
OS="$(uname)"
if [[ "$OS" == "Darwin" ]]; then
    printf "\$ %s\n" "$CMD" >> "$LOGFILE"
    eval "$CMD" >> "$LOGFILE" 2>&1
    cat "$LOGFILE"
elif [[ "$OS" == "Linux" ]]; then
    printf "\$ %s\n" "$CMD" >> "$LOGFILE"
    script -c "$CMD" -q /dev/null >> "$LOGFILE" 2>&1
    cat "$LOGFILE"
else
    echo "Unsupported operating system"
    exit 1
fi

# Check if the --drop-shadow flag is used
DROP_SHADOW=$(has_drop_shadow "$@")

# Generate an image from the log file using the Python script
# If the --drop-shadow flag is used, pass it to the Python script
if [[ "$*" == *"--drop-shadow"* ]]; then
  $PYTHON_CMD text_to_image.py "$LOGFILE" "$IMAGE" --drop-shadow
else
  $PYTHON_CMD text_to_image.py "$LOGFILE" "$IMAGE"
fi
