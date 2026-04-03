package com.jacob_hutchens.boardgmestattracker.ui.auth

/**
 * Mirrors the backend password validation rules so we fail fast on-device
 * and can show the exact same error message as the API.
 */
internal fun passwordValidationError(password: String): String? {
  if (password.length < 8) return "Password must be at least 8 characters long."
  if (!password.any { it.isUpperCase() }) return "Password must contain at least one uppercase letter."
  if (!password.any { it.isDigit() }) return "Password must contain at least one number."
  if (!password.any { !it.isLetterOrDigit() }) return "Password must contain at least one special character."
  return null
}

