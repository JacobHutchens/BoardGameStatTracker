package com.jacob_hutchens.boardgmestattracker

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.tooling.preview.Preview
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.jacob_hutchens.boardgmestattracker.ui.AppViewModelFactory
import com.jacob_hutchens.boardgmestattracker.ui.app.AppDataViewModel
import com.jacob_hutchens.boardgmestattracker.ui.auth.AuthViewModel
import com.jacob_hutchens.boardgmestattracker.ui.screens.CreateSessionScreen
import com.jacob_hutchens.boardgmestattracker.ui.screens.ExportScreen
import com.jacob_hutchens.boardgmestattracker.ui.screens.FeedScreen
import com.jacob_hutchens.boardgmestattracker.ui.screens.HomeScreen
import com.jacob_hutchens.boardgmestattracker.ui.screens.LibraryScreen
import com.jacob_hutchens.boardgmestattracker.ui.screens.LiveSessionsScreen
import com.jacob_hutchens.boardgmestattracker.ui.screens.LoginScreen
import com.jacob_hutchens.boardgmestattracker.ui.screens.ProfileScreen
import com.jacob_hutchens.boardgmestattracker.ui.screens.RegisterScreen
import com.jacob_hutchens.boardgmestattracker.ui.screens.SessionHistoryScreen
import com.jacob_hutchens.boardgmestattracker.ui.screens.SessionRoomScreen
import com.jacob_hutchens.boardgmestattracker.ui.screens.SettingsScreen
import com.jacob_hutchens.boardgmestattracker.ui.screens.StatsScreen
import com.jacob_hutchens.boardgmestattracker.ui.sessions.SessionRoomViewModel
import com.jacob_hutchens.boardgmestattracker.ui.sessions.SessionsViewModel

class MainActivity : ComponentActivity() {
  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    setContent {
      MaterialTheme {
        AppContent()
      }
    }
  }
}

@Composable
private fun AppContent() {
  val nav = rememberNavController()
  val factory = AppViewModelFactory(androidx.compose.ui.platform.LocalContext.current.applicationContext as android.app.Application)
  val authViewModel: AuthViewModel = viewModel(factory = factory)
  val sessionsViewModel: SessionsViewModel = viewModel(factory = factory)
  val sessionRoomViewModel: SessionRoomViewModel = viewModel(factory = factory)
  val appDataViewModel: AppDataViewModel = viewModel(factory = factory)

  NavHost(navController = nav, startDestination = "login") {
    composable("login") {
      LoginScreen(
        viewModel = authViewModel,
        onNavigateRegister = { nav.navigate("register") },
        onAuthenticated = {
          nav.navigate("home") {
            popUpTo("login") { inclusive = true }
          }
        },
      )
    }
    composable("register") {
      RegisterScreen(
        viewModel = authViewModel,
        onNavigateLogin = { nav.popBackStack() },
        onAuthenticated = {
          nav.navigate("home") {
            popUpTo("login") { inclusive = true }
          }
        },
      )
    }
    composable("home") {
      HomeScreen(
        viewModel = appDataViewModel,
        onGoSessions = { nav.navigate("sessions") },
        onGoLibrary = { nav.navigate("library") },
        onGoFeed = { nav.navigate("feed") },
        onGoProfile = { nav.navigate("profile") },
        onGoStats = { nav.navigate("stats") },
      )
    }
    composable("library") {
      LibraryScreen(
        viewModel = appDataViewModel,
        onOpenCreateSession = { nav.navigate("create_session") },
      )
    }
    composable("feed") {
      FeedScreen(viewModel = appDataViewModel)
    }
    composable("profile") {
      ProfileScreen(
        viewModel = appDataViewModel,
        onOpenSettings = { nav.navigate("settings") },
      )
    }
    composable("stats") {
      StatsScreen(
        viewModel = appDataViewModel,
        onOpenHistory = { nav.navigate("history") },
        onOpenExport = { nav.navigate("export") },
      )
    }
    composable("sessions") {
      LiveSessionsScreen(
        viewModel = sessionsViewModel,
        onCreateSession = { nav.navigate("create_session") },
        onOpenSession = { sessionId -> nav.navigate("session/$sessionId") },
      )
    }
    composable("create_session") {
      CreateSessionScreen(
        viewModel = appDataViewModel,
        onCreated = { sessionId -> nav.navigate("session/$sessionId") },
      )
    }
    composable("history") {
      SessionHistoryScreen(viewModel = appDataViewModel)
    }
    composable("export") {
      ExportScreen(viewModel = appDataViewModel)
    }
    composable("settings") {
      SettingsScreen(onGoHome = { nav.navigate("home") })
    }
    composable(
      route = "session/{sessionId}",
      arguments = listOf(navArgument("sessionId") { type = NavType.LongType }),
    ) { backStackEntry ->
      val sessionId = backStackEntry.arguments?.getLong("sessionId") ?: return@composable
      SessionRoomScreen(
        viewModel = sessionRoomViewModel,
        sessionId = sessionId,
      )
    }
  }
}

@Preview(showBackground = true)
@Composable
private fun AppContentPreview() {
  AppContent()
}

