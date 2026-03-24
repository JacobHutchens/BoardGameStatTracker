package com.jacob_hutchens.boardgmestattracker.ui.auth

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.jacob_hutchens.boardgmestattracker.data.local.TokenStore
import com.jacob_hutchens.boardgmestattracker.data.network.model.LoginRequest
import com.jacob_hutchens.boardgmestattracker.data.network.model.RegisterRequest
import com.jacob_hutchens.boardgmestattracker.data.repository.RestRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

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

  fun login(emailOrUsername: String, password: String) {
    viewModelScope.launch {
      _uiState.value = AuthUiState(loading = true)
      runCatching {
        repository.login(LoginRequest(emailOrUsername, password))
      }.onSuccess { auth ->
        tokenStore.saveTokens(auth.accessToken, auth.refreshToken)
        _uiState.value = AuthUiState(authenticated = true)
      }.onFailure { err ->
        _uiState.value = AuthUiState(error = err.message ?: "Login failed")
      }
    }
  }

  fun register(username: String, email: String, password: String) {
    viewModelScope.launch {
      _uiState.value = AuthUiState(loading = true)
      runCatching {
        repository.register(RegisterRequest(username, email, password))
      }.onSuccess { auth ->
        tokenStore.saveTokens(auth.accessToken, auth.refreshToken)
        _uiState.value = AuthUiState(authenticated = true)
      }.onFailure { err ->
        _uiState.value = AuthUiState(error = err.message ?: "Registration failed")
      }
    }
  }

  fun resetTransientState() {
    _uiState.value = _uiState.value.copy(error = null, authenticated = false, loading = false)
  }
}

