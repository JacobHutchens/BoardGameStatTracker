# Create Session - Select Game Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Create Session    Step 1 of 7  [❌] │
├─────────────────────────────────────────┤
│  ┌─────────────────────────────────┐  │
│  │ 🔍 Search games...              │  │
│  └─────────────────────────────────┘  │
│                                         │
│  [My Games] [All Games] [Recent]        │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Settlers of Catan            │  │
│  │    Played 15 times              │  │
│  │    Last: 2 days ago            │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Ticket to Ride               │  │
│  │    Played 12 times              │  │
│  │    Last: 1 week ago             │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Carcassonne                   │  │
│  │    Played 8 times               │  │
│  │    Last: 3 weeks ago            │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Wingspan                      │  │
│  │    Played 5 times               │  │
│  │    Last: 1 month ago            │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │    + Create New Game             │  │
│  └─────────────────────────────────┘  │
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
- **Content**: "Step 1 of 7" (14sp Roboto Medium)
- **Visual**: Progress bar with step indicators
- **Position**: Top of screen, below app bar

### Search Bar
- **Type**: Material Design 3 Search Bar
- **Height**: 56dp
- **Icon**: Search icon (24dp) on left
- **Placeholder**: "Search games..." (16sp Roboto Regular)
- **Clear Button**: X icon (24dp) when text entered
- **Padding**: 16dp horizontal

### Filter Tabs
- **Type**: Segmented Control or Filter Chips
- **Height**: 32dp
- **Options**: "My Games", "All Games", "Recent"
- **Selected**: Primary color background
- **Unselected**: Outlined, primary color text
- **Spacing**: 8dp between tabs

### Game Card
- **Type**: Material Design 3 Card (Elevated)
- **Height**: 88dp
- **Elevation**: 1dp (default), 4dp (pressed)
- **Corner Radius**: 16dp
- **Padding**: 16dp
- **Content**:
  - Game icon/emoji (32dp) on left
  - Game name (16sp Roboto Medium)
  - Play count (14sp Roboto Regular, secondary color)
  - Last played date (12sp Roboto Regular, secondary color)
- **Spacing**: 8dp vertical between cards

### Create New Game Button
- **Type**: Outlined Card or Button
- **Height**: 72dp
- **Content**: "+ Create New Game" (16sp Roboto Medium)
- **Icon**: Plus icon (24dp) on left
- **Border**: Dashed border (2dp)
- **Color**: Primary color

### Continue Button
- **Type**: Primary Action Button
- **Height**: 56dp
- **Width**: Full width minus 32dp margins
- **Text**: "Continue" (14sp Roboto Medium, white)
- **Background**: Primary brand color
- **Position**: Bottom of screen, 16dp padding
- **State**: Disabled until game selected

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Progress Indicator**: 16dp from app bar
- **Search Bar**: 16dp from progress indicator
- **Filter Tabs**: 16dp from search bar
- **Game Cards**: 8dp vertical spacing
- **Continue Button**: 16dp from last card, 16dp from bottom

---

## States & Interactions

### Default State
- Search bar empty
- "My Games" tab selected (default)
- Game list displayed
- Continue button disabled

### Search State
- Search results filtered
- Clear button visible
- Results update as user types

### Selected State
- Game card highlighted (2dp border, primary color)
- Continue button enabled
- Selected game name shown in button or header

### Empty State
- Illustration/icon (120dp)
- Title: "No games found" (20sp Roboto Medium)
- Description: "Create your first game to get started" (16sp Roboto Regular)
- Action Button: "Create New Game" (Primary button)

### Loading State
- Skeleton game cards (3-4 placeholders)
- Shimmer animation
- Search bar disabled

---

## Interactions

- **Tap Game Card**: Select game (highlighted)
- **Tap Create New Game**: Navigate to Create New Game screen
- **Tap Filter Tab**: Switch filter (My Games/All/Recent)
- **Type in Search**: Filter games in real-time
- **Tap Continue**: Proceed to next step (Session Limit Check)
- **Back Button**: Cancel session creation, return to Live Sessions

---

## Navigation

- **Back Button**: → Live Sessions List (cancels creation)
- **Create New Game**: → Create New Game Screen
- **Continue Button**: → Step 2 (Session Limit Popup, if applicable)
- **Close Button (X)**: → Cancel creation, return to Live Sessions

---

## Accessibility

- **Screen Reader**: "Create session, step 1 of 7. Select game. [Game name]. Played [number] times."
- **Touch Targets**: All cards minimum 88dp height (exceeds 48dp requirement)
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on selected game card

---

**Wireframe Description Complete**
