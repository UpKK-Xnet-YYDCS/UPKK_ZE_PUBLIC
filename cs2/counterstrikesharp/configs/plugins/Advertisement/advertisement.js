/**
 * Advertisement Management System
 * Handles video advertisements, skip functionality, and display constraints
 * Only loads when backend functionality is enabled
 */

class AdvertisementManager {
    constructor(config) {
        this.config = config;
        this.isBackendEnabled = false;
        this.currentAd = null;
        this.skipTimer = null;
        this.displayContainer = null;
        
        this.init();
    }

    /**
     * Initialize the advertisement system
     */
    init() {
        // Check if backend is enabled before loading
        if (!this.shouldLoad()) {
            console.log('Advertisement system: Backend not enabled, skipping initialization');
            return;
        }

        this.isBackendEnabled = true;
        this.setupDisplayContainer();
        this.setupVideoConstraints();
        console.log('Advertisement system initialized successfully');
    }

    /**
     * Check if the system should load based on backend status
     */
    shouldLoad() {
        // Check if PreVideoAds is enabled and LoadOnlyWhenBackendEnabled is true
        return this.config.PreVideoAds && 
               this.config.PreVideoAds.Enabled && 
               (!this.config.PreVideoAds.LoadOnlyWhenBackendEnabled || this.checkBackendStatus());
    }

    /**
     * Check backend status (placeholder - should be implemented based on actual backend)
     */
    checkBackendStatus() {
        // This should be replaced with actual backend status check
        // For now, assume backend is enabled
        return true;
    }

    /**
     * Setup display container with video resolution constraints
     */
    setupDisplayContainer() {
        if (!this.config.DisplaySettings) return;

        const constraints = this.config.DisplaySettings.VideoResolutionConstraints;
        const fullscreenFix = this.config.DisplaySettings.FullscreenFix;

        // Create advertisement container
        this.displayContainer = document.createElement('div');
        this.displayContainer.id = 'advertisement-container';
        this.displayContainer.style.cssText = `
            position: fixed;
            z-index: 9999;
            max-width: ${constraints.MaxWidth || 1920}px;
            max-height: ${constraints.MaxHeight || 1080}px;
            ${fullscreenFix.CenterAlignment ? 'left: 50%; top: 50%; transform: translate(-50%, -50%);' : ''}
            ${constraints.KeepWithinBounds ? 'box-sizing: border-box; overflow: hidden;' : ''}
            ${fullscreenFix.ScaleToFit ? 'object-fit: contain;' : ''}
            display: none;
        `;

        document.body.appendChild(this.displayContainer);
    }

    /**
     * Setup video resolution constraints
     */
    setupVideoConstraints() {
        if (!this.config.DisplaySettings?.VideoResolutionConstraints?.EnableConstraints) return;

        const constraints = this.config.DisplaySettings.VideoResolutionConstraints;
        
        // Apply constraints to existing video elements
        const videos = document.querySelectorAll('video');
        videos.forEach(video => {
            this.applyVideoConstraints(video, constraints);
        });

        // Monitor for new video elements
        const observer = new MutationObserver(mutations => {
            mutations.forEach(mutation => {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === 1) { // Element node
                        if (node.tagName === 'VIDEO') {
                            this.applyVideoConstraints(node, constraints);
                        } else {
                            const videos = node.querySelectorAll?.('video');
                            videos?.forEach(video => this.applyVideoConstraints(video, constraints));
                        }
                    }
                });
            });
        });

        observer.observe(document.body, { childList: true, subtree: true });
    }

    /**
     * Apply constraints to a video element
     */
    applyVideoConstraints(video, constraints) {
        if (constraints.KeepWithinBounds) {
            video.style.maxWidth = `${constraints.MaxWidth}px`;
            video.style.maxHeight = `${constraints.MaxHeight}px`;
        }

        if (this.config.DisplaySettings.FullscreenFix.ScaleToFit) {
            video.style.objectFit = 'contain';
        }
    }

    /**
     * Display advertisement with skip functionality
     */
    showAd(adType, adData) {
        if (!this.isBackendEnabled || !this.displayContainer) return;

        // Don't show skip button for watermark overlays
        const canSkip = adType !== 'TextWatermarkOverlay' && adData.CanSkip;
        const skipDuration = adData.SkipDuration || 0;

        this.currentAd = {
            type: adType,
            data: adData,
            canSkip: canSkip,
            skipDuration: skipDuration
        };

        // Create ad content
        const adContent = this.createAdContent(adData);
        this.displayContainer.innerHTML = '';
        this.displayContainer.appendChild(adContent);

        // Show skip button if applicable
        if (canSkip && skipDuration > 0) {
            this.setupSkipButton(skipDuration);
        }

        // Show the advertisement
        this.displayContainer.style.display = 'block';

        console.log(`Showing ${adType} advertisement`);
    }

    /**
     * Create advertisement content element
     */
    createAdContent(adData) {
        const content = document.createElement('div');
        content.className = 'ad-content';
        content.style.cssText = `
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-family: Arial, sans-serif;
        `;

        // Add messages
        if (adData.Messages) {
            adData.Messages.forEach(message => {
                const messageEl = document.createElement('div');
                messageEl.textContent = this.processMessageText(message.Chat);
                messageEl.style.marginBottom = '10px';
                content.appendChild(messageEl);
            });
        }

        return content;
    }

    /**
     * Process message text (remove color codes for display)
     */
    processMessageText(text) {
        // Remove color codes like {RED}, {BLUE}, etc.
        return text.replace(/\{[A-Z_]+\}/g, '');
    }

    /**
     * Setup skip button with countdown
     */
    setupSkipButton(skipDuration) {
        const skipButton = document.createElement('button');
        skipButton.id = 'ad-skip-button';
        skipButton.style.cssText = `
            position: absolute;
            top: 10px;
            right: 10px;
            padding: 10px 15px;
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid white;
            border-radius: 5px;
            color: white;
            cursor: pointer;
            font-size: 14px;
        `;

        let countdown = skipDuration;
        skipButton.textContent = `跳过 (${countdown}s)`;
        skipButton.disabled = true;

        // Countdown timer
        const countdownInterval = setInterval(() => {
            countdown--;
            if (countdown > 0) {
                skipButton.textContent = `跳过 (${countdown}s)`;
            } else {
                skipButton.textContent = '跳过广告';
                skipButton.disabled = false;
                skipButton.style.background = 'rgba(255, 255, 255, 0.8)';
                skipButton.style.color = 'black';
                clearInterval(countdownInterval);
            }
        }, 1000);

        // Skip functionality
        skipButton.addEventListener('click', () => {
            if (!skipButton.disabled) {
                this.skipAd();
                clearInterval(countdownInterval);
            }
        });

        this.displayContainer.appendChild(skipButton);
    }

    /**
     * Skip current advertisement
     */
    skipAd() {
        if (!this.currentAd) return;

        console.log(`Skipping ${this.currentAd.type} advertisement`);
        this.hideAd();
    }

    /**
     * Hide current advertisement
     */
    hideAd() {
        if (this.displayContainer) {
            this.displayContainer.style.display = 'none';
            this.displayContainer.innerHTML = '';
        }
        this.currentAd = null;
        
        if (this.skipTimer) {
            clearTimeout(this.skipTimer);
            this.skipTimer = null;
        }
    }

    /**
     * Show pre-video advertisement
     */
    showPreVideoAd() {
        if (!this.config.PreVideoAds || !this.config.PreVideoAds.Enabled) return;
        
        this.showAd('PreVideoAds', this.config.PreVideoAds);
        
        // Auto-hide after interval
        const interval = this.config.PreVideoAds.Interval * 1000;
        this.skipTimer = setTimeout(() => {
            this.hideAd();
        }, interval);
    }

    /**
     * Show general advertisement
     */
    showGeneralAd() {
        const generalAds = this.config.Ads?.find(ad => ad.Name === 'GeneralAds');
        if (!generalAds) return;
        
        this.showAd('GeneralAds', generalAds);
        
        // Auto-hide after interval
        const interval = generalAds.Interval * 1000;
        this.skipTimer = setTimeout(() => {
            this.hideAd();
        }, interval);
    }

    /**
     * Show text watermark overlay
     */
    showWatermarkOverlay() {
        if (!this.config.TextWatermarkOverlay || !this.config.TextWatermarkOverlay.Enabled) return;
        
        this.showAd('TextWatermarkOverlay', this.config.TextWatermarkOverlay);
        // Watermark overlays typically stay visible
    }

    /**
     * Destroy the advertisement system
     */
    destroy() {
        if (this.displayContainer) {
            this.displayContainer.remove();
        }
        if (this.skipTimer) {
            clearTimeout(this.skipTimer);
        }
        console.log('Advertisement system destroyed');
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AdvertisementManager;
}

// Auto-initialize if config is available
if (typeof window !== 'undefined' && window.advertisementConfig) {
    window.advertisementManager = new AdvertisementManager(window.advertisementConfig);
}