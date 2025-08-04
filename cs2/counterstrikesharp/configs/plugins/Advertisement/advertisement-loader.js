/**
 * Advertisement Configuration Loader
 * Handles conditional loading of advertisement system based on backend status
 */

(function() {
    'use strict';

    /**
     * Check if backend advertisement functionality is enabled
     */
    function checkBackendEnabled() {
        // This should be replaced with actual backend status check
        // For example, checking server settings or making an API call
        
        // Placeholder implementation - check for specific elements or settings
        const serverSettings = window.serverSettings || {};
        const advertisementEnabled = serverSettings.advertisementEnabled !== false;
        
        return advertisementEnabled;
    }

    /**
     * Load advertisement configuration
     */
    async function loadAdvertisementConfig() {
        try {
            // In a real implementation, this might load from a server endpoint
            // For now, we'll assume the config is embedded or loaded separately
            
            const configResponse = await fetch('./Advertisement.json');
            if (!configResponse.ok) {
                throw new Error('Failed to load advertisement configuration');
            }
            
            const config = await configResponse.json();
            return config;
        } catch (error) {
            console.error('Error loading advertisement configuration:', error);
            return null;
        }
    }

    /**
     * Load and initialize advertisement system
     */
    async function initializeAdvertisementSystem() {
        // Check if backend is enabled before loading anything
        if (!checkBackendEnabled()) {
            console.log('Advertisement system: Backend disabled, not loading');
            return;
        }

        try {
            // Load configuration
            const config = await loadAdvertisementConfig();
            if (!config) {
                console.error('Advertisement system: Failed to load configuration');
                return;
            }

            // Store config globally for the advertisement manager
            window.advertisementConfig = config;

            // Load the advertisement manager script
            const script = document.createElement('script');
            script.src = './advertisement.js';
            script.onload = function() {
                console.log('Advertisement system loaded successfully');
                
                // Initialize advertisement manager
                if (window.AdvertisementManager) {
                    window.advertisementManager = new window.AdvertisementManager(config);
                }
            };
            script.onerror = function() {
                console.error('Failed to load advertisement script');
            };

            document.head.appendChild(script);

        } catch (error) {
            console.error('Error initializing advertisement system:', error);
        }
    }

    /**
     * Setup page load handlers
     */
    function setupPageHandlers() {
        // Show pre-video ads when appropriate
        document.addEventListener('DOMContentLoaded', function() {
            if (window.advertisementManager) {
                // Show pre-video ad if enabled
                setTimeout(() => {
                    window.advertisementManager.showPreVideoAd();
                }, 100);
            }
        });

        // Monitor for video elements
        if (typeof MutationObserver !== 'undefined') {
            const observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    mutation.addedNodes.forEach(function(node) {
                        if (node.nodeType === 1 && node.tagName === 'VIDEO') {
                            // New video element detected, potentially show pre-video ad
                            if (window.advertisementManager) {
                                window.advertisementManager.showPreVideoAd();
                            }
                        }
                    });
                });
            });

            observer.observe(document.body, { childList: true, subtree: true });
        }
    }

    /**
     * Main initialization
     */
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            initializeAdvertisementSystem();
            setupPageHandlers();
        });
    } else {
        initializeAdvertisementSystem();
        setupPageHandlers();
    }

    // Export utilities for manual control
    window.AdvertisementLoader = {
        checkBackendEnabled: checkBackendEnabled,
        loadConfig: loadAdvertisementConfig,
        init: initializeAdvertisementSystem
    };

})();