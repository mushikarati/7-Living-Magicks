/**
 * Environment Configuration for Codex7 Verification API
 */

require('dotenv').config();

const config = {
  // Server Configuration
  server: {
    port: process.env.PORT || 3000,
    env: process.env.NODE_ENV || 'development',
    host: process.env.HOST || '0.0.0.0'
  },

  // Stripe Configuration
  stripe: {
    secretKey: process.env.STRIPE_SECRET_KEY,
    webhookSecret: process.env.STRIPE_WEBHOOK_SECRET,
    // Verification pricing (in cents)
    verificationPrice: parseInt(process.env.VERIFICATION_PRICE || '1'), // $0.01
    currency: process.env.CURRENCY || 'usd'
  },

  // API Authentication
  auth: {
    apiKeyHeader: 'X-API-Key',
    apiKeys: process.env.API_KEYS ? process.env.API_KEYS.split(',') : []
  },

  // Verification Engine
  verification: {
    pythonPath: process.env.PYTHON_PATH || 'python3',
    u9PipelinePath: process.env.U9_PIPELINE_PATH || './verification/u9_pipeline.py',
    codexKernelPath: process.env.CODEX_KERNEL_PATH || './verification/codex_kernel.py',
    timeout: parseInt(process.env.VERIFICATION_TIMEOUT || '30000') // 30 seconds
  },

  // Rate Limiting
  rateLimit: {
    windowMs: parseInt(process.env.RATE_LIMIT_WINDOW || '60000'), // 1 minute
    maxRequests: parseInt(process.env.RATE_LIMIT_MAX || '100')
  },

  // Logging
  logging: {
    level: process.env.LOG_LEVEL || 'INFO'
  },

  // Payout Configuration
  payout: {
    minimumAmount: parseInt(process.env.MINIMUM_PAYOUT_AMOUNT || '1000'), // $10.00
    currency: process.env.PAYOUT_CURRENCY || 'usd'
  }
};

// Validation
function validateConfig() {
  const errors = [];

  if (!config.stripe.secretKey) {
    errors.push('STRIPE_SECRET_KEY is required');
  }

  if (!config.stripe.webhookSecret && config.server.env === 'production') {
    errors.push('STRIPE_WEBHOOK_SECRET is required in production');
  }

  if (config.auth.apiKeys.length === 0 && config.server.env === 'production') {
    errors.push('API_KEYS must be configured in production');
  }

  if (errors.length > 0) {
    throw new Error(`Configuration validation failed:\n${errors.join('\n')}`);
  }
}

// Validate on load
try {
  validateConfig();
} catch (error) {
  console.error('Configuration Error:', error.message);
  if (config.server.env === 'production') {
    process.exit(1);
  }
}

module.exports = config;
