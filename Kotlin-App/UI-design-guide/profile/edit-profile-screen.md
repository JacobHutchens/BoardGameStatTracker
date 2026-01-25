# Edit Profile Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Edit Profile            [Save] [❌]   │
├─────────────────────────────────────────┤
│                                         │
│         [Avatar]                        │
│         [Change Photo]                 │
│                                         │
│    ┌─────────────────────────────┐    │
│    │ Username                     │    │
│    │ ──────────────────────────── │    │
│    │ @username                    │    │
│    └─────────────────────────────┘    │
│                                         │
│    ┌─────────────────────────────┐    │
│    │ Email                        │    │
│    │ ──────────────────────────── │    │
│    │ email@example.com           │    │
│    │ (Verification required)      │    │
│    └─────────────────────────────┘    │
│                                         │
│    ┌─────────────────────────────┐    │
│    │ Bio                          │    │
│    │ ──────────────────────────── │    │
│    │ (Optional, multi-line)       │    │
│    └─────────────────────────────┘    │
│                                         │
│    ┌──────────┐  ┌──────────┐         │
│    │  Cancel  │  │   Save   │         │
│    └──────────┘  └──────────┘         │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### App Bar
- **Height**: 56dp
- **Title**: "Edit Profile" (20sp Roboto Medium)
- **Actions**: Save button (14sp Roboto Medium, primary color), Close button (24dp)

### Avatar Section
- **Avatar Size**: 100dp x 100dp
- **Position**: Centered, 24dp below app bar
- **Border**: 2dp solid (primary color or divider)
- **Change Photo Button**: Text button below avatar
- **Text**: "Change Photo" (14sp Roboto Medium, primary color)
- **Position**: 8dp below avatar

### Username Input
- **Type**: Material Design 3 Outlined Text Field
- **Height**: 56dp
- **Label**: Floating label "Username"
- **Text**: 16sp Roboto Regular
- **Prefix**: "@" symbol (always visible)
- **Validation**: Real-time duplicate check
- **Helper Text**: "✓ Available" or "✗ Username taken"
- **Position**: 24dp below change photo button

### Email Input
- **Type**: Material Design 3 Outlined Text Field
- **Height**: 56dp
- **Label**: Floating label "Email"
- **Text**: 16sp Roboto Regular
- **Validation**: Real-time format validation
- **Helper Text**: "(Verification required)" (12sp Roboto Regular, secondary color)
- **Note**: Changing email requires verification
- **Position**: 16dp below username

### Bio Input
- **Type**: Material Design 3 Outlined Text Field (Multi-line)
- **Height**: 120dp (minimum, expands)
- **Label**: Floating label "Bio" (optional)
- **Text**: 16sp Roboto Regular
- **Placeholder**: "Tell us about yourself..."
- **Max Length**: 500 characters
- **Character Count**: Shown below input (e.g., "245/500")
- **Position**: 16dp below email

### Action Buttons
- **Cancel Button**: Secondary Action Button (48dp height)
- **Save Button**: Primary Action Button (56dp height)
- **Layout**: Side by side, equal width
- **Spacing**: 8dp between buttons
- **Position**: Bottom of screen, 16dp padding

---

## Spacing & Layout

- **Screen Margins**: 16dp horizontal
- **Avatar**: 24dp below app bar
- **Input Spacing**: 16dp vertical between inputs
- **Button Spacing**: 8dp horizontal between buttons
- **Button Position**: 24dp below bio input, 16dp from bottom

---

## States & Interactions

### Default State
- Current profile data displayed
- All inputs editable
- Save button enabled
- No error messages

### Focused State
- Input field shows focused border
- Label animates to top
- Keyboard appears
- Real-time validation begins

### Validation States
- **Username**: Shows "✓ Available" or "✗ Username taken" as user types
- **Email**: Shows "✓ Valid format" or "✗ Invalid email" as user types
- **Email Change**: Shows "Verification email will be sent" message

### Error States
- Red border on input field
- Error icon (24dp) on right
- Error message below input
- Save button disabled
- Examples:
  - "Username must be 3-20 characters"
  - "Email already registered"
  - "Invalid email format"

### Loading State
- Save button shows loading spinner
- Button text: "Saving..."
- All inputs disabled
- No interaction possible

### Success State
- Brief success animation
- Navigate to My Profile screen
- Success message: "Profile updated successfully"

---

## Photo Upload

### Change Photo Flow
- **Tap Change Photo**: Open image picker
- **Options**: Camera, Gallery, Remove Photo
- **Crop**: Allow cropping to square
- **Preview**: Show preview before saving
- **Upload**: Upload to server, show progress

---

## Accessibility

- **Screen Reader**: "Edit profile. Username input. Email input. Bio input."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: All text meets WCAG AA
- **Focus Indicators**: Clear focus on all inputs

---

## Navigation

- **Back Button**: → My Profile (cancels edits)
- **Save Button**: → My Profile (saves changes)
- **Close Button (X)**: → My Profile (cancels edits)

---

**Wireframe Description Complete**
