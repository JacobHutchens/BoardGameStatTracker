# Forgot Password Screen Wireframe
## Board Game Stat Tracker

---

## Screen Layout

```
┌─────────────────────────────────────────┐
│  ← Reset Password                       │
├─────────────────────────────────────────┤
│                                         │
│         [Lock Icon]                     │
│                                         │
│    Forgot your password?                │
│    Enter your email and we'll send      │
│    you a reset link.                    │
│                                         │
│    ┌─────────────────────────────┐    │
│    │ Email                        │    │
│    │ ──────────────────────────── │    │
│    └─────────────────────────────┘    │
│                                         │
│    ┌─────────────────────────────┐    │
│    │   SEND RESET LINK            │    │
│    └─────────────────────────────┘    │
│                                         │
│    [Back to Login]                     │
│                                         │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### Lock Icon
- **Size**: 64dp x 64dp
- **Color**: Primary color or secondary color
- **Position**: Centered, 24dp below app bar

### Title Text
- **Text**: "Forgot your password?" (20sp Roboto Medium)
- **Position**: 16dp below icon
- **Alignment**: Centered

### Description Text
- **Text**: "Enter your email and we'll send you a reset link." (16sp Roboto Regular, secondary color)
- **Position**: 8dp below title
- **Alignment**: Centered
- **Max Width**: 280dp

### Email Input
- **Type**: Material Design 3 Outlined Text Field
- **Height**: 56dp
- **Label**: Floating label "Email"
- **Text**: 16sp Roboto Regular
- **Placeholder**: "Enter your email"
- **Validation**: Real-time email format validation
- **Error State**: Red border, error icon, error message
- **Position**: 24dp below description

### Send Reset Link Button
- **Type**: Primary Action Button
- **Height**: 56dp
- **Width**: Full width minus 32dp margins
- **Text**: "SEND RESET LINK" (14sp Roboto Medium, white)
- **Background**: Primary brand color
- **Corner Radius**: 12dp
- **Position**: 16dp below email input
- **States**: Default, Pressed, Disabled (if email invalid), Loading

### Back to Login Link
- **Type**: Text Button
- **Text**: "Back to Login" (14sp Roboto Medium)
- **Color**: Primary color
- **Position**: 16dp below send button
- **Alignment**: Centered

---

## Spacing & Layout

- **Screen Margins**: 16dp on all sides
- **Icon Spacing**: 24dp from app bar
- **Text Spacing**: 16dp between title and description
- **Input Spacing**: 24dp from description
- **Button Spacing**: 16dp from input
- **Content Centering**: Vertically centered on screen

---

## States & Interactions

### Default State
- Empty email field
- Send Reset Link button disabled
- No error messages

### Focused State
- Email field shows focused border
- Label animates to top
- Keyboard appears
- Button enables when valid email entered

### Error State
- Red border on email field (1dp)
- Error icon (24dp) on right
- Error message below input (12sp Roboto Regular, red)
- Examples:
  - "Invalid email format"
  - "Email not found"
- Send Reset Link button disabled

### Loading State
- Send Reset Link button shows loading spinner
- Button text: "Sending..."
- Email input disabled
- No interaction possible

### Success State
- Success message displayed
- "Reset link sent! Check your email." (16sp Roboto Regular, green)
- Email input disabled
- Option to resend link after 60 seconds

---

## Accessibility

- **Screen Reader**: "Forgot password screen. Enter your email to receive a reset link."
- **Touch Targets**: All interactive elements minimum 48dp
- **Color Contrast**: Text meets WCAG AA
- **Focus Indicators**: Clear focus rings

---

## Navigation

- **Back Button**: → Login Screen
- **Send Reset Link Button**: → Success state (stays on screen)
- **Back to Login Link**: → Login Screen

---

**Wireframe Description Complete**
