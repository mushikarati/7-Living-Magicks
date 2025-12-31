/**
 * Stripe Service - Payment and Payout Integration
 */

const Stripe = require('stripe');
const config = require('../config');
const logger = require('../utils/logger');
const { PaymentError, InsufficientFundsError } = require('../utils/errors');

const stripe = new Stripe(config.stripe.secretKey);

class StripeService {
  /**
   * Create a payment intent for verification
   * @param {Object} params - Payment parameters
   * @returns {Promise<Object>} Payment intent
   */
  async createVerificationPayment({ amount, currency, metadata }) {
    try {
      const paymentIntent = await stripe.paymentIntents.create({
        amount: amount || config.stripe.verificationPrice,
        currency: currency || config.stripe.currency,
        metadata: {
          service: 'codex7_verification',
          ...metadata
        },
        automatic_payment_methods: {
          enabled: true,
        }
      });

      logger.logPayment(paymentIntent);
      return paymentIntent;
    } catch (error) {
      logger.logError(error, { context: 'createVerificationPayment' });
      throw new PaymentError('Failed to create payment intent', error);
    }
  }

  /**
   * Charge for verification using payment method
   * @param {string} paymentMethodId - Stripe payment method ID
   * @param {number} amount - Amount in cents
   * @param {Object} metadata - Additional metadata
   * @returns {Promise<Object>} Payment intent
   */
  async chargeForVerification(paymentMethodId, amount, metadata = {}) {
    try {
      const paymentIntent = await stripe.paymentIntents.create({
        amount: amount || config.stripe.verificationPrice,
        currency: config.stripe.currency,
        payment_method: paymentMethodId,
        confirm: true,
        metadata: {
          service: 'codex7_verification',
          ...metadata
        }
      });

      if (paymentIntent.status !== 'succeeded') {
        throw new PaymentError('Payment failed');
      }

      logger.logPayment(paymentIntent);
      return paymentIntent;
    } catch (error) {
      logger.logError(error, { context: 'chargeForVerification' });
      throw new PaymentError('Payment charge failed', error);
    }
  }

  /**
   * Retrieve payment intent
   * @param {string} paymentIntentId - Payment intent ID
   * @returns {Promise<Object>} Payment intent
   */
  async getPaymentIntent(paymentIntentId) {
    try {
      return await stripe.paymentIntents.retrieve(paymentIntentId);
    } catch (error) {
      logger.logError(error, { context: 'getPaymentIntent' });
      throw new PaymentError('Failed to retrieve payment intent', error);
    }
  }

  /**
   * Create connected account for payouts
   * @param {Object} accountData - Account creation data
   * @returns {Promise<Object>} Stripe account
   */
  async createConnectedAccount(accountData) {
    try {
      const account = await stripe.accounts.create({
        type: 'express',
        country: accountData.country || 'US',
        email: accountData.email,
        capabilities: {
          card_payments: { requested: true },
          transfers: { requested: true }
        },
        business_type: accountData.businessType || 'individual',
        metadata: accountData.metadata || {}
      });

      logger.info('Connected account created', { accountId: account.id });
      return account;
    } catch (error) {
      logger.logError(error, { context: 'createConnectedAccount' });
      throw new PaymentError('Failed to create connected account', error);
    }
  }

  /**
   * Create account link for onboarding
   * @param {string} accountId - Stripe account ID
   * @param {string} refreshUrl - URL to redirect on refresh
   * @param {string} returnUrl - URL to redirect on completion
   * @returns {Promise<Object>} Account link
   */
  async createAccountLink(accountId, refreshUrl, returnUrl) {
    try {
      const accountLink = await stripe.accountLinks.create({
        account: accountId,
        refresh_url: refreshUrl,
        return_url: returnUrl,
        type: 'account_onboarding'
      });

      return accountLink;
    } catch (error) {
      logger.logError(error, { context: 'createAccountLink' });
      throw new PaymentError('Failed to create account link', error);
    }
  }

  /**
   * Get account details
   * @param {string} accountId - Stripe account ID
   * @returns {Promise<Object>} Account details
   */
  async getAccount(accountId) {
    try {
      return await stripe.accounts.retrieve(accountId);
    } catch (error) {
      logger.logError(error, { context: 'getAccount' });
      throw new PaymentError('Failed to retrieve account', error);
    }
  }

  /**
   * Create payout to connected account
   * @param {Object} payoutData - Payout parameters
   * @returns {Promise<Object>} Payout object
   */
  async createPayout(payoutData) {
    const { accountId, amount, currency, metadata } = payoutData;

    try {
      // Validate minimum payout amount
      if (amount < config.payout.minimumAmount) {
        throw new InsufficientFundsError(
          `Minimum payout amount is ${config.payout.minimumAmount} cents`
        );
      }

      // Create transfer to connected account
      const transfer = await stripe.transfers.create({
        amount,
        currency: currency || config.payout.currency,
        destination: accountId,
        metadata: {
          service: 'codex7_payout',
          ...metadata
        }
      });

      logger.logPayout(transfer);
      return transfer;
    } catch (error) {
      logger.logError(error, { context: 'createPayout' });

      if (error instanceof InsufficientFundsError) {
        throw error;
      }

      throw new PaymentError('Failed to create payout', error);
    }
  }

  /**
   * Create instant payout (requires Stripe Balance)
   * @param {Object} payoutData - Payout parameters
   * @returns {Promise<Object>} Payout object
   */
  async createInstantPayout(payoutData) {
    const { amount, currency, method, metadata } = payoutData;

    try {
      const payout = await stripe.payouts.create({
        amount,
        currency: currency || config.payout.currency,
        method: method || 'instant',
        metadata: {
          service: 'codex7_instant_payout',
          ...metadata
        }
      });

      logger.logPayout(payout);
      return payout;
    } catch (error) {
      logger.logError(error, { context: 'createInstantPayout' });
      throw new PaymentError('Failed to create instant payout', error);
    }
  }

  /**
   * Get balance
   * @returns {Promise<Object>} Balance object
   */
  async getBalance() {
    try {
      return await stripe.balance.retrieve();
    } catch (error) {
      logger.logError(error, { context: 'getBalance' });
      throw new PaymentError('Failed to retrieve balance', error);
    }
  }

  /**
   * List payouts
   * @param {Object} params - Query parameters
   * @returns {Promise<Object>} List of payouts
   */
  async listPayouts(params = {}) {
    try {
      return await stripe.payouts.list({
        limit: params.limit || 10,
        ...params
      });
    } catch (error) {
      logger.logError(error, { context: 'listPayouts' });
      throw new PaymentError('Failed to list payouts', error);
    }
  }

  /**
   * Verify webhook signature
   * @param {string} payload - Raw request body
   * @param {string} signature - Stripe signature header
   * @returns {Object} Verified event
   */
  verifyWebhookSignature(payload, signature) {
    try {
      return stripe.webhooks.constructEvent(
        payload,
        signature,
        config.stripe.webhookSecret
      );
    } catch (error) {
      logger.logError(error, { context: 'verifyWebhookSignature' });
      throw new PaymentError('Webhook signature verification failed', error);
    }
  }
}

module.exports = new StripeService();
