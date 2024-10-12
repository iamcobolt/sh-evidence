# Sh-evidence: Capture Shell Command Output with Style

Sh-evidence is an innovative command-line utility designed to enhance your shell experience by capturing and preserving the output of executed commands. This powerful tool not only saves a comprehensive log of command output and error messages but also generates visually appealing screenshots of your shell window, providing a complete record of your command-line interactions.

## Key Features

- **Command Output Logging**: Automatically saves both standard output and error messages from executed shell commands.
- **Visual Documentation**: Generates high-quality screenshots of your shell window, preserving the visual context of your command execution.
- **Customizable Appearance**: Offers configurable options for fonts, padding, and visual effects to match your preferences.
- **Seamless Integration**: Easily incorporates into your existing workflow with a simple pipe command.

## Installation

To get started with Sh-evidence, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/your_username/sh-evidence.git
   ```
2. Run the setup script to configure default settings and create necessary directories:
   ```
   ./setup.sh
   ```
3. (Optional) Fine-tune your configuration by editing `~/.sh-evidence.conf`.

## Usage Guide

Integrating Sh-evidence into your command-line workflow is straightforward:

1. Navigate to your desired working directory.
2. Execute your shell command as usual.
3. Append `| sh-evidence` to your command to activate Sh-evidence:
   ```
   your_command | sh-evidence
   ```
4. Sh-evidence will capture the command output and generate a screenshot, saving both in the directory specified in your configuration.

## Advanced Configuration

Sh-evidence offers extensive customization options through the `~/.sh-evidence.conf` file:

- `FONT`: Specify the font for screenshot text rendering.
- `PADDING`: Adjust the padding around the text in screenshots for optimal readability.
- `DROP_SHADOW`: Enable or disable drop shadow effects (Default: False).
- `EVIDENCE_DIR`: Set the directory for storing log files and screenshots.

## Licensing

Sh-evidence is open-source software, released under the MIT License. For full details, please refer to the LICENSE file in the repository.

## Community and Contributions

We welcome contributions from the community! Whether you've found a bug, have a feature suggestion, or want to contribute code, please feel free to:

- Submit pull requests
- Open issues for bug reports or feature requests
- Share your ideas for improvements

Your input is valuable in making Sh-evidence even better!

## Acknowledgments

Sh-evidence was created by Carl Sue. We extend our gratitude to all contributors and users who have helped shape this project.