<?php
/**
 * PayPal Payment Gateway for yuempypay
 */

class PayPalGateway {
    private $config;
    
    public function __construct() {
        $this->config = include(__DIR__ . '/config.php');
    }
    
    /**
     * Get PayPal configuration
     */
    public function getConfig() {
        return $this->config['paypal'];
    }
    
    /**
     * Convert CNY to USD based on configured exchange rate
     */
    public function convertCurrency($amount_cny) {
        $exchange_rate = $this->config['paypal']['exchange_rate'];
        return round($amount_cny / $exchange_rate, 2);
    }
    
    /**
     * Get PayPal access token
     */
    private function getAccessToken() {
        $config = $this->config['paypal'];
        $url = $config['api_base_url'] . '/v1/oauth2/token';
        
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_HEADER, false);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_USERPWD, $config['client_id'] . ":" . $config['client_secret']);
        curl_setopt($ch, CURLOPT_POSTFIELDS, "grant_type=client_credentials");
        
        $result = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        if ($httpCode !== 200) {
            throw new Exception('Failed to get PayPal access token');
        }
        
        $json = json_decode($result, true);
        return $json['access_token'];
    }
    
    /**
     * Create PayPal order
     */
    public function createOrder($order_data) {
        $config = $this->config['paypal'];
        $access_token = $this->getAccessToken();
        
        $amount_usd = $this->convertCurrency($order_data['amount']);
        
        $order = [
            'intent' => 'CAPTURE',
            'purchase_units' => [[
                'amount' => [
                    'currency_code' => $config['currency'],
                    'value' => $amount_usd
                ],
                'description' => $order_data['description'] ?? 'yuempypay Payment',
                'custom_id' => $order_data['order_id']
            ]],
            'application_context' => [
                'return_url' => $this->config['yuempypay']['base_url'] . $this->config['yuempypay']['redirect_path'] . $order_data['order_id'],
                'cancel_url' => $order_data['cancel_url'] ?? '',
                'brand_name' => 'yuempypay',
                'landing_page' => 'LOGIN'
            ]
        ];
        
        $url = $config['api_base_url'] . '/v2/checkout/orders';
        
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_HEADER, false);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'Authorization: Bearer ' . $access_token
        ]);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($order));
        
        $result = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        if ($httpCode !== 201) {
            throw new Exception('Failed to create PayPal order: ' . $result);
        }
        
        return json_decode($result, true);
    }
    
    /**
     * Get PayPal approval URL from order response
     */
    public function getApprovalUrl($order_response) {
        foreach ($order_response['links'] as $link) {
            if ($link['rel'] === 'approve') {
                return $link['href'];
            }
        }
        throw new Exception('No approval URL found in PayPal order response');
    }
}