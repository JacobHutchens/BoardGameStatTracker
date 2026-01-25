# Stat Recording Modal Wireframe
## Board Game Stat Tracker

---

## Screen Layout (Bottom Sheet)

```
┌─────────────────────────────────────────┐
│            ═══                          │
│                                         │
│  Record Stat                            │
│  [Offline Indicator]                   │
├─────────────────────────────────────────┤
│                                         │
│  Select Stat                            │
│  ┌─────────────────────────────────┐  │
│  │ Points                    [▼]   │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Enter Value                            │
│  ┌─────────────────────────────────┐  │
│  │ 10                               │  │
│  │ ──────────────────────────────── │  │
│  │ Hint: Enter integer 0-100        │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Select Player                          │
│  ┌─────────────────────────────────┐  │
│  │ ○ Alice                            │  │
│  │ ● Bob                              │  │
│  │ ○ Charlie                          │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Round Number (Optional)                │
│  ┌─────────────────────────────────┐  │
│  │ 3                                │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌──────────────┐  ┌──────────────┐  │
│  │   Cancel     │  │    Record    │  │
│  └──────────────┘  └──────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### Drag Handle
- **Height**: 4dp
- **Width**: 40dp
- **Position**: Top center
- **Color**: Secondary color (60% opacity)
- **Corner Radius**: 2dp

### Modal Header
- **Height**: 56dp
- **Title**: "Record Stat" (20sp Roboto Medium)
- **Offline Indicator**: Badge (if offline)
- **Padding**: 16dp horizontal, 12dp vertical

### Stat Selector
- **Type**: Material Design 3 Outlined Menu
- **Height**: 56dp
- **Padding**: 16dp horizontal
- **Dropdown Icon**: 24dp on right
- **Selected Value**: Displayed prominently
- **Options**: List from configured stat set

### Value Input
- **Type**: Material Design 3 Outlined Text Field
- **Height**: 56dp
- **Label**: "Enter Value" (floating)
- **Input Type**: Based on stat data type
  - Integer: Numeric keypad
  - Float: Decimal numeric keypad
  - String: Text input
  - Boolean: Toggle switch
- **Helper Text**: Validation hint (e.g., "Enter integer 0-100")
- **Error State**: Red border, error icon, error message

### Player Selector
- **Type**: Radio Button Group
- **Layout**: Vertical list
- **Item Height**: 48dp
- **Radio Button**: 20dp diameter
- **Player Name**: 16sp Roboto Regular
- **Spacing**: 8dp between items
- **Note**: Only shown if stat scope is "player"

### Table Scope Toggle
- **Type**: Switch (if stat scope is "table")
- **Label**: "Apply to all players"
- **Track Width**: 40dp
- **Thumb Size**: 20dp

### Round Number Input
- **Type**: Material Design 3 Outlined Text Field
- **Height**: 56dp
- **Label**: "Round Number (Optional)"
- **Input Type**: Numeric
- **Placeholder**: "Enter round number"

### Action Buttons
- **Cancel**: Secondary Action Button (48dp height)
- **Record**: Primary Action Button (56dp height)
- **Layout**: Side by side, equal width
- **Spacing**: 8dp between buttons
- **Position**: Bottom of modal, 16dp padding

---

## Spacing & Layout

- **Modal Padding**: 16dp horizontal, 24dp vertical
- **Component Spacing**: 16dp vertical between fields
- **Button Spacing**: 8dp horizontal between buttons
- **Max Height**: 90% of screen height
- **Corner Radius**: 16dp (top corners)

---

## States & Interactions

### Default State
- Stat selector shows first stat or last used
- Value input empty
- Player selected (if applicable)
- Record button enabled

### Focused State
- Input field shows focused border
- Keyboard appears (if applicable)
- Helper text visible

### Error State
- Red border on input
- Error icon (24dp) on right
- Error message below input
- Record button disabled
- Example: "Value must be between 0-100"

### Offline State
- Offline indicator badge in header
- Warning message: "You are currently offline"
- Record button disabled
- Value input disabled

### Loading State
- Record button shows spinner
- Button text: "Recording..."
- All inputs disabled
- Cancel button still enabled

### Success State
- Brief success animation
- Modal closes
- Toast confirmation: "Stat recorded"
- All screens update in real-time

---

## Input Type Variations

### Integer Input
- Numeric keypad
- Min/max validation
- Increment/decrement buttons (optional)

### Float Input
- Decimal numeric keypad
- Decimal point support
- Precision validation

### String Input
- Text keyboard
- Character limit (if applicable)
- Multi-line support (if applicable)

### Boolean Input
- Toggle switch
- Labels: "Yes/No" or "True/False"
- Default: False

---

## Accessibility

- **Screen Reader**: "Record stat modal. Stat selector. Value input. Player selector."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: All text meets WCAG AA
- **Focus Management**: Logical tab order
- **Keyboard Navigation**: Full keyboard support

---

## Navigation

- **Cancel Button**: Closes modal, returns to Live Session Room
- **Record Button**: Records stat, closes modal, updates all screens
- **Back Gesture**: Swipe down or tap outside (if enabled)

---

## Quick Record Shortcuts

- **Swipe on Player Card**: Opens modal with most recent stat and player pre-selected
- **Long-press on Stat**: Opens modal with stat and last used value/player pre-selected
- **Quick Action Button**: Opens modal with specific stat pre-selected

---

**Wireframe Description Complete**
