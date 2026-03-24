package com.jacob_hutchens.boardgmestattracker.ui.app

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.jacob_hutchens.boardgmestattracker.data.network.model.CreateSessionRequest
import com.jacob_hutchens.boardgmestattracker.data.network.model.GameDto
import com.jacob_hutchens.boardgmestattracker.data.network.model.SessionDto
import com.jacob_hutchens.boardgmestattracker.data.network.model.UpdateUserMeRequest
import com.jacob_hutchens.boardgmestattracker.data.network.model.UserMe
import com.jacob_hutchens.boardgmestattracker.data.repository.RestRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

data class AppDataUiState(
  val loading: Boolean = false,
  val error: String? = null,
  val me: UserMe? = null,
  val games: List<GameDto> = emptyList(),
  val feedSessions: List<SessionDto> = emptyList(),
  val activeSessions: List<SessionDto> = emptyList(),
  val historySessions: List<SessionDto> = emptyList(),
  val myStats: Map<String, Any?> = emptyMap(),
  val exportPreview: String? = null,
)

class AppDataViewModel(
  private val repository: RestRepository,
) : ViewModel() {
  private val _uiState = MutableStateFlow(AppDataUiState())
  val uiState: StateFlow<AppDataUiState> = _uiState.asStateFlow()

  fun loadHome() {
    viewModelScope.launch {
      _uiState.value = _uiState.value.copy(loading = true, error = null)
      runCatching {
        val me = repository.getUserMe()
        val active = repository.getSessions(active = true, from = null, to = null, gameId = null, page = 1, limit = 20)
        _uiState.value.copy(loading = false, me = me, activeSessions = active.sessions)
      }.onSuccess { _uiState.value = it }
        .onFailure { _uiState.value = _uiState.value.copy(loading = false, error = it.message ?: "Failed to load home") }
    }
  }

  fun loadGames(search: String? = null) {
    viewModelScope.launch {
      _uiState.value = _uiState.value.copy(loading = true, error = null)
      runCatching { repository.getGames(filter = "all", search = search, page = 1, limit = 100) }
        .onSuccess { _uiState.value = _uiState.value.copy(loading = false, games = it.games) }
        .onFailure { _uiState.value = _uiState.value.copy(loading = false, error = it.message ?: "Failed to load games") }
    }
  }

  fun loadFeed() {
    viewModelScope.launch {
      _uiState.value = _uiState.value.copy(loading = true, error = null)
      runCatching { repository.getFeed(page = 1, limit = 50, since = null) }
        .onSuccess { _uiState.value = _uiState.value.copy(loading = false, feedSessions = it.sessions) }
        .onFailure { _uiState.value = _uiState.value.copy(loading = false, error = it.message ?: "Failed to load feed") }
    }
  }

  fun loadProfile() {
    viewModelScope.launch {
      _uiState.value = _uiState.value.copy(loading = true, error = null)
      runCatching { repository.getUserMe() }
        .onSuccess { _uiState.value = _uiState.value.copy(loading = false, me = it) }
        .onFailure { _uiState.value = _uiState.value.copy(loading = false, error = it.message ?: "Failed to load profile") }
    }
  }

  fun updateProfile(username: String, bio: String) {
    viewModelScope.launch {
      _uiState.value = _uiState.value.copy(loading = true, error = null)
      runCatching {
        repository.updateUserMe(UpdateUserMeRequest(username = username, bio = bio))
      }.onSuccess { _uiState.value = _uiState.value.copy(loading = false, me = it) }
        .onFailure { _uiState.value = _uiState.value.copy(loading = false, error = it.message ?: "Failed to update profile") }
    }
  }

  fun loadStats() {
    viewModelScope.launch {
      _uiState.value = _uiState.value.copy(loading = true, error = null)
      runCatching {
        val stats = repository.getMyStats().stats
        val history = repository.getSessions(active = false, from = null, to = null, gameId = null, page = 1, limit = 100)
        _uiState.value.copy(loading = false, myStats = stats, historySessions = history.sessions)
      }.onSuccess { _uiState.value = it }
        .onFailure { _uiState.value = _uiState.value.copy(loading = false, error = it.message ?: "Failed to load stats") }
    }
  }

  fun loadHistory() {
    viewModelScope.launch {
      _uiState.value = _uiState.value.copy(loading = true, error = null)
      runCatching { repository.getSessions(active = false, from = null, to = null, gameId = null, page = 1, limit = 100) }
        .onSuccess { _uiState.value = _uiState.value.copy(loading = false, historySessions = it.sessions) }
        .onFailure { _uiState.value = _uiState.value.copy(loading = false, error = it.message ?: "Failed to load history") }
    }
  }

  fun previewExport() {
    viewModelScope.launch {
      _uiState.value = _uiState.value.copy(loading = true, error = null)
      runCatching {
        repository.exportGet(
          gameIdsCsv = null,
          from = null,
          to = null,
          sessionIdsCsv = null,
          statSetIdsCsv = null,
          preview = true,
        )
      }.onSuccess {
        val text = "Sessions: ${it.sessionCount ?: 0}, Values: ${it.statValueCount ?: 0}, Estimated bytes: ${it.estimatedSizeBytes ?: 0}"
        _uiState.value = _uiState.value.copy(loading = false, exportPreview = text)
      }.onFailure {
        _uiState.value = _uiState.value.copy(loading = false, error = it.message ?: "Failed to preview export")
      }
    }
  }

  fun createSession(gameId: Long, statSetId: Long, onCreated: (Long) -> Unit) {
    viewModelScope.launch {
      _uiState.value = _uiState.value.copy(loading = true, error = null)
      runCatching {
        repository.createSession(
          CreateSessionRequest(
            gameId = gameId,
            statSetId = statSetId,
            invitedUserIds = emptyList(),
            nonAppPlayerNames = emptyList(),
          ),
        )
      }.onSuccess {
        _uiState.value = _uiState.value.copy(loading = false)
        onCreated(it.sessionId)
      }.onFailure {
        _uiState.value = _uiState.value.copy(loading = false, error = it.message ?: "Failed to create session")
      }
    }
  }
}

