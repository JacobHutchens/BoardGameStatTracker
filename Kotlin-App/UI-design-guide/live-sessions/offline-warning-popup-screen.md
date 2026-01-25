# Offline Warning Popup Wireframe
## Board Game Stat Tracker

---

## Screen Layout (Modal Overlay)

```
┌─────────────────────────────────────────┐
│                                         │
│              ┌─────────────────────┐   │
│              │ ⚠️ Offline          │   │
│              │                     │   │
│              │ You are currently   │   │
│              │ offline. Live       │   │
│              │ session features    │   │
│              │ require an internet │   │
│              │ connection.         │   │
│              │                     │   │
│              │ [Connection Status] │   │
│              │                     │   │
│              │      [OK]           │   │
│              └─────────────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### Modal Dialog
- **Type**: Material Design 3 Alert Dialog
- **Width**: 280dp minimum, 320dp preferred
- **Corner Radius**: 28dp (top corners)
- **Padding**: 24dp
- **Background**: Surface color
- **Elevation**: 24dp
- **Position**: Centered on screen

### Warning Icon
- **Size**: 48dp x 48dp
- **Icon**: Warning icon (⚠️)
- **Color**: Warning color (orange #FF9800)
- **Position**: Top center of modal, 24dp padding

### Title
- **Text**: "Offline" (20sp Roboto Medium)
- **Position**: 16dp below icon
- **Alignment**: Centered

### Message
- **Text**: "You are currently offline. Live session features require an internet connection." (16sp Roboto Regular)
- **Position**: 16dp below title
- **Alignment**: Left-aligned
- **Max Width**: 280dp
- **Line Height**: 24dp

### Connection Status Indicator
- **Type**: Status badge
- **Height**: 24dp
- **Background**: Warning color (orange) at 20% opacity
- **Border**: 1dp solid warning color
- **Corner Radius**: 12dp
- **Padding**: 8dp horizontal, 4dp vertical
- **Content**: "No Connection" (12sp Roboto Medium)
- **Icon**: Offline icon (16dp) on left
- **Position**: 16dp below message
- **Alignment**: Centered

### OK Button
- **Type**: Primary Action Button
- **Height**: 48dp
- **Width**: Full width minus 48dp margins
- **Text**: "OK" (14sp Roboto Medium, white)
- **Background**: Primary brand color
- **Corner Radius**: 12dp
- **Position**: 24dp below connection status
- **Alignment**: Centered

---

## Spacing & Layout

- **Modal Padding**: 24dp on all sides
- **Icon Spacing**: 24dp from top
- **Element Spacing**: 16dp vertical between elements
- **Button Spacing**: 24dp from connection status

---

## States & Interactions

### Default State
- Modal appears centered
- Warning icon visible
- Connection status shows "No Connection"
- OK button enabled

### Connection Restored State
- Connection status updates to "Connected" (green)
- Modal can be dismissed
- User can proceed with action

### Button Interaction
- **OK Button**: Dismisses modal, returns to Live Session Room (read-only mode)

---

## Accessibility

- **Screen Reader**: "Offline warning. You are currently offline. Live session features require an internet connection. OK button."
- **Touch Targets**: OK button minimum 48dp height
- **Color Contrast**: All text meets WCAG AA
- **Focus Management**: Focus trapped in modal, returns on dismiss

---

## Navigation

- **OK Button**: Dismisses modal, returns to Live Session Room
- **Backdrop Tap**: Dismisses modal (optional)
- **Back Button**: Dismisses modal

---

## Trigger Scenarios

1. **When Stat Recording Modal Opens**: Check offline status, show warning if offline
2. **When Trying to Record Stat**: Show warning if offline
3. **When Connection Lost During Session**: Show warning, disable recording

---

**Wireframe Description Complete**
