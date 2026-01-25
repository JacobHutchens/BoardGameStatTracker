# Create New Game Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Create New Game                     │
├─────────────────────────────────────────┤
│                                         │
│    ┌─────────────────────────────┐    │
│    │ Game Name                    │    │
│    │ ──────────────────────────── │    │
│    └─────────────────────────────┘    │
│                                         │
│    ┌─────────────────────────────┐    │
│    │ Description                  │    │
│    │ ──────────────────────────── │    │
│    │ (Multi-line)                 │    │
│    └─────────────────────────────┘    │
│                                         │
│    ┌──────────┐  ┌──────────┐          │
│    │ Min      │  │ Max      │          │
│    │ Players  │  │ Players  │          │
│    │ [  3  ]  │  │ [  4  ]  │          │
│    └──────────┘  └──────────┘          │
│                                         │
│    ☑ Can Win                            │
│                                         │
│    ┌─────────────────────────────┐    │
│    │      CREATE GAME             │    │
│    └─────────────────────────────┘    │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### Game Name Input
- **Type**: Material Design 3 Outlined Text Field
- **Height**: 56dp
- **Label**: Floating label "Game Name"
- **Text**: 16sp Roboto Regular
- **Placeholder**: "Enter game name"
- **Validation**: Required, min 1 character, max 45 characters
- **Position**: 16dp below app bar
- **Duplicate Check**: Real-time check when user finishes typing

### Description Input
- **Type**: Material Design 3 Outlined Text Field (Multi-line)
- **Height**: 120dp (minimum, expands)
- **Label**: Floating label "Description"
- **Text**: 16sp Roboto Regular
- **Placeholder**: "Describe the game..."
- **Validation**: Required, min 10 characters
- **Max Lines**: 5-6 lines visible
- **Position**: 16dp below game name

### Min Players Input
- **Type**: Material Design 3 Outlined Text Field
- **Height**: 56dp
- **Label**: Floating label "Min Players"
- **Text**: 16sp Roboto Regular
- **Input Type**: Numeric
- **Validation**: Integer, min 1, max 20
- **Position**: 16dp below description
- **Width**: Half width minus 4dp (for spacing)

### Max Players Input
- **Type**: Material Design 3 Outlined Text Field
- **Height**: 56dp
- **Label**: Floating label "Max Players"
- **Text**: 16sp Roboto Regular
- **Input Type**: Numeric
- **Validation**: Integer, min 1, max 20, must be >= min players
- **Position**: 16dp below description, right side
- **Width**: Half width minus 4dp (for spacing)

### Can Win Toggle
- **Type**: Switch
- **Track Width**: 40dp
- **Thumb Size**: 20dp
- **Label**: "Can Win" (16sp Roboto Regular)
- **Position**: 16dp below player inputs
- **Default**: ON (checked)

### Duplicate Check Popup
- **Type**: Alert Dialog
- **Trigger**: When game name matches existing game
- **Content**:
  - Title: "Game Already Exists"
  - Message: "A game with this name already exists. Select it or create a new one?"
  - List of matching games
  - Actions: "Select Existing" or "Create New Anyway"

### Create Game Button
- **Type**: Primary Action Button
- **Height**: 56dp
- **Width**: Full width minus 32dp margins
- **Text**: "CREATE GAME" (14sp Roboto Medium, white)
- **Background**: Primary brand color
- **Corner Radius**: 12dp
- **Position**: 24dp below toggle, 16dp from bottom
- **States**: Default, Pressed, Disabled (if validation fails), Loading

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Input Spacing**: 16dp vertical between inputs
- **Player Inputs**: Side by side, 8dp spacing between
- **Toggle Spacing**: 16dp from player inputs
- **Button Spacing**: 24dp from toggle, 16dp from bottom

---

## States & Interactions

### Default State
- All inputs empty
- Can Win toggle ON
- Create Game button disabled
- No error messages

### Input State
- Fields filled
- Real-time validation
- Create Game button enabled when all valid

### Duplicate Check State
- Popup appears with matching games
- User can select existing or create new
- List shows: Game name, description preview, play count

### Error States
- **Game Name**: "Game name is required" or "Game name too long"
- **Description**: "Description must be at least 10 characters"
- **Min Players**: "Must be at least 1" or "Invalid number"
- **Max Players**: "Must be at least min players" or "Invalid number"

### Loading State
- Create Game button shows loading spinner
- Button text: "Creating..."
- All inputs disabled
- No interaction possible

### Success State
- Brief success animation
- Navigate to Game Details screen (newly created game)

---

## Interactions

- **Type Game Name**: Real-time duplicate check
- **Type Description**: Multi-line input, character count
- **Type Player Counts**: Numeric input, validation
- **Toggle Can Win**: Switch on/off
- **Tap Create Game**: Create game, navigate to details
- **Select Existing Game**: Navigate to existing game details
- **Back Button**: Cancel creation, return to Game Library

---

## Accessibility

- **Screen Reader**: "Create new game. Game name input. Description input. Min players input."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on all inputs

---

## Navigation

- **Back Button**: → Game Library Browse (cancels creation)
- **Create Game Button**: → Game Details Screen (newly created)
- **Select Existing Game**: → Game Details Screen (existing game)

---

**Wireframe Description Complete**
