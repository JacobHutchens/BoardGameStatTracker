pluginManagement {
  repositories {
    google()
    mavenCentral()
    gradlePluginPortal()
  }
  plugins {
    id("com.android.application") version "8.13.2" apply false
    id("org.jetbrains.kotlin.android") version "2.1.10" apply false
    id("org.jetbrains.kotlin.plugin.compose") version "2.1.10" apply false
  }
}

dependencyResolutionManagement {
  repositories {
    google()
    mavenCentral()
  }
}

rootProject.name = "BoardGameStatTracker"
include(":app")
