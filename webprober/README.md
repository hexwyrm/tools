# webprober

`webprober` is a concurrent HTTP service scanner written in Rust.
It automates basic reconnaissance tasks by probing URLs, extracting service metadata, and performing lightweight fingerprinting.

This tool is designed for cybersecurity workflows, recon automation, and portfolio demonstration of Rust-based tooling.

---

## Features

- **Concurrent HTTP probing** (configurable worker count)
- **Extracts key metadata**:
  - HTTP status code
  - `Server` header
  - `X-Powered-By` header
  - `Content-Type` header
- **Basic fingerprinting**:
  - nginx
  - Apache
  - Microsoft IIS
  - PHP
  - Express (Node.js)
  - ASP.NET
  - JSON API
  - HTML
- **Pretty JSON output** for easy parsing and automation

---

## Installation

Ensure Rust is installed (via `rustup`):

```bash
rustup-init
source "$HOME/.cargo/env"
```
