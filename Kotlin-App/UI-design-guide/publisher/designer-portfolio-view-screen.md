# Designer Portfolio View Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← My Portfolio            [⚙️] [📤]   │
├─────────────────────────────────────────┤
│                                         │
│         [Avatar]                        │
│         [Edit]                          │
│                                         │
│    @designer_name                      │
│    Board game designer                 │
│    [Public Portfolio]                  │
│                                         │
│  Portfolio Stats                        │
│  ┌──────────┐  ┌──────────┐           │
│  │ Games    │  │ Total    │           │
│  │ Created  │  │ Sessions │           │
│  │   12     │  │   5,678  │           │
│  └──────────┘  └──────────┘           │
│  ┌──────────┐  ┌──────────┐           │
│  │ Active   │  │ Avg      │           │
│  │ Players  │  │ Rating   │           │
│  │   1,234  │  │   4.5⭐   │           │
│  └──────────┘  └──────────┘           │
│                                         │
│  My Games                               │
│  ┌─────────────────────────────────┐  │
│  │ 🔍 Search games...               │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Settlers of Catan              │  │
│  │    2,345 sessions • 4.8⭐        │  │
│  │    [View Analytics]               │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Ticket to Ride                │  │
│  │    1,890 sessions • 4.6⭐        │  │
│  │    [View Analytics]               │  │
│  └─────────────────────────────────┘  │
│                                         │
│                    [➕ Create Game]    │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 152dp (expanded), 64dp (collapsed)
- **Title**: "My Portfolio" (24sp expanded, 20sp collapsed)
- **Actions**: Settings icon (24dp), Share icon (24dp)

### Avatar
- **Size**: 80dp x 80dp
- **Position**: Centered, 24dp below app bar
- **Border**: 2dp solid (primary color or divider)
- **Edit Button**: Small edit icon (20dp) bottom-right of avatar
- **Tap Avatar**: Navigate to Edit Profile

### Designer Name
- **Text**: "@designer_name" (20sp Roboto Medium)
- **Position**: 16dp below avatar
- **Alignment**: Centered

### Bio/Description
- **Text**: "Board game designer" (16sp Roboto Regular, secondary color)
- **Position**: 8dp below name
- **Alignment**: Centered

### Public Portfolio Badge
- **Type**: Status Badge
- **Height**: 24dp
- **Padding**: 8dp horizontal, 4dp vertical
- **Typography**: 12sp Roboto Medium
- **Colors**: Green background (#4CAF50), white text
- **Text**: "PUBLIC PORTFOLIO"
- **Position**: 8dp below bio
- **Visibility**: Shows portfolio visibility status

### Portfolio Stats Section
- **Title**: "Portfolio Stats" (18sp Roboto Medium)
- **Position**: 24dp below badge

### Portfolio Stats Cards
- **Layout**: 2-column grid
- **Card Size**: Equal width, auto height
- **Spacing**: 8dp between cards
- **Padding**: 16dp
- **Content**:
  - Label (14sp Roboto Regular, secondary color)
  - Value (24sp Roboto Bold, primary color)
- **Cards**: Games Created, Total Sessions, Active Players, Average Rating

### My Games Section
- **Title**: "My Games" (18sp Roboto Medium)
- **Position**: 24dp below portfolio stats

### Search Bar
- **Type**: Material Design 3 Search Bar
- **Height**: 56dp
- **Icon**: Search icon (24dp) on left
- **Placeholder**: "Search games..." (16sp Roboto Regular)
- **Clear Button**: X icon (24dp) when text entered
- **Position**: 16dp below section title

### Game Card
- **Type**: Material Design 3 Card (Elevated)
- **Elevation**: 1dp
- **Corner Radius**: 12dp
- **Padding**: 16dp
- **Content**:
  - Game icon/emoji (32dp) on left
  - Game name (16sp Roboto Medium)
  - Session count and rating (14sp Roboto Regular, secondary color)
  - "View Analytics" button (Text button, 14sp Roboto Medium, primary color) on right
- **Spacing**: 8dp vertical between cards
- **Navigation**: → Game Analytics Screen

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
- **Avatar**: 24dp below app bar
- **Section Spacing**: 24dp vertical between sections
- **Card Spacing**: 8dp between cards in grid
- **FAB Position**: 16dp from bottom-right

---

## States & Interactions

### Default State
- Portfolio information displayed
- Stats shown
- Games listed
- All interactive elements enabled

### Search State
- Search results filtered
- Clear button visible
- Results update as user types

### Empty State (No Games)
- Illustration/icon (120dp)
- Title: "No games yet" (20sp Roboto Medium)
- Description: "Create your first game to start building your portfolio" (16sp Roboto Regular)
- Action Button: "Create Game" (Primary button)

### Loading State
- Skeleton cards matching layout
- Shimmer animation
- Buttons disabled

---

## Interactions

- **Tap Avatar**: Navigate to Edit Profile
- **Tap Edit Button**: Navigate to Edit Profile
- **Tap Game Card**: Navigate to Game Analytics
- **Tap View Analytics**: Navigate to Game Analytics
- **Type in Search**: Filter games in real-time
- **Tap Create Game FAB**: Navigate to Create New Game
- **Long-press Game Card**: Context menu (view, edit, delete)

---

## Accessibility

- **Screen Reader**: "My portfolio. [Designer name]. Portfolio stats: [values]. My games: [list]."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on all cards and buttons

---

## Navigation

- **Back Button**: → Profile or Settings
- **Edit Profile**: → Edit Profile Screen
- **Game Card**: → Game Analytics Screen
- **View Analytics Button**: → Game Analytics Screen
- **Create Game FAB**: → Create New Game Screen
- **Settings Icon**: → Portfolio Settings (if applicable)
- **Share Icon**: → Share Portfolio

---

**Wireframe Description Complete**
