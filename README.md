# 📱 Android APK Runner

<div align="center">

![Version](https://img.shields.io/badge/version-1.0-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.7+-green?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-orange?style=for-the-badge)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=for-the-badge)

**Run Android apps and games directly on your PC with a beautiful GUI interface**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Download Tools](#-download-android-tools) • [FAQ](#-faq)

</div>

---

## 📖 Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Download Android Tools](#-download-android-tools)
- [Requirements](#-requirements)
- [How It Works](#-how-it-works)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [License](#-license)

---

## 🌟 Overview

Android APK Runner is a desktop application that provides a beautiful, user-friendly interface for running Android apps on your PC. Whether you want to test your own apps, play mobile games on a bigger screen, or use Android-exclusive applications, this tool makes it easy.

The app helps you:
- **Browse & Select** APK files from your computer
- **Install** them to Android emulators or connected devices
- **Launch** apps automatically after installation
- **Manage** multiple Android devices and emulators

---

## ✨ Features

### 📱 APK Management
- **Browse APK Files** - Select any `.apk` file from your computer
- **View APK Details** - See file size, name, modification date
- **Install to Device** - One-click installation to emulators or phones
- **Auto-Launch** - Apps automatically open after installation

### 🎮 Device Control
- **Start/Stop Emulator** - Control Android emulator directly
- **Device Detection** - Automatically find connected devices
- **Multi-Device Support** - Install to multiple devices at once
- **Real-time Status** - Live indicators for ADB and emulator status

### 📥 Built-in Download Center
- **BlueStacks** - Easiest emulator (recommended for beginners)
- **Android SDK Tools** - Lightweight ADB and Fastboot
- **Nox Player** - Lightweight emulator option
- **LDPlayer** - Gaming-optimized emulator
- **Android Studio** - Full development environment

### 🎨 Beautiful Interface
- **Modern Dark Theme** with Android green accents
- **Color-coded Console** - Success, errors, and info in different colors
- **Status Indicators** - Live ADB and emulator status dots
- **Progress Feedback** - Real-time installation progress

### 🔒 Safe & Secure
- **No File Deletion** - Only installs, never removes
- **Preview Before Install** - See APK details before installing
- **Error Handling** - Clear error messages when things go wrong

---

## 📸 Screenshots

### Main Interface
The main window shows APK selection, device controls, and a live console output.

### Download Center
Built-in tool to download all required Android software with one click.

### APK Details
View detailed information about your APK file before installation.

*(Add actual screenshots here)*

---

## 📥 Installation

### Method 1: Download Executable (Recommended)

1. Go to [Releases Page](https://github.com/Neshley/apk-runner/releases)
2. Download `APKRunner.exe`
3. Double-click to run - no installation needed!

### Method 2: Run from Source

```bash
# Clone the repository
git clone https://github.com/Neshley/apk-runner.git
cd apk-runner

# Run the application
python apk_runner.py
```

## 🔧 APK Runner - Troubleshooting Guide

### Quick Diagnostic
Before troubleshooting, run the app to see console output:
```bash
python apk_runner.py

:: Run the app
python src\apk_runner.py

:: Run diagnostic
python src\apk_diagnostic.py

:: Run the EXE
dist\APKRunner.exe

:: Build new EXE
python -m PyInstaller --onefile --windowed --name=APKRunner src\apk_runner.py

:: Install the app (as Administrator)
installer\installer.bat
```