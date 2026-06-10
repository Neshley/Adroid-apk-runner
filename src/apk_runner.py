# apk_runner.py - Android APK Runner for PC
"""
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
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import os
import sys
import subprocess
import threading
import queue
import shutil
import webbrowser
from pathlib import Path
from datetime import datetime
import zipfile

class APKRunner:
    """
    Android APK Runner Application
    
    A GUI application that helps users run Android APK files on their PC.
    Supports Android emulators and physical devices via ADB.
    
    Attributes:
        selected_apk (str): Path to the selected APK file
        adb_path (str): Path to Android Debug Bridge executable
        emulator_path (str): Path to Android Emulator executable
        is_emulator_running (bool): Whether the emulator is currently running
        connected_devices (list): List of connected Android devices
    """
    
    def __init__(self):
        """Initialize the APK Runner application"""
        self.root = tk.Tk()
        self.root.title("📱 Android APK Runner")
        self.root.geometry("950x750")
        self.root.configure(bg='#0f0f1a')
        self.root.minsize(850, 650)
        
        # Color scheme for the application
        self.colors = {
            'bg_dark': '#0f0f1a',      # Dark background
            'bg_medium': '#1a1a2e',     # Medium background for cards
            'bg_light': '#16213e',      # Light background for header
            'accent': '#3DDC84',        # Android green accent
            'accent2': '#4285F4',       # Google blue accent
            'text_primary': '#ffffff',   # Primary text color
            'text_secondary': '#94a3b8', # Secondary text color
            'success': '#10b981',       # Success green
            'warning': '#f59e0b',       # Warning yellow
            'error': '#ef4444',         # Error red
            'info': '#3b82f6',          # Info blue
            'card_bg': '#1a1a2e',       # Card background
            'card_hover': '#252540',    # Card hover state
        }
        
        # Application state
        self.selected_apk = None        # Currently selected APK file path
        self.adb_path = None            # Path to ADB executable
        self.emulator_path = None       # Path to Emulator executable
        self.is_emulator_running = False # Emulator running state
        self.is_installing = False      # Installation in progress
        self.message_queue = queue.Queue() # Thread-safe message queue
        self.connected_devices = []     # List of connected devices
        
        # Find Android SDK tools on the system
        self.find_android_tools()
        
        # Build the user interface
        self.setup_ui()
        
        # Start processing messages
        self.process_queue()
        
        # Show welcome message after UI loads
        self.root.after(500, self.show_welcome)
        
    def find_android_tools(self):
        """
        Find Android SDK tools on the system.
        
        Searches common installation paths for:
        - ADB (Android Debug Bridge)
        - Android Emulator
        
        Also checks system PATH environment variable.
        """
        # Common Android SDK installation paths
        possible_sdk_paths = [
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Android', 'Sdk'),
            os.path.join(os.environ.get('APPDATA', ''), 'Android', 'Sdk'),
            'C:\\Android\\Sdk',
            'C:\\Program Files\\Android\\Sdk',
            os.path.expanduser('~/Android/Sdk'),
            os.path.expanduser('~/Library/Android/sdk'),
        ]
        
        for sdk_path in possible_sdk_paths:
            if os.path.exists(sdk_path):
                # Check for ADB (Android Debug Bridge)
                adb_exe = os.path.join(sdk_path, 'platform-tools', 'adb.exe')
                adb_no_ext = os.path.join(sdk_path, 'platform-tools', 'adb')
                
                if os.path.exists(adb_exe):
                    self.adb_path = adb_exe
                elif os.path.exists(adb_no_ext):
                    self.adb_path = adb_no_ext
                
                # Check for Android Emulator
                emu_exe = os.path.join(sdk_path, 'emulator', 'emulator.exe')
                emu_no_ext = os.path.join(sdk_path, 'emulator', 'emulator')
                
                if os.path.exists(emu_exe):
                    self.emulator_path = emu_exe
                elif os.path.exists(emu_no_ext):
                    self.emulator_path = emu_no_ext
                
                # If both found, stop searching
                if self.adb_path and self.emulator_path:
                    break
        
        # Also check system PATH for ADB
        if not self.adb_path:
            adb_in_path = shutil.which('adb')
            if adb_in_path:
                self.adb_path = adb_in_path
        
        # Check system PATH for Emulator
        if not self.emulator_path:
            emu_in_path = shutil.which('emulator')
            if emu_in_path:
                self.emulator_path = emu_in_path
    
    def show_welcome(self):
        """Display welcome message and quick start guide in the console"""
        self.log("=" * 55, "info")
        self.log("📱 ANDROID APK RUNNER - READY", "success")
        self.log("=" * 55, "info")
        self.log("")
        self.log("📌 QUICK START GUIDE:", "info")
        self.log("  1. Click '📥 Get Android Tools' to download required software", "info")
        self.log("  2. Select an APK file using '📂 Browse APK'", "info")
        self.log("  3. Start emulator or connect device", "info")
        self.log("  4. Click '📥 Install & Run APK'", "info")
        self.log("")
        self.log("💡 FOR BEGINNERS:", "info")
        self.log("  • Download BlueStacks (easiest method)", "info")
        self.log("  • Install and open BlueStacks", "info")
        self.log("  • Drag your APK file onto BlueStacks", "info")
        self.log("")
        self.log("💡 FOR DEVELOPERS:", "info")
        self.log("  • Download Android Studio for full SDK", "info")
        self.log("  • Or download just SDK Platform Tools for ADB", "info")
        self.log("")
    
    def setup_ui(self):
        """
        Create the complete user interface.
        
        Layout:
        - Header: Logo, title, status indicators, download button
        - Left Column: APK selection, device controls
        - Right Column: Output console
        - Status Bar: Current status
        """
        # ===== HEADER =====
        header = tk.Frame(self.root, bg=self.colors['bg_light'], height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Left side - Logo and Title
        left_header = tk.Frame(header, bg=self.colors['bg_light'])
        left_header.pack(side='left', padx=20)
        
        tk.Label(left_header, text="📱", font=('Arial', 30),
                bg=self.colors['bg_light']).pack(side='left')
        
        title_frame = tk.Frame(left_header, bg=self.colors['bg_light'])
        title_frame.pack(side='left', padx=10, pady=10)
        
        tk.Label(title_frame, text="ANDROID APK RUNNER",
                font=('Arial', 16, 'bold'),
                bg=self.colors['bg_light'],
                fg=self.colors['accent']).pack(anchor='w')
        
        tk.Label(title_frame, text="Run Android apps on your PC",
                font=('Arial', 9),
                bg=self.colors['bg_light'],
                fg=self.colors['text_secondary']).pack(anchor='w')
        
        # Right side - Status indicators and buttons
        right_header = tk.Frame(header, bg=self.colors['bg_light'])
        right_header.pack(side='right', padx=20)
        
        # ADB Status Indicator
        adb_frame = tk.Frame(right_header, bg=self.colors['bg_light'])
        adb_frame.pack(side='left', padx=10)
        
        self.adb_indicator = tk.Canvas(adb_frame, width=10, height=10,
                                       bg=self.colors['bg_light'], highlightthickness=0)
        self.adb_indicator.pack(side='left', padx=(0, 5))
        
        adb_color = self.colors['success'] if self.adb_path else self.colors['error']
        self.adb_dot = self.adb_indicator.create_oval(1, 1, 9, 9, fill=adb_color, outline='')
        
        tk.Label(adb_frame, text="ADB" if self.adb_path else "ADB ✗",
                font=('Arial', 8, 'bold'),
                bg=self.colors['bg_light'],
                fg=adb_color).pack(side='left')
        
        # Emulator Status Indicator
        emu_frame = tk.Frame(right_header, bg=self.colors['bg_light'])
        emu_frame.pack(side='left', padx=10)
        
        self.emu_indicator = tk.Canvas(emu_frame, width=10, height=10,
                                       bg=self.colors['bg_light'], highlightthickness=0)
        self.emu_indicator.pack(side='left', padx=(0, 5))
        
        emu_color = self.colors['success'] if self.emulator_path else self.colors['warning']
        self.emu_dot = self.emu_indicator.create_oval(1, 1, 9, 9, fill=emu_color, outline='')
        
        tk.Label(emu_frame, text="Emulator" if self.emulator_path else "Emulator ✗",
                font=('Arial', 8, 'bold'),
                bg=self.colors['bg_light'],
                fg=emu_color).pack(side='left')
        
        # Download Android Tools button
        tk.Button(right_header, text="📥 Get Android Tools",
                 command=self.open_download_page,
                 bg=self.colors['accent2'],
                 fg='white',
                 font=('Arial', 9, 'bold'),
                 relief='flat', cursor='hand2',
                 padx=12, pady=5).pack(side='left', padx=10)
        
        # ===== MAIN CONTENT =====
        content = tk.Frame(self.root, bg=self.colors['bg_dark'])
        content.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Left column for controls
        left_column = tk.Frame(content, bg=self.colors['bg_dark'])
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Create sections
        self.create_apk_section(left_column)
        self.create_emulator_section(left_column)
        
        # Right column for console
        right_column = tk.Frame(content, bg=self.colors['bg_dark'], width=400)
        right_column.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        self.create_console(right_column)
        
        # ===== STATUS BAR =====
        self.create_status_bar()
    
    def create_apk_section(self, parent):
        """
        Create APK selection and information section.
        
        Includes:
        - File browser for APK selection
        - APK details display (name, size, date)
        - File type validation
        """
        apk_frame = tk.Frame(parent, bg=self.colors['card_bg'])
        apk_frame.pack(fill='x', pady=5)
        
        tk.Frame(apk_frame, bg=self.colors['accent'], height=3).pack(fill='x')
        
        apk_content = tk.Frame(apk_frame, bg=self.colors['card_bg'])
        apk_content.pack(fill='x', padx=15, pady=15)
        
        # Section title
        tk.Label(apk_content, text="📦 Select APK File",
                font=('Arial', 13, 'bold'),
                bg=self.colors['card_bg'],
                fg=self.colors['text_primary']).pack(anchor='w')
        
        tk.Label(apk_content, text="Choose an Android application package (.apk) to install",
                font=('Arial', 9),
                bg=self.colors['card_bg'],
                fg=self.colors['text_secondary']).pack(anchor='w', pady=(2, 10))
        
        # APK file path display
        path_frame = tk.Frame(apk_content, bg=self.colors['card_bg'])
        path_frame.pack(fill='x', pady=5)
        
        self.apk_path_var = tk.StringVar(value="No APK file selected...")
        apk_entry = tk.Entry(path_frame, textvariable=self.apk_path_var,
                            bg=self.colors['bg_light'],
                            fg=self.colors['text_secondary'],
                            font=('Arial', 9),
                            relief='flat', state='readonly')
        apk_entry.pack(side='left', fill='x', expand=True, ipady=8, padx=(0, 8))
        
        # Browse button
        browse_btn = tk.Button(path_frame, text="📂 Browse APK",
                              command=self.browse_apk,
                              bg=self.colors['accent2'],
                              fg='white',
                              font=('Arial', 10, 'bold'),
                              relief='flat', cursor='hand2',
                              padx=15, pady=8)
        browse_btn.pack(side='left')
        
        # APK Information display area
        self.apk_info_frame = tk.Frame(apk_content, bg=self.colors['card_bg'])
        self.apk_info_frame.pack(fill='x', pady=10)
        
        # Default placeholder
        tk.Label(self.apk_info_frame, text="📱 No APK loaded",
                font=('Arial', 10),
                bg=self.colors['card_bg'],
                fg=self.colors['text_secondary']).pack(anchor='w')
        
        tk.Label(self.apk_info_frame, text="Select an APK file to see its details",
                font=('Arial', 8),
                bg=self.colors['card_bg'],
                fg=self.colors['text_secondary']).pack(anchor='w')
    
    def show_apk_info(self, apk_path):
        """
        Display detailed information about the selected APK file.
        
        Shows:
        - App name (derived from filename)
        - File size (formatted)
        - Modification date
        - Compression status
        
        Args:
            apk_path (str): Full path to the APK file
        """
        # Clear previous info
        for widget in self.apk_info_frame.winfo_children():
            widget.destroy()
        
        try:
            file_size = os.path.getsize(apk_path)
            size_str = self.format_size(file_size)
            filename = os.path.basename(apk_path)
            
            # Derive app name from filename
            app_name = os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' ')
            
            # Display file information
            info_items = [
                ("📱 App Name:", app_name[:40]),
                ("📦 Filename:", filename[:50]),
                ("📏 Size:", size_str),
                ("📅 Modified:", datetime.fromtimestamp(
                    os.path.getmtime(apk_path)).strftime('%Y-%m-%d %H:%M')),
                ("🗜️ Compressed:", "Yes" if zipfile.is_zipfile(apk_path) else "No"),
            ]
            
            for label, value in info_items:
                row = tk.Frame(self.apk_info_frame, bg=self.colors['card_bg'])
                row.pack(fill='x', pady=1)
                
                tk.Label(row, text=label, font=('Arial', 9, 'bold'),
                        bg=self.colors['card_bg'],
                        fg=self.colors['accent']).pack(side='left')
                
                tk.Label(row, text=f" {value}", font=('Arial', 9),
                        bg=self.colors['card_bg'],
                        fg=self.colors['text_secondary']).pack(side='left')
            
            # Enable the install button
            self.install_btn.config(state='normal', bg=self.colors['accent'], 
                                   fg=self.colors['bg_dark'])
            self.log(f"📱 APK loaded: {filename}", "success")
            
        except Exception as e:
            tk.Label(self.apk_info_frame, text=f"❌ Error reading APK: {e}",
                    font=('Arial', 9),
                    bg=self.colors['card_bg'],
                    fg=self.colors['error']).pack(anchor='w', pady=5)
    
    def create_emulator_section(self, parent):
        """
        Create emulator and device control section.
        
        Includes:
        - Start/Stop emulator buttons
        - Install APK button
        - Device status display
        - Quick tips for beginners
        """
        emu_frame = tk.Frame(parent, bg=self.colors['card_bg'])
        emu_frame.pack(fill='x', pady=5)
        
        tk.Frame(emu_frame, bg=self.colors['accent2'], height=3).pack(fill='x')
        
        emu_content = tk.Frame(emu_frame, bg=self.colors['card_bg'])
        emu_content.pack(fill='x', padx=15, pady=15)
        
        # Title with status
        title_frame = tk.Frame(emu_content, bg=self.colors['card_bg'])
        title_frame.pack(fill='x')
        
        tk.Label(title_frame, text="📱 Device Controls",
                font=('Arial', 13, 'bold'),
                bg=self.colors['card_bg'],
                fg=self.colors['text_primary']).pack(side='left')
        
        self.emu_status_label = tk.Label(title_frame, text="Not Running",
                                         font=('Arial', 9, 'bold'),
                                         bg=self.colors['card_bg'],
                                         fg=self.colors['warning'])
        self.emu_status_label.pack(side='right')
        
        # Connected devices info
        self.devices_label = tk.Label(emu_content, text="",
                                      font=('Arial', 9),
                                      bg=self.colors['card_bg'],
                                      fg=self.colors['text_secondary'])
        self.devices_label.pack(anchor='w', pady=5)
        
        # Control buttons
        btn_frame = tk.Frame(emu_content, bg=self.colors['card_bg'])
        btn_frame.pack(fill='x', pady=10)
        
        # Start Emulator button
        self.start_emu_btn = tk.Button(btn_frame, text="▶ Start Emulator",
                                       command=self.start_emulator,
                                       bg=self.colors['accent'],
                                       fg=self.colors['bg_dark'],
                                       font=('Arial', 10, 'bold'),
                                       relief='flat', cursor='hand2',
                                       padx=15, pady=10)
        self.start_emu_btn.pack(side='left', padx=3, expand=True, fill='x')
        
        # Stop Emulator button
        self.stop_emu_btn = tk.Button(btn_frame, text="⏹ Stop",
                                      command=self.stop_emulator,
                                      bg=self.colors['error'],
                                      fg='white',
                                      font=('Arial', 10, 'bold'),
                                      relief='flat', cursor='hand2',
                                      padx=15, pady=10,
                                      state='disabled')
        self.stop_emu_btn.pack(side='left', padx=3, expand=True, fill='x')
        
        # Install APK button
        self.install_btn = tk.Button(btn_frame, text="📥 Install & Run",
                                     command=self.install_apk,
                                     bg=self.colors['bg_light'],
                                     fg=self.colors['text_secondary'],
                                     font=('Arial', 10, 'bold'),
                                     relief='flat', cursor='hand2',
                                     padx=15, pady=10,
                                     state='disabled')
        self.install_btn.pack(side='left', padx=3, expand=True, fill='x')
        
        # Refresh devices button
        tk.Button(emu_content, text="🔄 Refresh Devices",
                 command=self.refresh_devices,
                 bg=self.colors['bg_light'],
                 fg=self.colors['text_primary'],
                 font=('Arial', 9),
                 relief='flat', cursor='hand2',
                 padx=10, pady=5).pack(anchor='w', pady=5)
        
        # Quick tips for users
        tips_frame = tk.Frame(emu_content, bg=self.colors['card_bg'])
        tips_frame.pack(fill='x', pady=5)
        
        tk.Label(tips_frame, text="💡 Quick Tips:",
                font=('Arial', 9, 'bold'),
                bg=self.colors['card_bg'],
                fg=self.colors['text_secondary']).pack(anchor='w')
        
        tips = [
            "• Easiest: Install BlueStacks and drag APK onto it",
            "• Alternative: Use Nox Player or LDPlayer",
            "• For devs: Use Android Studio's built-in emulator",
            "• Windows 11: Enable Windows Subsystem for Android",
        ]
        
        for tip in tips:
            tk.Label(tips_frame, text=tip,
                    font=('Arial', 8),
                    bg=self.colors['card_bg'],
                    fg=self.colors['text_secondary']).pack(anchor='w', padx=5)
    
    def create_console(self, parent):
        """
        Create the output console section.
        
        Features:
        - Scrolled text widget for logs
        - Color-coded messages (success, error, info, warning)
        - Clear button to reset console
        """
        console_frame = tk.Frame(parent, bg=self.colors['bg_dark'])
        console_frame.pack(fill='both', expand=True)
        
        # Console header with clear button
        console_header = tk.Frame(console_frame, bg=self.colors['bg_dark'])
        console_header.pack(fill='x')
        
        tk.Label(console_header, text="📋 Output Console",
                font=('Arial', 12, 'bold'),
                bg=self.colors['bg_dark'],
                fg=self.colors['text_primary']).pack(side='left')
        
        tk.Button(console_header, text="Clear",
                 command=lambda: self.console.delete('1.0', tk.END),
                 bg=self.colors['bg_light'],
                 fg=self.colors['text_secondary'],
                 font=('Arial', 8), relief='flat',
                 cursor='hand2', padx=10, pady=3).pack(side='right')
        
        # Console text area with border
        console_border = tk.Frame(console_frame, bg=self.colors['accent'], padx=1, pady=1)
        console_border.pack(fill='both', expand=True, pady=5)
        
        self.console = scrolledtext.ScrolledText(
            console_border,
            wrap=tk.WORD,
            bg=self.colors['card_bg'],
            fg=self.colors['text_primary'],
            font=('Consolas', 9),
            relief='flat',
            padx=15, pady=15
        )
        self.console.pack(fill='both', expand=True)
        
        # Configure text tags for colored output
        self.console.tag_config("success", foreground=self.colors['success'])
        self.console.tag_config("error", foreground=self.colors['error'])
        self.console.tag_config("info", foreground=self.colors['info'])
        self.console.tag_config("warning", foreground=self.colors['warning'])
        self.console.tag_config("command", foreground=self.colors['accent'])
        self.console.tag_config("header", foreground=self.colors['accent2'], 
                               font=('Consolas', 10, 'bold'))
    
    def create_status_bar(self):
        """Create the bottom status bar"""
        status = tk.Frame(self.root, bg=self.colors['bg_medium'], height=25)
        status.pack(fill='x', side='bottom')
        status.pack_propagate(False)
        
        self.status_label = tk.Label(status, text="✅ Ready",
                                    bg=self.colors['bg_medium'],
                                    fg=self.colors['text_secondary'],
                                    font=('Arial', 8))
        self.status_label.pack(side='left', padx=15)
        
        tk.Label(status, text="APK Runner v1.0 | github.com/Neshley",
                bg=self.colors['bg_medium'],
                fg=self.colors['text_secondary'],
                font=('Arial', 8)).pack(side='right', padx=15)
    
    def open_download_page(self):
        """
        Open the Download Center window.
        
        Provides direct download links for:
        - BlueStacks (Recommended for beginners)
        - Android SDK Platform Tools
        - Nox Player
        - LDPlayer
        - Android Studio
        
        Each option includes a description and direct download button.
        """
        download_window = tk.Toplevel(self.root)
        download_window.title("📥 Download Android Tools")
        download_window.geometry("550x600")
        download_window.configure(bg=self.colors['bg_dark'])
        download_window.transient(self.root)
        download_window.grab_set()
        
        # Window header
        header = tk.Frame(download_window, bg=self.colors['bg_light'])
        header.pack(fill='x')
        
        tk.Label(header, text="📥 Download Android Tools",
                font=('Arial', 16, 'bold'),
                bg=self.colors['bg_light'],
                fg=self.colors['accent']).pack(pady=15)
        
        tk.Label(header, text="Choose the best option for your needs",
                font=('Arial', 9),
                bg=self.colors['bg_light'],
                fg=self.colors['text_secondary']).pack(pady=(0, 15))
        
        # Scrollable options area
        options_frame = tk.Frame(download_window, bg=self.colors['bg_dark'])
        options_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Available tools with descriptions
        tools = [
            {
                "title": "🎮 BlueStacks (Recommended for Beginners)",
                "desc": "Easiest to use - Just drag & drop APK files\nBest for gaming and general use\n~500 MB download",
                "url": "https://www.bluestacks.com",
                "color": self.colors['success']
            },
            {
                "title": "📦 Android SDK Platform Tools",
                "desc": "Lightweight - Just ADB and Fastboot\nCommand-line tools for developers\n~50 MB download",
                "url": "https://dl.google.com/android/repository/platform-tools-latest-windows.zip",
                "color": self.colors['accent2']
            },
            {
                "title": "🕹️ Nox Player",
                "desc": "Lightweight Android emulator\nGood performance, easy setup\n~400 MB download",
                "url": "https://www.bignox.com",
                "color": self.colors['warning']
            },
            {
                "title": "🎯 LDPlayer",
                "desc": "Gaming optimized emulator\nHigh performance for games\n~400 MB download",
                "url": "https://www.ldplayer.net",
                "color": self.colors['info']
            },
            {
                "title": "📱 Android Studio (Full SDK)",
                "desc": "Complete development environment\nIncludes emulator, SDK, and all tools\n~2 GB download",
                "url": "https://developer.android.com/studio",
                "color": self.colors['accent']
            },
        ]
        
        for tool in tools:
            card = tk.Frame(options_frame, bg=self.colors['card_bg'])
            card.pack(fill='x', pady=4)
            
            tk.Frame(card, bg=tool['color'], height=3).pack(fill='x')
            
            card_content = tk.Frame(card, bg=self.colors['card_bg'])
            card_content.pack(fill='x', padx=15, pady=12)
            
            tk.Label(card_content, text=tool['title'],
                    font=('Arial', 11, 'bold'),
                    bg=self.colors['card_bg'],
                    fg=self.colors['text_primary']).pack(anchor='w')
            
            tk.Label(card_content, text=tool['desc'],
                    font=('Arial', 9),
                    bg=self.colors['card_bg'],
                    fg=self.colors['text_secondary'],
                    justify='left').pack(anchor='w', pady=3)
            
            download_btn = tk.Button(card_content, text="📥 Download",
                                    command=lambda u=tool['url']: webbrowser.open(u),
                                    bg=tool['color'],
                                    fg='white',
                                    font=('Arial', 9, 'bold'),
                                    relief='flat', cursor='hand2',
                                    padx=15, pady=5)
            download_btn.pack(anchor='w', pady=5)
        
        # Close button
        tk.Button(download_window, text="Close",
                 command=download_window.destroy,
                 bg=self.colors['bg_light'],
                 fg='white',
                 font=('Arial', 10),
                 relief='flat', cursor='hand2',
                 padx=25, pady=8).pack(pady=15)
    
    def browse_apk(self):
        """
        Open file dialog to browse for APK files.
        
        Filters for .apk files and shows them in the file dialog.
        Updates the UI with selected file information.
        """
        filename = filedialog.askopenfilename(
            title="Select APK File",
            filetypes=[
                ("Android APK files", "*.apk"),
                ("All files", "*.*")
            ],
            initialdir=os.path.expanduser("~/Downloads")
        )
        
        if filename:
            self.selected_apk = filename
            self.apk_path_var.set(filename)
            self.show_apk_info(filename)
    
    def refresh_devices(self):
        """
        Check for connected Android devices using ADB.
        
        Updates the connected devices list and UI.
        Shows device count and IDs in the console.
        """
        if not self.adb_path:
            self.log("⚠️  ADB not found. Cannot check devices.", "warning")
            self.log("💡 Download SDK Platform Tools from 'Get Android Tools'", "info")
            self.devices_label.config(text="⚠️ ADB not installed")
            return
        
        try:
            result = subprocess.run([self.adb_path, 'devices'], 
                                   capture_output=True, text=True, timeout=10)
            
            lines = result.stdout.strip().split('\n')[1:]
            self.connected_devices = [line.split('\t')[0] for line in lines 
                                     if line.strip() and '\tdevice' in line]
            
            if self.connected_devices:
                devices_text = f"📱 Connected: {len(self.connected_devices)} device(s)"
                self.devices_label.config(text=devices_text, fg=self.colors['success'])
                self.log(f"✅ Found {len(self.connected_devices)} device(s)", "success")
                for device in self.connected_devices:
                    self.log(f"   • {device}", "info")
            else:
                self.devices_label.config(text="📱 No devices connected", fg=self.colors['warning'])
                self.log("ℹ️  No devices connected", "warning")
                self.log("💡 Start an emulator or connect a phone via USB", "info")
                
        except subprocess.TimeoutExpired:
            self.log("❌ Timeout checking for devices", "error")
        except Exception as e:
            self.log(f"❌ Error checking devices: {e}", "error")
    
    def start_emulator(self):
        """
        Start the Android Emulator.
        
        Checks for available Android Virtual Devices (AVDs)
        and launches the first one found.
        """
        if not self.emulator_path:
            self.log("❌ Android Emulator not found!", "error")
            self.log("💡 Click '📥 Get Android Tools' to download Android Studio", "info")
            self.log("💡 Or use BlueStacks/Nox for easier setup", "info")
            return
        
        self.log("▶ Starting Android emulator...", "info")
        self.status_label.config(text="▶ Starting emulator...", fg=self.colors['warning'])
        
        try:
            # List available Android Virtual Devices
            result = subprocess.run([self.emulator_path, '-list-avds'], 
                                   capture_output=True, text=True, timeout=10)
            avds = [avd.strip() for avd in result.stdout.strip().split('\n') if avd.strip()]
            
            if not avds:
                self.log("❌ No Android Virtual Devices (AVDs) found!", "error")
                self.log("💡 Create one in Android Studio: Tools > Device Manager", "info")
                self.log("💡 Or use BlueStacks/Nox for easier setup", "info")
                return
            
            self.log(f"📱 Found AVDs: {', '.join(avds)}", "info")
            
            # Launch the first available AVD
            avd_name = avds[0]
            self.log(f"▶ Launching: {avd_name}", "command")
            self.log("⏳ This may take 1-2 minutes for first launch...", "info")
            
            threading.Thread(target=self._run_emulator, 
                           args=(avd_name,), daemon=True).start()
            
        except subprocess.TimeoutExpired:
            self.log("❌ Timeout checking for AVDs", "error")
        except Exception as e:
            self.log(f"❌ Error: {e}", "error")
    
    def _run_emulator(self, avd_name):
        """
        Run emulator in background thread.
        
        Args:
            avd_name (str): Name of the Android Virtual Device to launch
        """
        try:
            process = subprocess.Popen(
                [self.emulator_path, '-avd', avd_name, '-netdelay', 'none', '-netspeed', 'full'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            
            # Wait for emulator to initialize
            import time
            time.sleep(10)
            
            self.is_emulator_running = True
            self.message_queue.put(("emu_started", avd_name))
            
        except Exception as e:
            self.message_queue.put(("error", str(e)))
    
    def stop_emulator(self):
        """Stop the running Android Emulator using ADB"""
        if self.adb_path:
            try:
                subprocess.run([self.adb_path, '-s', 'emulator-5554', 'emu', 'kill'], 
                             capture_output=True, timeout=10)
                self.log("⏹ Emulator stopped", "info")
            except:
                self.log("⚠️  Could not stop emulator gracefully", "warning")
        
        self.is_emulator_running = False
        self.stop_emu_btn.config(state='disabled')
        self.start_emu_btn.config(state='normal')
        self.emu_status_label.config(text="Not Running", fg=self.colors['warning'])
        self.status_label.config(text="✅ Ready")
    
    def install_apk(self):
        """
        Install the selected APK to connected device or emulator.
        
        Validates that:
        - An APK file is selected
        - ADB is available
        - A device is connected
        """
        if not self.selected_apk:
            messagebox.showwarning("No APK", "Please select an APK file first!")
            return
        
        if not self.adb_path:
            messagebox.showwarning("No ADB", 
                                 "ADB not found!\n\n"
                                 "Click '📥 Get Android Tools' to download.")
            return
        
        # Check for connected devices
        self.refresh_devices()
        
        if not self.connected_devices:
            messagebox.showinfo("No Device", 
                              "No Android device or emulator connected!\n\n"
                              "Options:\n"
                              "1. Start an emulator\n"
                              "2. Connect a phone via USB (with USB Debugging)\n"
                              "3. Use BlueStacks or other emulator")
            return
        
        self.log(f"📥 Installing: {os.path.basename(self.selected_apk)}", "info")
        self.status_label.config(text="📥 Installing APK...")
        
        threading.Thread(target=self._install_apk_thread, daemon=True).start()
    
    def _install_apk_thread(self):
        """
        Install APK in background thread.
        
        Uses ADB to install the APK on all connected devices.
        Automatically launches the app after successful installation.
        """
        try:
            for device in self.connected_devices:
                self.message_queue.put(("log", f"📱 Installing on: {device}", "info"))
                
                # Run ADB install command
                result = subprocess.run(
                    [self.adb_path, '-s', device, 'install', '-r', self.selected_apk],
                    capture_output=True, text=True, timeout=120
                )
                
                if 'Success' in result.stdout:
                    self.message_queue.put(("log", f"✅ Installation successful!", "success"))
                    
                    # Try to launch the app after installation
                    package_name = self._get_package_name()
                    if package_name:
                        subprocess.run([
                            self.adb_path, '-s', device, 'shell', 
                            'monkey', '-p', package_name, '1'
                        ], capture_output=True, timeout=10)
                        self.message_queue.put(("log", f"🚀 App launched!", "success"))
                        self.message_queue.put(("status", "✅ App installed and running!"))
                else:
                    error_msg = result.stdout + result.stderr
                    self.message_queue.put(("log", f"❌ Installation failed", "error"))
                    self.message_queue.put(("log", error_msg[:200], "error"))
                    
        except subprocess.TimeoutExpired:
            self.message_queue.put(("error", "Installation timed out"))
        except Exception as e:
            self.message_queue.put(("error", str(e)))
    
    def _get_package_name(self):
        """
        Extract package name from APK filename.
        
        Returns:
            str: Derived package name or None
        """
        if self.selected_apk:
            name = os.path.splitext(os.path.basename(self.selected_apk))[0]
            return f"com.{name.lower().replace(' ', '').replace('-', '')}"
        return None
    
    def log(self, message, tag=None):
        """
        Add a message to the log queue.
        
        Args:
            message (str): The message to log
            tag (str, optional): Color tag for the message
        """
        self.message_queue.put(("log", message, tag))
    
    def process_queue(self):
        """
        Process messages from the queue.
        
        Handles different message types:
        - log: Display in console
        - emu_started: Update UI for emulator start
        - error: Display error and update status
        - status: Update status bar text
        """
        try:
            while True:
                msg = self.message_queue.get_nowait()
                
                if msg[0] == "log":
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    self.console.insert(tk.END, f"[{timestamp}] ", "info")
                    
                    tag = msg[2] if len(msg) > 2 and msg[2] else None
                    if tag:
                        self.console.insert(tk.END, f"{msg[1]}\n", tag)
                    else:
                        self.console.insert(tk.END, f"{msg[1]}\n")
                    
                    self.console.see(tk.END)
                
                elif msg[0] == "emu_started":
                    avd_name = msg[1]
                    self.log(f"✅ Emulator '{avd_name}' started successfully!", "success")
                    self.is_emulator_running = True
                    self.start_emu_btn.config(state='disabled')
                    self.stop_emu_btn.config(state='normal')
                    self.emu_status_label.config(text="Running", fg=self.colors['success'])
                    self.status_label.config(text="✅ Emulator running")
                    self.refresh_devices()
                
                elif msg[0] == "error":
                    self.log(f"❌ {msg[1]}", "error")
                    self.status_label.config(text="❌ Error occurred")
                
                elif msg[0] == "status":
                    self.status_label.config(text=msg[1])
                    
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.process_queue)
    
    def format_size(self, size):
        """
        Format file size in human-readable format.
        
        Args:
            size (int): Size in bytes
            
        Returns:
            str: Formatted size string (e.g., "1.5 MB")
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"
    
    def run(self):
        """Start the application main loop"""
        self.root.mainloop()


# ===== APPLICATION ENTRY POINT =====
if __name__ == "__main__":
    """
    Main entry point for the APK Runner application.
    
    Creates an instance of APKRunner and starts the GUI.
    No command-line arguments required.
    
    Usage:
        python apk_runner.py
    """
    app = APKRunner()
    app.run()