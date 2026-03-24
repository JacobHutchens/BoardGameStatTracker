package com.jacob_hutchens.boardgmestattracker.data.network

import com.jacob_hutchens.boardgmestattracker.Env

object BaseUrl {
  fun restApi(): String = ensureTrailingSlash(Env.restApiBaseUrl)

  private fun ensureTrailingSlash(raw: String): String {
    val trimmed = raw.trim()
    return if (trimmed.endsWith("/")) trimmed else "$trimmed/"
  }
}

