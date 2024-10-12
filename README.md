# Sh-evidence

Sh-evidence is a command-line utility that captures and saves a copy of the output and error messages of the executed shell command in a log file, and also captures a screenshot of the shell window. The log file and screenshot are saved in a specified directory, and the screenshot is generated using a Python script that converts the log file into an image.

## Installation

1. Clone this repository: `git clone https://github.com/your_username/sh-evidence.git`
2. Run the `setup.sh` script to configure the default settings and create the necessary directories.
3. You can modify the settings by editing the `~/.sh-evidence.conf` file.

## Usage

1. Navigate to the directory where you want to save the log file and screenshot.
2. Echo the shell command that you want to capture.
3. Add the `| sh-evidence` pipe at the end of the command to capture the output and error messages, and generate the screenshot.
4. The log file and screenshot will be saved in the directory specified in the `~/.sh-evidence.conf` file.

## Configuration

The `~/.sh-evidence.conf` file contains the default settings for the `sh-evidence` utility. You can modify these settings by editing the file. The settings include:

- `FONT`: The font used in the generated screenshot.
- `PADDING`: The padding around the text in the generated screenshot.
- `DROP_SHADOW`: Whether to add a drop shadow to the generated screenshot. Default: False
- `EVIDENCE_DIR`: The directory where the log file and screenshot will be saved.

## License

This project is licensed under the MIT License. See the LICENSE file for more information.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you find a bug or have a suggestion for improvement.

## Credits

This project was created by Carl Sue.