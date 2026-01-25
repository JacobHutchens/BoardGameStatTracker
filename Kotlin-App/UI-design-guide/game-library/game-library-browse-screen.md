# Game Library Browse Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  Game Library        [Grid] [List] [⚙️] │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ 🔍 Search games...              │  │
│  └─────────────────────────────────┘  │
│                                         │
│  [My Games] [All Games] [Recent]        │
│                                         │
│  ┌──────────┐  ┌──────────┐           │
│  │ 🎲       │  │ 🎲       │           │
│  │ Catan    │  │ Ticket   │           │
│  │ 15 plays │  │ 12 plays │           │
│  │ 2d ago   │  │ 1w ago   │           │
│  └──────────┘  └──────────┘           │
│                                         │
│  ┌──────────┐  ┌──────────┐           │
│  │ 🎲       │  │ 🎲       │           │
│  │ Wingspan│  │ Carcass. │           │
│  │ 5 plays │  │ 8 plays  │           │
│  │ 1m ago  │  │ 3w ago   │           │
│  └──────────┘  └──────────┘           │
│                                         │
│                    [➕ Create Game]    │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 56dp
- **Title**: "Game Library" (20sp Roboto Medium)
- **Actions**: 
  - Grid/List view toggle (24dp icons)
  - Settings icon (24dp) - optional

### Search Bar
- **Type**: Material Design 3 Search Bar
- **Height**: 56dp
- **Icon**: Search icon (24dp) on left
- **Placeholder**: "Search games..." (16sp Roboto Regular)
- **Clear Button**: X icon (24dp) when text entered
- **Position**: 16dp below app bar

### Filter Tabs
- **Type**: Segmented Control or Filter Chips
- **Height**: 32dp
- **Options**: "My Games", "All Games", "Recent"
- **Selected**: Primary color background, white text
- **Unselected**: Outlined, primary color text
- **Spacing**: 8dp between tabs
- **Position**: 16dp below search bar
- **Default**: "My Games" selected

### Game Card (Grid View)
- **Type**: Material Design 3 Card (Elevated)
- **Elevation**: 1dp (default), 4dp (pressed)
- **Corner Radius**: 16dp
- **Padding**: 16dp
- **Size**: 2 columns, equal width
- **Content**:
  - Game icon/emoji (48dp) centered
  - Game name (16sp Roboto Medium, centered)
  - Play count (14sp Roboto Regular, secondary color)
  - Last played date (12sp Roboto Regular, secondary color)
- **Spacing**: 8dp between cards (horizontal and vertical)

### Game Card (List View)
- **Type**: Material Design 3 Card (Elevated)
- **Elevation**: 1dp
- **Corner Radius**: 16dp
- **Padding**: 16dp
- **Height**: 88dp
- **Content**:
  - Game icon/emoji (40dp) on left
  - Game name (16sp Roboto Medium)
  - Description preview (14sp Roboto Regular, secondary color, 1 line)
  - Play count and last played (12sp Roboto Regular, secondary color, right-aligned)
- **Spacing**: 8dp vertical between cards

### Create Game FAB
- **Type**: Floating Action Button
- **Size**: 56dp diameter
- **Icon**: Plus icon (24dp)
- **Position**: Bottom-right, 16dp from edges
- **Elevation**: 6dp (default), 8dp (pressed)
- **Color**: Primary brand color
- **Navigation**: → Create New Game Screen

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Search Bar**: 16dp below app bar
- **Filter Tabs**: 16dp below search bar
- **Game Cards**: 8dp spacing (grid or list)
- **FAB Position**: 16dp from bottom-right

---

## States & Interactions

### Default State
- "My Games" tab selected
- Game list displayed
- Grid view default
- Search bar empty

### Search State
- Search results filtered
- Clear button visible
- Results update as user types

### Filter State
- Selected tab highlighted
- Game list filtered accordingly
- "My Games": Only games user has played/created
- "All Games": All games in library
- "Recent": Games played recently (last 30 days)

### Empty State
- Illustration/icon (120dp)
- Title: "No games found" (20sp Roboto Medium)
- Description: "Create your first game to get started" (16sp Roboto Regular)
- Action Button: "Create New Game" (Primary button)

### Loading State
- Skeleton game cards (4-6 placeholders)
- Shimmer animation
- Search disabled

---

## Interactions

- **Tap Game Card**: Navigate to Game Details
- **Tap Filter Tab**: Switch filter (My Games/All/Recent)
- **Tap Grid/List Toggle**: Switch view mode
- **Type in Search**: Filter games in real-time
- **Tap Create Game FAB**: Navigate to Create New Game
- **Long-press Game Card**: Context menu (view, edit if owner, delete if owner)

---

## Accessibility

- **Screen Reader**: "Game library. [Filter tab] selected. [Game name], played [count] times."
- **Touch Targets**: All cards minimum 88dp height (exceeds 48dp requirement)
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on selected filter tab and cards

---

## Navigation

- **Game Card**: → Game Details Screen
- **Create Game FAB**: → Create New Game Screen
- **Settings Icon**: → Settings (if applicable)

---

**Wireframe Description Complete**
