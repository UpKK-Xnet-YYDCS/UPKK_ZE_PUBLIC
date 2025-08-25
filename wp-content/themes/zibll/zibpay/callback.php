<?php
/**
 * PayPal callback handler for yuempypay
 * This handles the redirect from PayPal after payment approval
 */

$order_id = $_GET['order_id'] ?? '';

if (empty($order_id)) {
    http_response_code(400);
    die('Missing order ID');
}

// Get PayPal parameters
$paypal_order_id = $_GET['token'] ?? '';
$payer_id = $_GET['PayerID'] ?? '';

// Load configuration
$config = include(__DIR__ . '/config.php');
$yuempypay_url = $config['yuempypay']['base_url'] . $config['yuempypay']['redirect_path'] . $order_id;

// Add PayPal parameters if available
if (!empty($paypal_order_id)) {
    $yuempypay_url .= '?paypal_order_id=' . urlencode($paypal_order_id);
    if (!empty($payer_id)) {
        $yuempypay_url .= '&payer_id=' . urlencode($payer_id);
    }
}

// Redirect to yuempypay
wp_redirect($yuempypay_url);
exit;