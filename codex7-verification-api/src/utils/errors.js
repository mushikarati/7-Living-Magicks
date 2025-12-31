/**
 * Custom Error Classes for Codex7 Verification API
 */

class CodexError extends Error {
  constructor(message, statusCode = 500, code = 'INTERNAL_ERROR') {
    super(message);
    this.name = this.constructor.name;
    this.statusCode = statusCode;
    this.code = code;
    this.timestamp = new Date().toISOString();
    Error.captureStackTrace(this, this.constructor);
  }

  toJSON() {
    return {
      error: {
        name: this.name,
        message: this.message,
        code: this.code,
        statusCode: this.statusCode,
        timestamp: this.timestamp
      }
    };
  }
}

class ValidationError extends CodexError {
  constructor(message, field = null) {
    super(message, 400, 'VALIDATION_ERROR');
    this.field = field;
  }

  toJSON() {
    return {
      error: {
        name: this.name,
        message: this.message,
        code: this.code,
        field: this.field,
        statusCode: this.statusCode,
        timestamp: this.timestamp
      }
    };
  }
}

class AuthenticationError extends CodexError {
  constructor(message = 'Authentication failed') {
    super(message, 401, 'AUTHENTICATION_ERROR');
  }
}

class PaymentError extends CodexError {
  constructor(message, stripeError = null) {
    super(message, 402, 'PAYMENT_REQUIRED');
    this.stripeError = stripeError;
  }

  toJSON() {
    const json = super.toJSON();
    if (this.stripeError) {
      json.error.stripeError = {
        type: this.stripeError.type,
        code: this.stripeError.code,
        message: this.stripeError.message
      };
    }
    return json;
  }
}

class VerificationError extends CodexError {
  constructor(message, details = null) {
    super(message, 422, 'VERIFICATION_ERROR');
    this.details = details;
  }

  toJSON() {
    const json = super.toJSON();
    if (this.details) {
      json.error.details = this.details;
    }
    return json;
  }
}

class RateLimitError extends CodexError {
  constructor(message = 'Rate limit exceeded', retryAfter = 60) {
    super(message, 429, 'RATE_LIMIT_EXCEEDED');
    this.retryAfter = retryAfter;
  }

  toJSON() {
    const json = super.toJSON();
    json.error.retryAfter = this.retryAfter;
    return json;
  }
}

class NotFoundError extends CodexError {
  constructor(resource = 'Resource') {
    super(`${resource} not found`, 404, 'NOT_FOUND');
    this.resource = resource;
  }
}

class InsufficientFundsError extends CodexError {
  constructor(message = 'Insufficient funds in account') {
    super(message, 402, 'INSUFFICIENT_FUNDS');
  }
}

class WebhookError extends CodexError {
  constructor(message) {
    super(message, 400, 'WEBHOOK_ERROR');
  }
}

module.exports = {
  CodexError,
  ValidationError,
  AuthenticationError,
  PaymentError,
  VerificationError,
  RateLimitError,
  NotFoundError,
  InsufficientFundsError,
  WebhookError
};
