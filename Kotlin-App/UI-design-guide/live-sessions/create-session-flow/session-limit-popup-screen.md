# Create Session - Session Limit Popup Wireframe
## Board Game Stat Tracker

---

## Screen Layout (Modal Overlay)

```
┌─────────────────────────────────────────┐
│                                         │
│              ┌─────────────────────┐   │
│              │ Session Limit        │   │
│              │                     │   │
│              │ You have 2 sessions │   │
│              │ remaining this week.│   │
│              │                     │   │
│              │ [Upgrade to Premium]│   │
│              │                     │   │
│              │ [Continue] [Cancel] │   │
│              │                     │   │
│              │ ☐ Don't show again  │   │
│              └─────────────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### Modal Dialog
- **Type**: Material Design 3 Dialog
- **Width**: 280dp minimum, 320dp preferred
- **Corner Radius**: 28dp (top corners)
- **Padding**: 24dp
- **Background**: Surface color
- **Elevation**: 24dp
- **Position**: Centered on screen

### Title
- **Text**: "Session Limit" (20sp Roboto Medium)
- **Position**: Top of modal, 24dp padding
- **Alignment**: Left-aligned

### Message
- **Text**: "You have X sessions remaining this week." (16sp Roboto Regular)
- **Position**: 16dp below title
- **Alignment**: Left-aligned
- **Dynamic**: Shows actual remaining count

### Upgrade Button
- **Type**: Primary Action Button
- **Height**: 48dp
- **Width**: Full width minus 48dp margins
- **Text**: "Upgrade to Premium" (14sp Roboto Medium, white)
- **Background**: Primary brand color
- **Corner Radius**: 12dp
- **Position**: 24dp below message
- **Navigation**: → Subscription upgrade screen

### Continue Button
- **Type**: Secondary Action Button
- **Height**: 48dp
- **Width**: Full width minus 48dp margins
- **Text**: "Continue" (14sp Roboto Medium, primary color)
- **Border**: 1dp solid primary color
- **Position**: 8dp below upgrade button
- **Navigation**: → Step 3 (Invite Users)

### Cancel Button
- **Type**: Text Button
- **Height**: 40dp
- **Text**: "Cancel" (14sp Roboto Medium, primary color)
- **Position**: 8dp below continue button
- **Alignment**: Centered
- **Navigation**: → Cancel creation, return to Live Sessions

### Don't Show Again Checkbox
- **Size**: 20dp x 20dp
- **Label**: "Don't show again" (14sp Roboto Regular)
- **Position**: 16dp below cancel button
- **Visibility**: Only shown if user has seen upgrade prompt 3+ times
- **Behavior**: If checked, popup won't show again (but session limit still shown in header)

---

## Spacing & Layout

- **Modal Padding**: 24dp on all sides
- **Element Spacing**: 16dp vertical between elements
- **Button Spacing**: 8dp vertical between buttons
- **Checkbox Spacing**: 16dp from cancel button

---

## States & Interactions

### Default State
- Modal appears centered
- All buttons enabled
- Checkbox unchecked (if visible)

### First Time State
- Checkbox not visible
- Standard message displayed

### After 3+ Views State
- Checkbox visible
- User can dismiss permanently

### Button Interactions
- **Upgrade Button**: Navigate to subscription screen
- **Continue Button**: Dismiss modal, proceed to next step
- **Cancel Button**: Dismiss modal, cancel session creation
- **Checkbox**: Toggle "don't show again" preference

---

## Accessibility

- **Screen Reader**: "Session limit dialog. You have [number] sessions remaining this week."
- **Touch Targets**: All buttons minimum 48dp height
- **Color Contrast**: All text meets WCAG AA
- **Focus Management**: Focus trapped in modal, returns on dismiss

---

## Navigation

- **Upgrade Button**: → Subscription Upgrade Screen
- **Continue Button**: → Step 3 (Invite App Users)
- **Cancel Button**: → Live Sessions List (cancels creation)
- **Backdrop Tap**: Dismisses modal (optional)

---

**Wireframe Description Complete**
