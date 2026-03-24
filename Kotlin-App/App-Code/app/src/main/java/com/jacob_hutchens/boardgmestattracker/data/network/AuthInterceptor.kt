package com.jacob_hutchens.boardgmestattracker.data.network

import com.jacob_hutchens.boardgmestattracker.data.local.TokenStore
import okhttp3.Interceptor
import okhttp3.Response

class AuthInterceptor(
  private val tokenStore: TokenStore,
) : Interceptor {
  override fun intercept(chain: Interceptor.Chain): Response {
    val request = chain.request()
    val path = request.url.encodedPath
    val isAuthEndpoint = path.contains("/auth/login") ||
      path.contains("/auth/register") ||
      path.contains("/auth/refresh") ||
      path.contains("/auth/forgot-password") ||
      path.contains("/auth/reset-password")

    if (isAuthEndpoint) {
      return chain.proceed(request)
    }

    val token = tokenStore.getAccessToken()
    if (token.isNullOrBlank()) {
      return chain.proceed(request)
    }

    val authenticated = request.newBuilder()
      .addHeader("Authorization", "Bearer $token")
      .build()

    return chain.proceed(authenticated)
  }
}

