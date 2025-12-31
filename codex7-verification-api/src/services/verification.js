/**
 * Verification Service - Bridge to Python U9 Pipeline and U7 Codex Kernel
 */

const { spawn } = require('child_process');
const path = require('path');
const config = require('../config');
const logger = require('../utils/logger');
const { VerificationError } = require('../utils/errors');

class VerificationService {
  /**
   * Execute Python script and return parsed JSON result
   * @param {string} scriptPath - Path to Python script
   * @param {Array<string>} args - Script arguments
   * @returns {Promise<Object>} Parsed script output
   */
  async executePythonScript(scriptPath, args = []) {
    return new Promise((resolve, reject) => {
      const absolutePath = path.resolve(scriptPath);
      let stdout = '';
      let stderr = '';

      logger.debug('Executing Python script', { scriptPath: absolutePath, args });

      const pythonProcess = spawn(config.verification.pythonPath, [absolutePath, ...args]);

      pythonProcess.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      pythonProcess.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      pythonProcess.on('close', (code) => {
        if (code !== 0) {
          logger.error('Python script failed', { code, stderr, scriptPath });
          reject(new VerificationError(`Python script exited with code ${code}: ${stderr}`));
          return;
        }

        try {
          const result = JSON.parse(stdout);

          if (result.error) {
            reject(new VerificationError(result.error, result));
            return;
          }

          resolve(result);
        } catch (error) {
          logger.error('Failed to parse Python output', { stdout, error: error.message });
          reject(new VerificationError('Invalid JSON output from verification engine'));
        }
      });

      pythonProcess.on('error', (error) => {
        logger.error('Failed to start Python process', { error: error.message });
        reject(new VerificationError(`Failed to execute verification: ${error.message}`));
      });

      // Timeout handling
      const timeout = setTimeout(() => {
        pythonProcess.kill();
        reject(new VerificationError('Verification timeout exceeded'));
      }, config.verification.timeout);

      pythonProcess.on('close', () => {
        clearTimeout(timeout);
      });
    });
  }

  /**
   * Run U9 Pipeline verification
   * @param {string} text - Text to verify
   * @param {string} threshold - Phase threshold
   * @returns {Promise<Object>} Verification result
   */
  async runU9Pipeline(text, threshold = 'WHITE_LATTICE') {
    try {
      logger.info('Running U9 pipeline', { textLength: text.length, threshold });

      const result = await this.executePythonScript(
        config.verification.u9PipelinePath,
        [text, threshold]
      );

      logger.logVerification(result);
      return result;
    } catch (error) {
      logger.logError(error, { context: 'runU9Pipeline' });
      throw error;
    }
  }

  /**
   * Run U7 Codex Kernel
   * @param {string} text - Input text
   * @param {number} entropy - Shannon entropy
   * @param {number} compression - Compression ratio
   * @returns {Promise<Object>} Kernel analysis
   */
  async runCodexKernel(text, entropy, compression) {
    try {
      logger.info('Running Codex Kernel', { entropy, compression });

      const result = await this.executePythonScript(
        config.verification.codexKernelPath,
        [text, entropy.toString(), compression.toString()]
      );

      logger.debug('Codex Kernel result', result);
      return result;
    } catch (error) {
      logger.logError(error, { context: 'runCodexKernel' });
      throw error;
    }
  }

  /**
   * Run complete verification (U9 + U7)
   * @param {string} text - Text to verify
   * @param {string} threshold - Phase threshold
   * @param {boolean} includeKernel - Include U7 kernel analysis
   * @returns {Promise<Object>} Complete verification result
   */
  async runCompleteVerification(text, threshold = 'WHITE_LATTICE', includeKernel = true) {
    try {
      // Run U9 pipeline
      const u9Result = await this.runU9Pipeline(text, threshold);

      // Optionally run U7 kernel for deeper analysis
      let kernelResult = null;
      if (includeKernel) {
        kernelResult = await this.runCodexKernel(
          text,
          u9Result.metrics.entropy_bits,
          u9Result.metrics.compression_ratio
        );
      }

      const completeResult = {
        verification_id: this.generateVerificationId(),
        timestamp: new Date().toISOString(),
        u9_pipeline: u9Result,
        u7_kernel: kernelResult,
        summary: {
          verified: u9Result.verified,
          phase: u9Result.detected_phase,
          confidence: u9Result.confidence,
          lawfulness: kernelResult ? kernelResult.lawfulness : null,
          stability: kernelResult ? kernelResult.stability : null
        }
      };

      return completeResult;
    } catch (error) {
      logger.logError(error, { context: 'runCompleteVerification' });
      throw error;
    }
  }

  /**
   * Generate unique verification ID
   * @returns {string} Verification ID
   */
  generateVerificationId() {
    return `ver_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Batch verification for multiple texts
   * @param {Array<Object>} texts - Array of {text, threshold} objects
   * @returns {Promise<Array<Object>>} Array of verification results
   */
  async batchVerify(texts) {
    try {
      const results = await Promise.all(
        texts.map(({ text, threshold }) =>
          this.runCompleteVerification(text, threshold, false)
        )
      );

      return {
        batch_id: this.generateVerificationId(),
        timestamp: new Date().toISOString(),
        total_count: texts.length,
        results
      };
    } catch (error) {
      logger.logError(error, { context: 'batchVerify' });
      throw error;
    }
  }
}

module.exports = new VerificationService();
