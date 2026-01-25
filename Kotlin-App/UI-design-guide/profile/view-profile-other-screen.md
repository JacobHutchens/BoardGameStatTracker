# View Profile Screen (Other Users) Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← @alice_gamer          [⚙️] [☰]      │
├─────────────────────────────────────────┤
│                                         │
│         [Avatar]                        │
│                                         │
│    @alice_gamer                         │
│    Board game enthusiast                │
│    [Public Profile]                     │
│                                         │
│    [Follow] [Following]                │
│                                         │
│  Stats                                  │
│  ┌──────────┐  ┌──────────┐           │
│  │ Total    │  │ Win Rate │           │
│  │ Games    │  │          │           │
│  │   38     │  │   62%    │           │
│  └──────────┘  └──────────┘           │
│                                         │
│  Followers: 24  Following: 12          │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │    View Public Stats             │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Recent Public Sessions                 │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Catan • Won • 2d ago        │  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 152dp (expanded), 64dp (collapsed)
- **Title**: "@username" (24sp expanded, 20sp collapsed)
- **Actions**: Settings icon (24dp) if own profile, Drawer menu icon (24dp)

### Avatar
- **Size**: 80dp x 80dp
- **Position**: Centered, 24dp below app bar
- **Border**: 2dp solid (divider color)
- **Read-only**: Cannot be edited

### Username
- **Text**: "@username" (20sp Roboto Medium)
- **Position**: 16dp below avatar
- **Alignment**: Centered

### Bio
- **Text**: Bio text (16sp Roboto Regular, secondary color)
- **Position**: 8dp below username
- **Alignment**: Centered
- **Max Width**: 280dp
- **Multi-line**: Supported

### Public Profile Badge
- **Type**: Status Badge
- **Height**: 24dp
- **Padding**: 8dp horizontal, 4dp vertical
- **Typography**: 12sp Roboto Medium
- **Colors**: Green background (#4CAF50), white text
- **Text**: "PUBLIC PROFILE"
- **Position**: 8dp below bio
- **Visibility**: Only shown if user has public stats

### Follow/Following Button
- **Type**: Primary Action Button (Follow) or Outlined Button (Following)
- **Height**: 48dp
- **Width**: 200dp
- **Text**: "Follow" or "Following" (14sp Roboto Medium)
- **Position**: 16dp below badge
- **Alignment**: Centered
- **States**: 
  - Follow: Primary color background, white text
  - Following: Outlined, primary color text, checkmark icon

### Stats Section
- **Title**: "Stats" (18sp Roboto Medium)
- **Position**: 24dp below follow button
- **Note**: Only shows public stats

### Quick Stats Cards
- **Layout**: 2-column grid
- **Card Size**: Equal width, auto height
- **Spacing**: 8dp between cards
- **Padding**: 16dp
- **Content**:
  - Label (14sp Roboto Regular, secondary color)
  - Value (24sp Roboto Bold, primary color)
- **Cards**: Total Games (public), Win Rate (public)

### Followers/Following Count
- **Text**: "Followers: X  Following: Y" (16sp Roboto Regular, secondary color)
- **Position**: 16dp below stats
- **Alignment**: Centered
- **Tappable**: Navigate to Followers/Following List

### View Public Stats Button
- **Type**: Outlined Button
- **Height**: 48dp
- **Width**: Full width minus 32dp margins
- **Text**: "View Public Stats" (14sp Roboto Medium, primary color)
- **Border**: 1dp solid primary color
- **Position**: 16dp below followers count

### Recent Public Sessions Section
- **Title**: "Recent Public Sessions" (18sp Roboto Medium)
- **Position**: 24dp below view stats button

### Recent Session Item
- **Type**: List Item (Standard)
- **Height**: 56dp
- **Padding**: 16dp horizontal
- **Content**:
  - Game icon/emoji (24dp) on left
  - Game name and result (16sp Roboto Medium)
  - Date (14sp Roboto Regular, secondary color, right-aligned)
- **Spacing**: 8dp vertical between items
- **Navigation**: → Session Details (from Following Feed)

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Avatar**: 24dp below app bar
- **Section Spacing**: 24dp vertical between sections
- **Card Spacing**: 8dp between cards in grid
- **Button Spacing**: 16dp from adjacent elements

---

## States & Interactions

### Default State
- Profile information displayed
- Public stats shown
- Follow/Following button visible
- Recent public sessions listed

### Private Profile State
- Message: "This user's stats are private"
- Limited information shown
- No stats displayed
- Follow button still available

### Following State
- Follow button changes to "Following"
- Checkmark icon shown
- Can unfollow by tapping

### Loading State
- Skeleton cards matching layout
- Shimmer animation
- Buttons disabled

---

## Interactions

- **Tap Follow/Following**: Toggle follow status
- **Tap Followers/Following Count**: Navigate to Followers/Following List
- **Tap View Public Stats**: Navigate to user's public stats view
- **Tap Recent Session**: Navigate to Session Details (from feed)
- **Tap Settings Icon**: Open Settings (if own profile)

---

## Accessibility

- **Screen Reader**: "Profile. [Username]. [Bio]. Follow button. Stats: [values]."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on all buttons

---

## Navigation

- **Back Button**: → Previous screen
- **Follow/Following Button**: Toggle follow status (stays on screen)
- **Followers/Following Count**: → Followers/Following List Screen
- **View Public Stats**: → User's public stats view
- **Recent Session**: → Session Details (from Following Feed)

---

**Wireframe Description Complete**
