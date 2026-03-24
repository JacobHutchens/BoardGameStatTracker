package com.jacob_hutchens.boardgmestattracker.data.network

import android.content.Context
import com.jacob_hutchens.boardgmestattracker.data.local.TokenStore
import com.squareup.moshi.Moshi
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory
import java.util.concurrent.TimeUnit

object NetworkModule {
  @Volatile
  private var api: BoardGameApi? = null

  @Volatile
  private var tokenStore: TokenStore? = null

  fun tokenStore(context: Context): TokenStore {
    return tokenStore ?: synchronized(this) {
      tokenStore ?: TokenStore(context.applicationContext).also { tokenStore = it }
    }
  }

  fun api(context: Context): BoardGameApi {
    return api ?: synchronized(this) {
      api ?: createApi(context.applicationContext).also { api = it }
    }
  }

  private fun createApi(context: Context): BoardGameApi {
    val tokens = tokenStore(context)
    val logging = HttpLoggingInterceptor().apply {
      level = HttpLoggingInterceptor.Level.BODY
    }

    val okHttp = OkHttpClient.Builder()
      .connectTimeout(30, TimeUnit.SECONDS)
      .readTimeout(30, TimeUnit.SECONDS)
      .writeTimeout(30, TimeUnit.SECONDS)
      .addInterceptor(AuthInterceptor(tokens))
      .authenticator(TokenAuthenticator(tokens))
      .addInterceptor(logging)
      .build()

    val moshi = Moshi.Builder().build()

    return Retrofit.Builder()
      .baseUrl(BaseUrl.restApi())
      .client(okHttp)
      .addConverterFactory(MoshiConverterFactory.create(moshi))
      .build()
      .create(BoardGameApi::class.java)
  }
}

