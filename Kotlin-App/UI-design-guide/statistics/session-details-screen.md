# Session Details Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Session Details        [📤] [⚙️]    │
├─────────────────────────────────────────┤
│                                         │
│  🎲 Settlers of Catan                   │
│                                         │
│  Date: January 15, 2024                │
│  Duration: 2 hours 15 minutes           │
│  Round: 10                              │
│                                         │
│  Final Results                          │
│  ┌─────────────────────────────────┐  │
│  │ 🥇 Alice - Winner               │  │
│  │    Points: 10                   │  │
│  │    Resources: 12                │  │
│  │    Cities: 2                    │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ 🥈 Bob                           │  │
│  │    Points: 8                    │  │
│  │    Resources: 15                │  │
│  │    Cities: 1                    │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Round-by-Round Breakdown               │
│  ┌─────────────────────────────────┐  │
│  │ Round 1                          │  │
│  │   Alice: Points 2, Resources 5  │  │
│  │   Bob: Points 1, Resources 4    │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ Round 2                          │  │
│  │   Alice: Points 3, Resources 6  │  │
│  │   Bob: Points 2, Resources 5    │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │    Export Session Data          │  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 64dp (collapsible)
- **Title**: "Session Details" (20sp Roboto Medium)
- **Actions**: Share icon (24dp), Settings icon (24dp)

### Game Header
- **Game Name**: 24sp Roboto Medium
- **Position**: 16dp below app bar
- **Icon**: Game icon/emoji (32dp) on left

### Session Info
- **Date**: "Date: [formatted date]" (16sp Roboto Regular)
- **Duration**: "Duration: [time]" (16sp Roboto Regular, secondary color)
- **Round**: "Round: [number]" (16sp Roboto Regular, secondary color)
- **Position**: 16dp below header
- **Spacing**: 8dp between info items

### Final Results Section
- **Title**: "Final Results" (18sp Roboto Medium)
- **Position**: 24dp below session info

### Player Result Card
- **Type**: Material Design 3 Card (Elevated)
- **Elevation**: 1dp
- **Corner Radius**: 12dp
- **Padding**: 16dp
- **Content**:
  - Medal icon (🥇🥈🥉) or rank (24dp)
  - Player name (16sp Roboto Medium)
  - Winner badge (if applicable)
  - Final stat values (14sp Roboto Regular)
- **Spacing**: 8dp vertical between cards
- **Order**: Ranked by final score

### Round-by-Round Breakdown Section
- **Title**: "Round-by-Round Breakdown" (18sp Roboto Medium)
- **Position**: 24dp below results
- **Collapsible**: Can expand/collapse each round

### Round Card
- **Type**: Material Design 3 Card (Outlined)
- **Border**: 1dp solid (divider color)
- **Corner Radius**: 12dp
- **Padding**: 16dp
- **Content**:
  - Round number (16sp Roboto Medium)
  - Player stats for that round (14sp Roboto Regular)
- **Spacing**: 8dp vertical between rounds
- **Expandable**: Tap to expand/collapse

### Export Session Data Button
- **Type**: Outlined Button
- **Height**: 48dp
- **Width**: Full width minus 32dp margins
- **Text**: "Export Session Data" (14sp Roboto Medium, primary color)
- **Border**: 1dp solid primary color
- **Icon**: Download icon (18dp) on left
- **Position**: 24dp below round breakdown, 16dp from bottom
- **Navigation**: → Export Stats Screen

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Header**: 16dp below app bar
- **Section Spacing**: 24dp vertical between sections
- **Card Spacing**: 8dp vertical between cards
- **Button Spacing**: 24dp from last section, 16dp from bottom

---

## States & Interactions

### Default State
- Session details displayed
- Final results shown
- Round breakdown collapsed (or expanded)
- Export button enabled

### Expanded Round State
- Round details visible
- Player stats for that round shown
- Can collapse by tapping again

### Loading State
- Skeleton cards matching layout
- Shimmer animation
- Export button disabled

---

## Interactions

- **Tap Round Card**: Expand/collapse round details
- **Tap Player Card**: Show player's detailed stats (optional)
- **Tap Export**: Navigate to Export Stats
- **Pull to Refresh**: Refresh session data (if editable)

---

## Accessibility

- **Screen Reader**: "Session details. [Game name]. Date: [date]. Final results. [Player name], [score]."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on all cards and buttons

---

## Navigation

- **Back Button**: → Session History or Stats Dashboard
- **Export Button**: → Export Stats Screen
- **Share Icon**: → Share dialog

---

**Wireframe Description Complete**
