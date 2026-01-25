# Create Stat Set Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Create Stat Set          [Save] [❌] │
├─────────────────────────────────────────┤
│                                         │
│    ┌─────────────────────────────┐    │
│    │ Stat Set Name                │    │
│    │ ──────────────────────────── │    │
│    └─────────────────────────────┘    │
│                                         │
│  Stats                                  │
│  ┌─────────────────────────────────┐  │
│  │ Points                           │  │
│  │ Description: Player's score      │  │
│  │ Type: Integer  Scope: Player    │  │
│  │                          [✕]    │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ Resources                        │  │
│  │ Description: Resource count      │  │
│  │ Type: Integer  Scope: Player    │  │
│  │                          [✕]    │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │      + Add Stat                  │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │      Preview                     │  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 56dp
- **Title**: "Create Stat Set" (20sp Roboto Medium)
- **Actions**: Save button (14sp Roboto Medium, primary color), Close button (24dp)

### Stat Set Name Input
- **Type**: Material Design 3 Outlined Text Field
- **Height**: 56dp
- **Label**: Floating label "Stat Set Name"
- **Text**: 16sp Roboto Regular
- **Placeholder**: "Enter stat set name"
- **Validation**: Required, min 1 character, max 45 characters, unique name
- **Position**: 16dp below app bar

### Stats Section
- **Title**: "Stats" (18sp Roboto Medium)
- **Position**: 24dp below name input

### Stat Item Card
- **Type**: Material Design 3 Card (Outlined)
- **Border**: 1dp solid (divider color)
- **Corner Radius**: 12dp
- **Padding**: 16dp
- **Content**:
  - Stat name (16sp Roboto Medium)
  - Description (14sp Roboto Regular, secondary color)
  - Type and Scope (14sp Roboto Regular, secondary color)
  - Remove button (X icon, 24dp) on right
- **Spacing**: 8dp vertical between cards

### Add Stat Button
- **Type**: Outlined Button
- **Height**: 48dp
- **Width**: Full width minus 32dp margins
- **Text**: "+ Add Stat" (14sp Roboto Medium, primary color)
- **Border**: 1dp solid primary color
- **Icon**: Plus icon (18dp) on left
- **Position**: 16dp below stats list
- **Navigation**: → Add Stat Modal/Dialog

### Preview Button
- **Type**: Text Button
- **Height**: 40dp
- **Text**: "Preview" (14sp Roboto Medium, primary color)
- **Position**: 16dp below add stat button
- **Navigation**: → Stat Set Preview (modal)

### Save Button (App Bar)
- **Type**: Text Button
- **Text**: "Save" (14sp Roboto Medium, primary color)
- **Position**: App bar, right side
- **State**: Disabled until at least one stat added and name entered

---

## Add Stat Modal/Dialog

### Layout
```
┌─────────────────────────────────────────┐
│            ═══                          │
│                                         │
│  Add Stat                               │
├─────────────────────────────────────────┤
│                                         │
│  Stat Name                              │
│  ┌─────────────────────────────────┐  │
│  │ Points                           │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Description                            │
│  ┌─────────────────────────────────┐  │
│  │ Player's score                   │  │
│  │ (Multi-line)                     │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Data Type                              │
│  ┌─────────────────────────────────┐  │
│  │ Integer                  [▼]   │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Scope                                  │
│  ┌─────────────────────────────────┐  │
│  │ Player                   [▼]   │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌──────────┐  ┌──────────┐            │
│  │  Cancel  │  │   Add    │            │
│  └──────────┘  └──────────┘            │
│                                         │
└─────────────────────────────────────────┘
```

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Input Spacing**: 16dp vertical between inputs
- **Section Spacing**: 24dp vertical between sections
- **Card Spacing**: 8dp vertical between stat cards
- **Button Spacing**: 16dp from last stat card

---

## States & Interactions

### Default State
- Stat set name empty
- No stats added
- Save button disabled
- Add Stat button enabled

### Stat Added State
- Stat appears in list
- Save button enabled (if name entered)
- Can add more stats

### Validation States
- **Name Required**: "Stat set name is required"
- **Name Too Long**: "Stat set name must be 45 characters or less"
- **At Least One Stat**: "Add at least one stat to the set"
- **Duplicate Stat Name**: "Stat name already used in this set"

### Loading State
- Save button shows loading spinner
- All inputs disabled
- No interaction possible

### Success State
- Brief success animation
- Navigate to Stat Set Details or Game Details

---

## Interactions

- **Type Stat Set Name**: Real-time validation
- **Tap Add Stat**: Open Add Stat modal
- **Tap Remove (X)**: Remove stat from list
- **Tap Preview**: Show stat set preview
- **Tap Save**: Save stat set, navigate back
- **Back Button**: Cancel creation, return to previous screen

---

## Accessibility

- **Screen Reader**: "Create stat set. Stat set name input. Stats: [list]. Add stat button."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on all inputs

---

## Navigation

- **Back Button**: → Previous screen (Game Details or Create Session)
- **Save Button**: → Stat Set Details or Game Details
- **Close Button (X)**: → Cancel creation, return to previous screen
- **Add Stat Button**: → Add Stat Modal
- **Preview Button**: → Stat Set Preview (modal)

---

**Wireframe Description Complete**
