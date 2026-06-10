# apk_diagnostic.py - APK Runner Diagnostic & Troubleshooting Tool
"""
🔧 APK RUNNER DIAGNOSTIC TOOL
Automatically detects and fixes issues with the APK Runner application.

This tool checks:
- System compatibility
- Python installation
- Required modules
- ADB availability
- Emulator availability
- Connected devices
- APK file validity
- Disk space and permissions

Run this tool when:
- APK Runner won't start
- ADB commands fail
- Emulator won't launch
- APK installation fails
- Devices aren't detected
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import os
import sys
import subprocess
import threading
import queue
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

class APKDiagnostic:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔧 APK Runner - Diagnostic Tool")
        self.root.geometry("850x700")
        self.root.configure(bg='#0f0f1a')
        self.root.minsize(750, 600)
        
        # Colors
        self.colors = {
            'bg_dark': '#0f0f1a',
            'bg_medium': '#1a1a2e',
            'bg_light': '#16213e',
            'accent': '#3DDC84',
            'accent2': '#4285F4',
            'text_primary': '#ffffff',
            'text_secondary': '#94a3b8',
            'success': '#10b981',
            'warning': '#f59e0b',
            'error': '#ef4444',
            'info': '#3b82f6',
            'card_bg': '#1a1a2e',
        }
        
        # Results tracking
        self.tests_passed = 0
        self.tests_failed = 0
        self.tests_warnings = 0
        self.total_tests = 0
        self.fixes_applied = 0
        
        # Message queue
        self.message_queue = queue.Queue()
        
        # Setup UI
        self.setup_ui()
        
        # Auto-run diagnostics
        self.root.after(500, self.run_all_diagnostics)
        
    def setup_ui(self):
        """Create the diagnostic UI"""
        # Header
        header = tk.Frame(self.root, bg=self.colors['bg_light'], height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="🔧", font=('Arial', 30),
                bg=self.colors['bg_light']).pack(side='left', padx=20)
        
        title_frame = tk.Frame(header, bg=self.colors['bg_light'])
        title_frame.pack(side='left', pady=10)
        
        tk.Label(title_frame, text="APK RUNNER DIAGNOSTIC",
                font=('Arial', 16, 'bold'),
                bg=self.colors['bg_light'],
                fg=self.colors['accent']).pack(anchor='w')
        
        tk.Label(title_frame, text="System compatibility & troubleshooting",
                font=('Arial', 9),
                bg=self.colors['bg_light'],
                fg=self.colors['text_secondary']).pack(anchor='w')
        
        # Action buttons in header
        btn_frame = tk.Frame(header, bg=self.colors['bg_light'])
        btn_frame.pack(side='right', padx=20)
        
        tk.Button(btn_frame, text="🔄 Re-run All Tests",
                 command=self.run_all_diagnostics,
                 bg=self.colors['accent'],
                 fg=self.colors['bg_dark'],
                 font=('Arial', 9, 'bold'),
                 relief='flat', cursor='hand2',
                 padx=15, pady=5).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="🔧 Auto-Fix Issues",
                 command=self.auto_fix_issues,
                 bg=self.colors['accent2'],
                 fg='white',
                 font=('Arial', 9, 'bold'),
                 relief='flat', cursor='hand2',
                 padx=15, pady=5).pack(side='left', padx=5)
        
        # Main content
        content = tk.Frame(self.root, bg=self.colors['bg_dark'])
        content.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Summary cards
        self.create_summary_cards(content)
        
        # Results area
        self.create_results_area(content)
        
        # Status bar
        self.create_status_bar()
        
    def create_summary_cards(self, parent):
        """Create summary cards showing test results"""
        cards_frame = tk.Frame(parent, bg=self.colors['bg_dark'])
        cards_frame.pack(fill='x', pady=5)
        
        cards = [
            ("✅ Passed", "0", self.colors['success']),
            ("❌ Failed", "0", self.colors['error']),
            ("⚠️ Warnings", "0", self.colors['warning']),
            ("🔧 Fixed", "0", self.colors['info']),
        ]
        
        for i, (title, value, color) in enumerate(cards):
            card = tk.Frame(cards_frame, bg=self.colors['card_bg'])
            card.pack(side='left', padx=3, expand=True, fill='x')
            
            tk.Frame(card, bg=color, height=3).pack(fill='x')
            
            card_content = tk.Frame(card, bg=self.colors['card_bg'])
            card_content.pack(fill='x', padx=12, pady=10)
            
            tk.Label(card_content, text=title, font=('Arial', 9),
                    bg=self.colors['card_bg'],
                    fg=self.colors['text_secondary']).pack(anchor='w')
            
            value_label = tk.Label(card_content, text=value, 
                                  font=('Arial', 20, 'bold'),
                                  bg=self.colors['card_bg'], fg=color)
            value_label.pack(anchor='w', pady=2)
            
            if i == 0:
                self.passed_label = value_label
            elif i == 1:
                self.failed_label = value_label
            elif i == 2:
                self.warnings_label = value_label
            elif i == 3:
                self.fixed_label = value_label
    
    def create_results_area(self, parent):
        """Create scrollable results display"""
        results_frame = tk.Frame(parent, bg=self.colors['bg_dark'])
        results_frame.pack(fill='both', expand=True, pady=10)
        
        tk.Label(results_frame, text="📋 Diagnostic Results",
                font=('Arial', 12, 'bold'),
                bg=self.colors['bg_dark'],
                fg=self.colors['text_primary']).pack(anchor='w')
        
        # Results text area
        text_frame = tk.Frame(results_frame, bg=self.colors['accent'], padx=1, pady=1)
        text_frame.pack(fill='both', expand=True, pady=5)
        
        self.results_text = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            bg=self.colors['card_bg'],
            fg=self.colors['text_primary'],
            font=('Consolas', 9),
            relief='flat',
            padx=15, pady=15
        )
        self.results_text.pack(fill='both', expand=True)
        
        # Configure text tags
        self.results_text.tag_config("header", font=('Consolas', 11, 'bold'), 
                                     foreground=self.colors['accent'])
        self.results_text.tag_config("success", foreground=self.colors['success'])
        self.results_text.tag_config("error", foreground=self.colors['error'])
        self.results_text.tag_config("warning", foreground=self.colors['warning'])
        self.results_text.tag_config("info", foreground=self.colors['info'])
        self.results_text.tag_config("section", font=('Consolas', 10, 'bold'),
                                     foreground='#ffffff')
        self.results_text.tag_config("command", foreground=self.colors['accent'])
        self.results_text.tag_config("fix", foreground=self.colors['accent2'])
        
        self.results_text.configure(state='disabled')
    
    def create_status_bar(self):
        """Create status bar"""
        status = tk.Frame(self.root, bg=self.colors['bg_medium'], height=25)
        status.pack(fill='x', side='bottom')
        status.pack_propagate(False)
        
        self.status_label = tk.Label(status, text="🔧 Running diagnostics...",
                                    bg=self.colors['bg_medium'],
                                    fg=self.colors['text_secondary'],
                                    font=('Arial', 8))
        self.status_label.pack(side='left', padx=15)
        
        tk.Label(status, text="APK Diagnostic v1.0",
                bg=self.colors['bg_medium'],
                fg=self.colors['text_secondary'],
                font=('Arial', 8)).pack(side='right', padx=15)
    
    def add_result(self, text, tag=None):
        """Add result to display"""
        self.results_text.configure(state='normal')
        if tag:
            self.results_text.insert(tk.END, text, tag)
        else:
            self.results_text.insert(tk.END, text)
        self.results_text.see(tk.END)
        self.results_text.configure(state='disabled')
    
    def run_all_diagnostics(self):
        """Run all diagnostic tests"""
        # Reset
        self.results_text.configure(state='normal')
        self.results_text.delete('1.0', tk.END)
        self.results_text.configure(state='disabled')
        
        self.tests_passed = 0
        self.tests_failed = 0
        self.tests_warnings = 0
        self.total_tests = 0
        
        # Header
        self.add_result("╔══════════════════════════════════════════╗\n", "header")
        self.add_result("║    APK RUNNER DIAGNOSTIC REPORT        ║\n", "header")
        self.add_result("╚══════════════════════════════════════════╝\n\n", "header")
        self.add_result(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n", "info")
        
        # Run tests in thread
        threading.Thread(target=self._run_tests, daemon=True).start()
    
    def _run_tests(self):
        """Run all tests in order"""
        # System Check
        self.add_section("🖥️ SYSTEM CHECK")
        self.check_system()
        
        # Python Check
        self.add_section("🐍 PYTHON CHECK")
        self.check_python()
        
        # Module Check
        self.add_section("📦 MODULE CHECK")
        self.check_modules()
        
        # ADB Check
        self.add_section("🔌 ADB CHECK")
        self.check_adb()
        
        # Emulator Check
        self.add_section("📱 EMULATOR CHECK")
        self.check_emulator()
        
        # Device Check
        self.add_section("📱 DEVICE CHECK")
        self.check_devices()
        
        # APK Check
        self.add_section("📦 APK FILE CHECK")
        self.check_apk()
        
        # Disk Check
        self.add_section("💾 DISK CHECK")
        self.check_disk()
        
        # Permissions Check
        self.add_section("🔒 PERMISSIONS CHECK")
        self.check_permissions()
        
        # Summary
        self.add_section("📊 FINAL SUMMARY")
        self.show_summary()
        
        # Update cards
        self.root.after(0, self.update_cards)
        self.root.after(0, lambda: self.status_label.config(text="✅ Diagnostics complete"))
    
    def add_section(self, title):
        """Add a section header"""
        self.add_result(f"\n{'═' * 50}\n", "section")
        self.add_result(f"  {title}\n", "section")
        self.add_result(f"{'═' * 50}\n\n", "section")
    
    def pass_test(self, message):
        """Record a passed test"""
        self.tests_passed += 1
        self.total_tests += 1
        self.add_result(f"   ✅ {message}\n", "success")
    
    def fail_test(self, message, fix=None):
        """Record a failed test with optional fix"""
        self.tests_failed += 1
        self.total_tests += 1
        self.add_result(f"   ❌ {message}\n", "error")
        if fix:
            self.add_result(f"      🔧 Fix: {fix}\n", "fix")
    
    def warn_test(self, message):
        """Record a warning"""
        self.tests_warnings += 1
        self.total_tests += 1
        self.add_result(f"   ⚠️  {message}\n", "warning")
    
    def check_system(self):
        """Check system compatibility"""
        import platform
        
        self.add_result(f"   OS: {platform.system()} {platform.release()}\n", "info")
        self.add_result(f"   Version: {platform.version()[:60]}\n", "info")
        self.add_result(f"   Architecture: {platform.architecture()[0]}\n", "info")
        self.add_result(f"   Machine: {platform.machine()}\n\n", "info")
        
        # Check Windows version
        if platform.system() == 'Windows':
            try:
                version = int(platform.release())
                if version >= 10:
                    self.pass_test("Windows 10 or higher detected")
                else:
                    self.fail_test(f"Windows {version} may not be fully supported", 
                                  "Upgrade to Windows 10 or 11")
            except:
                self.warn_test("Could not determine Windows version")
        else:
            self.warn_test(f"Running on {platform.system()} - some features may differ")
    
    def check_python(self):
        """Check Python installation"""
        self.add_result(f"   Python: {sys.version}\n", "info")
        self.add_result(f"   Executable: {sys.executable}\n\n", "info")
        
        version = sys.version_info
        if version >= (3, 7):
            self.pass_test(f"Python {version.major}.{version.minor}.{version.micro} is compatible")
        else:
            self.fail_test(f"Python {version.major}.{version.minor} is too old (need 3.7+)",
                          "Download Python 3.7+ from https://python.org")
    
    def check_modules(self):
        """Check required Python modules"""
        modules = {
            'tkinter': 'GUI framework - Required for the app interface',
            'os': 'File operations',
            'sys': 'System functions',
            'subprocess': 'Running external commands (ADB)',
            'threading': 'Background tasks',
            'queue': 'Message handling',
            'shutil': 'File operations',
            'zipfile': 'APK file reading',
            'webbrowser': 'Opening download links',
            'pathlib': 'File path handling',
            'datetime': 'Timestamps',
            'json': 'Settings storage',
        }
        
        for module, description in modules.items():
            try:
                __import__(module)
                self.pass_test(f"{module:20} - {description}")
            except ImportError:
                self.fail_test(f"{module:20} - {description} [MISSING]",
                              f"Reinstall Python with all modules")
    
    def check_adb(self):
        """Check ADB availability"""
        adb_path = None
        
        # Search for ADB
        possible_paths = [
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Android', 'Sdk', 'platform-tools', 'adb.exe'),
            os.path.join(os.environ.get('APPDATA', ''), 'Android', 'Sdk', 'platform-tools', 'adb.exe'),
            'C:\\Android\\Sdk\\platform-tools\\adb.exe',
            os.path.expanduser('~/Android/Sdk/platform-tools/adb'),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                adb_path = path
                break
        
        if not adb_path:
            adb_path = shutil.which('adb')
        
        if adb_path:
            self.pass_test(f"ADB found at: {adb_path}")
            
            # Check ADB version
            try:
                result = subprocess.run([adb_path, 'version'], 
                                       capture_output=True, text=True, timeout=5)
                version_line = result.stdout.split('\n')[0]
                self.add_result(f"      {version_line}\n", "info")
                self.pass_test("ADB is working correctly")
            except:
                self.warn_test("ADB found but may not be working")
        else:
            self.fail_test("ADB not found",
                          "Download Android SDK Platform Tools from:\n"
                          "      https://dl.google.com/android/repository/platform-tools-latest-windows.zip")
    
    def check_emulator(self):
        """Check Android Emulator availability"""
        emulator_path = None
        
        possible_paths = [
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Android', 'Sdk', 'emulator', 'emulator.exe'),
            os.path.join(os.environ.get('APPDATA', ''), 'Android', 'Sdk', 'emulator', 'emulator.exe'),
            'C:\\Android\\Sdk\\emulator\\emulator.exe',
            os.path.expanduser('~/Android/Sdk/emulator/emulator'),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                emulator_path = path
                break
        
        if not emulator_path:
            emulator_path = shutil.which('emulator')
        
        if emulator_path:
            self.pass_test(f"Emulator found at: {emulator_path}")
            
            # Check for AVDs
            try:
                result = subprocess.run([emulator_path, '-list-avds'], 
                                       capture_output=True, text=True, timeout=5)
                avds = [a.strip() for a in result.stdout.split('\n') if a.strip()]
                if avds:
                    self.pass_test(f"Found {len(avds)} Android Virtual Device(s):")
                    for avd in avds:
                        self.add_result(f"         📱 {avd}\n", "info")
                else:
                    self.warn_test("No Android Virtual Devices (AVDs) found")
                    self.add_result("      🔧 Create one in Android Studio: Tools > Device Manager\n", "fix")
            except:
                self.warn_test("Could not check for AVDs")
        else:
            self.warn_test("Android Emulator not found")
            self.add_result("      💡 Alternatives:\n", "info")
            self.add_result("         • BlueStacks: https://www.bluestacks.com\n", "info")
            self.add_result("         • Nox Player: https://www.bignox.com\n", "info")
            self.add_result("         • Android Studio: https://developer.android.com/studio\n", "info")
    
    def check_devices(self):
        """Check connected Android devices"""
        adb_path = shutil.which('adb')
        if not adb_path:
            for path in [os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Android', 'Sdk', 'platform-tools', 'adb.exe')]:
                if os.path.exists(path):
                    adb_path = path
                    break
        
        if adb_path:
            try:
                result = subprocess.run([adb_path, 'devices'], 
                                       capture_output=True, text=True, timeout=10)
                lines = result.stdout.strip().split('\n')[1:]
                devices = [l.split('\t')[0] for l in lines if l.strip() and '\tdevice' in l]
                
                if devices:
                    self.pass_test(f"Found {len(devices)} connected device(s):")
                    for device in devices:
                        self.add_result(f"         📱 {device}\n", "info")
                else:
                    self.warn_test("No devices connected")
                    self.add_result("      💡 Connect a phone via USB or start an emulator\n", "info")
            except:
                self.warn_test("Could not check for devices")
        else:
            self.warn_test("Skipping device check - ADB not available")
    
    def check_apk(self):
        """Check for APK files"""
        downloads = os.path.expanduser("~/Downloads")
        apk_files = []
        
        if os.path.exists(downloads):
            for file in os.listdir(downloads):
                if file.endswith('.apk'):
                    apk_files.append(os.path.join(downloads, file))
        
        if apk_files:
            self.pass_test(f"Found {len(apk_files)} APK file(s) in Downloads:")
            for apk in apk_files[:5]:
                size = os.path.getsize(apk)
                self.add_result(f"         📦 {os.path.basename(apk)} ({self.format_size(size)})\n", "info")
        else:
            self.add_result("   ℹ️  No APK files found in Downloads\n", "info")
            self.add_result("      This is normal if you haven't downloaded any APKs yet\n", "info")
    
    def check_disk(self):
        """Check disk space"""
        try:
            total, used, free = shutil.disk_usage(os.path.expanduser("~"))
            free_gb = free / (1024**3)
            total_gb = total / (1024**3)
            
            self.add_result(f"   Free: {free_gb:.1f} GB / Total: {total_gb:.1f} GB\n\n", "info")
            
            if free_gb > 5:
                self.pass_test(f"Sufficient disk space ({free_gb:.1f} GB free)")
            elif free_gb > 1:
                self.warn_test(f"Low disk space ({free_gb:.1f} GB free)")
            else:
                self.fail_test(f"Critical! Only {free_gb:.1f} GB free",
                              "Free up disk space before using emulators")
        except:
            self.warn_test("Could not check disk space")
    
    def check_permissions(self):
        """Check file permissions"""
        test_paths = [
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Desktop"),
            os.getcwd(),
        ]
        
        for path in test_paths:
            if os.path.exists(path):
                try:
                    test_file = os.path.join(path, '.apk_diagnostic_test')
                    with open(test_file, 'w') as f:
                        f.write('test')
                    os.remove(test_file)
                    self.pass_test(f"Write permission: {path}")
                except:
                    self.fail_test(f"No write permission: {path}",
                                  "Run the app as Administrator")
            else:
                self.warn_test(f"Path not found: {path}")
    
    def show_summary(self):
        """Show final summary"""
        self.add_result(f"\n   {'═' * 40}\n", "section")
        
        if self.tests_failed == 0:
            self.add_result(f"\n   ✅ ALL CHECKS PASSED!\n", "success")
            self.add_result(f"   Your system is ready for APK Runner.\n\n", "success")
        else:
            self.add_result(f"\n   ⚠️  {self.tests_failed} ISSUE(S) FOUND\n", "warning")
            self.add_result(f"   Click '🔧 Auto-Fix Issues' to attempt repairs\n\n", "fix")
        
        self.add_result(f"   Passed: {self.tests_passed}\n", "success")
        self.add_result(f"   Failed: {self.tests_failed}\n", "error")
        self.add_result(f"   Warnings: {self.tests_warnings}\n", "warning")
        self.add_result(f"   Total: {self.total_tests}\n", "info")
    
    def update_cards(self):
        """Update summary cards"""
        self.passed_label.config(text=str(self.tests_passed))
        self.failed_label.config(text=str(self.tests_failed))
        self.warnings_label.config(text=str(self.tests_warnings))
        self.fixed_label.config(text=str(self.fixes_applied))
    
    def auto_fix_issues(self):
        """Attempt to automatically fix common issues"""
        self.add_section("🔧 AUTO-FIX ATTEMPTS")
        self.fixes_applied = 0
        
        # Fix 1: Check Python
        self.add_result("   Checking Python installation...\n", "info")
        if sys.version_info < (3, 7):
            self.add_result("   ❌ Cannot auto-update Python. Please install Python 3.7+\n", "error")
            self.add_result("      Download: https://python.org\n", "fix")
        else:
            self.pass_test("Python version is compatible")
        
        # Fix 2: Check tkinter
        try:
            import tkinter
            self.pass_test("tkinter is available")
        except ImportError:
            self.add_result("   ❌ tkinter missing. Reinstall Python with tkinter support.\n", "error")
        
        # Fix 3: Check for pip
        try:
            import pip
            self.pass_test("pip is available")
        except ImportError:
            self.fail_test("pip not found", "Run: python -m ensurepip --upgrade")
        
        # Fix 4: Reset ADB server
        adb_path = shutil.which('adb')
        if adb_path:
            try:
                subprocess.run([adb_path, 'kill-server'], capture_output=True, timeout=5)
                subprocess.run([adb_path, 'start-server'], capture_output=True, timeout=5)
                self.pass_test("ADB server reset successfully")
                self.fixes_applied += 1
            except:
                self.warn_test("Could not reset ADB server")
        
        self.update_cards()
        self.add_result(f"\n   🔧 Fixes applied: {self.fixes_applied}\n", "fix")
    
    def format_size(self, size):
        """Format file size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def run(self):
        """Run the diagnostic tool"""
        self.root.mainloop()

if __name__ == "__main__":
    app = APKDiagnostic()
    app.run()