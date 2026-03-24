package com.jacob_hutchens.boardgmestattracker.ui

import android.app.Application
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.jacob_hutchens.boardgmestattracker.data.network.NetworkModule
import com.jacob_hutchens.boardgmestattracker.data.repository.RestRepository
import com.jacob_hutchens.boardgmestattracker.ui.auth.AuthViewModel
import com.jacob_hutchens.boardgmestattracker.ui.app.AppDataViewModel
import com.jacob_hutchens.boardgmestattracker.ui.sessions.SessionRoomViewModel
import com.jacob_hutchens.boardgmestattracker.ui.sessions.SessionsViewModel

class AppViewModelFactory(
  private val application: Application,
) : ViewModelProvider.Factory {
  private val repo: RestRepository by lazy {
    RestRepository(NetworkModule.api(application))
  }

  @Suppress("UNCHECKED_CAST")
  override fun <T : ViewModel> create(modelClass: Class<T>): T {
    return when {
      modelClass.isAssignableFrom(AuthViewModel::class.java) -> {
        AuthViewModel(
          repository = repo,
          tokenStore = NetworkModule.tokenStore(application),
        ) as T
      }
      modelClass.isAssignableFrom(SessionsViewModel::class.java) -> {
        SessionsViewModel(repository = repo) as T
      }
      modelClass.isAssignableFrom(SessionRoomViewModel::class.java) -> {
        SessionRoomViewModel(repository = repo) as T
      }
      modelClass.isAssignableFrom(AppDataViewModel::class.java) -> {
        AppDataViewModel(repository = repo) as T
      }
      else -> error("Unknown ViewModel class: ${modelClass.name}")
    }
  }
}

