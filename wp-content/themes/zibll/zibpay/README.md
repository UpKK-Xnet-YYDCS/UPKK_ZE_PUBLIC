# PayPal yuempypay Integration

This module adds PayPal payment support to the yuempypay system in the Zibll WordPress theme.

## Features

- **Configurable Exchange Rate**: Set custom CNY to USD exchange rate (default: 7.3 = 1 USD)
- **API Endpoint**: `/api/create_order` with PayPal support (`type: "paypal"`)
- **PayPal Payment Button**: Automatically integrated PayPal payment interface
- **Order Redirection**: After payment approval, redirects to yuempypay's `/pay/{order_number}`
- **WordPress Integration**: Full WordPress admin panel integration

## Files

- `config.php` - Configuration file for PayPal settings and exchange rates
- `paypal-gateway.php` - PayPal API integration class
- `api.php` - REST API endpoint handler
- `paypal-button.js` - Frontend JavaScript for PayPal button
- `functions.php` - WordPress integration functions
- `README.md` - This documentation

## Installation

1. Copy all files to `/wp-content/themes/zibll/zibpay/`
2. Configure PayPal credentials in WordPress admin: **Settings > PayPal yuempypay**
3. Include the PayPal functions in your theme:

```php
<?php
// In your theme's functions.php
require_once(get_template_directory() . '/zibpay/functions.php');
?>
```

## Usage

### Display Payment Button

```php
<?php
// Display PayPal payment button with amount
YuempypayPayPal::display_payment_button(100); // 100 CNY
?>
```

### API Usage

**Create PayPal Order**

```javascript
// POST /api/create_order
{
    "type": "paypal",
    "amount": 100,
    "order_id": "unique_order_id",
    "description": "Payment description",
    "cancel_url": "https://yoursite.com/cancel"
}
```

**Response**

```javascript
{
    "success": true,
    "data": {
        "order_id": "unique_order_id",
        "paypal_order_id": "paypal_generated_id",
        "approval_url": "https://paypal.com/approve/...",
        "amount_cny": 100,
        "amount_usd": 13.70,
        "exchange_rate": 7.3
    }
}
```

## Configuration

### PayPal Settings

Configure in WordPress admin or directly edit `config.php`:

```php
'paypal' => [
    'enabled' => true,
    'exchange_rate' => 7.3, // 7.3 CNY = 1 USD
    'currency' => 'USD',
    'base_currency' => 'CNY',
    'sandbox' => true, // Set to false for production
    'client_id' => 'YOUR_PAYPAL_CLIENT_ID',
    'client_secret' => 'YOUR_PAYPAL_CLIENT_SECRET',
    'api_base_url' => 'https://api.sandbox.paypal.com',
]
```

### yuempypay Settings

```php
'yuempypay' => [
    'base_url' => 'https://your-yuempypay-domain.com',
    'redirect_path' => '/pay/',
]
```

## Workflow

1. User clicks PayPal payment button
2. JavaScript validates amount and creates order via `/api/create_order`
3. PayPal order is created with converted USD amount
4. User is redirected to PayPal for approval
5. After approval, user is redirected to yuempypay: `/pay/{order_id}`

## Requirements

- PHP 7.4+
- WordPress 5.0+
- cURL extension
- PayPal Business Account
- SSL certificate (required by PayPal)

## Security Features

- WordPress nonce verification
- Input sanitization and validation
- Secure PayPal API integration
- Error handling and logging

## Support

For configuration issues, check:
1. PayPal credentials are correct
2. SSL is enabled (required by PayPal)
3. Server has cURL support
4. WordPress admin settings are saved
5. JavaScript console for frontend errors