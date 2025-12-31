/**
 * Payout Routes
 * Handle Stripe payouts and transfers
 */

const express = require('express');
const router = express.Router();
const stripeService = require('../services/stripe');
const logger = require('../utils/logger');
const { ValidationError, InsufficientFundsError } = require('../utils/errors');
const config = require('../config');

/**
 * POST /api/payout/transfer
 * Create transfer to connected account
 */
router.post('/transfer', async (req, res, next) => {
  try {
    const { accountId, amount, currency, metadata } = req.body;

    if (!accountId) {
      throw new ValidationError('Account ID is required', 'accountId');
    }

    if (!amount || amount < config.payout.minimumAmount) {
      throw new ValidationError(
        `Amount must be at least ${config.payout.minimumAmount} cents`,
        'amount'
      );
    }

    logger.info('Creating payout transfer', { accountId, amount });

    const transfer = await stripeService.createPayout({
      accountId,
      amount,
      currency: currency || config.payout.currency,
      metadata
    });

    res.json({
      success: true,
      transfer_id: transfer.id,
      amount: transfer.amount,
      currency: transfer.currency,
      destination: transfer.destination,
      status: transfer.status,
      created: transfer.created
    });
  } catch (error) {
    next(error);
  }
});

/**
 * POST /api/payout/instant
 * Create instant payout (requires Stripe Balance)
 */
router.post('/instant', async (req, res, next) => {
  try {
    const { amount, currency, metadata } = req.body;

    if (!amount || amount < config.payout.minimumAmount) {
      throw new ValidationError(
        `Amount must be at least ${config.payout.minimumAmount} cents`,
        'amount'
      );
    }

    logger.info('Creating instant payout', { amount });

    const payout = await stripeService.createInstantPayout({
      amount,
      currency: currency || config.payout.currency,
      method: 'instant',
      metadata
    });

    res.json({
      success: true,
      payout_id: payout.id,
      amount: payout.amount,
      currency: payout.currency,
      status: payout.status,
      arrival_date: payout.arrival_date,
      method: payout.method
    });
  } catch (error) {
    next(error);
  }
});

/**
 * GET /api/payout/balance
 * Get current Stripe balance
 */
router.get('/balance', async (req, res, next) => {
  try {
    logger.info('Retrieving balance');

    const balance = await stripeService.getBalance();

    res.json({
      success: true,
      available: balance.available,
      pending: balance.pending,
      currency: config.payout.currency
    });
  } catch (error) {
    next(error);
  }
});

/**
 * GET /api/payout/list
 * List recent payouts
 */
router.get('/list', async (req, res, next) => {
  try {
    const { limit = 10, startingAfter, endingBefore } = req.query;

    logger.info('Listing payouts', { limit });

    const payouts = await stripeService.listPayouts({
      limit: parseInt(limit),
      starting_after: startingAfter,
      ending_before: endingBefore
    });

    res.json({
      success: true,
      payouts: payouts.data.map(p => ({
        id: p.id,
        amount: p.amount,
        currency: p.currency,
        status: p.status,
        arrival_date: p.arrival_date,
        method: p.method,
        created: p.created
      })),
      has_more: payouts.has_more
    });
  } catch (error) {
    next(error);
  }
});

/**
 * GET /api/payout/settings
 * Get payout configuration
 */
router.get('/settings', (req, res) => {
  res.json({
    minimum_amount: config.payout.minimumAmount,
    minimum_amount_formatted: `$${(config.payout.minimumAmount / 100).toFixed(2)}`,
    currency: config.payout.currency,
    instant_payout_available: true,
    standard_payout_available: true
  });
});

module.exports = router;
