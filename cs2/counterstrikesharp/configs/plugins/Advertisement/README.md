# Advertisement System Enhancement

This document describes the enhancements made to the CS2 Advertisement system to address fullscreen display issues, add individual skip duration configuration, and implement pre-video advertisement functionality.

## New Features

### 1. Fullscreen Display Fix (全屏显示修复)

The system now includes display constraints to ensure advertisements display within video resolution ranges:

```json
"DisplaySettings": {
  "VideoResolutionConstraints": {
    "EnableConstraints": true,
    "MaxWidth": 1920,
    "MaxHeight": 1080,
    "KeepWithinBounds": true
  },
  "FullscreenFix": {
    "EnableFullscreenFix": true,
    "ScaleToFit": true,
    "CenterAlignment": true
  }
}
```

**Features:**
- Prevents advertisements from exceeding video resolution boundaries
- Automatically scales content to fit within constraints
- Centers content for better user experience
- Supports dynamic video element monitoring

### 2. Individual Skip Duration Configuration (单独跳过时长配置)

Each advertisement category now supports individual skip duration settings:

```json
"Ads": [{
  "Name": "GeneralAds",
  "Interval": 65,
  "SkipDuration": 5,
  "CanSkip": true,
  // ... messages
}]
```

**Features:**
- Per-advertisement skip duration configuration
- Skip button with countdown timer
- Text watermark overlays cannot be skipped (as requested)
- Customizable skip button appearance

### 3. Pre-Video Load Advertisement Tab (视频加载前广告选项卡)

New advertisement category specifically for pre-video loading:

```json
"PreVideoAds": {
  "Enabled": true,
  "Interval": 30,
  "SkipDuration": 3,
  "CanSkip": true,
  "LoadOnlyWhenBackendEnabled": true,
  "Messages": [
    {"Chat": "{pre_video_ad_1}"},
    {"Chat": "{pre_video_ad_2}"}
  ]
}
```

**Features:**
- Displays before video content loads
- Only loads when backend functionality is enabled
- Configurable duration and skip settings
- Automatic detection of video elements

### 4. Separate JavaScript Module (独立JS模块)

Advertisement functionality has been moved to separate JavaScript files for easier management:

- `advertisement.js` - Main advertisement management system
- `advertisement-loader.js` - Conditional loading based on backend status

**Features:**
- Modular architecture for easier maintenance
- Conditional loading based on backend enablement
- Video element monitoring and constraint application
- Skip functionality with countdown timers

## Configuration Structure

### Advertisement Categories

1. **GeneralAds** - Regular advertisements with configurable skip duration
2. **PreVideoAds** - Shown before video content loads
3. **TextWatermarkOverlay** - Cannot be skipped, used for server branding

### Display Settings

- **VideoResolutionConstraints** - Controls how ads fit within video boundaries
- **FullscreenFix** - Handles fullscreen display issues

### Language Support

All advertisement messages support multiple languages:
- CN (Chinese Simplified)
- US (English)
- TW (Chinese Traditional)
- JP (Japanese)
- KR (Korean)

## Usage

### Basic Setup

1. Configure `Advertisement.json` with desired settings
2. Include `advertisement-loader.js` in your web interface
3. The system will automatically load when backend is enabled

### Manual Control

```javascript
// Check if backend is enabled
if (window.AdvertisementLoader.checkBackendEnabled()) {
  // Initialize manually
  window.AdvertisementLoader.init();
}

// Show specific advertisement types
if (window.advertisementManager) {
  window.advertisementManager.showPreVideoAd();
  window.advertisementManager.showGeneralAd();
  window.advertisementManager.showWatermarkOverlay();
}
```

### Skip Button Customization

The skip button can be customized via CSS:

```css
#ad-skip-button {
  /* Custom styling */
  background: your-color;
  border: your-border;
  /* etc. */
}
```

## Technical Details

### Video Constraint Application

The system automatically:
- Monitors for new video elements
- Applies resolution constraints
- Ensures content stays within bounds
- Handles fullscreen scaling

### Backend Integration

- Only loads when `LoadOnlyWhenBackendEnabled` is true and backend is available
- Checks backend status before initialization
- Provides fallback behavior when backend is disabled

### Performance Considerations

- Uses MutationObserver for efficient DOM monitoring
- Lazy loading of advertisement resources
- Minimal overhead when backend is disabled
- Proper cleanup and resource management

## Migration Notes

### From Previous Version

The new configuration is backward compatible. Existing `Advertisement.json` files will continue to work, but won't have the new features until updated.

### Required Changes

1. Update `Advertisement.json` structure (optional for basic functionality)
2. Include new JavaScript files in your web interface
3. Configure backend enablement checks as needed

## Troubleshooting

### Advertisements Not Showing

1. Check if backend is enabled
2. Verify `LoadOnlyWhenBackendEnabled` setting
3. Check browser console for error messages
4. Ensure JavaScript files are properly loaded

### Skip Button Not Working

1. Verify `CanSkip` is set to `true`
2. Check if `SkipDuration` is configured properly
3. Ensure the advertisement type supports skipping

### Video Constraints Not Applied

1. Check if `EnableConstraints` is `true`
2. Verify video elements are being detected
3. Check console for constraint application messages