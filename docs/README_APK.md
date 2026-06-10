# apk_runner.py - Android APK Runner for PC


📱 ANDROID APK RUNNER
Run Android apps and games directly on your PC with a beautiful GUI interface.

Version: 1.0
Author: Neshley
GitHub: https://github.com/Neshley/apk-runner
License: MIT

FEATURES:
- Browse & Select APK files from your computer
- View APK details (size, name, modification date)
- Start/Stop Android Emulator directly from the app
- Install APK to emulators or connected devices
- Auto-Launch apps after installation
- Built-in Download Center for Android tools
- Real-time console output with colored logs
- Multi-device support

REQUIREMENTS:
- Python 3.7 or higher
- No additional packages needed (uses only standard library)
- Android SDK or emulator for full functionality

QUICK START:
1. Click '📥 Get Android Tools' to download required software
2. Select an APK file using '📂 Browse APK'
3. Start emulator or connect device
4. Click '📥 Install & Run APK'

FOR BEGINNERS (Easiest Method):
1. Download BlueStacks from the Download Center
2. Install BlueStacks and open it
3. Drag your APK file onto BlueStacks window
4. Done! Your app is now running on PC

FOR DEVELOPERS:
1. Download Android Studio
2. Create a virtual device (AVD Manager)
3. Start the emulator from APK Runner
4. Install and run your APK

USING A REAL PHONE:
1. Enable Developer Options on your phone
2. Enable USB Debugging
3. Connect via USB cable
4. Select APK and click Install & Run

DOWNLOAD LINKS FOR ANDROID TOOLS:

🎮 BlueStacks (Recommended for beginners):
   https://www.bluestacks.com
   - Easiest to use - Just drag & drop APK files
   - Best for gaming and general use
   - ~500 MB download

📦 Android SDK Platform Tools (ADB & Fastboot):
   Windows: https://dl.google.com/android/repository/platform-tools-latest-windows.zip
   Mac: https://dl.google.com/android/repository/platform-tools-latest-darwin.zip
   Linux: https://dl.google.com/android/repository/platform-tools-latest-linux.zip
   - Lightweight - Just command-line tools
   - ~50 MB download

🕹️ Nox Player:
   https://www.bignox.com
   - Lightweight Android emulator
   - Good performance, easy setup
   - ~400 MB download

🎯 LDPlayer:
   https://www.ldplayer.net
   - Gaming optimized emulator
   - High performance for games
   - ~400 MB download

📱 Android Studio (Full SDK):
   https://developer.android.com/studio
   - Complete development environment
   - Includes emulator, SDK, and all tools
   - ~2 GB download

MEmu Play:
   https://www.memuplay.com
   - Supports multiple instances
   - Good for running multiple apps

GameLoop:
   https://www.gameloop.com
   - Optimized for Tencent games
   - Good for PUBG Mobile, Call of Duty Mobile

Windows Subsystem for Android (Windows 11):
   https://apps.microsoft.com/detail/9p3395vx91nr
   - Built into Windows 11
   - Requires Windows 11

TROUBLESHOOTING:

Problem: "ADB not found"
Solution: Download SDK Platform Tools from the Download Center

Problem: "No devices connected"
Solution: Start an emulator or connect a phone via USB with USB Debugging enabled

Problem: "Installation failed"
Solution: Check if APK is compatible with your Android version

Problem: "Emulator won't start"
Solution: Enable virtualization in BIOS (VT-x for Intel, SVM for AMD)

Problem: "App crashes on startup"
Solution: 
1. Check if Python 3.7+ is installed: python --version
2. Run from command line to see errors: python apk_runner.py
3. Check if tkinter is installed: python -c "import tkinter"

HOW TO ENABLE USB DEBUGGING ON ANDROID:
1. Go to Settings > About Phone
2. Tap "Build Number" 7 times until you see "You are now a developer!"
3. Go back to Settings > System > Developer Options
4. Enable "USB Debugging"
5. Connect your phone via USB cable
6. Accept the RSA key fingerprint on your phone

HOW TO ENABLE VIRTUALIZATION IN BIOS:
1. Restart your computer
2. Press F2, F10, DEL, or ESC during boot (varies by manufacturer)
3. Find "Virtualization Technology" (Intel VT-x) or "SVM Mode" (AMD)
4. Enable it
5. Save and exit

SYSTEM REQUIREMENTS:
Minimum:
- OS: Windows 10
- Python: 3.7+
- RAM: 4 GB
- Storage: 1 GB
- Processor: Dual Core

Recommended:
- OS: Windows 11
- Python: 3.10+
- RAM: 8 GB
- Storage: 5 GB
- Processor: Quad Core with VT-x/AMD-V

FILE CATEGORIES SUPPORTED:
The app can install any .apk file including:
- Games (PUBG, Call of Duty, Among Us, etc.)
- Social Media (Instagram, TikTok, Snapchat, etc.)
- Productivity (Microsoft Office, Google Drive, etc.)
- Streaming (Netflix, YouTube, Spotify, etc.)
- Custom/Development APKs



## 🔧 Diagnostic & Troubleshooting Tool

The project includes a **built-in diagnostic tool** that automatically checks your system and identifies issues with APK Runner.

### 🚀 Quick Run

```bash
python apk_diagnostic.py
```


```system output```

╔══════════════════════════════════════════╗
║    APK RUNNER DIAGNOSTIC REPORT        ║
╚══════════════════════════════════════════╝

🕐 2026-01-10 14:30:00

══════════════════════════════════════════
  🖥️ SYSTEM CHECK
══════════════════════════════════════════

   ✅ Windows 10 or higher detected
   ✅ Architecture: 64bit

══════════════════════════════════════════
  🐍 PYTHON CHECK
══════════════════════════════════════════

   ✅ Python 3.10.0 is compatible

══════════════════════════════════════════
  📦 MODULE CHECK
══════════════════════════════════════════

   ✅ tkinter             - GUI framework
   ✅ subprocess           - Running ADB commands
   ✅ threading            - Background tasks
   ... (all modules passed)

══════════════════════════════════════════
  🔌 ADB CHECK
══════════════════════════════════════════

   ✅ ADB found at: C:\Android\Sdk\platform-tools\adb.exe
   ✅ ADB is working correctly

══════════════════════════════════════════
  📊 FINAL SUMMARY
══════════════════════════════════════════

   ✅ ALL CHECKS PASSED!
   Your system is ready for APK Runner.

   Passed: 18
   Failed: 0
   Warnings: 0
   Total: 18

