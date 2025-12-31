/**
 * Webhook Routes
 * Handle Stripe webhook events
 */

const express = require('express');
const router = express.Router();
const stripeService = require('../services/stripe');
const logger = require('../utils/logger');
const { WebhookError } = require('../utils/errors');

/**
 * POST /api/webhook/stripe
 * Handle Stripe webhook events
 * Note: This endpoint requires raw body parsing
 */
router.post('/stripe', async (req, res, next) => {
  try {
    const signature = req.headers['stripe-signature'];

    if (!signature) {
      throw new WebhookError('Missing Stripe signature header');
    }

    // Verify webhook signature
    const event = stripeService.verifyWebhookSignature(
      req.body,
      signature
    );

    logger.info('Webhook event received', {
      type: event.type,
      id: event.id
    });

    // Handle different event types
    switch (event.type) {
      case 'payment_intent.succeeded':
        await handlePaymentIntentSucceeded(event.data.object);
        break;

      case 'payment_intent.payment_failed':
        await handlePaymentIntentFailed(event.data.object);
        break;

      case 'payout.paid':
        await handlePayoutPaid(event.data.object);
        break;

      case 'payout.failed':
        await handlePayoutFailed(event.data.object);
        break;

      case 'transfer.created':
        await handleTransferCreated(event.data.object);
        break;

      case 'transfer.updated':
        await handleTransferUpdated(event.data.object);
        break;

      case 'account.updated':
        await handleAccountUpdated(event.data.object);
        break;

      default:
        logger.debug('Unhandled webhook event type', { type: event.type });
    }

    // Acknowledge receipt
    res.json({ received: true, event_type: event.type });
  } catch (error) {
    next(error);
  }
});

/**
 * Handle payment intent succeeded event
 */
async function handlePaymentIntentSucceeded(paymentIntent) {
  logger.info('Payment intent succeeded', {
    id: paymentIntent.id,
    amount: paymentIntent.amount,
    currency: paymentIntent.currency
  });

  // Here you could:
  // - Update database with successful payment
  // - Send confirmation email
  // - Trigger verification workflow
  // - Update analytics

  // For now, just log
  logger.logPayment(paymentIntent);
}

/**
 * Handle payment intent failed event
 */
async function handlePaymentIntentFailed(paymentIntent) {
  logger.warn('Payment intent failed', {
    id: paymentIntent.id,
    amount: paymentIntent.amount,
    last_payment_error: paymentIntent.last_payment_error
  });

  // Here you could:
  // - Update database with failed payment
  // - Send failure notification
  // - Trigger retry logic
}

/**
 * Handle payout paid event
 */
async function handlePayoutPaid(payout) {
  logger.info('Payout completed', {
    id: payout.id,
    amount: payout.amount,
    arrival_date: payout.arrival_date
  });

  // Here you could:
  // - Update payout status in database
  // - Send confirmation to recipient
  // - Update accounting records
}

/**
 * Handle payout failed event
 */
async function handlePayoutFailed(payout) {
  logger.error('Payout failed', {
    id: payout.id,
    amount: payout.amount,
    failure_message: payout.failure_message
  });

  // Here you could:
  // - Update payout status in database
  // - Send failure notification
  // - Trigger retry or alternative payout method
}

/**
 * Handle transfer created event
 */
async function handleTransferCreated(transfer) {
  logger.info('Transfer created', {
    id: transfer.id,
    amount: transfer.amount,
    destination: transfer.destination
  });

  // Update tracking system
}

/**
 * Handle transfer updated event
 */
async function handleTransferUpdated(transfer) {
  logger.info('Transfer updated', {
    id: transfer.id,
    status: transfer.status
  });

  // Update tracking system
}

/**
 * Handle account updated event
 */
async function handleAccountUpdated(account) {
  logger.info('Account updated', {
    id: account.id,
    charges_enabled: account.charges_enabled,
    payouts_enabled: account.payouts_enabled
  });

  // Here you could:
  // - Update account status in database
  // - Notify account owner of status changes
}

module.exports = router;
