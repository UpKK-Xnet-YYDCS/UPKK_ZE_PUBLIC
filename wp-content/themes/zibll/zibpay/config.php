<?php
/**
 * PayPal Configuration for yuempypay system
 */

return [
    'paypal' => [
        'enabled' => true,
        'exchange_rate' => 7.3, // 7.3 yuan = 1 USD (configurable)
        'currency' => 'USD',
        'base_currency' => 'CNY',
        'sandbox' => true, // Set to false for production
        'client_id' => 'YOUR_PAYPAL_CLIENT_ID',
        'client_secret' => 'YOUR_PAYPAL_CLIENT_SECRET',
        'api_base_url' => 'https://api.sandbox.paypal.com', // Change for production: https://api.paypal.com
    ],
    'yuempypay' => [
        'base_url' => 'https://your-yuempypay-domain.com',
        'redirect_path' => '/pay/',
    ],
];