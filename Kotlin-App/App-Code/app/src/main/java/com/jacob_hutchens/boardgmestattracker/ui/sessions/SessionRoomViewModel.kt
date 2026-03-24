package com.jacob_hutchens.boardgmestattracker.ui.sessions

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.jacob_hutchens.boardgmestattracker.data.network.model.SessionDto
import com.jacob_hutchens.boardgmestattracker.data.repository.RestRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

data class SessionRoomUiState(
  val loading: Boolean = false,
  val error: String? = null,
  val session: SessionDto? = null,
)

class SessionRoomViewModel(
  private val repository: RestRepository,
) : ViewModel() {
  private val _uiState = MutableStateFlow(SessionRoomUiState(loading = true))
  val uiState: StateFlow<SessionRoomUiState> = _uiState.asStateFlow()

  fun loadSession(sessionId: Long) {
    viewModelScope.launch {
      _uiState.value = SessionRoomUiState(loading = true)
      runCatching {
        repository.getSession(sessionId)
      }.onSuccess { session ->
        _uiState.value = SessionRoomUiState(session = session)
      }.onFailure { err ->
        _uiState.value = SessionRoomUiState(error = err.message ?: "Unable to load session")
      }
    }
  }
}

