/**
 * Error Handler Middleware
 * Centralized error handling and formatting
 */

const logger = require('../utils/logger');
const { CodexError } = require('../utils/errors');

/**
 * Global error handler
 * @param {Error} err - Error object
 * @param {Object} req - Express request
 * @param {Object} res - Express response
 * @param {Function} next - Next middleware
 */
function errorHandler(err, req, res, next) {
  // Log the error
  logger.logError(err, {
    method: req.method,
    path: req.path,
    ip: req.ip
  });

  // Handle CodexError and subclasses
  if (err instanceof CodexError) {
    return res.status(err.statusCode).json(err.toJSON());
  }

  // Handle Stripe errors
  if (err.type && err.type.startsWith('Stripe')) {
    return res.status(402).json({
      error: {
        name: 'PaymentError',
        message: err.message,
        code: err.code,
        type: err.type,
        statusCode: 402,
        timestamp: new Date().toISOString()
      }
    });
  }

  // Handle validation errors
  if (err.name === 'ValidationError') {
    return res.status(400).json({
      error: {
        name: 'ValidationError',
        message: err.message,
        code: 'VALIDATION_ERROR',
        statusCode: 400,
        timestamp: new Date().toISOString()
      }
    });
  }

  // Handle 404 errors
  if (err.status === 404) {
    return res.status(404).json({
      error: {
        name: 'NotFoundError',
        message: 'Route not found',
        code: 'NOT_FOUND',
        statusCode: 404,
        timestamp: new Date().toISOString()
      }
    });
  }

  // Generic error response
  const statusCode = err.statusCode || err.status || 500;
  const message = err.message || 'Internal server error';

  res.status(statusCode).json({
    error: {
      name: err.name || 'Error',
      message,
      code: err.code || 'INTERNAL_ERROR',
      statusCode,
      timestamp: new Date().toISOString(),
      ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
    }
  });
}

/**
 * 404 handler for undefined routes
 * @param {Object} req - Express request
 * @param {Object} res - Express response
 */
function notFoundHandler(req, res) {
  res.status(404).json({
    error: {
      name: 'NotFoundError',
      message: `Route ${req.method} ${req.path} not found`,
      code: 'NOT_FOUND',
      statusCode: 404,
      timestamp: new Date().toISOString()
    }
  });
}

module.exports = {
  errorHandler,
  notFoundHandler
};
