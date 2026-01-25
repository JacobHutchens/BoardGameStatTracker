# Game Details Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Settlers of Catan        [⚙️] [📤]   │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Settlers of Catan            │  │
│  │                                 │  │
│  │ A strategy game of building    │  │
│  │ settlements and trading         │  │
│  │ resources.                      │  │
│  │                                 │  │
│  │ Players: 3-4                    │  │
│  │ Can Win: Yes                    │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Stat Sets                             │
│  ┌─────────────────────────────────┐  │
│  │ Standard Set              [Use]  │  │
│  │ • Points, Resources, Cities       │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ Custom Set               [Use]  │  │
│  │ • Points, Gold, Settlements     │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ Create New Stat Set             │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ Create New Based On...           │  │
│  └─────────────────────────────────┘  │
│                                         │
│  My Stats                               │
│  ┌──────────┐  ┌──────────┐           │
│  │ Played   │  │ Win Rate │           │
│  │   15     │  │   60%    │           │
│  └──────────┘  └──────────┘           │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │    View All Stats                │  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 64dp (collapsible, can expand to 152dp)
- **Title**: Game name (20sp Roboto Medium)
- **Actions**: Settings icon (24dp), Share icon (24dp)

### Game Info Card
- **Type**: Material Design 3 Card (Elevated)
- **Elevation**: 1dp
- **Corner Radius**: 16dp
- **Padding**: 16dp
- **Content**:
  - Game icon/emoji (64dp) centered or left
  - Game name (24sp Roboto Medium)
  - Description (16sp Roboto Regular, multi-line)
  - Player count: "Players: X-Y" (14sp Roboto Regular, secondary color)
  - Can win indicator: "Can Win: Yes/No" (14sp Roboto Regular, secondary color)
- **Position**: Top, 16dp below app bar

### Stat Sets Section
- **Title**: "Stat Sets" (18sp Roboto Medium)
- **Position**: 24dp below game info card

### Stat Set Card
- **Type**: Material Design 3 Card (Outlined)
- **Border**: 1dp solid (divider color)
- **Corner Radius**: 12dp
- **Padding**: 16dp
- **Content**:
  - Stat set name (16sp Roboto Medium)
  - Stat list preview (14sp Roboto Regular, secondary color)
  - "Use" button (Text button, 14sp Roboto Medium, primary color) on right
- **Spacing**: 8dp vertical between cards

### Create New Stat Set Button
- **Type**: Outlined Button
- **Height**: 48dp
- **Width**: Full width minus 32dp margins
- **Text**: "Create New Stat Set" (14sp Roboto Medium, primary color)
- **Border**: 1dp solid primary color
- **Position**: 16dp below stat sets list

### Build On Existing Button
- **Type**: Outlined Button
- **Height**: 48dp
- **Width**: Full width minus 32dp margins
- **Text**: "Create New Based On..." (14sp Roboto Medium, primary color)
- **Subtext**: "(Copy and modify existing)" (12sp Roboto Regular, secondary color)
- **Border**: 1dp solid primary color
- **Position**: 8dp below create new button
- **Tooltip**: Available on long-press

### My Stats Section
- **Title**: "My Stats" (18sp Roboto Medium)
- **Position**: 24dp below buttons

### Quick Stats Cards
- **Layout**: 2-column grid
- **Card Size**: Equal width, auto height
- **Spacing**: 8dp between cards
- **Padding**: 16dp
- **Content**:
  - Label (14sp Roboto Regular, secondary color)
  - Value (24sp Roboto Bold, primary color)
- **Cards**: Played (count), Win Rate (percentage)

### View All Stats Button
- **Type**: Outlined Button
- **Height**: 48dp
- **Width**: Full width minus 32dp margins
- **Text**: "View All Stats" (14sp Roboto Medium, primary color)
- **Border**: 1dp solid primary color
- **Position**: 16dp below quick stats
- **Navigation**: → Game-Specific Stats Screen

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Game Info Card**: 16dp below app bar
- **Section Spacing**: 24dp vertical between sections
- **Card Spacing**: 8dp vertical between stat set cards
- **Button Spacing**: 8dp vertical between buttons

---

## States & Interactions

### Default State
- Game info displayed
- Stat sets list shown
- Quick stats displayed
- All buttons enabled

### Empty Stat Sets State
- Stat sets section shows "No stat sets available"
- Create New Stat Set button prominent
- Message: "Create your first stat set for this game"

### Loading State
- Skeleton cards matching layout
- Shimmer animation
- Buttons disabled

---

## Interactions

- **Tap Stat Set Card**: Navigate to Stat Set Details
- **Tap Use Button**: Use stat set for new session
- **Tap Create New Stat Set**: Navigate to Create Stat Set screen
- **Tap Build On Existing**: Navigate to Build On Stat Set screen
- **Tap View All Stats**: Navigate to Game-Specific Stats
- **Long-press Build On**: Show tooltip explaining immutability

---

## Accessibility

- **Screen Reader**: "Game details. [Game name]. [Description]. Stat sets: [list]. My stats: [values]."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on all cards and buttons

---

## Navigation

- **Back Button**: → Game Library Browse
- **Stat Set Card**: → Stat Set Details
- **Use Button**: → Create Session Flow (with stat set pre-selected)
- **Create New Stat Set**: → Create Stat Set Screen
- **Build On Existing**: → Build On Stat Set Screen
- **View All Stats**: → Game-Specific Stats Screen

---

**Wireframe Description Complete**
