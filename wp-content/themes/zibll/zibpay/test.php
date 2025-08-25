#!/usr/bin/env php
<?php
/**
 * Test script for PayPal yuempypay integration
 */

require_once(__DIR__ . '/paypal-gateway.php');

class PayPalTest {
    
    public function run() {
        echo "=== PayPal yuempypay Integration Test ===\n\n";
        
        $this->testConfig();
        $this->testCurrencyConversion();
        $this->testOrderCreation();
    }
    
    private function testConfig() {
        echo "1. Testing configuration...\n";
        
        try {
            $gateway = new PayPalGateway();
            $config = $gateway->getConfig();
            
            echo "   ✓ Configuration loaded successfully\n";
            echo "   ✓ Exchange rate: {$config['exchange_rate']}\n";
            echo "   ✓ Currency: {$config['currency']}\n";
            echo "   ✓ Sandbox mode: " . ($config['sandbox'] ? 'enabled' : 'disabled') . "\n";
            
        } catch (Exception $e) {
            echo "   ✗ Configuration error: " . $e->getMessage() . "\n";
        }
        
        echo "\n";
    }
    
    private function testCurrencyConversion() {
        echo "2. Testing currency conversion...\n";
        
        try {
            $gateway = new PayPalGateway();
            
            $test_amounts = [100, 73, 146, 500];
            
            foreach ($test_amounts as $cny) {
                $usd = $gateway->convertCurrency($cny);
                echo "   ✓ ¥{$cny} CNY = \${$usd} USD\n";
            }
            
        } catch (Exception $e) {
            echo "   ✗ Currency conversion error: " . $e->getMessage() . "\n";
        }
        
        echo "\n";
    }
    
    private function testOrderCreation() {
        echo "3. Testing order creation (simulation)...\n";
        
        try {
            $gateway = new PayPalGateway();
            
            $order_data = [
                'order_id' => 'test_' . time(),
                'amount' => 100,
                'description' => 'Test Payment',
                'cancel_url' => 'https://example.com/cancel'
            ];
            
            // Note: This will fail without valid PayPal credentials
            // But we can test the data preparation
            $config = $gateway->getConfig();
            $amount_usd = $gateway->convertCurrency($order_data['amount']);
            
            echo "   ✓ Order data prepared:\n";
            echo "     - Order ID: {$order_data['order_id']}\n";
            echo "     - Amount CNY: ¥{$order_data['amount']}\n";
            echo "     - Amount USD: \${$amount_usd}\n";
            echo "     - Description: {$order_data['description']}\n";
            echo "   ⚠ Actual PayPal API call requires valid credentials\n";
            
        } catch (Exception $e) {
            echo "   ✗ Order creation test error: " . $e->getMessage() . "\n";
        }
        
        echo "\n";
    }
}

// Run tests if script is executed directly
if (php_sapi_name() === 'cli') {
    $test = new PayPalTest();
    $test->run();
    
    echo "=== Test Complete ===\n";
    echo "To complete setup:\n";
    echo "1. Configure PayPal credentials in config.php\n";
    echo "2. Set up WordPress admin settings\n";
    echo "3. Test with actual PayPal sandbox\n";
    echo "4. Deploy to production with live PayPal credentials\n\n";
}