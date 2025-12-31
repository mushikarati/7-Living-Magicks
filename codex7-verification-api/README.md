# Codex7 Verification API

**U9 Pipeline & U7 Thermodynamic Verification Engine with Stripe Payment Integration**

A production-ready API that charges $0.01 per verification call for thermodynamic text analysis using the U9 9-phase verification pipeline and U7 Codex Kernel.

---

## What This Does

- **Verifies text** using thermodynamic entropy and compression analysis
- **Classifies content** into 9 phases (Crystal White → Black Collapse)
- **Charges automatically** via Stripe ($0.01/verification)
- **Processes payouts** to connected accounts
- **Production-ready** with authentication, rate limiting, and webhooks

---

## Quick Start

### 1. Install Dependencies

```bash
cd codex7-verification-api
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your Stripe keys:

```env
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
API_KEYS=your_secret_api_key_here
```

### 3. Start Server

```bash
npm start
```

Server runs on `http://localhost:3000`

---

## API Endpoints

### Authentication

All endpoints require `X-API-Key` header:

```bash
curl -H "X-API-Key: your_api_key" https://api.example.com/api/verify
```

### Verification Endpoints

#### POST `/api/verify`
Complete verification (U9 + U7 kernel)

**Request:**
```json
{
  "text": "Your text to verify",
  "threshold": "WHITE_LATTICE",
  "paymentMethodId": "pm_card_visa",
  "includeKernel": true
}
```

**Response:**
```json
{
  "success": true,
  "payment_id": "pi_abc123",
  "amount_charged": 1,
  "currency": "usd",
  "verification_id": "ver_1234567890_abc",
  "u9_pipeline": {
    "verified": true,
    "detected_phase": "YELLOW_IGNITION",
    "phase_number": 3,
    "confidence": 0.8542,
    "metrics": {
      "entropy_bits": 4.1234,
      "compression_ratio": 0.2857,
      "coherence": 0.8000,
      "stability": 0.7542
    }
  },
  "u7_kernel": {
    "thermodynamic_state": {
      "entropy_bits": 4.1234,
      "free_energy": 79.383,
      "temperature_K": 479.32,
      "pressure": 2.456
    },
    "dominant_operator": "IGNITION",
    "regime": "LAWFUL",
    "lawfulness": 0.7542
  }
}
```

#### POST `/api/verify/free`
Free verification for testing (no payment required)

**Request:**
```json
{
  "text": "Test text",
  "threshold": "WHITE_LATTICE"
}
```

#### POST `/api/verify/batch`
Batch verification (charges per verification)

**Request:**
```json
{
  "texts": [
    {"text": "First text", "threshold": "WHITE_LATTICE"},
    {"text": "Second text", "threshold": "YELLOW_IGNITION"}
  ],
  "paymentMethodId": "pm_card_visa"
}
```

#### GET `/api/verify/pricing`
Get current pricing

**Response:**
```json
{
  "verification_price": 1,
  "currency": "usd",
  "price_formatted": "$0.01"
}
```

---

### Payout Endpoints

#### POST `/api/payout/transfer`
Create transfer to connected account

**Request:**
```json
{
  "accountId": "acct_abc123",
  "amount": 1000,
  "currency": "usd"
}
```

#### POST `/api/payout/instant`
Create instant payout

**Request:**
```json
{
  "amount": 1000,
  "currency": "usd"
}
```

#### GET `/api/payout/balance`
Get current Stripe balance

#### GET `/api/payout/list`
List recent payouts

---

### Account Endpoints

#### POST `/api/accounts/create`
Create Stripe Connect account

**Request:**
```json
{
  "email": "user@example.com",
  "country": "US",
  "businessType": "individual"
}
```

#### POST `/api/accounts/onboarding-link`
Create onboarding link for account setup

**Request:**
```json
{
  "accountId": "acct_abc123",
  "refreshUrl": "https://example.com/reauth",
  "returnUrl": "https://example.com/return"
}
```

#### GET `/api/accounts/:accountId`
Get account details

---

### Webhook Endpoint

#### POST `/api/webhook/stripe`
Stripe webhook handler (no auth required)

Handles events:
- `payment_intent.succeeded`
- `payment_intent.payment_failed`
- `payout.paid`
- `payout.failed`
- `transfer.created`
- `account.updated`

Configure webhook URL in Stripe Dashboard:
```
https://your-domain.com/api/webhook/stripe
```

---

## Phase Classification

The U9 Pipeline classifies text into 9 thermodynamic phases:

| Phase | Entropy Max | Compression Min | Description |
|-------|-------------|-----------------|-------------|
| **CRYSTAL_WHITE** | 3.5 | 0.40 | Highest order, crystalline structure |
| **WHITE_LATTICE** | 3.8 | 0.35 | High structure, stable lattice |
| **YELLOW_IGNITION** | 4.2 | 0.25 | Phase transition activation |
| **GREEN_ACCUMULATION** | 4.5 | 0.20 | Energy gathering state |
| **RED_COMBUSTION** | 4.8 | 0.15 | Active transformation |
| **ORANGE_HARVEST** | 5.2 | 0.10 | Peak energy extraction |
| **BLUE_DISPERSION** | 5.5 | 0.05 | Energy spreading |
| **VIOLET_DISSOLUTION** | 6.2 | 0.02 | Near-maximum entropy |
| **BLACK_COLLAPSE** | 7.0 | 0.0 | Total disorder |

---

## Revenue Model

### Pricing
- **$0.01 per verification** (1 cent)
- Charged via Stripe before execution
- Supports batch pricing

### Revenue Math

```
100 calls/day = $1/day = $30/month
1,000 calls/day = $10/day = $300/month
10,000 calls/day = $100/day = $3,000/month
```

### Target Customers

1. **AI Agent Developers** - Need verification for agent outputs
2. **Crypto Bot Builders** - Symbolic validation for trading bots
3. **Game Developers** - Procedural content verification
4. **Content Platforms** - Text quality/coherence scoring
5. **Research Labs** - Thermodynamic text analysis

---

## How to Sell This API

### Launch Strategy

#### Week 1: Free Launch
1. **Product Hunt**: Post as "Codex7 Verification API - $0.01/call"
2. **Twitter**: Tweet at AI/crypto devs with free beta codes
3. **Reddit**: Post to r/SideProject, r/webdev, r/cryptodevs
4. **Discord**: Share in developer communities

#### Week 2-4: Paid Conversion
1. Convert free users to paid ($0.01/call is impulse-buy pricing)
2. Offer volume discounts (1M+ calls)
3. Add enterprise tier ($99/month unlimited)

#### Month 2-3: Scale
1. Add integrations (Zapier, Make.com)
2. Create SDKs (Python, JavaScript, Ruby)
3. Build dashboard for usage analytics
4. Add webhook notifications

### Marketing Copy

**For Twitter/Reddit:**
```
Codex7 Verification API is live 🔥

Thermodynamic text verification via U9 pipeline:
- 9-phase classification
- Entropy + compression analysis
- $0.01 per call
- Stripe integration

Built for AI agents, crypto bots, and procedural generation.

Free beta keys 👇
```

**For Product Hunt:**
```
Title: Codex7 Verification API - Thermodynamic Text Analysis at $0.01/call

Description:
Verify text using thermodynamic principles. Our U9 pipeline analyzes
entropy, compression, and coherence to classify content into 9 phases
from Crystal White (maximum order) to Black Collapse (chaos).

Perfect for:
✅ AI agent output validation
✅ Crypto bot symbolic verification
✅ Procedural content scoring
✅ Text quality analysis

Battle-tested U7 thermodynamic engine. Production-ready with Stripe
payments, webhooks, and rate limiting.

$0.01 per verification. No subscription. Pay as you go.
```

---

## Deployment

### Option 1: Railway (Recommended)

1. Push to GitHub
2. Go to railway.app
3. "New Project" → "Deploy from GitHub"
4. Add environment variables
5. Deploy

**Cost:** $5-20/month

### Option 2: Heroku

```bash
heroku create codex7-api
heroku config:set STRIPE_SECRET_KEY=your_key
heroku config:set API_KEYS=your_api_key
git push heroku main
```

**Cost:** $7-25/month

### Option 3: DigitalOcean App Platform

1. Push to GitHub
2. Create App on DigitalOcean
3. Connect repo
4. Add environment variables
5. Deploy

**Cost:** $5-12/month

### Option 4: VPS (Cheapest)

```bash
# On your VPS (Ubuntu 22.04)
git clone https://github.com/yourusername/codex7-verification-api
cd codex7-verification-api
npm install
pm2 start src/server.js --name codex7-api
pm2 startup
pm2 save
```

**Cost:** $5/month (Vultr, Linode, Hetzner)

---

## Testing

### Test with cURL

```bash
# Free verification
curl -X POST http://localhost:3000/api/verify/free \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key" \
  -d '{"text": "Hello world, this is a test", "threshold": "WHITE_LATTICE"}'

# Paid verification (requires Stripe test card)
curl -X POST http://localhost:3000/api/verify \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key" \
  -d '{
    "text": "Test verification",
    "paymentMethodId": "pm_card_visa"
  }'
```

### Stripe Test Cards

- **Success**: `4242 4242 4242 4242`
- **Decline**: `4000 0000 0000 0002`
- **Insufficient funds**: `4000 0000 0000 9995`

---

## Roadmap

- [ ] Add usage dashboard
- [ ] Create JavaScript SDK
- [ ] Create Python SDK
- [ ] Add batch discount pricing
- [ ] Implement caching for repeated texts
- [ ] Add webhook notifications
- [ ] Create Zapier integration
- [ ] Add GraphQL API
- [ ] Enterprise tier with SLA

---

## Support

Questions? Issues?

- **GitHub Issues**: https://github.com/yourusername/codex7-verification-api/issues
- **Email**: support@codex7.io
- **Twitter**: @codex7api

---

## License

MIT License - Free to use commercially

---

## Your Edge: U9 Magick

Nobody else has "thermodynamic computational cycles" + "Loagaeth tensor network" verification.

**That's your moat. That's your $10K/month.**

Ship it. Tell devs. Collect checks.
