/**
 * Verification Routes
 * Endpoints for U9 and U7 verification
 */

const express = require('express');
const router = express.Router();
const verificationService = require('../services/verification');
const stripeService = require('../services/stripe');
const logger = require('../utils/logger');
const { ValidationError } = require('../utils/errors');
const config = require('../config');

/**
 * POST /api/verify
 * Run paid verification (charges via Stripe)
 */
router.post('/verify', async (req, res, next) => {
  try {
    const { text, threshold, paymentMethodId, includeKernel } = req.body;

    // Validate input
    if (!text) {
      throw new ValidationError('Text is required', 'text');
    }

    if (!paymentMethodId) {
      throw new ValidationError('Payment method ID is required', 'paymentMethodId');
    }

    // Charge for verification BEFORE executing
    logger.info('Processing payment for verification');
    const payment = await stripeService.chargeForVerification(
      paymentMethodId,
      config.stripe.verificationPrice,
      {
        text_length: text.length,
        threshold: threshold || 'WHITE_LATTICE'
      }
    );

    // Execute verification
    logger.info('Payment successful, executing verification');
    const result = await verificationService.runCompleteVerification(
      text,
      threshold,
      includeKernel !== false
    );

    res.json({
      success: true,
      payment_id: payment.id,
      amount_charged: payment.amount,
      currency: payment.currency,
      ...result
    });
  } catch (error) {
    next(error);
  }
});

/**
 * POST /api/verify/free
 * Free verification (no payment required, for testing)
 */
router.post('/verify/free', async (req, res, next) => {
  try {
    const { text, threshold, includeKernel } = req.body;

    if (!text) {
      throw new ValidationError('Text is required', 'text');
    }

    logger.info('Running free verification (testing mode)');

    const result = await verificationService.runCompleteVerification(
      text,
      threshold,
      includeKernel !== false
    );

    res.json({
      success: true,
      note: 'This is a free verification for testing purposes',
      ...result
    });
  } catch (error) {
    next(error);
  }
});

/**
 * POST /api/verify/batch
 * Batch verification (charges per verification)
 */
router.post('/verify/batch', async (req, res, next) => {
  try {
    const { texts, paymentMethodId } = req.body;

    if (!texts || !Array.isArray(texts) || texts.length === 0) {
      throw new ValidationError('Texts array is required', 'texts');
    }

    if (!paymentMethodId) {
      throw new ValidationError('Payment method ID is required', 'paymentMethodId');
    }

    // Calculate total cost
    const totalCost = texts.length * config.stripe.verificationPrice;

    // Charge for all verifications upfront
    logger.info('Processing batch payment', { count: texts.length, totalCost });
    const payment = await stripeService.chargeForVerification(
      paymentMethodId,
      totalCost,
      {
        batch_count: texts.length,
        service: 'batch_verification'
      }
    );

    // Execute batch verification
    logger.info('Batch payment successful, executing verifications');
    const results = await verificationService.batchVerify(texts);

    res.json({
      success: true,
      payment_id: payment.id,
      amount_charged: payment.amount,
      currency: payment.currency,
      per_verification_cost: config.stripe.verificationPrice,
      ...results
    });
  } catch (error) {
    next(error);
  }
});

/**
 * POST /api/verify/u9
 * Direct U9 pipeline access (paid)
 */
router.post('/verify/u9', async (req, res, next) => {
  try {
    const { text, threshold, paymentMethodId } = req.body;

    if (!text) {
      throw new ValidationError('Text is required', 'text');
    }

    if (!paymentMethodId) {
      throw new ValidationError('Payment method ID is required', 'paymentMethodId');
    }

    // Charge for verification
    const payment = await stripeService.chargeForVerification(
      paymentMethodId,
      config.stripe.verificationPrice,
      { service: 'u9_pipeline' }
    );

    // Run U9 only
    const result = await verificationService.runU9Pipeline(text, threshold);

    res.json({
      success: true,
      payment_id: payment.id,
      amount_charged: payment.amount,
      ...result
    });
  } catch (error) {
    next(error);
  }
});

/**
 * POST /api/verify/u7
 * Direct U7 kernel access (paid)
 */
router.post('/verify/u7', async (req, res, next) => {
  try {
    const { text, entropy, compression, paymentMethodId } = req.body;

    if (!text) {
      throw new ValidationError('Text is required', 'text');
    }

    if (entropy === undefined || compression === undefined) {
      throw new ValidationError('Entropy and compression are required for U7 kernel', 'entropy');
    }

    if (!paymentMethodId) {
      throw new ValidationError('Payment method ID is required', 'paymentMethodId');
    }

    // Charge for verification
    const payment = await stripeService.chargeForVerification(
      paymentMethodId,
      config.stripe.verificationPrice,
      { service: 'u7_kernel' }
    );

    // Run U7 kernel
    const result = await verificationService.runCodexKernel(text, entropy, compression);

    res.json({
      success: true,
      payment_id: payment.id,
      amount_charged: payment.amount,
      ...result
    });
  } catch (error) {
    next(error);
  }
});

/**
 * GET /api/verify/pricing
 * Get pricing information
 */
router.get('/pricing', (req, res) => {
  res.json({
    verification_price: config.stripe.verificationPrice,
    currency: config.stripe.currency,
    price_formatted: `$${(config.stripe.verificationPrice / 100).toFixed(2)}`,
    endpoints: {
      '/api/verify': 'Complete verification (U9 + U7)',
      '/api/verify/u9': 'U9 pipeline only',
      '/api/verify/u7': 'U7 kernel only',
      '/api/verify/batch': 'Batch verification (price per verification)'
    }
  });
});

module.exports = router;
