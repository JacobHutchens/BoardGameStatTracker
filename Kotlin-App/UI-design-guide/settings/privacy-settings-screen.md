# Privacy Settings Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Privacy Settings                     │
├─────────────────────────────────────────┤
│                                         │
│  Default Privacy                        │
│  ┌─────────────────────────────────┐  │
│  │ Default for new games             │  │
│  │ ────────────────────────────────│  │
│  │ Public                    [▼]   │  │
│  └─────────────────────────────────┘  │
│                                         │
│  Per-Game Privacy                       │
│  ┌─────────────────────────────────┐  │
│  │ [Set All Public] [Set All Private] │
│  └─────────────────────────────────┘  │
│                                         │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Settlers of Catan            │  │
│  │    Public                [Toggle]│  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Ticket to Ride               │  │
│  │    Private               [Toggle]│  │
│  └─────────────────────────────────┘  │
│  ┌─────────────────────────────────┐  │
│  │ 🎲 Carcassonne                   │  │
│  │    Public                [Toggle]│  │
│  └─────────────────────────────────┘  │
│                                         │
│  Follower Visibility                    │
│  ┌─────────────────────────────────┐  │
│  │ Show followers count      [Toggle]│  │
│  └─────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 56dp
- **Title**: "Privacy Settings" (20sp Roboto Medium)
- **Back Button**: 24dp

### Default Privacy Section
- **Title**: "Default Privacy" (16sp Roboto Medium)
- **Position**: 16dp below app bar

### Default Privacy Dropdown
- **Type**: Material Design 3 Outlined Menu
- **Height**: 56dp
- **Label**: "Default for new games"
- **Options**: "Public" and "Private"
- **Position**: 16dp below section title
- **Note**: Sets default privacy for new games

### Per-Game Privacy Section
- **Title**: "Per-Game Privacy" (16sp Roboto Medium)
- **Position**: 24dp below default privacy

### Bulk Actions
- **Type**: Button Group
- **Layout**: Side by side, equal width
- **Buttons**:
  - "Set All Public" (Outlined Button, 48dp height)
  - "Set All Private" (Outlined Button, 48dp height)
- **Position**: 16dp below section title
- **Spacing**: 8dp between buttons

### Game Privacy Item
- **Type**: List Item (Two-Line)
- **Height**: 72dp
- **Padding**: 16dp horizontal
- **Content**:
  - Game icon/emoji (32dp) on left
  - Game name (16sp Roboto Medium)
  - Privacy status (14sp Roboto Regular, secondary color)
  - Toggle switch (40dp track width) on right
- **Spacing**: 1dp divider between items
- **Toggle States**: ON (Public), OFF (Private)

### Follower Visibility Section
- **Title**: "Follower Visibility" (16sp Roboto Medium)
- **Position**: 24dp below per-game privacy

### Follower Visibility Item
- **Type**: List Item (Standard)
- **Height**: 56dp
- **Padding**: 16dp horizontal
- **Content**:
  - "Show followers count" (16sp Roboto Medium)
  - Toggle switch (40dp track width) on right
- **Default**: ON

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Section Spacing**: 24dp vertical between sections
- **Item Spacing**: 1dp divider between items
- **Bulk Action Spacing**: 8dp horizontal between buttons

---

## States & Interactions

### Default State
- Default privacy set (Public or Private)
- Per-game privacy toggles shown
- Follower visibility toggle shown
- All toggles enabled

### Toggle State
- Privacy status updates immediately
- Visual feedback (toggle animation)
- Save automatically (no save button needed)

### Bulk Action State
- All games set to selected privacy
- Toggles update to reflect change
- Confirmation: "All games set to [Public/Private]"

---

## Interactions

- **Select Default Privacy**: Update default for new games
- **Toggle Game Privacy**: Toggle individual game privacy
- **Tap Set All Public**: Set all games to public
- **Tap Set All Private**: Set all games to private
- **Toggle Follower Visibility**: Show/hide followers count

---

## Accessibility

- **Screen Reader**: "Privacy settings. Default privacy: [value]. [Game name], [privacy status], toggle."
- **Touch Targets**: All items minimum 56dp height (exceeds 48dp requirement)
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on all toggles

---

## Navigation

- **Back Button**: → Settings Main Screen

---

**Wireframe Description Complete**
