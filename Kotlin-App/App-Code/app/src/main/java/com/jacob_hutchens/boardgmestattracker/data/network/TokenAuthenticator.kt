package com.jacob_hutchens.boardgmestattracker.data.network

import com.jacob_hutchens.boardgmestattracker.data.local.TokenStore
import com.jacob_hutchens.boardgmestattracker.data.network.model.RefreshRequest
import com.squareup.moshi.Moshi
import com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory
import kotlinx.coroutines.runBlocking
import okhttp3.Authenticator
import okhttp3.Request
import okhttp3.Response
import okhttp3.Route
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory

class TokenAuthenticator(
  private val tokenStore: TokenStore,
) : Authenticator {
  private val refreshLock = Any()

  override fun authenticate(route: Route?, response: Response): Request? {
    if (responseCount(response) >= 2) return null

    val refreshToken = tokenStore.getRefreshToken() ?: return null

    synchronized(refreshLock) {
      val latestAccess = tokenStore.getAccessToken()
      val sentAuth = response.request.header("Authorization")
      if (!latestAccess.isNullOrBlank() && sentAuth != "Bearer $latestAccess") {
        return response.request.newBuilder()
          .header("Authorization", "Bearer $latestAccess")
          .build()
      }

      val refreshApi = Retrofit.Builder()
        .baseUrl(BaseUrl.restApi())
        .addConverterFactory(
          MoshiConverterFactory.create(
            Moshi.Builder()
              .addLast(KotlinJsonAdapterFactory())
              .build()
          )
        )
        .build()
        .create(BoardGameApi::class.java)

      val refreshResponse = try {
        runBlocking { refreshApi.refresh(RefreshRequest(refreshToken)) }
      } catch (_: Throwable) {
        null
      } ?: return null

      val newAccess = refreshResponse.accessToken
      val newRefresh = refreshResponse.refreshToken ?: refreshToken
      tokenStore.saveTokens(newAccess, newRefresh)

      return response.request.newBuilder()
        .header("Authorization", "Bearer $newAccess")
        .build()
    }
  }

  private fun responseCount(response: Response): Int {
    var current: Response? = response
    var result = 1
    while (current?.priorResponse != null) {
      result++
      current = current.priorResponse
    }
    return result
  }
}

