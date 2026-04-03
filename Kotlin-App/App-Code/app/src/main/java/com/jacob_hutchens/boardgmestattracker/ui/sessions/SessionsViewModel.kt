package com.jacob_hutchens.boardgmestattracker.ui.sessions

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.jacob_hutchens.boardgmestattracker.data.network.model.SessionDto
import com.jacob_hutchens.boardgmestattracker.data.repository.RestRepository
import com.jacob_hutchens.boardgmestattracker.ui.network.toUserFacingNetworkMessageOrNull
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

data class SessionsUiState(
  val loading: Boolean = false,
  val error: String? = null,
  val sessions: List<SessionDto> = emptyList(),
  val sessionsUsedThisWeek: Int? = null,
  val sessionsLimitPerWeek: Int? = null,
)

class SessionsViewModel(
  private val repository: RestRepository,
) : ViewModel() {
  private val _uiState = MutableStateFlow(SessionsUiState(loading = true))
  val uiState: StateFlow<SessionsUiState> = _uiState.asStateFlow()

  init {
    refresh()
  }

  fun refresh() {
    viewModelScope.launch {
      _uiState.value = _uiState.value.copy(loading = true, error = null)
      runCatching {
        val me = repository.getUserMe()
        val sessions = repository.getSessions(active = true, from = null, to = null, gameId = null, page = 1, limit = 50)
        SessionsUiState(
          loading = false,
          sessions = sessions.sessions,
          sessionsUsedThisWeek = me.sessionQuota?.sessionsUsedThisWeek,
          sessionsLimitPerWeek = me.sessionQuota?.sessionsLimitPerWeek,
        )
      }.onSuccess {
        _uiState.value = it
      }.onFailure { err ->
        val msg = err.toUserFacingNetworkMessageOrNull() ?: err.message ?: "Unable to load sessions"
        _uiState.value = _uiState.value.copy(loading = false, error = msg)
      }
    }
  }

  fun joinByKey(sessionKey: String, onSuccess: (Long) -> Unit) {
    viewModelScope.launch {
      _uiState.value = _uiState.value.copy(loading = true, error = null)
      runCatching {
        repository.joinSession(com.jacob_hutchens.boardgmestattracker.data.network.model.JoinSessionRequest(sessionKey))
      }.onSuccess { session ->
        _uiState.value = _uiState.value.copy(loading = false)
        onSuccess(session.id)
      }.onFailure { err ->
        val msg = err.toUserFacingNetworkMessageOrNull() ?: err.message ?: "Join failed"
        _uiState.value = _uiState.value.copy(loading = false, error = msg)
      }
    }
  }
}

