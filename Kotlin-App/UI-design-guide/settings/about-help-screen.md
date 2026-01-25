# About/Help Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← About & Help                         │
├─────────────────────────────────────────┤
│                                         │
│         [App Icon]                      │
│                                         │
│    Board Game Stat Tracker              │
│    Version 1.0.0                        │
│                                         │
│  Help                                   │
│  ┌─────────────────────────────────┐  │
│  │ Getting Started Guide     [>]    │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ FAQ                      [>]    │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ Contact Support           [>]    │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Legal                                  │
│  ┌─────────────────────────────────┐  │
│  │ Terms of Service          [>]    │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ Privacy Policy            [>]    │  │
│  └─────────────────────────────────┘  │
│                                         │
│  About                                  │
│  ┌─────────────────────────────────┐  │
│  │ Open Source Licenses      [>]    │  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 56dp
- **Title**: "About & Help" (20sp Roboto Medium)
- **Back Button**: 24dp

### App Icon
- **Size**: 80dp x 80dp
- **Position**: Centered, 24dp below app bar

### App Name
- **Text**: "Board Game Stat Tracker" (20sp Roboto Medium)
- **Position**: 16dp below icon
- **Alignment**: Centered

### Version
- **Text**: "Version X.X.X" (16sp Roboto Regular, secondary color)
- **Position**: 8dp below app name
- **Alignment**: Centered

### Help Section
- **Title**: "Help" (16sp Roboto Medium)
- **Position**: 24dp below version

### Help Item
- **Type**: List Item (Standard)
- **Height**: 56dp
- **Padding**: 16dp horizontal
- **Content**:
  - Title (16sp Roboto Medium)
  - Chevron icon (24dp) on right
- **Spacing**: 1dp divider between items

### Legal Section
- **Title**: "Legal" (16sp Roboto Medium)
- **Position**: 24dp below help section

### Legal Item
- **Type**: List Item (Standard)
- **Height**: 56dp
- **Padding**: 16dp horizontal
- **Content**:
  - Title (16sp Roboto Medium)
  - Chevron icon (24dp) on right
- **Spacing**: 1dp divider between items

### About Section
- **Title**: "About" (16sp Roboto Medium)
- **Position**: 24dp below legal section

### About Item
- **Type**: List Item (Standard)
- **Height**: 56dp
- **Padding**: 16dp horizontal
- **Content**:
  - Title (16sp Roboto Medium)
  - Chevron icon (24dp) on right
- **Spacing**: 1dp divider between items

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Icon**: 24dp below app bar
- **Section Spacing**: 24dp vertical between sections
- **Item Spacing**: 1dp divider between items

---

## States & Interactions

### Default State
- App info displayed
- All help and legal items shown
- All items enabled

---

## Interactions

- **Tap Help Item**: Navigate to help content (in-app or web)
- **Tap Legal Item**: Navigate to legal document (web)
- **Tap About Item**: Navigate to licenses (in-app or web)

---

## Accessibility

- **Screen Reader**: "About and help. [App name], version [number]. [Item name]."
- **Touch Targets**: All items minimum 56dp height (exceeds 48dp requirement)
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on all items

---

## Navigation

- **Back Button**: → Settings Main Screen
- **Help Items**: → Help content (in-app screens or web)
- **Legal Items**: → Legal documents (web)
- **About Items**: → License information (in-app or web)

---

**Wireframe Description Complete**
