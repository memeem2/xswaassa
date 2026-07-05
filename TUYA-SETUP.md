# How to Get Your Tuya Smart Plug Info

You need **4 values** to control your plug from the Pi:

| Value | Example | What it is |
|-------|---------|------------|
| `TUYA_DEVICE_ID` | `bf1234567890abcdef` | Unique plug ID |
| `TUYA_LOCAL_KEY` | `a1b2c3d4e5f6g7h8` | 16-char secret key |
| `TUYA_IP` | `192.168.1.45` | Plug's IP on your WiFi |
| `TUYA_VERSION` | `3.3` | Protocol version (usually 3.3) |

---

## Before You Start

- Plug must be **paired in Smart Life app** (or Tuya Smart app)
- Pi/PC must be on the **same WiFi** as the plug
- **Close Smart Life app** on your phone before testing (only one connection at a time)
- Run commands on your **Raspberry Pi** (or any PC with Python on same network)

---

## Quick Way (Recommended)

On your Raspberry Pi:

```bash
cd ~/charger-monitor-pi/scripts
chmod +x get-tuya-info.sh
./get-tuya-info.sh
```

This runs scan + wizard + test for you.

---

## Manual Step-by-Step

### Step 1 — Install TinyTuya on Pi

```bash
sudo apt update
sudo apt install -y python3-pip
pip3 install tinytuya
```

### Step 2 — Scan network (gets Device ID + IP)

```bash
python3 -m tinytuya scan
```

You'll see something like:

```
Address = 192.168.1.45   Device ID = bf1234567890abcdef   Version = 3.3
```

Write down the **Device ID**, **IP**, and **Version** for your plug.

> If nothing shows up: wait 20+ seconds, make sure plug is powered on, and try `python3 -m tinytuya scan 50`

---

### Step 3 — Get Local Key via Tuya Developer Account

The local key cannot be guessed — you need a free Tuya cloud account to extract it.

#### 3a. Create developer account

1. Go to **https://iot.tuya.com** and register
2. When asked "Account Type" → click **Skip this step**
3. Click **Cloud** → **Create Cloud Project**
4. Pick the **Data Center / Region** closest to you  
   (UK users sometimes need "Central Europe" not "Western Europe")
5. On project **Overview**, copy:
   - **Access ID** (also called Client ID / API Key)
   - **Access Secret** (also called Client Secret / API Secret)

#### 3b. Link your Smart Life app

1. In your project → **Devices** tab → **Link Tuya App Account**
2. Click **Add App Account**
3. Choose **Automatic** + **Read Only Status**
4. A **QR code** appears
5. On your phone: open **Smart Life** → **Me** tab → tap QR icon (top right) → scan it
6. Your plug should now appear under **Devices** in the Tuya portal

> **No devices showing?** Wrong data center — create a new project with a different region.

#### 3c. Enable API access

1. **Service API** tab → **Go to Authorize**
2. Subscribe to **IoT Core** (disable popup blockers!)
3. This subscription expires monthly — renew it if wizard stops working later

#### 3d. Run the wizard

```bash
python3 -m tinytuya wizard
```

It will ask for:
- **API Key** → your Access ID
- **API Secret** → your Access Secret  
- **API Region** → `eu`, `us`, `eu-w`, etc. (match your data center)
- **Device ID** → type `scan` or paste from Step 2

When done it creates **`devices.json`** with all your devices:

```json
[
  {
    "name": "Charger Plug",
    "id": "bf1234567890abcdef",
    "key": "a1b2c3d4e5f6g7h8",
    "mac": "...",
    "uuid": "...",
    "sn": "...",
    "category": "cz",
    "product_name": "Smart Plug",
    "product_id": "...",
    "biz_type": 0,
    "model": "...",
    "sub": false,
    "icon": "..."
  }
]
```

---

### Step 4 — Test the plug works

```bash
# List devices
python3 -m tinytuya list

# Turn ON (use your plug's name from the list)
python3 -m tinytuya on --name "Charger Plug"

# Check status
python3 -m tinytuya get --name "Charger Plug"

# Turn OFF
python3 -m tinytuya off --name "Charger Plug"
```

If ON/OFF works, you have everything you need.

---

### Step 5 — Fill in config

Put these in your `config.env`:

```env
TUYA_DEVICE_ID=bf1234567890abcdef
TUYA_LOCAL_KEY=a1b2c3d4e5f6g7h8
TUYA_IP=192.168.1.45
TUYA_VERSION=3.3
TUYA_SWITCH_DP=1
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Scan finds nothing | Plug off wrong WiFi; use 2.4GHz not 5GHz; run `scan 50` |
| Wizard: no devices | Wrong Tuya data center region; re-link Smart Life app |
| `Error 914` key/version | Re-run wizard — local key changed if you re-paired plug |
| Plug won't toggle | Close Smart Life app; check IP hasn't changed (set DHCP reservation) |
| `switch` wrong DP | Try `TUYA_SWITCH_DP=1` (most plugs use DPS 1) |

---

## Optional: Run from Windows PC

If your PC is on the same WiFi as the plug:

1. Install Python from https://python.org (check "Add to PATH")
2. Open PowerShell:
   ```powershell
   pip install tinytuya
   python -m tinytuya scan
   python -m tinytuya wizard
   ```