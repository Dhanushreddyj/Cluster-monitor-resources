
---

# Network Discovery Script

This repository contains a network discovery script that automates the scanning of network devices and logs detailed results. The script is designed to run on macOS and uses Python 3.

## Features

- Automated network discovery using launchd on macOS.
- Enhanced logging:
  - Logs the start and end of the scanning process.
  - Logs the time taken for each scan.
  - Logs detailed results of each scan (e.g., open ports).

## Prerequisites

- macOS
- Python 3
- Homebrew

## Installation

1. **Install Python 3 using Homebrew:**
    ```sh
    brew install python
    ```

2. **Install required Python packages:**
    ```sh
    pip3 install -r requirements.txt
    ```

## Usage

1. **Set up the network discovery script (`autofsdscript.py`) to run with launchd:**

    - Copy your script (`autofsdscript.py`) to the desired location on your system.

    - Create a launchd plist file (e.g., `com.example.networkscan.plist`):
      ```xml
      <?xml version="1.0" encoding="UTF-8"?>
      <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
      <plist version="1.0">
      <dict>
          <key>Label</key>
          <string>com.example.networkscan</string>
          <key>ProgramArguments</key>
          <array>
              <string>/usr/bin/python3</string>
              <string>/path_to_your_script/autofsdscript.py</string> <!-- Update this path -->
          </array>
          <key>RunAtLoad</key>
          <true/>
          <key>StartInterval</key>
          <integer>3600</integer>
      </dict>
      </plist>
      ```

    - Load the plist file into launchd:
      ```sh
      launchctl load /path_to_plist/com.example.networkscan.plist
      ```

## Logging

The script generates logs that include:

- The start and end of the scanning process.
- The time taken for each scan.
- Detailed results of each scan, such as open ports.

Logs are stored in the directory `/path_to_logs/`. Ensure this directory is writable by the script.

## Prometheus and Grafana Setup

To locally run the dashboard, you need to install Prometheus, Alertmanager, Windows Exporter, Node Exporter, and Grafana on their respective devices. Use the configuration files provided in this repository.

1. **Install Prometheus:**
    - Follow the [Prometheus installation guide](https://prometheus.io/docs/prometheus/latest/installation/).
    - Copy the Prometheus configuration file (`prometheus.yml`) from this repository to your Prometheus installation directory.

2. **Install Alertmanager:**
    - Follow the [Alertmanager installation guide](https://prometheus.io/docs/alerting/latest/alertmanager/).
    - Copy the Alertmanager configuration file (`alertmanager.yml`) from this repository to your Alertmanager installation directory.

3. **Install Windows Exporter:**
    - Follow the [Windows Exporter installation guide](https://github.com/prometheus-community/windows_exporter).
    - Configure the Windows Exporter as needed.

4. **Install Node Exporter:**
    - Follow the [Node Exporter installation guide](https://prometheus.io/docs/guides/node-exporter/).
    - Configure the Node Exporter as needed.

5. **Install Grafana:**
    - Follow the [Grafana installation guide](https://grafana.com/docs/grafana/latest/installation/).
    - Copy the Grafana configuration files from this repository to your Grafana installation directory.
    - Import the provided dashboards into Grafana.

## Configuration

- **Prometheus Target Configuration:**
  - The script dynamically generates Prometheus target configurations in YAML format.
  - The target file path is `/opt/homebrew/etc/targets.yml`.
  - The `os` label is included for operating system detection, and the `env` label is removed.

## Development

To enhance or modify the script, follow these steps:

1. **Clone the repository:**
    ```sh
    git clone path_to_your_repository
    cd path_to_your_repository
    ```

2. **Modify the script:**
    - Edit `autofsdscript.py` to add new features or change existing ones.

3. **Test the script:**
    - Run the script manually to ensure it works as expected:
      ```sh
      /usr/bin/python3 /path_to_your_script/autofsdscript.py
      ```

4. **Commit and push your changes:**
    ```sh
    git add .
    git commit -m "Description of changes"
    git push origin main
    ```

## License

This project is not licensed under any License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please contact [Dhanush reddy Janagama](f20220005@hyderabad.bits-pilani.ac.in).

---

Replace `/path_to_your_script/` with the actual path where you place your `autofsdscript.py` file. This will guide users to customize the location based on their device folders.
