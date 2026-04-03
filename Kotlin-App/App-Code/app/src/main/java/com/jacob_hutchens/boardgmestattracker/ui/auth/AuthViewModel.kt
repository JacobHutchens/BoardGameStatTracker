package com.jacob_hutchens.boardgmestattracker.ui.auth

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.jacob_hutchens.boardgmestattracker.data.local.TokenStore
import com.jacob_hutchens.boardgmestattracker.data.network.model.LoginRequest
import com.jacob_hutchens.boardgmestattracker.data.network.model.ApiErrorBody
import com.jacob_hutchens.boardgmestattracker.data.network.model.RegisterRequest
import com.jacob_hutchens.boardgmestattracker.data.repository.RestRepository
import com.jacob_hutchens.boardgmestattracker.ui.auth.passwordValidationError
import com.jacob_hutchens.boardgmestattracker.ui.network.toUserFacingNetworkMessageOrNull
import com.squareup.moshi.Moshi
import com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import retrofit2.HttpException

data class AuthUiState(
  val loading: Boolean = false,
  val error: String? = null,
  val authenticated: Boolean = false,
)

class AuthViewModel(
  private val repository: RestRepository,
  private val tokenStore: TokenStore,
) : ViewModel() {
  private val _uiState = MutableStateFlow(AuthUiState())
  val uiState: StateFlow<AuthUiState> = _uiState.asStateFlow()

  private val moshi: Moshi = Moshi.Builder()
    .addLast(KotlinJsonAdapterFactory())
    .build()

  private fun Throwable.toApiErrorMessageOrNull(): String? {
    val http = this as? HttpException ?: return null
    val errorBody = http.response()?.errorBody()?.string() ?: return null
    val adapter = moshi.adapter(ApiErrorBody::class.java)
    val parsed = adapter.fromJson(errorBody)
    return parsed?.error?.message ?: parsed?.details?.firstOrNull()
  }

  fun login(emailOrUsername: String, password: String) {
    viewModelScope.launch {
      _uiState.value = AuthUiState(loading = true)
      runCatching {
        repository.login(LoginRequest(emailOrUsername, password))
      }.onSuccess { auth ->
        tokenStore.saveTokens(auth.accessToken, auth.refreshToken)
        _uiState.value = AuthUiState(authenticated = true)
      }.onFailure { err ->
        val apiMsg = err.toApiErrorMessageOrNull()
        val netMsg = err.toUserFacingNetworkMessageOrNull()
        _uiState.value = AuthUiState(error = apiMsg ?: netMsg ?: err.message ?: "Login failed")
      }
    }
  }

  fun register(username: String, email: String, password: String) {
    viewModelScope.launch {
      _uiState.value = AuthUiState(loading = true)
      passwordValidationError(password)?.let { localError ->
        _uiState.value = AuthUiState(loading = false, error = localError)
        return@launch
      }
      runCatching {
        repository.register(RegisterRequest(username, email, password))
      }.onSuccess { auth ->
        tokenStore.saveTokens(auth.accessToken, auth.refreshToken)
        _uiState.value = AuthUiState(authenticated = true)
      }.onFailure { err ->
        val apiMsg = err.toApiErrorMessageOrNull()
        val netMsg = err.toUserFacingNetworkMessageOrNull()
        _uiState.value = AuthUiState(error = apiMsg ?: netMsg ?: err.message ?: "Registration failed")
      }
    }
  }

  fun resetTransientState() {
    _uiState.value = _uiState.value.copy(error = null, authenticated = false, loading = false)
  }
}

