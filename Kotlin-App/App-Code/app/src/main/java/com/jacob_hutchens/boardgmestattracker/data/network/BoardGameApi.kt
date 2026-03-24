package com.jacob_hutchens.boardgmestattracker.data.network

import com.jacob_hutchens.boardgmestattracker.data.network.model.AssignDesignerRequest
import com.jacob_hutchens.boardgmestattracker.data.network.model.AuthResponse
import com.jacob_hutchens.boardgmestattracker.data.network.model.CreateGameRequest
import com.jacob_hutchens.boardgmestattracker.data.network.model.CreateSessionRequest
import com.jacob_hutchens.boardgmestattracker.data.network.model.CreateSessionResponse
import com.jacob_hutchens.boardgmestattracker.data.network.model.CreateStatSetRequest
import com.jacob_hutchens.boardgmestattracker.data.network.model.DataTypesResponse
import com.jacob_hutchens.boardgmestattracker.data.network.model.ExportFilters
import com.jacob_hutchens.boardgmestattracker.data.network.model.ExportPreviewResponse
import com.jacob_hutchens.boardgmestattracker.data.network.model.FeedResponse
import com.jacob_hutchens.boardgmestattracker.data.network.model.FollowersResponse
import com.jacob_hutchens.boardgmestattracker.data.network.model.FollowingResponse
import com.jacob_hutchens.boardgmestattracker.data.network.model.ForgotPasswordRequest
import com.jacob_hutchens.boardgmestattracker.data.network.model.GameDto
import com.jacob_hutchens.boardgmestattracker.data.network.model.GamesResponse
import com.jacob_hutchens.boardgmestattracker.data.network.model.HealthResponse
import com.jacob_hutchens.boardgmestattracker.data.network.model.JoinSessionRequest
import com.jacob_hutchens.boardgmestattracker.data.network.model.LoginRequest
import com.jacob_hutchens.boardgmestattracker.data.network.model.PatchSessionRequest
import com.jacob_hutchens.boardgmestattracker.data.network.model.PublisherAnalyticsResponse
import com.jacob_hutchens.boardgmestattracker.data.network.model.PublisherDesignersResponse
import com.jacob_hutchens.boardgmestattracker.data.network.model.PublisherMeResponse
import com.jacob_hutchens.boardgmestattracker.data.network.model.RefreshRequest
import com.jacob_hutchens.boardgmestattracker.data.network.model.RegisterRequest
import com.jacob_hutchens.boardgmestattracker.data.network.model.ResetPasswordRequest
import com.jacob_hutchens.boardgmestattracker.data.network.model.ScopesResponse
import com.jacob_hutchens.boardgmestattracker.data.network.model.SessionDto
import com.jacob_hutchens.boardgmestattracker.data.network.model.SessionInvitesResponse
import com.jacob_hutchens.boardgmestattracker.data.network.model.SessionsResponse
import com.jacob_hutchens.boardgmestattracker.data.network.model.StatSetDto
import com.jacob_hutchens.boardgmestattracker.data.network.model.StatSetsResponse
import com.jacob_hutchens.boardgmestattracker.data.network.model.UpdateUserMeRequest
import com.jacob_hutchens.boardgmestattracker.data.network.model.UserMe
import com.jacob_hutchens.boardgmestattracker.data.network.model.UserPublic
import com.jacob_hutchens.boardgmestattracker.data.network.model.UserStatsResponse
import com.jacob_hutchens.boardgmestattracker.data.network.model.UsernameAvailabilityResponse
import com.jacob_hutchens.boardgmestattracker.data.network.model.UsersSearchResponse
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.DELETE
import retrofit2.http.GET
import retrofit2.http.PATCH
import retrofit2.http.POST
import retrofit2.http.Path
import retrofit2.http.Query

interface BoardGameApi {
  @GET("health")
  suspend fun health(): HealthResponse

  @POST("auth/login")
  suspend fun login(@Body body: LoginRequest): AuthResponse

  @POST("auth/register")
  suspend fun register(@Body body: RegisterRequest): AuthResponse

  @POST("auth/publisher/login")
  suspend fun publisherLogin(@Body body: LoginRequest): AuthResponse

  @POST("auth/refresh")
  suspend fun refresh(@Body body: RefreshRequest): AuthResponse

  @POST("auth/forgot-password")
  suspend fun forgotPassword(@Body body: ForgotPasswordRequest): Response<Unit>

  @POST("auth/reset-password")
  suspend fun resetPassword(@Body body: ResetPasswordRequest): Response<Unit>

  @POST("auth/logout")
  suspend fun logout(): Response<Unit>

  @GET("users/check-username")
  suspend fun checkUsername(@Query("username") username: String): UsernameAvailabilityResponse

  @GET("scopes")
  suspend fun getScopes(): ScopesResponse

  @GET("data-types")
  suspend fun getDataTypes(): DataTypesResponse

  @GET("games")
  suspend fun getGames(
    @Query("filter") filter: String? = null,
    @Query("search") search: String? = null,
    @Query("page") page: Int? = null,
    @Query("limit") limit: Int? = null,
  ): GamesResponse

  @GET("games/{gameId}")
  suspend fun getGame(@Path("gameId") gameId: Long): GameDto

  @POST("games")
  suspend fun createGame(@Body body: CreateGameRequest): GameDto

  @GET("games/{gameId}/stat-sets")
  suspend fun getStatSets(@Path("gameId") gameId: Long): StatSetsResponse

  @GET("games/{gameId}/stat-sets/{statSetId}")
  suspend fun getStatSet(
    @Path("gameId") gameId: Long,
    @Path("statSetId") statSetId: Long,
  ): StatSetDto

  @POST("games/{gameId}/stat-sets")
  suspend fun createStatSet(
    @Path("gameId") gameId: Long,
    @Body body: CreateStatSetRequest,
  ): StatSetDto

  @GET("sessions")
  suspend fun getSessions(
    @Query("active") active: Boolean? = null,
    @Query("from") from: String? = null,
    @Query("to") to: String? = null,
    @Query("gameId") gameId: Long? = null,
    @Query("page") page: Int? = null,
    @Query("limit") limit: Int? = null,
  ): SessionsResponse

  @GET("sessions/{sessionId}")
  suspend fun getSession(@Path("sessionId") sessionId: Long): SessionDto

  @POST("sessions")
  suspend fun createSession(@Body body: CreateSessionRequest): CreateSessionResponse

  @PATCH("sessions/{sessionId}")
  suspend fun patchSession(
    @Path("sessionId") sessionId: Long,
    @Body body: PatchSessionRequest,
  ): SessionDto

  @DELETE("sessions/{sessionId}")
  suspend fun deleteSession(@Path("sessionId") sessionId: Long): Response<Unit>

  @POST("sessions/join")
  suspend fun joinSession(@Body body: JoinSessionRequest): SessionDto

  @GET("sessions/invites")
  suspend fun getSessionInvites(
    @Query("pending") pending: Boolean? = null,
    @Query("page") page: Int? = null,
    @Query("limit") limit: Int? = null,
  ): SessionInvitesResponse

  @GET("users/me")
  suspend fun getUserMe(): UserMe

  @PATCH("users/me")
  suspend fun updateUserMe(@Body body: UpdateUserMeRequest): UserMe

  @GET("users/{userId}")
  suspend fun getUser(@Path("userId") userId: Long): UserPublic

  @GET("users/me/stats")
  suspend fun getMyStats(): UserStatsResponse

  @GET("users/{userId}/stats")
  suspend fun getUserStats(@Path("userId") userId: Long): UserStatsResponse

  @GET("games/{gameId}/stats")
  suspend fun getGameStats(@Path("gameId") gameId: Long): UserStatsResponse

  @GET("users/{userId}/followers")
  suspend fun getFollowers(
    @Path("userId") userId: Long,
    @Query("page") page: Int? = null,
    @Query("limit") limit: Int? = null,
    @Query("search") search: String? = null,
  ): FollowersResponse

  @GET("users/{userId}/following")
  suspend fun getFollowing(
    @Path("userId") userId: Long,
    @Query("page") page: Int? = null,
    @Query("limit") limit: Int? = null,
    @Query("search") search: String? = null,
  ): FollowingResponse

  @POST("users/{userId}/follow")
  suspend fun follow(@Path("userId") userId: Long): Response<Unit>

  @DELETE("users/{userId}/follow")
  suspend fun unfollow(@Path("userId") userId: Long): Response<Unit>

  @GET("users/search")
  suspend fun searchUsers(
    @Query("q") query: String,
    @Query("page") page: Int? = null,
    @Query("limit") limit: Int? = null,
  ): UsersSearchResponse

  @GET("feed")
  suspend fun getFeed(
    @Query("page") page: Int? = null,
    @Query("limit") limit: Int? = null,
    @Query("since") since: String? = null,
  ): FeedResponse

  @GET("users/me/export")
  suspend fun exportGet(
    @Query("gameIds") gameIdsCsv: String? = null,
    @Query("from") from: String? = null,
    @Query("to") to: String? = null,
    @Query("sessionIds") sessionIdsCsv: String? = null,
    @Query("statSetIds") statSetIdsCsv: String? = null,
    @Query("preview") preview: Boolean = true,
  ): ExportPreviewResponse

  @POST("users/me/export")
  suspend fun exportPost(@Body body: ExportFilters): ExportPreviewResponse

  @GET("publishers/me")
  suspend fun getPublisherMe(): PublisherMeResponse

  @GET("publishers/me/designers")
  suspend fun getPublisherDesigners(
    @Query("page") page: Int? = null,
    @Query("limit") limit: Int? = null,
  ): PublisherDesignersResponse

  @GET("publishers/me/analytics")
  suspend fun getPublisherAnalytics(
    @Query("from") from: String? = null,
    @Query("to") to: String? = null,
  ): PublisherAnalyticsResponse

  @POST("publishers/me/designers")
  suspend fun assignDesigner(@Body body: AssignDesignerRequest): Response<Unit>

  @DELETE("publishers/me/designers/{userId}")
  suspend fun revokeDesigner(@Path("userId") userId: Long): Response<Unit>
}

