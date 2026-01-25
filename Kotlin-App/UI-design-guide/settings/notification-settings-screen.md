# Notification Settings Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Notification Settings                │
├─────────────────────────────────────────┤
│                                         │
│  Push Notifications                    │
│  ┌─────────────────────────────────┐  │
│  │ Enable Push Notifications        │  │
│  │                           [Toggle]│  │
│  └─────────────────────────────────┘  │
│                                         │
│  Live Session Notifications             │
│  ┌─────────────────────────────────┐  │
│  │ Stat updates in live sessions    │  │
│  │                           [Toggle]│  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ Session invitations              │  │
│  │                           [Toggle]│  │
│  └─────────────────────────────────┘  │
│                                         │
│  Social Notifications                   │
│  ┌─────────────────────────────────┐  │
│  │ New followers                    │  │
│  │                           [Toggle]│  │
│  └─────────────────────────────────┘  │
│                                         │
│  Email Notifications                    │
│  ┌─────────────────────────────────┐  │
│  │ Weekly stats summary             │  │
│  │                           [Toggle]│  │
│  └─────────────────────────────────┘  │
│                                         │
│  Notification Preferences               │
│  ┌─────────────────────────────────┐  │
│  │ Sound                            │  │
│  │                           [Toggle]│  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ Vibration                        │  │
│  │                           [Toggle]│  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 56dp
- **Title**: "Notification Settings" (20sp Roboto Medium)
- **Back Button**: 24dp

### Settings Section
- **Title**: Section name (16sp Roboto Medium)
- **Position**: 16dp below previous section
- **Spacing**: 24dp between sections

### Notification Item
- **Type**: List Item (Standard or Two-Line)
- **Height**: 56dp
- **Padding**: 16dp horizontal
- **Content**:
  - Title (16sp Roboto Medium)
  - Subtitle (14sp Roboto Regular, secondary color) if applicable
  - Toggle switch (40dp track width) on right
- **Spacing**: 1dp divider between items
- **Toggle States**: ON (enabled), OFF (disabled)

### Master Toggle
- **Type**: List Item (Standard)
- **Height**: 56dp
- **Content**: "Enable Push Notifications" (16sp Roboto Medium)
- **Toggle**: Large toggle switch
- **Behavior**: When OFF, all push notification toggles disabled
- **Position**: Top of screen, 16dp below app bar

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Section Spacing**: 24dp vertical between sections
- **Item Spacing**: 1dp divider between items

---

## States & Interactions

### Default State
- All notification toggles shown
- Master toggle enabled
- Individual toggles enabled

### Master Toggle OFF State
- All push notification toggles disabled
- Visual indication (grayed out)
- Message: "Enable push notifications to configure individual settings"

### Toggle State
- Notification preference updates immediately
- Visual feedback (toggle animation)
- Save automatically (no save button needed)

---

## Interactions

- **Toggle Master Switch**: Enable/disable all push notifications
- **Toggle Individual Setting**: Enable/disable specific notification type
- **Back Button**: Return to Settings Main Screen

---

## Accessibility

- **Screen Reader**: "Notification settings. Enable push notifications, toggle. [Setting name], toggle."
- **Touch Targets**: All items minimum 56dp height (exceeds 48dp requirement)
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on all toggles

---

## Navigation

- **Back Button**: → Settings Main Screen

---

**Wireframe Description Complete**
