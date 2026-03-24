package com.jacob_hutchens.boardgmestattracker.data.local

import android.content.Context
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

class TokenStore(context: Context) {
  private val sharedPrefs = EncryptedSharedPreferences.create(
    context,
    PREF_FILE,
    MasterKey.Builder(context).setKeyScheme(MasterKey.KeyScheme.AES256_GCM).build(),
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM,
  )

  fun getAccessToken(): String? = sharedPrefs.getString(KEY_ACCESS, null)

  fun getRefreshToken(): String? = sharedPrefs.getString(KEY_REFRESH, null)

  fun saveTokens(accessToken: String, refreshToken: String?) {
    sharedPrefs.edit()
      .putString(KEY_ACCESS, accessToken)
      .apply {
        if (refreshToken != null) putString(KEY_REFRESH, refreshToken)
      }
      .apply()
  }

  fun clear() {
    sharedPrefs.edit().clear().apply()
  }

  private companion object {
    const val PREF_FILE = "auth_secure_store"
    const val KEY_ACCESS = "access_token"
    const val KEY_REFRESH = "refresh_token"
  }
}

