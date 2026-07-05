# Charger Monitor (Raspberry Pi 3B)

Phone streams camera to the Pi via WebRTC. Gemini AI checks if a phone is plugged into the charger. Tuya smart plug turns ON/OFF automatically.

## Your plug (already configured)

| Setting | Value |
|---------|-------|
| Name | WiFi Socket |
| Device ID | `bf3df924c7cdfb2c14mzdq` |
| IP | `192.168.1.131` |
| Version | `3.4` |
| Switch DP | `1` |

Credentials are in `devices.json` and `config.env`.

## Quick start on Raspberry Pi

### 1. Copy project to Pi

```bash
scp -r charger-monitor-pi pi@<pi-ip>:~/
```

### 2. Install dependencies

```bash
cd ~/charger-monitor-pi
chmod +x scripts/*.sh
sudo ./scripts/install-deps.sh
```

### 3. Add an OpenRouter API key (recommended, free)

Get a free key: https://openrouter.ai/keys

```bash
sudo nano /etc/charger-monitor/config.env   # after install
# OR before install:
nano config.env
# Set: AI_PROVIDER=openrouter
#      OPENROUTER_API_KEY=sk-or-v1-your_key_here
```

Note: `/etc/charger-monitor/config.env` is only ever *created* on install if it
doesn't already exist - reinstalling or upgrading the `.deb` package will
never overwrite it, so your key is safe across upgrades. Gemini is still
supported as a fallback (`AI_PROVIDER=gemini` + `GEMINI_API_KEY=...`).

### 4. Build and install (one command)

```bash
cd ~/charger-monitor-pi
chmod +x scripts/install-on-pi.sh
./scripts/install-on-pi.sh
```

This builds the .deb, installs it, copies your config, generates SSL, and starts the service.

**Manual build** (if you prefer):

```bash
chmod +x debian/rules debian/postinst debian/prerm
rm -f debian/compat   # must not exist alongside debhelper-compat in control
sudo apt install -y debhelper build-essential
dpkg-buildpackage -us -uc -b
sudo dpkg -i ../charger-monitor_1.0.0_all.deb
```

### 5. Check service

```bash
sudo systemctl status charger-monitor
journalctl -u charger-monitor -f
```

### 8. Open on phone

```
https://<pi-ip>:8443
```

- Accept the self-signed certificate warning
- Tap **Start Stream**
- Use **Flip Camera** to switch front/back
- Point camera at your charger

## Dev mode (without .deb)

```bash
cd charger-monitor-pi
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

## Manual plug test

```bash
python -m tinytuya on --id bf3df924c7cdfb2c14mzdq --ip 192.168.1.131 --version 3.4
python -m tinytuya off --id bf3df924c7cdfb2c14mzdq --ip 192.168.1.131 --version 3.4
```

## How it works

1. Phone opens HTTPS site and streams camera (WebRTC)
2. Pi grabs a frame every 10 seconds
3. Gemini AI answers: phone on charger? yes/no
4. Tuya plug ON if yes, OFF if no

## Files

```
app/main.py           - FastAPI server
app/webrtc_handler.py - WebRTC signaling
app/ai_analyzer.py    - Gemini vision
app/tuya_controller.py - TinyTuya plug control
app/static/           - Phone web UI
config.env            - Your settings
devices.json          - Tuya credentials
debian/               - Debian package
```