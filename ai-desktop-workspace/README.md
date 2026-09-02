# AI Desktop Workspace
**Author:** Hexwyrm
A secure, multi‑tab GTK3/WebKit2GTK desktop client for modern AI chat services including ChatGPT, Gemini, Copilot, and Claude.
Designed for systemd‑free Linux environments such as **Artix**, **Void**, and **Devuan**, while remaining fully compatible with Arch‑based systems.

---

## 🚀 Features

### ✔ Multi‑Tab AI Workspace
Each AI service opens in its own tab with a close button. Tabs are deduplicated—launching an already‑open service switches focus instead of spawning duplicates.

### ✔ Secure Domain‑Locked Browsing
Each service is restricted to its known OAuth/login domains. External links automatically open in the system browser.

### ✔ Persistent Cookie Storage
WebKit2GTK stores cookies in a private SQLite file under `~/.local/share/ai-desktop-workspace` with strict 0700 permissions.

### ✔ System Tray Integration
Closing the window hides the application to the tray (AppIndicator3 or Gtk.StatusIcon fallback).

### ✔ Desktop Menu Integration
A `.desktop` launcher registers the app under Network/WebBrowser categories across Xfce, MATE, LXQt, KDE, Cinnamon, and others.

### ✔ Init‑Agnostic
No systemd dependencies. Works cleanly on OpenRC, runit, s6, and dinit systems.

---

## 📁 Project Structure

```
ai-desktop-workspace/
├── ai-desktop.py        # Main GTK3/WebKit2GTK application
├── ai-desktop.desktop   # Desktop launcher
└── install.sh           # Automated installer
```

---

## 🔧 Requirements

Install required packages (Artix/Arch example):

```bash
pacman -S python python-gobject webkit2gtk libayatana-appindicator
```

---

Installation
```bash
chmod +x install.sh
./install.sh
Make sure ~/.local/bin is in your PATH:
```

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
Launch the app:
```

```bash
ai-desktop
Or use your desktop environment’s application menu.
```

---

🛡 Security Model
WebKit2GTK sandboxing enabled when supported
- Strict domain whitelisting per service
- No universal file access
- No developer tools
- Cookies stored in private directories with 0700 permissions
- External navigation blocked and redirected to system browser

This hopefully will make the wrapper suitable for cybersecurity‑focused portfolios and secure desktop environments.

---

📜 License
This project is authored by Hexwyrm and licensed under the Apache License 2.0.
