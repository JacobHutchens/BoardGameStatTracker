import java.io.File

plugins {
  id("com.android.application")
  id("org.jetbrains.kotlin.android")
  id("org.jetbrains.kotlin.plugin.compose")
}

fun loadEnvFile(file: File): Map<String, String> {
  if (!file.exists()) return emptyMap()
  val out = mutableMapOf<String, String>()
  file.forEachLine { rawLine ->
    val line = rawLine.trim()
    if (line.isBlank() || line.startsWith("#")) return@forEachLine
    val idx = line.indexOf('=')
    if (idx <= 0) return@forEachLine
    val key = line.substring(0, idx).trim()
    val value = line.substring(idx + 1).trim()
    if (key.isNotBlank()) out[key] = value
  }
  return out
}

val envFile = rootProject.file(".env").takeIf { it.exists() } ?: rootProject.file(".env.example")
val env = loadEnvFile(envFile)

val restApiBaseUrl = env["REST_API_BASE_URL"] ?: "https://boardgamestattracker.example.com/api/v1"
val wsBaseUrl = env["WS_BASE_URL"] ?: "wss://boardgamestattracker.example.com/ws"

android {
  namespace = "com.jacob_hutchens.boardgmestattracker"
  compileSdk = 35

  defaultConfig {
    applicationId = "com.jacob_hutchens.boardgmestattracker"
    minSdk = 26
    targetSdk = 35

    versionCode = 1
    versionName = "1.0"

    // Build-time constants sourced from Kotlin-App/App-Code/.env (fallback: .env.example).
    buildConfigField(
      "String",
      "REST_API_BASE_URL",
      "\"$restApiBaseUrl\""
    )
    buildConfigField(
      "String",
      "WS_BASE_URL",
      "\"$wsBaseUrl\""
    )
  }

  buildTypes {
    release {
      isMinifyEnabled = false
    }
  }

  buildFeatures {
    compose = true
    buildConfig = true
  }

  compileOptions {
    sourceCompatibility = JavaVersion.VERSION_17
    targetCompatibility = JavaVersion.VERSION_17
  }

  kotlinOptions {
    jvmTarget = "17"
  }
}

dependencies {
  val composeBom = platform("androidx.compose:compose-bom:2025.02.00")
  implementation(composeBom)
  androidTestImplementation(composeBom)

  implementation("androidx.compose.material3:material3")
  implementation("androidx.compose.ui:ui")
  implementation("androidx.compose.ui:ui-tooling-preview")
  debugImplementation("androidx.compose.ui:ui-tooling")

  implementation("androidx.activity:activity-compose:1.10.0")
  implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.8.7")
  implementation("androidx.lifecycle:lifecycle-viewmodel-ktx:2.8.7")
  implementation("androidx.lifecycle:lifecycle-runtime-compose:2.8.7")
  implementation("androidx.navigation:navigation-compose:2.8.8")
  implementation("androidx.compose.material:material-icons-extended")
  implementation("androidx.core:core-ktx:1.15.0")

  implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.10.1")

  implementation("com.squareup.retrofit2:retrofit:2.11.0")
  implementation("com.squareup.retrofit2:converter-moshi:2.11.0")
  implementation("com.squareup.okhttp3:okhttp:4.12.0")
  implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")
  implementation("com.squareup.moshi:moshi-kotlin:1.15.2")

  implementation("androidx.security:security-crypto-ktx:1.1.0-alpha06")
  implementation("com.google.android.material:material:1.12.0")
}
