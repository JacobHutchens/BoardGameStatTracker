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
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
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
import com.jacob_hutchens.boardgmestattracker.ui.app.AppDataViewModel

@Composable
fun HomeScreen(
  viewModel: AppDataViewModel,
  onGoSessions: () -> Unit,
  onGoLibrary: () -> Unit,
  onGoFeed: () -> Unit,
  onGoProfile: () -> Unit,
  onGoStats: () -> Unit,
) {
  val ui by viewModel.uiState.collectAsStateWithLifecycle()
  LaunchedEffect(Unit) { viewModel.loadHome() }
  ScreenFrame("Home Dashboard") {
    if (ui.loading) CircularProgressIndicator()
    ui.error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
    Text("Welcome ${ui.me?.username ?: ""}")
    Text("Sessions this week: ${ui.me?.sessionQuota?.sessionsUsedThisWeek ?: 0}")
    Spacer(Modifier.height(8.dp))
    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
      Button(onClick = onGoSessions) { Text("Sessions") }
      Button(onClick = onGoLibrary) { Text("Library") }
    }
    Spacer(Modifier.height(8.dp))
    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
      Button(onClick = onGoFeed) { Text("Feed") }
      Button(onClick = onGoProfile) { Text("Profile") }
      Button(onClick = onGoStats) { Text("Stats") }
    }
  }
}

@Composable
fun LibraryScreen(
  viewModel: AppDataViewModel,
  onOpenCreateSession: () -> Unit,
) {
  val ui by viewModel.uiState.collectAsStateWithLifecycle()
  var search by remember { mutableStateOf("") }
  LaunchedEffect(Unit) { viewModel.loadGames() }
  ScreenFrame("Game Library") {
    OutlinedTextField(
      value = search,
      onValueChange = { search = it },
      label = { Text("Search games") },
      modifier = Modifier.fillMaxWidth(),
    )
    Spacer(Modifier.height(8.dp))
    Button(onClick = { viewModel.loadGames(search.ifBlank { null }) }) { Text("Search") }
    Spacer(Modifier.height(8.dp))
    Button(onClick = onOpenCreateSession) { Text("Create Session") }
    Spacer(Modifier.height(8.dp))
    if (ui.loading) CircularProgressIndicator()
    ui.error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
    LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
      items(ui.games) { game ->
        Column(Modifier.fillMaxWidth().clickable { }.padding(8.dp)) {
          Text(game.gameName, style = MaterialTheme.typography.titleMedium)
          Text("${game.minPlayerCount}-${game.maxPlayerCount} players", style = MaterialTheme.typography.bodySmall)
        }
      }
    }
  }
}

@Composable
fun FeedScreen(viewModel: AppDataViewModel) {
  val ui by viewModel.uiState.collectAsStateWithLifecycle()
  LaunchedEffect(Unit) { viewModel.loadFeed() }
  ScreenFrame("Following Feed") {
    if (ui.loading) CircularProgressIndicator()
    ui.error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
    LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
      items(ui.feedSessions) { session ->
        Column(Modifier.fillMaxWidth().padding(8.dp)) {
          Text(session.game?.get("gameName")?.toString() ?: "Session ${session.id}")
          Text("Players: ${session.players.size}", style = MaterialTheme.typography.bodySmall)
        }
      }
    }
  }
}

@Composable
fun ProfileScreen(
  viewModel: AppDataViewModel,
  onOpenSettings: () -> Unit,
) {
  val ui by viewModel.uiState.collectAsStateWithLifecycle()
  var username by remember { mutableStateOf("") }
  var bio by remember { mutableStateOf("") }
  LaunchedEffect(Unit) { viewModel.loadProfile() }
  LaunchedEffect(ui.me?.id) {
    username = ui.me?.username ?: ""
    bio = ui.me?.bio ?: ""
  }
  ScreenFrame("My Profile") {
    if (ui.loading) CircularProgressIndicator()
    ui.error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
    Text("Email: ${ui.me?.email ?: ""}")
    Spacer(Modifier.height(8.dp))
    OutlinedTextField(value = username, onValueChange = { username = it }, label = { Text("Username") }, modifier = Modifier.fillMaxWidth())
    Spacer(Modifier.height(8.dp))
    OutlinedTextField(value = bio, onValueChange = { bio = it }, label = { Text("Bio") }, modifier = Modifier.fillMaxWidth())
    Spacer(Modifier.height(8.dp))
    Button(onClick = { viewModel.updateProfile(username, bio) }) { Text("Save Profile") }
    TextButton(onClick = onOpenSettings) { Text("Open Settings") }
  }
}

@Composable
fun StatsScreen(
  viewModel: AppDataViewModel,
  onOpenHistory: () -> Unit,
  onOpenExport: () -> Unit,
) {
  val ui by viewModel.uiState.collectAsStateWithLifecycle()
  LaunchedEffect(Unit) { viewModel.loadStats() }
  ScreenFrame("Stats Dashboard") {
    if (ui.loading) CircularProgressIndicator()
    ui.error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
    Text("My Stats Entries: ${ui.myStats.size}")
    Text("History Sessions: ${ui.historySessions.size}")
    Spacer(Modifier.height(8.dp))
    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
      Button(onClick = onOpenHistory) { Text("Session History") }
      Button(onClick = onOpenExport) { Text("Export Stats") }
    }
  }
}

@Composable
fun SessionHistoryScreen(viewModel: AppDataViewModel) {
  val ui by viewModel.uiState.collectAsStateWithLifecycle()
  LaunchedEffect(Unit) { viewModel.loadHistory() }
  ScreenFrame("Session History") {
    if (ui.loading) CircularProgressIndicator()
    ui.error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
    LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
      items(ui.historySessions) { session ->
        Column(Modifier.fillMaxWidth().padding(8.dp)) {
          Text(session.game?.get("gameName")?.toString() ?: "Session ${session.id}")
          Text("Started: ${session.timeStarted ?: "-"}", style = MaterialTheme.typography.bodySmall)
          Text("Ended: ${session.timeEnded ?: "-"}", style = MaterialTheme.typography.bodySmall)
        }
      }
    }
  }
}

@Composable
fun ExportScreen(viewModel: AppDataViewModel) {
  val ui by viewModel.uiState.collectAsStateWithLifecycle()
  ScreenFrame("Export Stats") {
    if (ui.loading) CircularProgressIndicator()
    ui.error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
    Button(onClick = { viewModel.previewExport() }) { Text("Preview Export") }
    Spacer(Modifier.height(8.dp))
    Text(ui.exportPreview ?: "No preview yet")
  }
}

@Composable
fun SettingsScreen(
  onGoHome: () -> Unit,
) {
  ScreenFrame("Settings") {
    Text("Settings placeholders wired. Add privacy/notifications/export sub-screens next.")
    Spacer(Modifier.height(8.dp))
    Button(onClick = onGoHome) { Text("Back Home") }
  }
}

@Composable
fun CreateSessionScreen(
  viewModel: AppDataViewModel,
  onCreated: (Long) -> Unit,
) {
  val ui by viewModel.uiState.collectAsStateWithLifecycle()
  var gameId by remember { mutableStateOf("") }
  var statSetId by remember { mutableStateOf("") }
  ScreenFrame("Create Session") {
    ui.error?.let { Text(it, color = MaterialTheme.colorScheme.error) }
    if (ui.loading) CircularProgressIndicator()
    OutlinedTextField(gameId, { gameId = it }, label = { Text("Game ID") }, modifier = Modifier.fillMaxWidth())
    Spacer(Modifier.height(8.dp))
    OutlinedTextField(statSetId, { statSetId = it }, label = { Text("Stat Set ID") }, modifier = Modifier.fillMaxWidth())
    Spacer(Modifier.height(8.dp))
    Button(
      enabled = gameId.toLongOrNull() != null && statSetId.toLongOrNull() != null && !ui.loading,
      onClick = {
        viewModel.createSession(gameId.toLong(), statSetId.toLong(), onCreated)
      },
    ) { Text("Create") }
  }
}

@Composable
@OptIn(ExperimentalMaterial3Api::class)
private fun ScreenFrame(
  title: String,
  content: @Composable () -> Unit,
) {
  Scaffold(topBar = { TopAppBar(title = { Text(title) }) }) { padding ->
    Column(
      modifier = Modifier
        .fillMaxSize()
        .padding(padding)
        .padding(16.dp),
      verticalArrangement = Arrangement.Top,
    ) {
      content()
    }
  }
}

