# Android APK Runner

A lightweight desktop utility for running Android APK files on a PC using an Android emulator or a connected device via ADB.

This project is designed for local use and testing workflows. It is not a hardened enterprise application and should be used carefully with APKs from untrusted sources.

## Repository name notice

The GitHub repository is named:

https://github.com/Neshley/Adroid-apk-runner

Use the exact folder name shown below when cloning and running the project. The repo name is `Adroid-apk-runner` (with `Adroid`, not `Android`).

## Features

- Browse and select APK files from the local machine
- Show basic file metadata such as name, size, and modification date
- Detect available Android SDK tools and connected devices
- Start an Android emulator if one is available
- Install APKs to an emulator or connected device through ADB
- Launch a package after installation when the package name can be identified
- Includes a small diagnostic window for troubleshooting environment issues

## Supported environments

- Windows 10 / 11 (primary target)
- macOS and Linux are possible in principle, but the Windows installer and common paths are the main tested paths
- Python 3.7+
- Android SDK Platform Tools (`adb`) and/or Android Emulator

## Security notice

This project installs APKs to real Android devices and emulators. That means it sits on a trust boundary:

- Only install APKs from sources you trust.
- Do not run APKs from unknown or unverified third parties.
- Prefer APKs with known signatures or provenance.
- Treat the application installer as a privileged system action on Windows.

This project intentionally does not perform deep APK verification or trust checks beyond basic local file handling. For production or enterprise use, add package validation, manifest parsing, and stricter user prompts.

## Requirements

- Python 3.7 or newer
- `tkinter` support in the Python installation
- Android SDK platform tools, including `adb`
- Optional: Android Emulator for local AVD testing

## Installation

### Option 1: Run from source

```bash
git clone https://github.com/Neshley/Adroid-apk-runner.git
cd Adroid-apk-runner
python src/apk_runner.py
```

If you are running from Command Prompt on Windows, the equivalent commands are:

```bat
git clone https://github.com/Neshley/Adroid-apk-runner.git
cd Adroid-apk-runner
python src\apk_runner.py
```

### Option 2: Use the bundled Windows installer

From the repository root:

```bat
installer\installer.bat
```

This installer copies the application to `Program Files\APK Runner` and creates desktop/start menu shortcuts, and it requires administrator rights. Use it only on a machine you trust.

## Usage

1. Open a terminal in the repository folder.
2. Start the app:

```bash
python src/apk_runner.py
```

On Windows CMD:

```bat
python src\apk_runner.py
```

3. Click `Browse APK` and select an `.apk` file.
4. Ensure ADB is available and a device/emulator is connected.
5. Start an Android emulator if needed.
6. Click `Install & Run` to install the APK to the selected device.

## Troubleshooting

### Folder not found after clone

Use the exact repository name:

```bat
cd Adroid-apk-runner
```

Do not use `cd Android-apk-runner` unless the folder was actually created with that name.

### ADB not found

Install Android SDK Platform Tools and make sure `adb` is available in PATH.

### Emulator not found

Install Android Studio or use a device/emulator already configured on your system.

### No devices connected

- Start an AVD in Android Studio
- Or connect a physical Android device via USB with USB debugging enabled

### App launch fails

The project currently derives a package name from the APK filename. This is a convenience heuristic and may not match the actual Android package name in the APK manifest.

## Repository structure

```text
.
├── README.md
├── LICENSE
├── requirements.txt
├── requirements-dev.txt
├── makefile.mk
├── dist/
├── docs/
├── installer/
└── src/
    ├── apk_runner.py
    ├── apk_diagnostic.py
    └── main.py
```

## Notes for maintainers

The project is compact and straightforward, but the main application file is large. Recommended follow-up improvements include:

- parse the APK manifest instead of deriving package names from the filename
- add APK signature or metadata validation
- make the installer portable and less privileged
- add automated tests and CI
- separate the UI, Android tooling logic, and diagnostics into smaller modules

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## Project status

This is a local utility for experimentation and personal use. It is functional as a simple tool for Android APK testing workflows, but it is not a fully hardened or production-grade installer.
