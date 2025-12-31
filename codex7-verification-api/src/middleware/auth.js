/**
 * Authentication Middleware
 * API Key-based authentication
 */

const config = require('../config');
const logger = require('../utils/logger');
const { AuthenticationError } = require('../utils/errors');

/**
 * Verify API key from request headers
 * @param {Object} req - Express request
 * @param {Object} res - Express response
 * @param {Function} next - Next middleware
 */
function authenticateApiKey(req, res, next) {
  const apiKey = req.get(config.auth.apiKeyHeader);

  if (!apiKey) {
    logger.warn('Missing API key', { ip: req.ip, path: req.path });
    return next(new AuthenticationError('API key required'));
  }

  // Validate API key
  if (!config.auth.apiKeys.includes(apiKey)) {
    logger.warn('Invalid API key', { ip: req.ip, path: req.path });
    return next(new AuthenticationError('Invalid API key'));
  }

  // Store API key in request for logging
  req.apiKey = apiKey;

  logger.debug('API key validated', { ip: req.ip });
  next();
}

/**
 * Optional authentication - allows unauthenticated requests
 * but sets req.authenticated flag
 * @param {Object} req - Express request
 * @param {Object} res - Express response
 * @param {Function} next - Next middleware
 */
function optionalAuth(req, res, next) {
  const apiKey = req.get(config.auth.apiKeyHeader);

  if (apiKey && config.auth.apiKeys.includes(apiKey)) {
    req.authenticated = true;
    req.apiKey = apiKey;
  } else {
    req.authenticated = false;
  }

  next();
}

module.exports = {
  authenticateApiKey,
  optionalAuth
};
