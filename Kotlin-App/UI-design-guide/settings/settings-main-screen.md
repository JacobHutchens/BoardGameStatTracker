# Settings Main Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Settings                             │
├─────────────────────────────────────────┤
│                                         │
│  Account                                │
│  ┌─────────────────────────────────┐  │
│  │ Account Settings          [>]    │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Privacy                                │
│  ┌─────────────────────────────────┐  │
│  │ Privacy Settings          [>]    │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Notifications                          │
│  ┌─────────────────────────────────┐  │
│  │ Notification Settings      [>]    │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Preferences                            │
│  ┌─────────────────────────────────┐  │
│  │ App Preferences           [>]    │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Data                                   │
│  ┌─────────────────────────────────┐  │
│  │ Export Stats               [>]    │  │
│  └─────────────────────────────────┘  │
│                                         │
│  About                                  │
│  ┌─────────────────────────────────┐  │
│  │ Help & Support            [>]    │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ About                    [>]    │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │      Logout                      │  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 56dp
- **Title**: "Settings" (20sp Roboto Medium)
- **Back Button**: 24dp

### Settings Section
- **Title**: Section name (16sp Roboto Medium)
- **Position**: 16dp below previous section
- **Spacing**: 24dp between sections

### Settings Item
- **Type**: List Item (Standard)
- **Height**: 56dp
- **Padding**: 16dp horizontal
- **Content**:
  - Title (16sp Roboto Medium)
  - Chevron icon (24dp) on right
- **Spacing**: 1dp divider between items
- **Navigation**: → Corresponding settings screen

### Logout Button
- **Type**: Text Button (Error Color)
- **Height**: 56dp
- **Width**: Full width minus 32dp margins
- **Text**: "Logout" (14sp Roboto Medium, error color)
- **Position**: 24dp below last section, 16dp from bottom
- **Confirmation**: Shows confirmation dialog before logout

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Section Spacing**: 24dp vertical between sections
- **Item Spacing**: 1dp divider between items
- **Button Spacing**: 24dp from last section, 16dp from bottom

---

## States & Interactions

### Default State
- All settings sections displayed
- All items enabled
- Logout button visible

### Logout Confirmation State
- Confirmation dialog appears
- "Are you sure you want to logout?" (16sp Roboto Regular)
- Actions: "Cancel" or "Logout"

---

## Interactions

- **Tap Settings Item**: Navigate to corresponding settings screen
- **Tap Logout**: Show confirmation dialog
- **Back Button**: Return to previous screen

---

## Accessibility

- **Screen Reader**: "Settings. [Section name]. [Item name]."
- **Touch Targets**: All items minimum 56dp height (exceeds 48dp requirement)
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on all items

---

## Navigation

- **Back Button**: → Previous screen (Profile or Drawer)
- **Account Settings**: → Account Settings Screen
- **Privacy Settings**: → Privacy Settings Screen
- **Notification Settings**: → Notification Settings Screen
- **App Preferences**: → App Preferences Screen
- **Export Stats**: → Export Stats Screen
- **Help & Support**: → Help & Support Screen
- **About**: → About Screen
- **Logout**: Confirmation dialog, then → Login Screen

---

**Wireframe Description Complete**
