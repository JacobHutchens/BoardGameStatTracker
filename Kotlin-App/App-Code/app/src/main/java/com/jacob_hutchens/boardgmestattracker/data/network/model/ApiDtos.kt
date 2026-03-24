package com.jacob_hutchens.boardgmestattracker.data.network.model

import com.squareup.moshi.JsonClass

@JsonClass(generateAdapter = true)
data class ApiErrorBody(
  val error: ApiError? = null,
  val details: List<String> = emptyList(),
)

@JsonClass(generateAdapter = true)
data class ApiError(
  val code: String? = null,
  val message: String? = null,
)

@JsonClass(generateAdapter = true)
data class LoginRequest(
  val emailOrUsername: String,
  val password: String,
)

@JsonClass(generateAdapter = true)
data class RegisterRequest(
  val username: String,
  val email: String,
  val password: String,
)

@JsonClass(generateAdapter = true)
data class RefreshRequest(val refreshToken: String)

@JsonClass(generateAdapter = true)
data class ForgotPasswordRequest(val email: String)

@JsonClass(generateAdapter = true)
data class ResetPasswordRequest(
  val token: String,
  val newPassword: String,
)

@JsonClass(generateAdapter = true)
data class AuthResponse(
  val accessToken: String,
  val refreshToken: String? = null,
  val expiresIn: Long? = null,
  val user: UserMe? = null,
)

@JsonClass(generateAdapter = true)
data class UserMe(
  val id: Long,
  val username: String,
  val email: String,
  val bio: String? = null,
  val avatarUrl: String? = null,
  val designer: Boolean = false,
  val sessionQuota: SessionQuota? = null,
  val defaultSessionVisibility: String? = null,
  val time_zone: String? = null,
  val quickStats: Map<String, Any?>? = null,
)

@JsonClass(generateAdapter = true)
data class SessionQuota(
  val sessionsUsedThisWeek: Int? = null,
  val sessionsLimitPerWeek: Int? = null,
)

@JsonClass(generateAdapter = true)
data class UserPublic(
  val id: Long,
  val username: String,
  val avatarUrl: String? = null,
  val bio: String? = null,
  val designer: Boolean = false,
)

@JsonClass(generateAdapter = true)
data class ScopeDto(val id: Long, val scope: String)

@JsonClass(generateAdapter = true)
data class ScopesResponse(val scopes: List<ScopeDto>)

@JsonClass(generateAdapter = true)
data class DataTypeDto(val id: Long, val dataType: String)

@JsonClass(generateAdapter = true)
data class DataTypesResponse(val dataTypes: List<DataTypeDto>)

@JsonClass(generateAdapter = true)
data class GameDto(
  val id: Long,
  val gameName: String,
  val description: String,
  val minPlayerCount: Int,
  val maxPlayerCount: Int,
  val canWin: Boolean,
)

@JsonClass(generateAdapter = true)
data class GamesResponse(
  val games: List<GameDto>,
  val total: Int,
  val page: Int,
)

@JsonClass(generateAdapter = true)
data class CreateGameRequest(
  val gameName: String,
  val description: String,
  val minPlayerCount: Int,
  val maxPlayerCount: Int,
  val canWin: Boolean,
)

@JsonClass(generateAdapter = true)
data class StatDefinitionDto(
  val id: Long? = null,
  val statName: String,
  val description: String? = null,
  val dataTypeId: Long,
  val scopeId: Long,
)

@JsonClass(generateAdapter = true)
data class StatSetDto(
  val id: Long,
  val gameId: Long,
  val setName: String,
  val userId: Long? = null,
  val stats: List<StatDefinitionDto> = emptyList(),
)

@JsonClass(generateAdapter = true)
data class StatSetsResponse(val statSets: List<StatSetDto>)

@JsonClass(generateAdapter = true)
data class CreateStatSetRequest(
  val setName: String,
  val stats: List<StatDefinitionDto>? = null,
  val sourceStatSetId: Long? = null,
)

@JsonClass(generateAdapter = true)
data class SessionPlayerDto(
  val sessionPlayerId: Long? = null,
  val userId: Long? = null,
  val playerName: String? = null,
  val isSpectator: Boolean = false,
  val won: Boolean? = null,
)

@JsonClass(generateAdapter = true)
data class SessionDto(
  val id: Long,
  val sessionKey: String,
  val gameId: Long,
  val game: Map<String, Any?>? = null,
  val statSetId: Long,
  val statSet: Map<String, Any?>? = null,
  val timeStarted: String? = null,
  val timeEnded: String? = null,
  val currentRound: Int? = null,
  val visibility: String? = null,
  val players: List<SessionPlayerDto> = emptyList(),
  val trackedStats: List<Map<String, Any?>> = emptyList(),
)

@JsonClass(generateAdapter = true)
data class SessionsResponse(
  val sessions: List<SessionDto>,
  val total: Int,
  val page: Int,
)

@JsonClass(generateAdapter = true)
data class CreateSessionRequest(
  val gameId: Long,
  val statSetId: Long,
  val invitedUserIds: List<Long> = emptyList(),
  val nonAppPlayerNames: List<String> = emptyList(),
)

@JsonClass(generateAdapter = true)
data class CreateSessionResponse(
  val sessionId: Long,
  val sessionKey: String,
)

@JsonClass(generateAdapter = true)
data class PatchSessionRequest(
  val timeEnded: String? = null,
  val visibilityOverride: String? = null,
  val status: String? = null,
)

@JsonClass(generateAdapter = true)
data class JoinSessionRequest(val sessionKey: String)

@JsonClass(generateAdapter = true)
data class SessionInviteDto(
  val id: Long,
  val sessionId: Long,
  val invitedAt: String? = null,
  val session: SessionDto? = null,
)

@JsonClass(generateAdapter = true)
data class SessionInvitesResponse(
  val invites: List<SessionInviteDto>,
  val total: Int,
  val page: Int,
)

@JsonClass(generateAdapter = true)
data class UpdateUserMeRequest(
  val username: String? = null,
  val email: String? = null,
  val bio: String? = null,
  val avatarUrl: String? = null,
  val time_zone: String? = null,
)

@JsonClass(generateAdapter = true)
data class UserStatsResponse(
  val stats: Map<String, Any?> = emptyMap(),
)

@JsonClass(generateAdapter = true)
data class FollowersResponse(
  val followers: List<UserPublic>,
  val total: Int,
  val page: Int,
)

@JsonClass(generateAdapter = true)
data class FollowingResponse(
  val following: List<UserPublic>,
  val total: Int,
  val page: Int,
)

@JsonClass(generateAdapter = true)
data class UsersSearchResponse(
  val users: List<UserPublic>,
  val total: Int,
  val page: Int,
)

@JsonClass(generateAdapter = true)
data class FeedResponse(
  val sessions: List<SessionDto>,
  val total: Int,
  val page: Int,
)

@JsonClass(generateAdapter = true)
data class ExportFilters(
  val gameIds: List<Long>? = null,
  val from: String? = null,
  val to: String? = null,
  val sessionIds: List<Long>? = null,
  val statSetIds: List<Long>? = null,
  val preview: Boolean = false,
)

@JsonClass(generateAdapter = true)
data class ExportPreviewResponse(
  val sessionCount: Int? = null,
  val statValueCount: Int? = null,
  val estimatedSizeBytes: Long? = null,
)

@JsonClass(generateAdapter = true)
data class PublisherMeResponse(
  val id: Long,
  val name: String,
  val designerTagCount: Int? = null,
  val assignedCount: Int? = null,
)

@JsonClass(generateAdapter = true)
data class PublisherDesignersResponse(
  val designers: List<Map<String, Any?>> = emptyList(),
  val total: Int,
  val page: Int,
)

@JsonClass(generateAdapter = true)
data class PublisherAnalyticsResponse(
  val aggregates: Map<String, Any?> = emptyMap(),
)

@JsonClass(generateAdapter = true)
data class AssignDesignerRequest(val userId: Long)

@JsonClass(generateAdapter = true)
data class UsernameAvailabilityResponse(val available: Boolean)

@JsonClass(generateAdapter = true)
data class HealthResponse(
  val status: String,
  val database: String? = null,
)

