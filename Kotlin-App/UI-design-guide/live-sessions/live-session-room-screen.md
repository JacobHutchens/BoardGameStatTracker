# Live Session Room Wireframe
## Board Game Stat Tracker

---

## Screen Layout (Normal Mode)

```
┌─────────────────────────────────────────┐
│  ← Settlers of Catan        [⚙️] [❌]   │
│  Round 3                    [Focus Mode]│
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ 👤 Alice              [SPECTATOR]│  │
│  │ ────────────────────────────────│  │
│  │ Points: 8                        │  │
│  │ Resources: 12                    │  │
│  │ Cities: 2                        │  │
│  │ [▼ Show All Stats]              │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ 👤 Bob                           │  │
│  │ ────────────────────────────────│  │
│  │ Points: 6                        │  │
│  │ Resources: 15                    │  │
│  │ Cities: 1                        │  │
│  │ [▼ Show All Stats]              │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ 👤 Charlie                       │  │
│  │ ────────────────────────────────│  │
│  │ Points: 10                       │  │
│  │ Resources: 8                     │  │
│  │ Cities: 3                        │  │
│  │ [▼ Show All Stats]              │  │
│  └─────────────────────────────────┘  │
│                                         │
│  [⚡ Quick: Points] [⚡ Quick: Resources]│
│                                         │
│                    [➕ Add Stat]        │
│                                         │
└─────────────────────────────────────────┘
```

---

## Screen Layout (Focus Mode)

```
┌─────────────────────────────────────────┐
│  ← Settlers of Catan        [⚙️] [❌]   │
│  Round 3              [Focus Mode: ON]   │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ At a Glance                      │  │
│  │ ────────────────────────────────│  │
│  │ Leading: Charlie (10 points)     │  │
│  │ Key Stats:                       │  │
│  │ • Points: 10                    │  │
│  │ • Resources: 8              │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ 👤 Alice              [SPECTATOR]│  │
│  │ Points: 8                        │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ 👤 Bob                           │  │
│  │ Points: 6                        │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ 👤 Charlie                       │  │
│  │ Points: 10                       │  │
│  └─────────────────────────────────┘  │
│                                         │
│  [⚡ Quick: Points] [⚡ Quick: Resources]│
│                                         │
│                    [➕ Add Stat]        │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 56dp
- **Title**: Game name (20sp Roboto Medium)
- **Subtitle**: "Round X" (14sp Roboto Regular, secondary color)
- **Actions**: Settings icon (24dp), Leave/End icon (24dp)
- **Focus Mode Toggle**: Chip or switch (32dp height)

### Player Card
- **Type**: Material Design 3 Card (Outlined)
- **Border**: 1dp solid (divider color), 2dp when active
- **Corner Radius**: 12dp
- **Padding**: 16dp
- **Content**:
  - Player name/avatar (left-aligned)
  - Spectator badge (if applicable)
  - Stats list (collapsible)
  - Expand/collapse indicator
- **States**: Default, Active (highlighted border), Spectator (badge)

### Quick Action Buttons
- **Type**: Floating Action Buttons (compact)
- **Size**: 48dp diameter
- **Icon**: 24dp
- **Position**: Above main FAB, horizontal row
- **Spacing**: 8dp between buttons
- **Usage**: Frequently used stats (e.g., "Points", "Resources")

### Add Stat Button (FAB)
- **Type**: Floating Action Button
- **Size**: 56dp diameter
- **Icon**: Plus icon (24dp)
- **Position**: Bottom-right, 16dp from edges
- **Elevation**: 6dp (default), 8dp (pressed)
- **Color**: Primary brand color

### Real-time Update Indicator
- **Type**: Pulse animation on updated values
- **Duration**: 300ms
- **Color**: Primary color at 20% opacity
- **Frequency**: When any user records a stat

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Player Card Spacing**: 16dp vertical between cards
- **Quick Actions Spacing**: 8dp horizontal between buttons
- **FAB Position**: 16dp from bottom-right corner
- **Content Padding**: 16dp from screen edges

---

## States & Interactions

### Normal State
- All stats visible (if expanded)
- All players shown
- Quick actions visible

### Focus Mode State
- Only key stats shown
- "At a Glance" summary at top
- Compact player cards
- Toggle shows "Focus Mode: ON"

### Stat Update State
- Updated stat value pulses
- Card briefly highlights
- Smooth animation (300ms)

### Offline State
- Offline indicator in app bar
- Warning badge on stat recording button
- Cached data shown with "Offline" badge

### Spectator State
- Spectator badge on player card
- Same UI, clear indicator
- Can still record stats

---

## Gestures

- **Swipe on Player Card**: Record most recent stat for that player
- **Long-press on Stat**: Quick record with last used value
- **Tap Player Card**: Expand/collapse stat details
- **Tap Quick Action**: Open stat recording modal with stat pre-selected

---

## Accessibility

- **Screen Reader**: "Live session room. Game: [name]. Round: [number]. Player: [name]. Points: [value]."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on player cards and buttons

---

## Navigation

- **Back Button**: → Live Sessions List
- **Settings Icon**: → Session Settings
- **Leave/End Icon**: → Confirm leave/end dialog
- **Add Stat Button**: → Stat Recording Modal
- **Quick Action**: → Stat Recording Modal (with stat pre-selected)

---

**Wireframe Description Complete**
