package com.jacob_hutchens.boardgmestattracker.data.repository

import com.jacob_hutchens.boardgmestattracker.data.network.BoardGameApi
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

class RestRepository(
  private val api: BoardGameApi,
) {
  suspend fun health(): HealthResponse = api.health()
  suspend fun login(body: LoginRequest): AuthResponse = api.login(body)
  suspend fun register(body: RegisterRequest): AuthResponse = api.register(body)
  suspend fun publisherLogin(body: LoginRequest): AuthResponse = api.publisherLogin(body)
  suspend fun refresh(body: RefreshRequest): AuthResponse = api.refresh(body)
  suspend fun forgotPassword(body: ForgotPasswordRequest) = api.forgotPassword(body)
  suspend fun resetPassword(body: ResetPasswordRequest) = api.resetPassword(body)
  suspend fun logout() = api.logout()
  suspend fun checkUsername(username: String): UsernameAvailabilityResponse = api.checkUsername(username)
  suspend fun getScopes(): ScopesResponse = api.getScopes()
  suspend fun getDataTypes(): DataTypesResponse = api.getDataTypes()
  suspend fun getGames(filter: String?, search: String?, page: Int?, limit: Int?): GamesResponse =
    api.getGames(filter, search, page, limit)
  suspend fun getGame(gameId: Long): GameDto = api.getGame(gameId)
  suspend fun createGame(body: CreateGameRequest): GameDto = api.createGame(body)
  suspend fun getStatSets(gameId: Long): StatSetsResponse = api.getStatSets(gameId)
  suspend fun getStatSet(gameId: Long, statSetId: Long): StatSetDto = api.getStatSet(gameId, statSetId)
  suspend fun createStatSet(gameId: Long, body: CreateStatSetRequest): StatSetDto = api.createStatSet(gameId, body)
  suspend fun getSessions(active: Boolean?, from: String?, to: String?, gameId: Long?, page: Int?, limit: Int?): SessionsResponse =
    api.getSessions(active, from, to, gameId, page, limit)
  suspend fun getSession(sessionId: Long): SessionDto = api.getSession(sessionId)
  suspend fun createSession(body: CreateSessionRequest): CreateSessionResponse = api.createSession(body)
  suspend fun patchSession(sessionId: Long, body: PatchSessionRequest): SessionDto = api.patchSession(sessionId, body)
  suspend fun deleteSession(sessionId: Long) = api.deleteSession(sessionId)
  suspend fun joinSession(body: JoinSessionRequest): SessionDto = api.joinSession(body)
  suspend fun getSessionInvites(pending: Boolean?, page: Int?, limit: Int?): SessionInvitesResponse =
    api.getSessionInvites(pending, page, limit)
  suspend fun getUserMe(): UserMe = api.getUserMe()
  suspend fun updateUserMe(body: UpdateUserMeRequest): UserMe = api.updateUserMe(body)
  suspend fun getUser(userId: Long): UserPublic = api.getUser(userId)
  suspend fun getMyStats(): UserStatsResponse = api.getMyStats()
  suspend fun getUserStats(userId: Long): UserStatsResponse = api.getUserStats(userId)
  suspend fun getGameStats(gameId: Long): UserStatsResponse = api.getGameStats(gameId)
  suspend fun getFollowers(userId: Long, page: Int?, limit: Int?, search: String?): FollowersResponse =
    api.getFollowers(userId, page, limit, search)
  suspend fun getFollowing(userId: Long, page: Int?, limit: Int?, search: String?): FollowingResponse =
    api.getFollowing(userId, page, limit, search)
  suspend fun follow(userId: Long) = api.follow(userId)
  suspend fun unfollow(userId: Long) = api.unfollow(userId)
  suspend fun searchUsers(query: String, page: Int?, limit: Int?): UsersSearchResponse = api.searchUsers(query, page, limit)
  suspend fun getFeed(page: Int?, limit: Int?, since: String?): FeedResponse = api.getFeed(page, limit, since)
  suspend fun exportGet(
    gameIdsCsv: String?,
    from: String?,
    to: String?,
    sessionIdsCsv: String?,
    statSetIdsCsv: String?,
    preview: Boolean,
  ): ExportPreviewResponse = api.exportGet(gameIdsCsv, from, to, sessionIdsCsv, statSetIdsCsv, preview)
  suspend fun exportPost(body: ExportFilters): ExportPreviewResponse = api.exportPost(body)
  suspend fun getPublisherMe(): PublisherMeResponse = api.getPublisherMe()
  suspend fun getPublisherDesigners(page: Int?, limit: Int?): PublisherDesignersResponse = api.getPublisherDesigners(page, limit)
  suspend fun getPublisherAnalytics(from: String?, to: String?): PublisherAnalyticsResponse = api.getPublisherAnalytics(from, to)
  suspend fun assignDesigner(body: AssignDesignerRequest) = api.assignDesigner(body)
  suspend fun revokeDesigner(userId: Long) = api.revokeDesigner(userId)
}

