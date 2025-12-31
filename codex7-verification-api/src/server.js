/**
 * Codex7 Verification API Server
 * Express server with Stripe payment integration
 */

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const config = require('./config');
const logger = require('./utils/logger');
const { authenticateApiKey } = require('./middleware/auth');
const { errorHandler, notFoundHandler } = require('./middleware/errorHandler');

// Import routes
const verificationRoutes = require('./routes/verification');
const payoutRoutes = require('./routes/payout');
const accountsRoutes = require('./routes/accounts');
const webhookRoutes = require('./routes/webhook');

// Initialize Express app
const app = express();

// Security middleware
app.use(helmet());
app.use(cors());

// Webhook routes MUST use raw body parsing
app.use('/api/webhook', express.raw({ type: 'application/json' }));

// JSON body parser for all other routes
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Request logging
app.use((req, res, next) => {
  logger.logRequest(req);
  next();
});

// Rate limiting
const limiter = rateLimit({
  windowMs: config.rateLimit.windowMs,
  max: config.rateLimit.maxRequests,
  message: {
    error: {
      name: 'RateLimitError',
      message: 'Too many requests, please try again later',
      code: 'RATE_LIMIT_EXCEEDED',
      statusCode: 429
    }
  },
  standardHeaders: true,
  legacyHeaders: false
});

app.use('/api/', limiter);

// Health check endpoint (no auth required)
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    service: 'codex7-verification-api'
  });
});

// API info endpoint (no auth required)
app.get('/api', (req, res) => {
  res.json({
    name: 'Codex7 Verification API',
    version: '1.0.0',
    description: 'U9 Pipeline and U7 Thermodynamic Verification Engine',
    endpoints: {
      verification: '/api/verify',
      payout: '/api/payout',
      accounts: '/api/accounts',
      webhook: '/api/webhook',
      pricing: '/api/verify/pricing'
    },
    documentation: 'See README.md for full API documentation'
  });
});

// Mount routes with authentication
app.use('/api/verify', authenticateApiKey, verificationRoutes);
app.use('/api/payout', authenticateApiKey, payoutRoutes);
app.use('/api/accounts', authenticateApiKey, accountsRoutes);
app.use('/api/webhook', webhookRoutes); // Webhooks don't use API key auth

// 404 handler
app.use(notFoundHandler);

// Global error handler (must be last)
app.use(errorHandler);

// Start server
const PORT = config.server.port;
const HOST = config.server.host;

app.listen(PORT, HOST, () => {
  logger.info(`Codex7 Verification API started`, {
    port: PORT,
    host: HOST,
    environment: config.server.env,
    nodeVersion: process.version
  });

  logger.info('Available endpoints', {
    health: '/health',
    api_info: '/api',
    verification: '/api/verify',
    payout: '/api/payout',
    accounts: '/api/accounts',
    webhook: '/api/webhook'
  });
});

// Graceful shutdown
process.on('SIGTERM', () => {
  logger.info('SIGTERM received, shutting down gracefully');
  process.exit(0);
});

process.on('SIGINT', () => {
  logger.info('SIGINT received, shutting down gracefully');
  process.exit(0);
});

module.exports = app;
