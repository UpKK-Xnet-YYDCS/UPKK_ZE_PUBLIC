<?php
/**
 * WordPress integration functions for yuempypay PayPal support
 */

require_once(__DIR__ . '/api.php');

class YuempypayPayPal {
    private $config;
    
    public function __construct() {
        $this->config = include(__DIR__ . '/config.php');
        $this->init();
    }
    
    /**
     * Initialize WordPress hooks
     */
    public function init() {
        // Add PayPal support to payment methods
        add_action('wp_enqueue_scripts', [$this, 'enqueue_scripts']);
        add_action('wp_ajax_create_paypal_order', [$this, 'handle_ajax_create_order']);
        add_action('wp_ajax_nopriv_create_paypal_order', [$this, 'handle_ajax_create_order']);
        
        // Handle API routes
        add_action('init', [$this, 'handle_api_routes']);
        
        // Add PayPal settings to admin
        add_action('admin_menu', [$this, 'add_admin_menu']);
    }
    
    /**
     * Enqueue scripts and styles
     */
    public function enqueue_scripts() {
        wp_enqueue_script(
            'paypal-payment',
            get_template_directory_uri() . '/zibpay/paypal-button.js',
            ['jquery'],
            '1.0.0',
            true
        );
        
        // Pass configuration to JavaScript
        wp_localize_script('paypal-payment', 'paypalConfig', [
            'exchangeRate' => $this->config['paypal']['exchange_rate'],
            'apiEndpoint' => home_url('/api/create_order'),
            'ajaxUrl' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('paypal_payment_nonce')
        ]);
    }
    
    /**
     * Handle API routes
     */
    public function handle_api_routes() {
        $request_uri = $_SERVER['REQUEST_URI'];
        
        if (preg_match('/\/api\/create_order$/', $request_uri)) {
            $api = new PaymentAPI();
            $api->handleRequest();
            exit;
        }
    }
    
    /**
     * Handle AJAX order creation
     */
    public function handle_ajax_create_order() {
        // Verify nonce
        if (!wp_verify_nonce($_POST['nonce'], 'paypal_payment_nonce')) {
            wp_die('Security check failed');
        }
        
        try {
            $paypal_gateway = new PayPalGateway();
            
            $order_data = [
                'order_id' => sanitize_text_field($_POST['order_id']),
                'amount' => floatval($_POST['amount']),
                'description' => sanitize_text_field($_POST['description'] ?? 'yuempypay Payment'),
                'cancel_url' => esc_url($_POST['cancel_url'] ?? '')
            ];
            
            $paypal_order = $paypal_gateway->createOrder($order_data);
            $approval_url = $paypal_gateway->getApprovalUrl($paypal_order);
            
            wp_send_json_success([
                'order_id' => $order_data['order_id'],
                'paypal_order_id' => $paypal_order['id'],
                'approval_url' => $approval_url,
                'amount_cny' => $order_data['amount'],
                'amount_usd' => $paypal_gateway->convertCurrency($order_data['amount']),
                'exchange_rate' => $paypal_gateway->getConfig()['exchange_rate']
            ]);
            
        } catch (Exception $e) {
            wp_send_json_error('Failed to create order: ' . $e->getMessage());
        }
    }
    
    /**
     * Add admin menu for PayPal settings
     */
    public function add_admin_menu() {
        add_options_page(
            'PayPal Settings',
            'PayPal yuempypay',
            'manage_options',
            'paypal-yuempypay',
            [$this, 'admin_page']
        );
    }
    
    /**
     * Admin settings page
     */
    public function admin_page() {
        if (isset($_POST['submit'])) {
            $this->save_settings();
        }
        
        $config = $this->config['paypal'];
        ?>
        <div class="wrap">
            <h1>PayPal yuempypay Settings</h1>
            <form method="post" action="">
                <?php wp_nonce_field('paypal_settings'); ?>
                
                <table class="form-table">
                    <tr>
                        <th scope="row">Enable PayPal</th>
                        <td>
                            <input type="checkbox" name="enabled" value="1" <?php checked($config['enabled']); ?>>
                            <label>Enable PayPal payment gateway</label>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">Exchange Rate (CNY to USD)</th>
                        <td>
                            <input type="number" step="0.01" name="exchange_rate" value="<?php echo esc_attr($config['exchange_rate']); ?>" class="regular-text">
                            <p class="description">How many Chinese Yuan equals 1 USD (e.g., 7.3)</p>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">PayPal Client ID</th>
                        <td>
                            <input type="text" name="client_id" value="<?php echo esc_attr($config['client_id']); ?>" class="regular-text">
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">PayPal Client Secret</th>
                        <td>
                            <input type="password" name="client_secret" value="<?php echo esc_attr($config['client_secret']); ?>" class="regular-text">
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">Sandbox Mode</th>
                        <td>
                            <input type="checkbox" name="sandbox" value="1" <?php checked($config['sandbox']); ?>>
                            <label>Enable sandbox mode for testing</label>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">yuempypay Base URL</th>
                        <td>
                            <input type="url" name="yuempypay_url" value="<?php echo esc_attr($this->config['yuempypay']['base_url']); ?>" class="regular-text">
                            <p class="description">Base URL for yuempypay system</p>
                        </td>
                    </tr>
                </table>
                
                <?php submit_button(); ?>
            </form>
        </div>
        <?php
    }
    
    /**
     * Save admin settings
     */
    private function save_settings() {
        if (!wp_verify_nonce($_POST['_wpnonce'], 'paypal_settings')) {
            wp_die('Security check failed');
        }
        
        $config = [
            'paypal' => [
                'enabled' => isset($_POST['enabled']),
                'exchange_rate' => floatval($_POST['exchange_rate']),
                'currency' => 'USD',
                'base_currency' => 'CNY',
                'sandbox' => isset($_POST['sandbox']),
                'client_id' => sanitize_text_field($_POST['client_id']),
                'client_secret' => sanitize_text_field($_POST['client_secret']),
                'api_base_url' => isset($_POST['sandbox']) ? 
                    'https://api.sandbox.paypal.com' : 
                    'https://api.paypal.com',
            ],
            'yuempypay' => [
                'base_url' => esc_url($_POST['yuempypay_url']),
                'redirect_path' => '/pay/',
            ],
        ];
        
        // Save to config file
        $config_content = "<?php\n/**\n * PayPal Configuration for yuempypay system\n */\n\nreturn " . var_export($config, true) . ";";
        file_put_contents(__DIR__ . '/config.php', $config_content);
        
        add_action('admin_notices', function() {
            echo '<div class="notice notice-success"><p>Settings saved successfully!</p></div>';
        });
    }
    
    /**
     * Display PayPal payment button
     */
    public static function display_payment_button($amount = 0) {
        ?>
        <div id="paypal-payment-section">
            <input type="hidden" id="payment-amount" value="<?php echo esc_attr($amount); ?>">
            <div id="paypal-button-container"></div>
        </div>
        <?php
    }
}

// Initialize the PayPal integration
new YuempypayPayPal();