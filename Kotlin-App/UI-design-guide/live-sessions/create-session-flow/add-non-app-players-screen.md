# Create Session - Add Non-App Players Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Add Players        Step 4 of 7  [❌] │
├─────────────────────────────────────────┤
│                                         │
│  Add players who don't use the app     │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ Nickname                        │  │
│  │ ──────────────────────────────── │  │
│  └─────────────────────────────┘    │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │      + Add Player               │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Non-App Players                        │
│  ┌─────────────────────────────────┐  │
│  │ 👤 "Player 1"          [✕]     │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ 👤 "Guest"             [✕]     │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ⚠️ Player count will be locked        │
│     once session starts                │
│                                         │
│              [Continue]                 │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### Progress Indicator
- **Type**: Multi-step progress indicator
- **Height**: 48dp
- **Content**: "Step 4 of 7" (14sp Roboto Medium)
- **Visual**: Progress bar with step indicators
- **Position**: Top of screen, below app bar

### Description Text
- **Text**: "Add players who don't use the app" (16sp Roboto Regular, secondary color)
- **Position**: 16dp below progress indicator
- **Alignment**: Left-aligned

### Nickname Input
- **Type**: Material Design 3 Outlined Text Field
- **Height**: 56dp
- **Label**: Floating label "Nickname"
- **Text**: 16sp Roboto Regular
- **Placeholder**: "Enter player nickname"
- **Position**: 16dp below description
- **Validation**: Required, min 1 character, max 45 characters

### Add Player Button
- **Type**: Outlined Button
- **Height**: 48dp
- **Width**: Full width minus 32dp margins
- **Text**: "+ Add Player" (14sp Roboto Medium, primary color)
- **Border**: 1dp solid primary color
- **Icon**: Plus icon (18dp) on left
- **Position**: 16dp below nickname input
- **State**: Enabled when nickname entered

### Non-App Players Section
- **Title**: "Non-App Players" (16sp Roboto Medium)
- **Position**: 24dp below add button
- **Visibility**: Only shown if players added

### Non-App Player Chip
- **Type**: Action Chip
- **Height**: 48dp
- **Content**:
  - Player icon (24dp) on left
  - Nickname (14sp Roboto Medium)
  - Remove button (X icon, 18dp) on right
- **Spacing**: 8dp vertical between chips
- **Layout**: Vertical list

### Warning Message
- **Type**: Alert/Info banner
- **Background**: Warning color (orange) at 10% opacity
- **Border**: 1dp solid warning color
- **Corner Radius**: 8dp
- **Padding**: 12dp
- **Content**:
  - Warning icon (20dp) on left
  - Text: "Player count will be locked once session starts" (14sp Roboto Regular)
- **Position**: 16dp below players list
- **Visibility**: Always visible

### Continue Button
- **Type**: Primary Action Button
- **Height**: 56dp
- **Width**: Full width minus 32dp margins
- **Text**: "Continue" (14sp Roboto Medium, white)
- **Background**: Primary brand color
- **Corner Radius**: 12dp
- **Position**: 16dp below warning, 16dp from bottom
- **State**: Always enabled (non-app players optional)

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Progress Indicator**: 16dp from app bar
- **Description**: 16dp from progress indicator
- **Input Spacing**: 16dp vertical between elements
- **Section Spacing**: 24dp vertical between sections
- **Continue Button**: 16dp from warning, 16dp from bottom

---

## States & Interactions

### Default State
- Nickname input empty
- Add Player button disabled
- No players added
- Warning message visible

### Input State
- Nickname entered
- Add Player button enabled
- Validation: Min 1 character, max 45 characters

### Players Added State
- Players appear in Non-App Players list
- Nickname input clears after adding
- Remove buttons available

### Empty State (No Players)
- Non-App Players section hidden or shows "No players added"
- Continue button still enabled
- Optional: "Skip" option

### Error State
- Invalid nickname (too long, invalid characters)
- Error message below input
- Add Player button disabled

---

## Interactions

- **Type Nickname**: Input validation in real-time
- **Tap Add Player**: Add player to list, clear input
- **Tap Remove (X)**: Remove player from list
- **Tap Continue**: Proceed to next step (Select Stat Set)
- **Back Button**: Return to previous step (Invite Users)

---

## Validation Rules

- **Nickname Required**: Must have at least 1 character
- **Max Length**: 45 characters (matches database VARCHAR(45))
- **Invalid Characters**: Prevent special characters that could cause issues
- **Duplicate Names**: Allow (players can have same nickname)

---

## Accessibility

- **Screen Reader**: "Add players, step 4 of 7. Nickname input. Add player button."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on input and buttons

---

## Navigation

- **Back Button**: → Step 3 (Invite App Users)
- **Continue Button**: → Step 5 (Select Stat Set)
- **Close Button (X)**: → Cancel creation, return to Live Sessions

---

**Wireframe Description Complete**
