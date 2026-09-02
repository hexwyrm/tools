#!/usr/bin/env python3
# Author: Hexwyrm
"""
AI Desktop Workspace
A secure, multi-tab GTK3/WebKit2GTK desktop client for AI interfaces.
Configured for init-agnostic systemd-free environments (Artix, Void, Devuan, etc.).
"""

import os
import sys

# FIX: Disable WebKit hardware acceleration/GBM buffer creation before importing WebKit
os.environ["WEBKIT_DISABLE_COMPOSITING_MODE"] = "1"
os.environ["WEBKIT_HARDWARE_ACCELERATION_POLICY"] = "NEVER"

import stat
import signal
from urllib.parse import urlparse

import gi
gi.require_version('Gtk', '3.0')

try:
    gi.require_version('WebKit2', '4.1')
except ValueError:
    try:
        gi.require_version('WebKit2', '4.0')
    except ValueError:
        sys.exit("Error: WebKit2GTK (4.0 or 4.1) is required but not installed.")

from gi.repository import Gtk, Gdk, WebKit2, GLib, Gio

# Tray indicator setup
HAS_APPINDICATOR = False
try:
    gi.require_version('AyatanaAppIndicator3', '0.1')
    from gi.repository import AyatanaAppIndicator3 as AppIndicator3
    HAS_APPINDICATOR = True
except Exception:
    try:
        gi.require_version('AppIndicator3', '0.1')
        from gi.repository import AppIndicator3
        HAS_APPINDICATOR = True
    except Exception:
        HAS_APPINDICATOR = False

SERVICES = {
    "chatgpt": {
        "name": "ChatGPT",
        "url": "https://chatgpt.com",
        "icon": "dialog-messages-symbolic",
        "allowed_domains": ["chatgpt.com", "openai.com", "auth0.com", "msauth.net"]
    },
    "gemini": {
        "name": "Gemini",
        "url": "https://gemini.google.com",
        "icon": "user-available-symbolic",
        "allowed_domains": ["gemini.google.com", "google.com", "accounts.google.com", "gstatic.com", "googleusercontent.com"]
    },
    "copilot": {
        "name": "Copilot",
        "url": "https://copilot.microsoft.com",
        "icon": "system-help-symbolic",
        "allowed_domains": ["copilot.microsoft.com", "microsoft.com", "live.com", "microsoftonline.com", "bing.com"]
    },
    "claude": {
        "name": "Claude",
        "url": "https://claude.ai",
        "icon": "edit-select-all-symbolic",
        "allowed_domains": ["claude.ai", "anthropic.com"]
    }
}


class SecureWebContextManager:
    """Singleton manager for WebKit2 data isolation and persistent cookie storage."""
    _context = None
    _settings = None

    @classmethod
    def get_context(cls):
        if cls._context is None:
            data_dir = os.path.expanduser("~/.local/share/ai-desktop-workspace")
            cache_dir = os.path.expanduser("~/.cache/ai-desktop-workspace")

            for path in [data_dir, cache_dir]:
                os.makedirs(path, mode=0o700, exist_ok=True)
                os.chmod(path, stat.S_IRWXU)

            cls._context = WebKit2.WebContext.get_default()

            cookie_mgr = cls._context.get_cookie_manager()
            cookie_file = os.path.join(data_dir, "cookies.sqlite")
            cookie_mgr.set_persistent_storage(
                cookie_file, WebKit2.CookiePersistentStorage.SQLITE
            )

        return cls._context

    @classmethod
    def get_settings(cls):
        if cls._settings is None:
            cls._settings = WebKit2.Settings()
            cls._settings.set_disable_web_security(False)
            cls._settings.set_allow_file_access_from_file_urls(False)
            cls._settings.set_allow_universal_access_from_file_urls(False)
            cls._settings.set_enable_developer_extras(False)
            cls._settings.set_enable_javascript(True)
            cls._settings.set_enable_webaudio(True)
            cls._settings.set_enable_resizable_text_areas(True)

            user_agent = (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
            )
            cls._settings.set_user_agent(user_agent)
        return cls._settings


class AIDesktopWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="AI Workspace")
        self.set_default_size(1150, 780)
        self.set_icon_name("network-workgroup")

        self.open_tabs = {}

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(main_box)

        header = Gtk.HeaderBar()
        header.set_show_close_button(True)
        header.set_title("AI Desktop Workspace")
        self.set_titlebar(header)

        launch_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        for sid, sinfo in SERVICES.items():
            btn = Gtk.Button(label=sinfo["name"])
            btn.set_tooltip_text(f"Open or switch to {sinfo['name']}")
            btn.connect("clicked", lambda _, s=sid: self.open_service(s))
            launch_box.pack_start(btn, False, False, 0)

        header.pack_start(launch_box)

        self.notebook = Gtk.Notebook()
        self.notebook.set_scrollable(True)
        main_box.pack_start(self.notebook, True, True, 0)

        self.connect("delete-event", self._on_delete_event)
        self.tray = SystemTrayManager(self)

        self.open_service("chatgpt")

    def open_service(self, service_id: str):
        if service_id in self.open_tabs:
            page_widget = self.open_tabs[service_id]["page_widget"]
            page_idx = self.notebook.page_num(page_widget)
            if page_idx != -1:
                self.notebook.set_current_page(page_idx)
            return

        service_info = SERVICES[service_id]
        context = SecureWebContextManager.get_context()
        settings = SecureWebContextManager.get_settings()

        webview = WebKit2.WebView.new_with_context(context)
        webview.set_settings(settings)

        webview.connect("decide-policy", self._on_decide_policy, service_id)

        scrolled = Gtk.ScrolledWindow()
        scrolled.add(webview)
        scrolled.show_all()

        tab_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        tab_label = Gtk.Label(label=service_info["name"])

        close_btn = Gtk.Button()
        close_btn.set_relief(Gtk.ReliefStyle.NONE)
        close_btn.set_focus_on_click(False)
        close_icon = Gtk.Image.new_from_icon_name("window-close-symbolic", Gtk.IconSize.MENU)
        close_btn.add(close_icon)
        close_btn.connect("clicked", lambda _: self.close_service_tab(service_id))

        tab_box.pack_start(tab_label, True, True, 0)
        tab_box.pack_start(close_btn, False, False, 0)
        tab_box.show_all()

        page_idx = self.notebook.append_page(scrolled, tab_box)
        self.notebook.child_set_property(scrolled, "tab-expand", False)

        self.open_tabs[service_id] = {
            "webview": webview,
            "page_widget": scrolled
        }

        webview.load_uri(service_info["url"])
        self.notebook.set_current_page(page_idx)

    def close_service_tab(self, service_id: str):
        if service_id in self.open_tabs:
            page_widget = self.open_tabs[service_id]["page_widget"]
            page_idx = self.notebook.page_num(page_widget)
            if page_idx != -1:
                self.notebook.remove_page(page_idx)
            del self.open_tabs[service_id]

    def _on_decide_policy(self, webview, decision, decision_type, service_id):
        if decision_type == WebKit2.PolicyDecisionType.NAVIGATION_ACTION:
            action = decision.get_navigation_action()
            request = action.get_request()
            if request:
                uri = request.get_uri()
                if uri:
                    parsed = urlparse(uri)
                    domain = parsed.netloc.lower()
                    allowed_domains = SERVICES[service_id]["allowed_domains"]

                    is_allowed = any(domain == d or domain.endswith("." + d) for d in allowed_domains)

                    if not is_allowed and parsed.scheme in ["http", "https"]:
                        decision.ignore()
                        Gio.AppInfo.launch_default_for_uri(uri, None)
                        return True
        return False

    def _on_delete_event(self, widget, event):
        self.hide()
        return True


class SystemTrayManager:
    def __init__(self, main_window: AIDesktopWindow):
        self.main_window = main_window
        self.menu = Gtk.Menu()

        for sid, info in SERVICES.items():
            item = Gtk.MenuItem(label=f"Open {info['name']}")
            item.connect("activate", lambda _, s=sid: self._open_service(s))
            self.menu.append(item)

        self.menu.append(Gtk.SeparatorMenuItem())

        toggle_item = Gtk.MenuItem(label="Show / Hide Window")
        toggle_item.connect("activate", self._toggle_window)
        self.menu.append(toggle_item)

        quit_item = Gtk.MenuItem(label="Quit Application")
        quit_item.connect("activate", self._quit)
        self.menu.append(quit_item)

        self.menu.show_all()

        if HAS_APPINDICATOR:
            self.indicator = AppIndicator3.Indicator.new(
                "ai-desktop-workspace",
                "utilities-terminal",
                AppIndicator3.IndicatorCategory.APPLICATION_STATUS
            )
            self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
            self.indicator.set_menu(self.menu)

    def _open_service(self, service_id):
        self.main_window.present()
        self.main_window.open_service(service_id)

    def _toggle_window(self, *args):
        if self.main_window.get_visible():
            self.main_window.hide()
        else:
            self.main_window.present()

    def _quit(self, *args):
        Gtk.main_quit()


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = AIDesktopWindow()
    app.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
