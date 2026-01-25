# Create Session - Select Stat Set Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Select Stat Set   Step 5 of 7  [❌] │
├─────────────────────────────────────────┤
│                                         │
│  Choose stat set for this session      │
│                                         │
│  Stat Set                               │
│  ┌─────────────────────────────────┐  │
│  │ Standard Set            [▼]     │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Preview                                │
│  ┌─────────────────────────────────┐  │
│  │ Standard Set                     │  │
│  │ ────────────────────────────────│  │
│  │ • Points (int, player)          │  │
│  │ • Resources (int, player)        │  │
│  │ • Cities (int, player)           │  │
│  │ • Longest Road (bool, player)    │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ Create New Stat Set             │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ Create New Based On...           │  │
│  │ (Copy and modify existing)      │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ⚠️ Player count will be locked        │
│     once session starts                │
│                                         │
│         [Start Session]                 │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### Progress Indicator
- **Type**: Multi-step progress indicator
- **Height**: 48dp
- **Content**: "Step 5 of 7" (14sp Roboto Medium)
- **Visual**: Progress bar with step indicators
- **Position**: Top of screen, below app bar

### Description Text
- **Text**: "Choose stat set for this session" (16sp Roboto Regular, secondary color)
- **Position**: 16dp below progress indicator
- **Alignment**: Left-aligned

### Stat Set Dropdown
- **Type**: Material Design 3 Outlined Menu
- **Height**: 56dp
- **Label**: "Stat Set" (floating label)
- **Selected Value**: Displayed prominently (16sp Roboto Medium)
- **Dropdown Icon**: 24dp on right
- **Position**: 16dp below description
- **Options**: List of existing stat sets for selected game

### Stat Set Preview Card
- **Type**: Material Design 3 Card (Outlined)
- **Border**: 1dp solid (divider color)
- **Corner Radius**: 12dp
- **Padding**: 16dp
- **Content**:
  - Stat set name (16sp Roboto Medium)
  - List of stats:
    - Stat name (14sp Roboto Regular)
    - Data type and scope in parentheses (12sp Roboto Regular, secondary color)
- **Position**: 16dp below dropdown
- **Visibility**: Shown when stat set selected

### Create New Stat Set Button
- **Type**: Outlined Button
- **Height**: 48dp
- **Width**: Full width minus 32dp margins
- **Text**: "Create New Stat Set" (14sp Roboto Medium, primary color)
- **Border**: 1dp solid primary color
- **Position**: 16dp below preview
- **Navigation**: → Create Stat Set Screen

### Build On Existing Button
- **Type**: Outlined Button
- **Height**: 48dp
- **Width**: Full width minus 32dp margins
- **Text**: "Create New Based On..." (14sp Roboto Medium, primary color)
- **Subtext**: "(Copy and modify existing)" (12sp Roboto Regular, secondary color)
- **Border**: 1dp solid primary color
- **Position**: 8dp below create new button
- **Tooltip**: Available on long-press explaining immutability
- **Navigation**: → Build On Stat Set Screen

### Warning Message
- **Type**: Alert/Info banner
- **Background**: Warning color (orange) at 10% opacity
- **Border**: 1dp solid warning color
- **Corner Radius**: 8dp
- **Padding**: 12dp
- **Content**:
  - Warning icon (20dp) on left
  - Text: "Player count will be locked once session starts" (14sp Roboto Regular)
- **Position**: 16dp below buttons
- **Visibility**: Always visible

### Start Session Button
- **Type**: Primary Action Button
- **Height**: 56dp
- **Width**: Full width minus 32dp margins
- **Text**: "Start Session" (14sp Roboto Medium, white)
- **Background**: Primary brand color
- **Corner Radius**: 12dp
- **Position**: 16dp below warning, 16dp from bottom
- **State**: Enabled when stat set selected

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Progress Indicator**: 16dp from app bar
- **Description**: 16dp from progress indicator
- **Element Spacing**: 16dp vertical between elements
- **Section Spacing**: 24dp vertical between sections
- **Start Button**: 16dp from warning, 16dp from bottom

---

## States & Interactions

### Default State
- Stat set dropdown shows first option or "Select stat set"
- Preview card hidden or shows placeholder
- Start Session button disabled

### Stat Set Selected State
- Stat set name displayed in dropdown
- Preview card shows stat set details
- Start Session button enabled

### Empty State (No Stat Sets)
- Dropdown shows "No stat sets available"
- Preview card hidden
- Create New Stat Set button prominent
- Message: "Create your first stat set for this game"

### Loading State
- Dropdown shows loading spinner
- Preview card shows skeleton
- Buttons disabled

---

## Interactions

- **Tap Dropdown**: Open stat set selection menu
- **Select Stat Set**: Update dropdown, show preview
- **Tap Create New Stat Set**: Navigate to Create Stat Set screen
- **Tap Build On Existing**: Navigate to Build On Stat Set screen
- **Long-press Build On**: Show tooltip explaining immutability
- **Tap Start Session**: Create session, navigate to Live Session Room
- **Back Button**: Return to previous step (Add Non-App Players)

---

## Tooltip Content (Build On Existing)

**On Long-press or Info Icon**:
- **Title**: "Create New Based On Existing"
- **Content**: "This will create a new stat set with a new name based on the selected set. The original stat set will not be modified. Stat sets are immutable to preserve data integrity for filtering."

---

## Accessibility

- **Screen Reader**: "Select stat set, step 5 of 7. Stat set selector. [Selected stat set name]. [List of stats]."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on dropdown and buttons

---

## Navigation

- **Back Button**: → Step 4 (Add Non-App Players)
- **Create New Stat Set**: → Create Stat Set Screen
- **Build On Existing**: → Build On Stat Set Screen
- **Start Session Button**: → Live Session Room (session created)
- **Close Button (X)**: → Cancel creation, return to Live Sessions

---

**Wireframe Description Complete**
