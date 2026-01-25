# Home Dashboard Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  Home                    [⚙️] [🔄]      │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ Active Sessions                 │  │
│  │ ────────────────────────────────│  │
│  │ 🎲 Settlers of Catan            │  │
│  │    3 players • Round 3          │  │
│  │    [Tap to join]                │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Recent Activity                        │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Ticket to Ride               │  │
│  │    Won • 2 days ago             │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Carcassonne                   │  │
│  │    Lost • 5 days ago            │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Quick Stats                            │
│  ┌──────────┐  ┌──────────┐           │
│  │ Total    │  │ Win Rate │           │
│  │ Games    │  │          │           │
│  │   42     │  │   65%    │           │
│  └──────────┘  └──────────┘           │
│                                         │
│  Quick Actions                          │
│  ┌──────────┐  ┌──────────┐           │
│  │ Create   │  │ View     │           │
│  │ Session  │  │ Stats    │           │
│  └──────────┘  └──────────┘           │
│  ┌──────────┐  ┌──────────┐           │
│  │ Game     │  │ Follow   │           │
│  │ Library  │  │ Feed     │           │
│  └──────────┘  └──────────┘           │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 56dp
- **Title**: "Home" (20sp Roboto Medium)
- **Actions**: Settings icon (24dp), Refresh icon (24dp)
- **Refresh**: Pull-to-refresh also available

### Active Sessions Card
- **Type**: Material Design 3 Card (Elevated)
- **Elevation**: 2dp
- **Corner Radius**: 16dp
- **Padding**: 16dp
- **Content**:
  - Title: "Active Sessions" (16sp Roboto Medium)
  - Game name with icon (16sp Roboto Medium)
  - Player count and round (14sp Roboto Regular, secondary color)
  - "Tap to join" hint (12sp Roboto Regular, primary color)
- **States**: Default, Pressed (elevation 4dp)
- **Navigation**: → Live Session Room

### Recent Activity Section
- **Title**: "Recent Activity" (16sp Roboto Medium)
- **Position**: 24dp below active sessions card
- **List**: Last 3-5 sessions
- **Item Height**: 72dp
- **Content**:
  - Game icon/emoji (24dp)
  - Game name (16sp Roboto Medium)
  - Result (Won/Lost) and date (14sp Roboto Regular, secondary color)
- **Spacing**: 8dp between items
- **Navigation**: → Session Details

### Quick Stats Cards
- **Layout**: 2-column grid
- **Card Size**: Equal width, auto height
- **Spacing**: 8dp between cards
- **Padding**: 16dp
- **Content**:
  - Label (14sp Roboto Regular, secondary color)
  - Value (24sp Roboto Bold, primary color)
  - Optional icon or trend indicator
- **Cards**: Total Games, Win Rate, Favorite Game, Sessions This Week

### Quick Actions Grid
- **Layout**: 2-column grid
- **Card Size**: Equal width, 80dp height
- **Spacing**: 8dp between cards
- **Padding**: 16dp
- **Content**:
  - Icon (32dp) centered
  - Label (14sp Roboto Medium) below icon
- **Actions**:
  - Create Session → Create Session Flow
  - View Stats → Stats Dashboard
  - Game Library → Game Library Browse
  - Follow Feed → Following Feed

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Section Spacing**: 24dp vertical between sections
- **Card Spacing**: 8dp between cards in grid
- **Content Padding**: 16dp from screen edges
- **Pull-to-Refresh**: Available from top

---

## States & Interactions

### Default State
- Active sessions card visible (if active sessions exist)
- Recent activity list shown
- Quick stats displayed
- Quick actions available

### Loading State
- Skeleton screens matching layout
- Shimmer animation
- Placeholder cards

### Empty State (No Active Sessions)
- Active sessions card shows: "No active sessions"
- "Create Session" button in card
- Rest of dashboard normal

### Empty State (No Recent Activity)
- Recent activity section shows: "No recent activity"
- "View All Sessions" button
- Rest of dashboard normal

### Refresh State
- Pull-to-refresh indicator at top
- Circular progress indicator
- Content updates when complete

---

## Interactions

- **Tap Active Sessions Card**: → Live Session Room
- **Tap Recent Activity Item**: → Session Details
- **Tap Quick Stats Card**: → Detailed stat view
- **Tap Quick Action**: → Corresponding screen
- **Pull to Refresh**: Refresh all data
- **Swipe on Recent Activity**: Quick actions (view, share)

---

## Accessibility

- **Screen Reader**: "Home dashboard. Active sessions: [count]. Recent activity. [Game name], [result]."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on all cards

---

## Navigation

- **Settings Icon**: → Settings Main Screen
- **Refresh Icon**: Refresh dashboard data
- **Active Sessions Card**: → Live Session Room
- **Recent Activity Item**: → Session Details
- **Quick Stats Card**: → Stats Dashboard or detailed view
- **Quick Actions**: → Corresponding screens

---

**Wireframe Description Complete**
