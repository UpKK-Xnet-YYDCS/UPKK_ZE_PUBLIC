/**
 * PayPal Payment Button JavaScript for yuempypay
 */

class PayPalPayment {
    constructor(config = {}) {
        this.config = {
            exchangeRate: 7.3,
            apiEndpoint: '/api/create_order',
            currency: 'CNY',
            ...config
        };
        this.init();
    }
    
    init() {
        this.createPayPalButton();
    }
    
    /**
     * Create PayPal payment button
     */
    createPayPalButton() {
        // Create button container if it doesn't exist
        if (!document.getElementById('paypal-button-container')) {
            const container = document.createElement('div');
            container.id = 'paypal-button-container';
            container.style.margin = '20px 0';
            
            // Find a suitable parent element to append the button
            const paymentSection = document.querySelector('.payment-methods') || 
                                 document.querySelector('.payment-section') || 
                                 document.body;
            paymentSection.appendChild(container);
        }
        
        // Create PayPal button HTML
        const paypalButton = document.createElement('div');
        paypalButton.innerHTML = `
            <div class="paypal-payment-section">
                <h3>PayPal 支付</h3>
                <div class="payment-info">
                    <p>汇率: ¥${this.config.exchangeRate} = $1 USD</p>
                    <div class="amount-display">
                        <span>支付金额: </span>
                        <span class="cny-amount">¥0.00</span>
                        <span> ≈ </span>
                        <span class="usd-amount">$0.00</span>
                    </div>
                </div>
                <button id="paypal-pay-button" class="paypal-button" disabled>
                    <img src="https://www.paypalobjects.com/webstatic/mktg/logo/pp_cc_mark_111x69.jpg" alt="PayPal" style="height: 30px; vertical-align: middle;">
                    <span style="margin-left: 10px;">使用 PayPal 支付</span>
                </button>
                <div class="paypal-loading" style="display: none;">
                    <p>正在创建订单...</p>
                </div>
            </div>
        `;
        
        // Add CSS styles
        const style = document.createElement('style');
        style.textContent = `
            .paypal-payment-section {
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
                background-color: #f9f9f9;
            }
            .paypal-payment-section h3 {
                margin: 0 0 15px 0;
                color: #003087;
            }
            .payment-info {
                margin-bottom: 15px;
                font-size: 14px;
            }
            .amount-display {
                margin: 10px 0;
                font-weight: bold;
            }
            .paypal-button {
                background: #0070ba;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 20px;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.3s;
                width: 100%;
                max-width: 300px;
            }
            .paypal-button:hover:not(:disabled) {
                background: #005ea6;
            }
            .paypal-button:disabled {
                background: #ccc;
                cursor: not-allowed;
            }
            .paypal-loading {
                text-align: center;
                color: #666;
            }
        `;
        document.head.appendChild(style);
        
        document.getElementById('paypal-button-container').appendChild(paypalButton);
        
        // Add event listener to the button
        document.getElementById('paypal-pay-button').addEventListener('click', () => {
            this.handlePayPalPayment();
        });
        
        // Update amount display when payment amount changes
        this.updateAmountDisplay();
    }
    
    /**
     * Update amount display based on current payment amount
     */
    updateAmountDisplay() {
        // Try to find amount input field
        const amountInput = document.querySelector('#payment-amount') || 
                          document.querySelector('[name="amount"]') || 
                          document.querySelector('.amount-input');
        
        if (amountInput) {
            const updateDisplay = () => {
                const cnyAmount = parseFloat(amountInput.value) || 0;
                const usdAmount = (cnyAmount / this.config.exchangeRate).toFixed(2);
                
                document.querySelector('.cny-amount').textContent = `¥${cnyAmount.toFixed(2)}`;
                document.querySelector('.usd-amount').textContent = `$${usdAmount}`;
                
                // Enable/disable button based on amount
                const button = document.getElementById('paypal-pay-button');
                button.disabled = cnyAmount <= 0;
            };
            
            amountInput.addEventListener('input', updateDisplay);
            amountInput.addEventListener('change', updateDisplay);
            updateDisplay();
        }
    }
    
    /**
     * Handle PayPal payment process
     */
    async handlePayPalPayment() {
        try {
            // Get payment amount
            const amount = this.getPaymentAmount();
            if (!amount || amount <= 0) {
                alert('请输入有效的支付金额');
                return;
            }
            
            // Generate order ID
            const orderId = this.generateOrderId();
            
            // Show loading
            this.showLoading(true);
            
            // Create order via API
            const orderData = {
                type: 'paypal',
                amount: amount,
                order_id: orderId,
                description: 'yuempypay Payment',
                cancel_url: window.location.href
            };
            
            const response = await this.createOrder(orderData);
            
            if (response.success) {
                // Redirect to PayPal for approval
                window.location.href = response.data.approval_url;
            } else {
                throw new Error(response.error || 'Failed to create order');
            }
            
        } catch (error) {
            console.error('PayPal payment error:', error);
            alert('创建PayPal订单失败: ' + error.message);
            this.showLoading(false);
        }
    }
    
    /**
     * Get current payment amount
     */
    getPaymentAmount() {
        const amountInput = document.querySelector('#payment-amount') || 
                          document.querySelector('[name="amount"]') || 
                          document.querySelector('.amount-input');
        
        return amountInput ? parseFloat(amountInput.value) : 0;
    }
    
    /**
     * Generate unique order ID
     */
    generateOrderId() {
        const timestamp = Date.now();
        const random = Math.floor(Math.random() * 1000);
        return `paypal_${timestamp}_${random}`;
    }
    
    /**
     * Create order via API
     */
    async createOrder(orderData) {
        const response = await fetch(this.config.apiEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(orderData)
        });
        
        return await response.json();
    }
    
    /**
     * Show/hide loading state
     */
    showLoading(show) {
        const button = document.getElementById('paypal-pay-button');
        const loading = document.querySelector('.paypal-loading');
        
        if (show) {
            button.style.display = 'none';
            loading.style.display = 'block';
        } else {
            button.style.display = 'block';
            loading.style.display = 'none';
        }
    }
}

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize PayPal payment with configuration
    const paypalConfig = window.paypalConfig || {
        exchangeRate: 7.3,
        apiEndpoint: '/api/create_order'
    };
    
    new PayPalPayment(paypalConfig);
});

// Export for manual initialization if needed
window.PayPalPayment = PayPalPayment;