from http.server import BaseHTTPRequestHandler
import json
import math
import zlib
from urllib.parse import parse_qs, urlparse

# Core Codex 7 Thermodynamic Bounds
PHASE_BOUNDS = {
    "WHITE_LATTICE": {"entropy_max": 3.8, "compression_min": 0.35},
    "YELLOW_IGNITION": {"entropy_max": 4.2, "compression_min": 0.25},
    "RED_COMBUSTION": {"entropy_max": 4.8, "compression_min": 0.15},
    "ORANGE_HARVEST": {"entropy_max": 5.2, "compression_min": 0.10},
    "GREEN_ACCUMULATION": {"entropy_max": 4.5, "compression_min": 0.20},
    "BLUE_DISPERSION": {"entropy_max": 5.5, "compression_min": 0.05},
    "BLACK_COLLAPSE": {"entropy_max": 7.0, "compression_min": 0.0}
}

def shannon_entropy(text):
    """Calculate Shannon entropy in bits"""
    if not text:
        return 0.0
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    total = len(text)
    return -sum((count/total) * math.log2(count/total) for count in freq.values())

def compression_ratio(text):
    """Calculate compression ratio as fuel density measure"""
    if not text:
        return 0.0
    raw = text.encode('utf-8')
    compressed = zlib.compress(raw, level=9)
    return 1.0 - (len(compressed) / len(raw))

def classify_phase(entropy_val, comp_ratio):
    """Determine Z₇ phase based on thermodynamic bounds"""
    # Ordered by strictness (White → Black)
    if entropy_val <= 3.8 and comp_ratio >= 0.35:
        return "WHITE_LATTICE"
    elif entropy_val <= 4.2 and comp_ratio >= 0.25:
        return "YELLOW_IGNITION"
    elif entropy_val <= 4.5 and comp_ratio >= 0.20:
        return "GREEN_ACCUMULATION"
    elif entropy_val <= 4.8 and comp_ratio >= 0.15:
        return "RED_COMBUSTION"
    elif entropy_val <= 5.2 and comp_ratio >= 0.10:
        return "ORANGE_HARVEST"
    elif entropy_val <= 5.5 and comp_ratio >= 0.05:
        return "BLUE_DISPERSION"
    else:
        return "BLACK_COLLAPSE"

def verify_text(text, threshold="WHITE_LATTICE"):
    """Main verification logic"""
    entropy_val = shannon_entropy(text)
    comp_ratio = compression_ratio(text)
    detected_phase = classify_phase(entropy_val, comp_ratio)

    # Check if detected phase meets threshold
    phase_order = list(PHASE_BOUNDS.keys())
    threshold_idx = phase_order.index(threshold)
    detected_idx = phase_order.index(detected_phase)

    verified = detected_idx <= threshold_idx

    return {
        "verified": verified,
        "detected_phase": detected_phase,
        "threshold_phase": threshold,
        "metrics": {
            "entropy_bits": round(entropy_val, 4),
            "compression_ratio": round(comp_ratio, 4),
            "text_length": len(text)
        },
        "bounds_used": PHASE_BOUNDS[detected_phase]
    }

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            query = parse_qs(urlparse(self.path).query)
            text = query.get('text', [''])[0]
            threshold = query.get('threshold', ['WHITE_LATTICE'])[0]

            if not text:
                result = {"error": "Missing 'text' parameter"}
                status = 400
            else:
                result = verify_text(text, threshold)
                status = 200

        except Exception as e:
            result = {"error": str(e)}
            status = 500

        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(result, indent=2).encode())

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))

            text = data.get('text', '')
            threshold = data.get('threshold', 'WHITE_LATTICE')

            if not text:
                result = {"error": "Missing 'text' in request body"}
                status = 400
            else:
                result = verify_text(text, threshold)
                status = 200

        except Exception as e:
            result = {"error": str(e)}
            status = 500

        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(result, indent=2).encode())
