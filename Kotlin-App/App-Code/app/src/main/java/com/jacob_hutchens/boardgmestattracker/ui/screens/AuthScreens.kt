package com.jacob_hutchens.boardgmestattracker.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.jacob_hutchens.boardgmestattracker.ui.auth.AuthViewModel

@Composable
fun LoginScreen(
  viewModel: AuthViewModel,
  onNavigateRegister: () -> Unit,
  onAuthenticated: () -> Unit,
) {
  val uiState by viewModel.uiState.collectAsStateWithLifecycle()
  var emailOrUsername by remember { mutableStateOf("") }
  var password by remember { mutableStateOf("") }

  LaunchedEffect(uiState.authenticated) {
    if (uiState.authenticated) {
      viewModel.resetTransientState()
      onAuthenticated()
    }
  }

  Column(
    modifier = Modifier
      .fillMaxSize()
      .padding(16.dp),
    verticalArrangement = Arrangement.Center,
  ) {
    Text("Board Game Stat Tracker", style = MaterialTheme.typography.headlineSmall)
    Spacer(Modifier.height(20.dp))
    OutlinedTextField(
      modifier = Modifier.fillMaxWidth(),
      value = emailOrUsername,
      onValueChange = { emailOrUsername = it },
      label = { Text("Email or Username") },
    )
    Spacer(Modifier.height(12.dp))
    OutlinedTextField(
      modifier = Modifier.fillMaxWidth(),
      value = password,
      onValueChange = { password = it },
      label = { Text("Password") },
    )
    Spacer(Modifier.height(16.dp))
    uiState.error?.let {
      Text(it, color = MaterialTheme.colorScheme.error)
      Spacer(Modifier.height(8.dp))
    }
    Button(
      modifier = Modifier.fillMaxWidth(),
      enabled = !uiState.loading && emailOrUsername.isNotBlank() && password.isNotBlank(),
      onClick = { viewModel.login(emailOrUsername.trim(), password) },
    ) {
      if (uiState.loading) {
        CircularProgressIndicator(strokeWidth = 2.dp)
      } else {
        Text("LOGIN")
      }
    }
    TextButton(onClick = onNavigateRegister) {
      Text("Register")
    }
  }
}

@Composable
fun RegisterScreen(
  viewModel: AuthViewModel,
  onNavigateLogin: () -> Unit,
  onAuthenticated: () -> Unit,
) {
  val uiState by viewModel.uiState.collectAsStateWithLifecycle()
  var username by remember { mutableStateOf("") }
  var email by remember { mutableStateOf("") }
  var password by remember { mutableStateOf("") }

  LaunchedEffect(uiState.authenticated) {
    if (uiState.authenticated) {
      viewModel.resetTransientState()
      onAuthenticated()
    }
  }

  Column(
    modifier = Modifier
      .fillMaxSize()
      .padding(16.dp),
    verticalArrangement = Arrangement.Center,
  ) {
    Text("Create Account", style = MaterialTheme.typography.headlineSmall)
    Spacer(Modifier.height(20.dp))
    OutlinedTextField(
      modifier = Modifier.fillMaxWidth(),
      value = username,
      onValueChange = { username = it },
      label = { Text("Username") },
    )
    Spacer(Modifier.height(12.dp))
    OutlinedTextField(
      modifier = Modifier.fillMaxWidth(),
      value = email,
      onValueChange = { email = it },
      label = { Text("Email") },
    )
    Spacer(Modifier.height(12.dp))
    OutlinedTextField(
      modifier = Modifier.fillMaxWidth(),
      value = password,
      onValueChange = { password = it },
      label = { Text("Password") },
    )
    Spacer(Modifier.height(16.dp))
    uiState.error?.let {
      Text(it, color = MaterialTheme.colorScheme.error)
      Spacer(Modifier.height(8.dp))
    }
    Button(
      modifier = Modifier.fillMaxWidth(),
      enabled = !uiState.loading && username.isNotBlank() && email.isNotBlank() && password.isNotBlank(),
      onClick = { viewModel.register(username.trim(), email.trim(), password) },
    ) {
      if (uiState.loading) {
        CircularProgressIndicator(strokeWidth = 2.dp)
      } else {
        Text("CREATE ACCOUNT")
      }
    }
    TextButton(onClick = onNavigateLogin) {
      Text("Back to Login")
    }
  }
}

