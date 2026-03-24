package com.jacob_hutchens.boardgmestattracker.ui.screens

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.jacob_hutchens.boardgmestattracker.ui.sessions.SessionRoomViewModel
import com.jacob_hutchens.boardgmestattracker.ui.sessions.SessionsViewModel

@Composable
@OptIn(ExperimentalMaterial3Api::class)
fun LiveSessionsScreen(
  viewModel: SessionsViewModel,
  onCreateSession: () -> Unit,
  onOpenSession: (Long) -> Unit,
) {
  val uiState by viewModel.uiState.collectAsStateWithLifecycle()
  var joinKey by remember { mutableStateOf("") }

  Scaffold(
    topBar = {
      TopAppBar(
        title = {
          val used = uiState.sessionsUsedThisWeek ?: 0
          val limit = uiState.sessionsLimitPerWeek?.toString() ?: "∞"
          Text("Live Sessions  $used/$limit this week")
        },
        actions = {
          IconButton(onClick = { viewModel.refresh() }) {
            Icon(Icons.Default.Refresh, contentDescription = "Refresh")
          }
        },
      )
    },
  ) { padding ->
    Column(
      modifier = Modifier
        .fillMaxSize()
        .padding(padding)
        .padding(16.dp),
    ) {
      if (uiState.loading) {
        CircularProgressIndicator()
      }
      uiState.error?.let {
        Text(it, color = MaterialTheme.colorScheme.error)
        Spacer(Modifier.height(8.dp))
      }
      Text("Active Sessions", style = MaterialTheme.typography.titleMedium)
      Spacer(Modifier.height(8.dp))
      LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.weight(1f)) {
        items(uiState.sessions) { session ->
          Card(
            modifier = Modifier
              .fillMaxWidth()
              .clickable { onOpenSession(session.id) },
          ) {
            Column(Modifier.padding(16.dp)) {
              Text(session.game?.get("gameName")?.toString() ?: "Session #${session.id}")
              val players = session.players.size
              val round = session.currentRound ?: 0
              Text("$players players • Round $round", style = MaterialTheme.typography.bodySmall)
            }
          }
        }
      }
      Spacer(Modifier.height(12.dp))
      Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        OutlinedTextField(
          modifier = Modifier.weight(1f),
          value = joinKey,
          onValueChange = { joinKey = it },
          label = { Text("Enter session key") },
        )
        Button(
          enabled = joinKey.isNotBlank() && !uiState.loading,
          onClick = {
            viewModel.joinByKey(joinKey.trim()) { onOpenSession(it) }
          },
        ) {
          Text("Join")
        }
      }
      Spacer(Modifier.height(8.dp))
      Button(
        modifier = Modifier.fillMaxWidth(),
        onClick = onCreateSession,
      ) {
        Icon(Icons.Default.Add, contentDescription = null)
        Spacer(Modifier.height(0.dp))
        Text("+ Create New Session")
      }
    }
  }
}

@Composable
@OptIn(ExperimentalMaterial3Api::class)
fun SessionRoomScreen(
  viewModel: SessionRoomViewModel,
  sessionId: Long,
) {
  val uiState by viewModel.uiState.collectAsStateWithLifecycle()
  LaunchedEffect(sessionId) {
    viewModel.loadSession(sessionId)
  }

  Scaffold(
    topBar = {
      TopAppBar(title = { Text("Live Session Room") })
    },
  ) { padding ->
    Column(
      modifier = Modifier
        .fillMaxSize()
        .padding(padding)
        .padding(16.dp),
    ) {
      when {
        uiState.loading -> CircularProgressIndicator()
        uiState.error != null -> Text(uiState.error ?: "Unknown error", color = MaterialTheme.colorScheme.error)
        uiState.session != null -> {
          val session = uiState.session!!
          Text(session.game?.get("gameName")?.toString() ?: "Session #${session.id}", style = MaterialTheme.typography.titleLarge)
          Text("Round ${session.currentRound ?: 0}", style = MaterialTheme.typography.bodyMedium)
          Spacer(Modifier.height(12.dp))
          Text("Players", style = MaterialTheme.typography.titleMedium)
          Spacer(Modifier.height(8.dp))
          session.players.forEach { player ->
            Card(modifier = Modifier.fillMaxWidth().padding(bottom = 8.dp)) {
              Column(Modifier.padding(12.dp)) {
                Text(player.playerName ?: "Player")
                Text(if (player.isSpectator) "Spectator" else "Player", style = MaterialTheme.typography.bodySmall)
              }
            }
          }
          Spacer(Modifier.height(8.dp))
          Text("Tracked Stats: ${session.trackedStats.size}")
        }
      }
    }
  }
}

