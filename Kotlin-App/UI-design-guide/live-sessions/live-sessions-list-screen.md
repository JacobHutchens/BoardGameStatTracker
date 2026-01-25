# Live Sessions List Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  Live Sessions       2/2 this week [⚙️] │
├─────────────────────────────────────────┤
│                                         │
│  Active Sessions                        │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Settlers of Catan            │  │
│  │    3 players • Round 3          │  │
│  │    Started 2 hours ago          │  │
│  │    [Tap to join]                │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Ticket to Ride               │  │
│  │    4 players • Round 5          │  │
│  │    Started 30 minutes ago        │  │
│  │    [Tap to join]                │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │      + Create New Session       │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │      Join Session                │  │
│  │      [Enter session key]          │  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 56dp
- **Title**: "Live Sessions" (20sp Roboto Medium)
- **Session Limit**: "2/2 this week" (14sp Roboto Regular, secondary color)
- **Action**: Settings icon (24dp)

### Active Sessions Section
- **Title**: "Active Sessions" (16sp Roboto Medium)
- **Position**: Top, 16dp below app bar
- **Visibility**: Only shown if user has active sessions

### Active Session Card
- **Type**: Material Design 3 Card (Elevated)
- **Elevation**: 2dp (default), 4dp (pressed)
- **Corner Radius**: 16dp
- **Padding**: 16dp
- **Content**:
  - Game icon/emoji (32dp) on left
  - Game name (16sp Roboto Medium)
  - Player count and round (14sp Roboto Regular, secondary color)
  - Time started (12sp Roboto Regular, secondary color)
  - "Tap to join" hint (12sp Roboto Regular, primary color)
- **Spacing**: 8dp vertical between cards
- **States**: Default, Pressed, Active (highlighted border)

### Create New Session Button
- **Type**: Primary Action Button (Full Width)
- **Height**: 56dp
- **Text**: "+ Create New Session" (14sp Roboto Medium, white)
- **Background**: Primary brand color
- **Corner Radius**: 12dp
- **Icon**: Plus icon (24dp) on left
- **Position**: 24dp below active sessions section
- **States**: Default, Pressed, Disabled (if at session limit)

### Join Session Button
- **Type**: Outlined Button (Full Width)
- **Height**: 56dp
- **Text**: "Join Session" (14sp Roboto Medium, primary color)
- **Border**: 1dp solid primary color
- **Position**: 16dp below create button
- **Navigation**: → Join Session Screen

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Section Spacing**: 24dp vertical between sections
- **Card Spacing**: 8dp vertical between cards
- **Button Spacing**: 16dp vertical between buttons
- **Content Padding**: 16dp from screen edges

---

## States & Interactions

### Default State
- Active sessions list displayed (if any)
- Create and Join buttons visible
- Session limit shown in header

### Empty State (No Active Sessions)
- Active Sessions section hidden or shows "No active sessions"
- Create and Join buttons still visible
- Empty state message optional

### Loading State
- Skeleton session cards (2-3 placeholders)
- Shimmer animation
- Buttons disabled

### At Session Limit State
- Session limit highlighted in header (orange or warning color)
- Create button shows tooltip or disabled state
- Upgrade prompt available

### Pull-to-Refresh State
- Circular progress indicator at top
- Content refreshes
- Active sessions list updates

---

## Interactions

- **Tap Active Session Card**: → Live Session Room
- **Tap Create New Session**: → Create Session Flow (Step 1)
- **Tap Join Session**: → Join Session Screen
- **Pull to Refresh**: Refresh active sessions list
- **Long-press Session Card**: Context menu (leave session, view details)

---

## Accessibility

- **Screen Reader**: "Live sessions. Active sessions: [count]. [Game name], [player count] players, round [number]."
- **Touch Targets**: All cards and buttons minimum 48dp height
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on all interactive elements

---

## Navigation

- **Settings Icon**: → Settings Main Screen
- **Active Session Card**: → Live Session Room
- **Create New Session Button**: → Create Session Flow (Select Game)
- **Join Session Button**: → Join Session Screen

---

**Wireframe Description Complete**
