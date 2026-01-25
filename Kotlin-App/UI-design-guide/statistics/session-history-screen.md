# Session History Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Session History        [🔍] [⚙️]    │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ 🔍 Search sessions...            │  │
│  └─────────────────────────────────┘  │
│                                         │
│  [All] [This Week] [This Month] [Custom] │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Settlers of Catan            │  │
│  │    Won • January 15, 2024      │  │
│  │    2 hours 15 minutes          │  │
│  │    [Swipe for actions]          │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Ticket to Ride               │  │
│  │    Lost • January 12, 2024     │  │
│  │    1 hour 45 minutes           │  │
│  │    [Swipe for actions]          │  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 56dp
- **Title**: "Session History" (20sp Roboto Medium)
- **Actions**: Search icon (24dp), Settings/Filter icon (24dp)

### Search Bar
- **Type**: Material Design 3 Search Bar
- **Height**: 56dp
- **Icon**: Search icon (24dp) on left
- **Placeholder**: "Search sessions..." (16sp Roboto Regular)
- **Clear Button**: X icon (24dp) when text entered
- **Position**: 16dp below app bar

### Time Filter Tabs
- **Type**: Segmented Control or Filter Chips
- **Height**: 40dp
- **Options**: "All", "This Week", "This Month", "Custom"
- **Selected**: Primary color background, white text
- **Unselected**: Outlined, primary color text
- **Spacing**: 8dp between tabs
- **Position**: 16dp below search bar
- **Default**: "All" selected

### Session Card
- **Type**: Material Design 3 Card (Elevated)
- **Elevation**: 1dp (default), 4dp (pressed)
- **Corner Radius**: 16dp
- **Padding**: 16dp
- **Content**:
  - Game icon/emoji (32dp) on left
  - Game name (16sp Roboto Medium)
  - Result badge (Won/Lost) (12sp Roboto Medium, badge style)
  - Date (14sp Roboto Regular, secondary color)
  - Duration (14sp Roboto Regular, secondary color)
  - Swipe hint: "[Swipe for actions]" (12sp Roboto Regular, secondary color)
- **Spacing**: 8dp vertical between cards
- **Swipe Actions**: Left swipe reveals actions (View, Export, Delete)

### Swipe Actions
- **View**: Primary color background, view icon (24dp)
- **Export**: Secondary color background, export icon (24dp)
- **Delete**: Error color background, delete icon (24dp)
- **Width**: 80dp per action
- **Reveal**: Swipe left to reveal, swipe right to hide

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Search Bar**: 16dp below app bar
- **Filter Tabs**: 16dp below search bar
- **Card Spacing**: 8dp vertical between cards
- **Content Padding**: 16dp from screen edges

---

## States & Interactions

### Default State
- All sessions listed (or filtered by time)
- Search bar empty
- "All" tab selected
- Cards show basic info

### Search State
- Search results filtered
- Clear button visible
- Results update as user types

### Filter State
- Sessions filtered by selected time period
- Custom range shows date picker

### Empty State
- Illustration/icon (120dp)
- Title: "No sessions found" (20sp Roboto Medium)
- Description: "Start playing games to see your session history" (16sp Roboto Regular)
- Action Button: "Create Session" (Primary button)

### Loading State
- Skeleton session cards (3-4 placeholders)
- Shimmer animation
- Search disabled

---

## Interactions

- **Type in Search**: Filter sessions in real-time
- **Tap Filter Tab**: Filter by time period
- **Tap Session Card**: Navigate to Session Details
- **Swipe Left on Card**: Reveal swipe actions
- **Tap Swipe Action**: Perform action (view, export, delete)
- **Pull to Refresh**: Refresh session list

---

## Swipe Actions Details

### View Action
- **Color**: Primary color
- **Icon**: Eye icon (24dp)
- **Action**: Navigate to Session Details

### Export Action
- **Color**: Secondary color
- **Icon**: Download icon (24dp)
- **Action**: Export session data as JSON

### Delete Action
- **Color**: Error color (red)
- **Icon**: Delete icon (24dp)
- **Action**: Show confirmation dialog, delete session

---

## Accessibility

- **Screen Reader**: "Session history. [Game name], [result], [date]. Swipe left for actions."
- **Touch Targets**: All cards minimum 88dp height (exceeds 48dp requirement)
- **Color Contrast**: All text meets WCAG AA
- **Swipe Alternative**: Long-press menu provides alternative to swipe

---

## Navigation

- **Back Button**: → Profile or Stats Dashboard
- **Session Card**: → Session Details
- **View Action**: → Session Details
- **Export Action**: → Export Stats Screen
- **Delete Action**: Confirmation dialog, then remove from list

---

**Wireframe Description Complete**
