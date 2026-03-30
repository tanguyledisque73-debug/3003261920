/**
 * Centralized logging utility
 * Allows easy toggling between development and production logging
 */

const isDevelopment = process.env.NODE_ENV === 'development';

const LogLevel = {
  ERROR: 'error',
  WARN: 'warn',
  INFO: 'info',
  DEBUG: 'debug'
};

class Logger {
  constructor() {
    this.enabled = isDevelopment;
  }

  error(message, ...args) {
    if (this.enabled || process.env.REACT_APP_LOG_ERRORS === 'true') {
      console.error(`[ERROR] ${message}`, ...args);
    }
  }

  warn(message, ...args) {
    if (this.enabled) {
      console.warn(`[WARN] ${message}`, ...args);
    }
  }

  info(message, ...args) {
    if (this.enabled) {
      console.info(`[INFO] ${message}`, ...args);
    }
  }

  debug(message, ...args) {
    if (this.enabled) {
      console.log(`[DEBUG] ${message}`, ...args);
    }
  }

  // Production-safe error logging
  logError(error, context = '') {
    const errorInfo = {
      message: error.message,
      stack: error.stack,
      context,
      timestamp: new Date().toISOString()
    };

    if (this.enabled) {
      console.error('[ERROR]', errorInfo);
    }

    // In production, you could send to error tracking service
    if (!isDevelopment && process.env.REACT_APP_ERROR_TRACKING_URL) {
      fetch(process.env.REACT_APP_ERROR_TRACKING_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(errorInfo)
      }).catch(() => {
        // Silently fail if error tracking unavailable
      });
    }

    return errorInfo;
  }
}

// Export singleton instance
const logger = new Logger();

export default logger;
export { LogLevel };
