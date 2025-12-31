/**
 * Structured Logger for Codex7 Verification API
 * Provides consistent logging with levels and metadata
 */

const LOG_LEVELS = {
  ERROR: 0,
  WARN: 1,
  INFO: 2,
  DEBUG: 3
};

class Logger {
  constructor(level = 'INFO') {
    this.level = LOG_LEVELS[level] || LOG_LEVELS.INFO;
  }

  formatMessage(level, message, metadata = {}) {
    return JSON.stringify({
      timestamp: new Date().toISOString(),
      level,
      message,
      ...metadata
    });
  }

  error(message, metadata = {}) {
    if (this.level >= LOG_LEVELS.ERROR) {
      console.error(this.formatMessage('ERROR', message, metadata));
    }
  }

  warn(message, metadata = {}) {
    if (this.level >= LOG_LEVELS.WARN) {
      console.warn(this.formatMessage('WARN', message, metadata));
    }
  }

  info(message, metadata = {}) {
    if (this.level >= LOG_LEVELS.INFO) {
      console.log(this.formatMessage('INFO', message, metadata));
    }
  }

  debug(message, metadata = {}) {
    if (this.level >= LOG_LEVELS.DEBUG) {
      console.log(this.formatMessage('DEBUG', message, metadata));
    }
  }

  // Specialized logging methods
  logRequest(req) {
    this.info('Incoming request', {
      method: req.method,
      path: req.path,
      ip: req.ip,
      userAgent: req.get('user-agent')
    });
  }

  logVerification(result) {
    this.info('Verification completed', {
      verified: result.verified,
      phase: result.detected_phase,
      confidence: result.confidence
    });
  }

  logPayment(paymentIntent) {
    this.info('Payment processed', {
      id: paymentIntent.id,
      amount: paymentIntent.amount,
      currency: paymentIntent.currency,
      status: paymentIntent.status
    });
  }

  logPayout(payout) {
    this.info('Payout processed', {
      id: payout.id,
      amount: payout.amount,
      currency: payout.currency,
      status: payout.status,
      destination: payout.destination
    });
  }

  logError(error, context = {}) {
    this.error(error.message, {
      name: error.name,
      code: error.code,
      statusCode: error.statusCode,
      stack: error.stack,
      ...context
    });
  }
}

// Export singleton instance
const logger = new Logger(process.env.LOG_LEVEL || 'INFO');

module.exports = logger;
