# Navigation Structure Wireframe
## Board Game Stat Tracker

---

## Bottom Navigation Bar

### Layout
```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│                    Content Area                        │
│                                                         │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  [🏠]      [👥]      [📚]      [📰]      [👤]        │
│  Home   Sessions  Library   Feed    Profile            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Specifications
- **Height**: 80dp total (56dp content + 24dp safe area)
- **Background**: Surface color (Material Design 3)
- **Elevation**: 8dp
- **Tabs**: 5 tabs with icons and labels
- **Active Indicator**: Underline, 3dp height, primary color
- **Touch Target**: 48dp minimum per tab

### Tab Details
1. **Home** - Home icon, "Home" label
2. **Live Sessions** - Group/People icon, "Sessions" label
3. **Game Library** - Library/Collection icon, "Library" label
4. **Following Feed** - Feed/Activity icon, "Feed" label
5. **Profile** - Account/Person icon, "Profile" label

---

## Drawer Menu (Navigation Drawer)

### Layout
```
┌──────────────────────┐
│  [User Avatar]       │
│  Username            │
│  email@example.com   │
├──────────────────────┤
│  📜 Session History  │
│  📤 Export Stats     │
├──────────────────────┤
│  ⚙️  Settings        │
│  ❓ Help/About       │
├──────────────────────┤
│  🚪 Logout           │
├──────────────────────┤
│  App Version 1.0     │
└──────────────────────┘
```

### Specifications
- **Width**: 280dp (standard), 320dp (tablets)
- **Header Height**: 160dp
- **Menu Item Height**: 48dp
- **Elevation**: 16dp when open
- **Animation**: Slide in from left, 300ms

---

## App Bar (Top Bar)

### Standard App Bar
```
┌─────────────────────────────────────────┐
│  ←  Screen Title              [⚙️] [🔍] │
└─────────────────────────────────────────┘
```
- **Height**: 56dp
- **Elevation**: 4dp (when scrolled)
- **Back Icon**: 24dp
- **Action Icons**: 24dp (right side)

### Large App Bar (Collapsible)
```
┌─────────────────────────────────────────┐
│                                         │
│  Screen Title                           │
│  Subtitle                               │
│  [Action Buttons]                       │
└─────────────────────────────────────────┘
```
- **Height**: 152dp (expanded), 64dp (collapsed)
- **Background**: Primary color or image

---

**Wireframe Description Complete**
