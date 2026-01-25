# Following Feed Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  Following Feed                         │
├─────────────────────────────────────────┤
│                                         │
│  Feed Preview                            │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Settlers of Catan            │  │
│  │    @alice_gamer • Won           │  │
│  │    2 days ago                   │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Ticket to Ride               │  │
│  │    @bob_player • Lost           │  │
│  │    3 days ago                   │  │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │      View All Feed               │  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Screen Layout (Expanded)

```
┌─────────────────────────────────────────┐
│  Following Feed            [🔄] [⚙️]   │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Settlers of Catan            │  │
│  │    @alice_gamer [Public]        │  │
│  │    Won • 2 days ago             │  │
│  │    [View Details]                │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Ticket to Ride               │  │
│  │    @bob_player [Public]         │  │
│  │    Lost • 3 days ago            │  │
│  │    [View Details]                │  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Carcassonne                   │  │
│  │    @charlie_designer [Public]   │  │
│  │    Won • 5 days ago             │  │
│  │    [View Details]                │  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 56dp
- **Title**: "Following Feed" (20sp Roboto Medium)
- **Actions**: Refresh icon (24dp), Settings icon (24dp)

### Feed Preview Section
- **Title**: "Feed Preview" (16sp Roboto Medium)
- **Position**: Top, 16dp below app bar
- **Content**: Last 2-3 recent sessions
- **Visibility**: Always visible (not hidden behind button)

### Session Preview Card
- **Type**: Material Design 3 Card (Elevated)
- **Elevation**: 1dp
- **Corner Radius**: 16dp
- **Padding**: 16dp
- **Content**:
  - Game icon/emoji (32dp) on left
  - Game name (16sp Roboto Medium)
  - Designer handle (14sp Roboto Regular, secondary color)
  - Result (Won/Lost) and date (14sp Roboto Regular, secondary color)
- **Spacing**: 8dp vertical between cards

### View All Feed Button
- **Type**: Primary Action Button
- **Height**: 56dp
- **Width**: Full width minus 32dp margins
- **Text**: "View All Feed" (14sp Roboto Medium, white)
- **Background**: Primary brand color
- **Corner Radius**: 12dp
- **Position**: 16dp below preview cards
- **Navigation**: → Expanded feed view

### Expanded Feed Session Card
- **Type**: Material Design 3 Card (Elevated)
- **Elevation**: 1dp
- **Corner Radius**: 16dp
- **Padding**: 16dp
- **Content**:
  - Game icon/emoji (32dp) on left
  - Game name (16sp Roboto Medium)
  - Designer handle with link (14sp Roboto Medium, primary color)
  - Privacy badge: "[Public]" or "[Private]" (12sp Roboto Medium, badge style)
  - Result and date (14sp Roboto Regular, secondary color)
  - "View Details" button (Text button, 14sp Roboto Medium, primary color)
- **Spacing**: 8dp vertical between cards

### Privacy Badge
- **Type**: Status Badge
- **Height**: 20dp
- **Padding**: 6dp horizontal, 4dp vertical
- **Typography**: 10sp Roboto Medium
- **Colors**:
  - Public: Green background (#4CAF50), white text
  - Private: Gray background (#9E9E9E), white text
- **Text**: "PUBLIC" or "PRIVATE"

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Preview Section**: 16dp below app bar
- **Card Spacing**: 8dp vertical between cards
- **Button Spacing**: 16dp from last preview card
- **Expanded Feed**: 16dp below app bar

---

## States & Interactions

### Default State (Preview)
- Last 2-3 sessions shown
- View All Feed button visible
- Pull-to-refresh available

### Expanded State
- All recent sessions shown
- Privacy badges visible
- Designer links available
- View Details buttons available

### Empty State
- Illustration/icon (120dp)
- Title: "No activity yet" (20sp Roboto Medium)
- Description: "Follow designers to see their public stats" (16sp Roboto Regular)
- Action Button: "Find Designers to Follow" (Primary button)

### Loading State
- Skeleton session cards (2-3 placeholders)
- Shimmer animation
- Refresh indicator

---

## Interactions

- **Tap Preview Card**: Navigate to Session Details (from feed)
- **Tap View All Feed**: Expand to show all sessions
- **Tap Designer Handle**: Navigate to Designer Profile
- **Tap View Details**: Navigate to Session Details
- **Pull to Refresh**: Refresh feed content
- **Swipe on Card**: Quick actions (optional)

---

## Accessibility

- **Screen Reader**: "Following feed. [Game name], [designer], [result], [date]."
- **Touch Targets**: All cards and buttons minimum 48dp height
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on all interactive elements

---

## Navigation

- **Session Card**: → Session Details (from Following Feed)
- **Designer Handle**: → View Profile Screen (Other User)
- **View Details Button**: → Session Details (from Following Feed)
- **Settings Icon**: → Feed Settings (if applicable)

---

**Wireframe Description Complete**
