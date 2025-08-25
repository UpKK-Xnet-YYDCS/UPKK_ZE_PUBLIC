<?php
/**
 * API Endpoints for yuempypay PayPal integration
 */

require_once(__DIR__ . '/paypal-gateway.php');

class PaymentAPI {
    private $paypal_gateway;
    
    public function __construct() {
        $this->paypal_gateway = new PayPalGateway();
    }
    
    /**
     * Handle API requests
     */
    public function handleRequest() {
        $request_uri = $_SERVER['REQUEST_URI'];
        $method = $_SERVER['REQUEST_METHOD'];
        
        // Parse the URI to get the endpoint
        if (preg_match('/\/api\/create_order$/', $request_uri)) {
            if ($method === 'POST') {
                $this->createOrder();
            } else {
                $this->sendError('Method not allowed', 405);
            }
        } else {
            $this->sendError('Endpoint not found', 404);
        }
    }
    
    /**
     * Create order endpoint
     */
    private function createOrder() {
        try {
            // Get JSON input
            $input = json_decode(file_get_contents('php://input'), true);
            
            if (!$input) {
                $this->sendError('Invalid JSON input', 400);
                return;
            }
            
            // Validate required fields
            if (!isset($input['type']) || !isset($input['amount']) || !isset($input['order_id'])) {
                $this->sendError('Missing required fields: type, amount, order_id', 400);
                return;
            }
            
            if ($input['type'] !== 'paypal') {
                $this->sendError('Unsupported payment type: ' . $input['type'], 400);
                return;
            }
            
            // Create PayPal order
            $order_data = [
                'order_id' => $input['order_id'],
                'amount' => floatval($input['amount']),
                'description' => $input['description'] ?? 'yuempypay Payment',
                'cancel_url' => $input['cancel_url'] ?? ''
            ];
            
            $paypal_order = $this->paypal_gateway->createOrder($order_data);
            $approval_url = $this->paypal_gateway->getApprovalUrl($paypal_order);
            
            // Return response
            $this->sendSuccess([
                'order_id' => $input['order_id'],
                'paypal_order_id' => $paypal_order['id'],
                'approval_url' => $approval_url,
                'amount_cny' => $input['amount'],
                'amount_usd' => $this->paypal_gateway->convertCurrency($input['amount']),
                'exchange_rate' => $this->paypal_gateway->getConfig()['exchange_rate']
            ]);
            
        } catch (Exception $e) {
            $this->sendError('Failed to create order: ' . $e->getMessage(), 500);
        }
    }
    
    /**
     * Send success response
     */
    private function sendSuccess($data) {
        header('Content-Type: application/json');
        http_response_code(200);
        echo json_encode([
            'success' => true,
            'data' => $data
        ]);
        exit;
    }
    
    /**
     * Send error response
     */
    private function sendError($message, $code = 500) {
        header('Content-Type: application/json');
        http_response_code($code);
        echo json_encode([
            'success' => false,
            'error' => $message
        ]);
        exit;
    }
}

// Handle API requests if this file is accessed directly
if (basename($_SERVER['SCRIPT_NAME']) === 'api.php') {
    $api = new PaymentAPI();
    $api->handleRequest();
}