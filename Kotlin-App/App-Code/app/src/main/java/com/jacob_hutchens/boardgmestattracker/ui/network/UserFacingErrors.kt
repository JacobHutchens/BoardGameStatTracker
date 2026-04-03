package com.jacob_hutchens.boardgmestattracker.ui.network

import java.io.IOException
import java.net.ConnectException
import java.net.SocketTimeoutException
import java.net.UnknownHostException

internal fun Throwable.toUserFacingNetworkMessageOrNull(): String? {
  return when (this) {
    is SocketTimeoutException -> "Request timed out. The server may be unavailable (or the database may be offline). Please try again."
    is UnknownHostException -> "Can’t reach the server. Check your internet connection and the API base URL."
    is ConnectException -> "Can’t connect to the server. Please try again later."
    is IOException -> "Network error while contacting the server. Please try again."
    else -> null
  }
}

