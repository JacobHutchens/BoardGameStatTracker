# Stats Dashboard - Quick Stats View Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← My Stats                [⚙️] [📤]   │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────┐  ┌──────────┐           │
│  │ Total    │  │ Win Rate │           │
│  │ Games    │  │          │           │
│  │   42     │  │   65%    │           │
│  └──────────┘  └──────────┘           │
│                                         │
│  ┌──────────┐  ┌──────────┐           │
│  │ Favorite │  │ Sessions │           │
│  │ Game     │  │ This Week│           │
│  │ Catan    │  │    5     │           │
│  └──────────┘  └──────────┘           │
│                                         │
│  Favorite Games                        │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Settlers of Catan           15  │  │
│  │    Win Rate: 60%                │  │
│  │    Last Played: 2 days ago      │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Ticket to Ride            12  │  │
│  │    Win Rate: 58%                │  │
│  │    Last Played: 1 week ago      │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Win Rate by Game                       │
│  ┌─────────────────────────────────┐  │
│  │ Catan        ████████░░ 60%     │  │
│  │ Ticket       ███████░░░ 58%     │  │
│  │ Carcassonne  ██████░░░░ 50%     │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Recent Trends                          │
│  ┌─────────────────────────────────┐  │
│  │    [Mini Line Chart]             │  │
│  │    Win Rate Over Time           │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │    Show Advanced Filters         │  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 56dp
- **Title**: "My Stats" (20sp Roboto Medium)
- **Actions**: Settings icon (24dp), Export icon (24dp)
- **Back Button**: 24dp

### Overview Cards (Grid)
- **Layout**: 2 columns
- **Card Size**: Equal width, auto height
- **Spacing**: 8dp between cards
- **Padding**: 16dp
- **Content**:
  - Label (14sp Roboto Regular, secondary color)
  - Value (24sp Roboto Bold, primary color)
  - Optional icon or trend indicator
- **Cards**:
  - Total Games
  - Win Rate
  - Favorite Game
  - Sessions This Week

### Favorite Games List
- **Type**: List with cards
- **Item Height**: 72dp
- **Content**:
  - Game icon/emoji (24dp)
  - Game name (16sp Roboto Medium)
  - Play count (14sp Roboto Regular, right-aligned)
  - Win rate (14sp Roboto Regular, secondary color)
  - Last played date (12sp Roboto Regular, secondary color)
- **Spacing**: 8dp between items

### Win Rate by Game
- **Type**: Horizontal bar chart
- **Height**: 48dp per item
- **Content**:
  - Game name (14sp Roboto Medium)
  - Progress bar (visual representation)
  - Percentage (14sp Roboto Medium, right-aligned)
- **Spacing**: 8dp between items

### Recent Trends
- **Type**: Mini chart card
- **Height**: 120dp
- **Content**: Small line or bar chart
- **Title**: "Win Rate Over Time" (14sp Roboto Medium)
- **Chart**: Simplified visualization

### Show Advanced Filters Button
- **Type**: Outlined Button
- **Height**: 48dp
- **Width**: Full width minus 32dp margins
- **Text**: "Show Advanced Filters" (14sp Roboto Medium)
- **Icon**: Filter icon (18dp) on left
- **Position**: Bottom of content, 24dp spacing

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Section Spacing**: 24dp vertical between sections
- **Card Spacing**: 8dp between cards in grid
- **List Item Spacing**: 8dp vertical
- **Content Padding**: 16dp from screen edges

---

## States & Interactions

### Default State
- All overview cards visible
- Favorite games list shown
- Win rate chart displayed
- Recent trends visible

### Loading State
- Skeleton screens matching layout
- Shimmer animation
- Placeholder cards

### Empty State
- Illustration/icon (120dp)
- Title: "No stats yet" (20sp Roboto Medium)
- Description: "Start tracking games to see your stats" (16sp Roboto Regular)
- Action Button: "Create Your First Session" (Primary button)

### Error State
- Error icon (48dp)
- Error message (16sp Roboto Regular)
- Retry button (Primary button)

---

## Interactions

- **Tap Overview Card**: Navigate to detailed view
- **Tap Favorite Game**: Navigate to game-specific stats
- **Tap Win Rate Bar**: Navigate to detailed win rate analysis
- **Tap Recent Trends**: Navigate to full trend visualization
- **Tap Show Advanced**: Navigate to Advanced Filters screen
- **Pull to Refresh**: Refresh all stats data

---

## Accessibility

- **Screen Reader**: "My stats dashboard. Total games: [number]. Win rate: [percentage]."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: All text meets WCAG AA
- **Chart Accessibility**: Text alternatives for charts

---

## Navigation

- **Back Button**: → Previous screen
- **Settings Icon**: → Stats Settings
- **Export Icon**: → Export Stats screen
- **Overview Card**: → Detailed stat view
- **Favorite Game**: → Game-Specific Stats
- **Show Advanced**: → Advanced Stats Filter screen

---

**Wireframe Description Complete**
