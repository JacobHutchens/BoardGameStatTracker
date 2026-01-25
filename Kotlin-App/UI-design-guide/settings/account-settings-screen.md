# Account Settings Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Account Settings                    │
├─────────────────────────────────────────┤
│                                         │
│  Password                               │
│  ┌─────────────────────────────────┐  │
│  │ Change Password           [>]    │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Email                                  │
│  ┌─────────────────────────────────┐  │
│  │ Change Email              [>]    │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Subscription                           │
│  ┌─────────────────────────────────┐  │
│  │ Premium Subscription      [>]    │  │
│  │ Upgrade for unlimited sessions  │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Session Limits                         │
│  ┌─────────────────────────────────┐  │
│  │ Sessions This Week: 2/2          │  │
│  │ Reset: Every Monday              │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Account Actions                        │
│  ┌─────────────────────────────────┐  │
│  │ Delete Account                  │  │
│  │ (This action cannot be undone)   │  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 56dp
- **Title**: "Account Settings" (20sp Roboto Medium)
- **Back Button**: 24dp

### Settings Section
- **Title**: Section name (16sp Roboto Medium)
- **Position**: 16dp below previous section
- **Spacing**: 24dp between sections

### Settings Item
- **Type**: List Item (Standard or Two-Line)
- **Height**: 56dp (standard) or 72dp (two-line)
- **Padding**: 16dp horizontal
- **Content**:
  - Title (16sp Roboto Medium)
  - Subtitle (14sp Roboto Regular, secondary color) if applicable
  - Chevron icon (24dp) on right
- **Spacing**: 1dp divider between items

### Session Limits Card
- **Type**: Info Card
- **Background**: Secondary color at 10% opacity
- **Border**: 1dp solid secondary color
- **Corner Radius**: 8dp
- **Padding**: 16dp
- **Content**:
  - "Sessions This Week: X/Y" (16sp Roboto Medium)
  - "Reset: Every Monday" (14sp Roboto Regular, secondary color)
- **Position**: 24dp below subscription section

### Delete Account Item
- **Type**: List Item (Two-Line)
- **Height**: 72dp
- **Text Color**: Error color (red)
- **Content**:
  - "Delete Account" (16sp Roboto Medium, error color)
  - "(This action cannot be undone)" (14sp Roboto Regular, secondary color)
- **Confirmation**: Shows confirmation dialog before deletion

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Section Spacing**: 24dp vertical between sections
- **Item Spacing**: 1dp divider between items
- **Card Spacing**: 24dp from adjacent sections

---

## States & Interactions

### Default State
- All settings items displayed
- Session limits shown
- Delete account item visible

### Delete Confirmation State
- Confirmation dialog appears
- "Are you sure you want to delete your account? This action cannot be undone." (16sp Roboto Regular)
- Actions: "Cancel" or "Delete Account"

---

## Interactions

- **Tap Change Password**: Navigate to Change Password Screen
- **Tap Change Email**: Navigate to Change Email Screen
- **Tap Premium Subscription**: Navigate to Subscription Screen
- **Tap Delete Account**: Show confirmation dialog

---

## Accessibility

- **Screen Reader**: "Account settings. Change password. Change email. [Session limits]."
- **Touch Targets**: All items minimum 56dp height (exceeds 48dp requirement)
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on all items

---

## Navigation

- **Back Button**: → Settings Main Screen
- **Change Password**: → Change Password Screen
- **Change Email**: → Change Email Screen
- **Premium Subscription**: → Subscription Screen
- **Delete Account**: Confirmation dialog, then → Login Screen (if confirmed)

---

**Wireframe Description Complete**
