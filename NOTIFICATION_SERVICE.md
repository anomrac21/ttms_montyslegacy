# Notification Service Configuration

This template includes built-in support for the TTMenus Notification Service.

## Configuration

The notification service is configured in `hugo.toml`:

```toml
[params.notifications]
  enabled = true
  apiUrl = "https://notify.ttmenus.com/api/v1"
  websocketUrl = "wss://notify.ttmenus.com/api/v1/ws/connect"
```

## What's Included

The notification service integration is provided by the `_menus_ttms` theme (git submodule), which includes:

- **Notification Client JavaScript** - Handles subscriptions, WebSocket connections, and notification display
- **Notification UI** - Beautiful notification display with animations
- **Auto-Subscription** - Automatically subscribes authenticated users
- **Real-Time Delivery** - WebSocket connection for instant notifications

## Setup Requirements

### 1. Client Registration

Before notifications will work, the client must be registered with the notification service. This can be done:

- **Automatically** - If your CPS (Client Provisioning Service) handles this
- **Manually** - Register the client using the notification service API:

```bash
curl -X POST https://notify.ttmenus.com/api/v1/clients/register \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "{{CLIENT_NAME}}.ttmenus.com",
    "client_name": "{{SITE_TITLE}}",
    "service_group": "ttmenus",
    "auth_client_id": "ttms_{{CLIENT_NAME}}"
  }'
```

### 2. Auth Service Integration

Notifications require the auth service to be enabled and configured. The template includes this by default:

```toml
[params.auth]
  enabled = true
  apiUrl = "https://auth.ttmenus.com/api/v1"
```

## How It Works

1. **User Authentication** - User logs in via auth service
2. **Auto-Subscription** - Notification client automatically subscribes the user
3. **WebSocket Connection** - Real-time connection established
4. **Notification Delivery** - Notifications received and displayed automatically

## Features

- ✅ Auto-subscription for authenticated users
- ✅ Real-time WebSocket notifications
- ✅ Beautiful notification UI
- ✅ Support for all notification types (menu_update, promotion, order, system, general)
- ✅ Priority-based styling (urgent, high, normal, low)
- ✅ Mobile responsive
- ✅ Auto-reconnect on connection loss

## Notification Types

- `menu_update` - Menu changes
- `promotion` - Promotions and offers
- `order` - Order updates
- `system` - System announcements
- `general` - General notifications

## Disabling Notifications

To disable notifications for a specific client, set in their `hugo.toml`:

```toml
[params.notifications]
  enabled = false
```

Or remove the section entirely.

## Customization

Notification styling and behavior can be customized in the theme:
- CSS: `themes/_menus_ttms/static/css/notifications.css`
- JavaScript: `themes/_menus_ttms/static/js/notify-client.js`

## Documentation

For detailed integration documentation, see:
- Theme documentation: `themes/_menus_ttms/NOTIFICATION_INTEGRATION.md`
- Notification service: See notify-service repository

