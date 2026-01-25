# Join Session Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Join Session                         │
├─────────────────────────────────────────┤
│                                         │
│         [Session Icon]                  │
│                                         │
│    Enter Session Key                    │
│                                         │
│    ┌─────────────────────────────┐    │
│    │ Session Key                  │    │
│    │ ──────────────────────────── │    │
│    │ ABC123                        │    │
│    │ (6 characters)               │    │
│    └─────────────────────────────┘    │
│                                         │
│    ┌─────────────────────────────┐    │
│    │        JOIN SESSION          │    │
│    └─────────────────────────────┘    │
│                                         │
│    [Scan QR Code]                      │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### Session Icon
- **Size**: 64dp x 64dp
- **Color**: Primary color or secondary color
- **Position**: Centered, 24dp below app bar

### Title Text
- **Text**: "Enter Session Key" (20sp Roboto Medium)
- **Position**: 16dp below icon
- **Alignment**: Centered

### Session Key Input
- **Type**: Material Design 3 Outlined Text Field
- **Height**: 56dp
- **Label**: Floating label "Session Key"
- **Text**: 16sp Roboto Medium (uppercase, monospace font)
- **Placeholder**: "ABC123"
- **Helper Text**: "(6 characters)" (12sp Roboto Regular, secondary color)
- **Auto-format**: Auto-uppercase, auto-format with hyphen (ABC-123)
- **Max Length**: 6 characters
- **Position**: 24dp below title
- **Validation**: Real-time format validation

### Join Session Button
- **Type**: Primary Action Button
- **Height**: 56dp
- **Width**: Full width minus 32dp margins
- **Text**: "JOIN SESSION" (14sp Roboto Medium, white)
- **Background**: Primary brand color
- **Corner Radius**: 12dp
- **Position**: 16dp below input
- **States**: Default, Pressed, Disabled (if key invalid), Loading

### Scan QR Code Button
- **Type**: Text Button
- **Text**: "Scan QR Code" (14sp Roboto Medium)
- **Color**: Primary color
- **Icon**: QR code icon (18dp) on left
- **Position**: 16dp below join button
- **Alignment**: Centered
- **Navigation**: → QR Code Scanner

---

## Spacing & Layout

- **Screen Margins**: 16dp on all sides
- **Icon Spacing**: 24dp from app bar
- **Text Spacing**: 16dp between title and input
- **Input Spacing**: 24dp from title
- **Button Spacing**: 16dp from input
- **Content Centering**: Vertically centered on screen

---

## States & Interactions

### Default State
- Empty session key input
- Join Session button disabled
- No error messages

### Input State
- Session key entered (auto-formatted)
- Join Session button enabled when 6 characters entered
- Real-time format validation

### Error States
- **Invalid Format**: "Session key must be 6 characters" (red)
- **Session Not Found**: "Session not found. Check the key and try again." (red)
- **Session Full**: "Session is full. Cannot join." (red)
- **Session Ended**: "Session has already ended." (red)
- **Already Joined**: "You are already in this session." (red)

### Loading State
- Join Session button shows loading spinner
- Button text: "Joining..."
- Input disabled
- No interaction possible

### Success State
- Brief success animation
- Navigate to Live Session Room

---

## QR Code Scanner

### Scanner Layout
```
┌─────────────────────────────────────────┐
│  ← Scan QR Code            [❌]        │
├─────────────────────────────────────────┤
│                                         │
│         [Camera View]                   │
│                                         │
│    Position QR code within frame        │
│                                         │
│    ┌─────────────────────────────┐    │
│    │    [Scanning Frame]          │    │
│    └─────────────────────────────┘    │
│                                         │
│    [Enter Key Manually]                 │
│                                         │
└─────────────────────────────────────────┘
```

---

## Accessibility

- **Screen Reader**: "Join session screen. Enter session key. [Key value]."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on input

---

## Navigation

- **Back Button**: → Live Sessions List
- **Join Session Button**: → Live Session Room (on success)
- **Scan QR Code**: → QR Code Scanner (returns to Join Session with key filled)
- **Error States**: Stay on screen, allow retry

---

**Wireframe Description Complete**
