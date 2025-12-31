/**
 * Accounts Routes
 * Manage Stripe Connect accounts for payouts
 */

const express = require('express');
const router = express.Router();
const stripeService = require('../services/stripe');
const logger = require('../utils/logger');
const { ValidationError } = require('../utils/errors');

/**
 * POST /api/accounts/create
 * Create a new Stripe Connect account
 */
router.post('/create', async (req, res, next) => {
  try {
    const { email, country, businessType, metadata } = req.body;

    if (!email) {
      throw new ValidationError('Email is required', 'email');
    }

    logger.info('Creating connected account', { email });

    const account = await stripeService.createConnectedAccount({
      email,
      country: country || 'US',
      businessType: businessType || 'individual',
      metadata
    });

    res.json({
      success: true,
      account_id: account.id,
      email: account.email,
      country: account.country,
      type: account.type,
      created: account.created
    });
  } catch (error) {
    next(error);
  }
});

/**
 * POST /api/accounts/onboarding-link
 * Create onboarding link for account setup
 */
router.post('/onboarding-link', async (req, res, next) => {
  try {
    const { accountId, refreshUrl, returnUrl } = req.body;

    if (!accountId) {
      throw new ValidationError('Account ID is required', 'accountId');
    }

    if (!refreshUrl || !returnUrl) {
      throw new ValidationError('Refresh URL and return URL are required');
    }

    logger.info('Creating account onboarding link', { accountId });

    const accountLink = await stripeService.createAccountLink(
      accountId,
      refreshUrl,
      returnUrl
    );

    res.json({
      success: true,
      url: accountLink.url,
      expires_at: accountLink.expires_at
    });
  } catch (error) {
    next(error);
  }
});

/**
 * GET /api/accounts/:accountId
 * Get account details
 */
router.get('/:accountId', async (req, res, next) => {
  try {
    const { accountId } = req.params;

    logger.info('Retrieving account details', { accountId });

    const account = await stripeService.getAccount(accountId);

    res.json({
      success: true,
      account: {
        id: account.id,
        email: account.email,
        country: account.country,
        type: account.type,
        charges_enabled: account.charges_enabled,
        payouts_enabled: account.payouts_enabled,
        details_submitted: account.details_submitted,
        created: account.created
      }
    });
  } catch (error) {
    next(error);
  }
});

/**
 * GET /api/accounts/:accountId/balance
 * Get account balance
 */
router.get('/:accountId/balance', async (req, res, next) => {
  try {
    const { accountId } = req.params;

    logger.info('Retrieving account balance', { accountId });

    // Note: This requires the account to be retrieved first
    const account = await stripeService.getAccount(accountId);

    // For connected accounts, use Stripe API with account parameter
    const balance = await stripeService.getBalance();

    res.json({
      success: true,
      account_id: accountId,
      balance: {
        available: balance.available,
        pending: balance.pending
      }
    });
  } catch (error) {
    next(error);
  }
});

module.exports = router;
