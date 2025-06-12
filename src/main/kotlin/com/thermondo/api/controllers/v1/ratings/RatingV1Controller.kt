package com.thermondo.api.controllers.v1.ratings

import com.thermondo.api.dto.*
import com.thermondo.api.dto.RatingResponse.Companion.fromRating
import com.thermondo.api.dto.UserRatingProfileResponse.Companion.fromUserRatingProfile
import com.thermondo.api.services.RatingService
import io.swagger.v3.oas.annotations.Operation
import io.swagger.v3.oas.annotations.tags.Tag
import jakarta.validation.Valid
import org.slf4j.LoggerFactory
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*
import java.util.*

@RestController
@RequestMapping("/api/v1/ratings")
@Tag(name = "Ratings", description = "Rating management endpoints")
class RatingV1Controller(
    private val ratingService: RatingService,
) {
    private val logger = LoggerFactory.getLogger(RatingV1Controller::class.java)

    @PostMapping("/user/{userId}")
    @Operation(summary = "Create a new rating for a user")
    fun createRating(
        @PathVariable userId: UUID,
        @Valid @RequestBody request: CreateRatingRequest
    ): ResponseEntity<RatingResponse> {
        logger.info("Creating rating for user: $userId, movie: ${request.movieId}")
        val response = fromRating(
            ratingService.createRating(userId, request)
        )
        return ResponseEntity.status(HttpStatus.CREATED).body(response)
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get rating by ID")
    fun getRatingById(@PathVariable id: UUID): ResponseEntity<RatingResponse> {
        logger.debug("Fetching rating with id: $id")
        val response = fromRating(
            ratingService.getRatingById(id)
        )
        return ResponseEntity.ok(response)
    }

    @GetMapping("/user/{userId}/movie/{movieId}")
    @Operation(summary = "Get user's rating for a specific movie")
    fun getUserRating(
        @PathVariable userId: UUID,
        @PathVariable movieId: UUID
    ): ResponseEntity<RatingResponse> {
        logger.debug("Fetching rating for user: $userId, movie: $movieId")
        val response = fromRating(
            ratingService.getUserRating(userId, movieId)
        )
        return ResponseEntity.ok(response)
    }

    @GetMapping("/user/{userId}")
    @Operation(summary = "Get all ratings by user")
    fun getRatingsByUserId(
        @PathVariable userId: UUID
    ): ResponseEntity<List<RatingResponse>> {
        logger.debug("Fetching ratings for user: $userId")
        val response = ratingService.getRatingsByUserId(userId).map { rating ->
            fromRating(rating)
        }
        return ResponseEntity.ok(response)
    }

    @GetMapping("/movie/{movieId}")
    @Operation(summary = "Get all ratings for a movie")
    fun getRatingsByMovieId(
        @PathVariable movieId: UUID
    ): ResponseEntity<List<RatingResponse>> {
        logger.debug("Fetching ratings for movie: $movieId")
        val response = ratingService.getRatingsByMovieId(movieId).map { rating ->
            fromRating(rating)
        }
        return ResponseEntity.ok(response)
    }

    @GetMapping("/user/{userId}/profile")
    @Operation(summary = "Get user's rating profile")
    fun getUserRatingProfile(@PathVariable userId: UUID): ResponseEntity<UserRatingProfileResponse> {
        logger.debug("Fetching rating profile for user: $userId")
        val userRatingProfile = ratingService.getUserRatingProfile(userId)
        return ResponseEntity.ok(
            fromUserRatingProfile(userRatingProfile)
        )
    }

    @PutMapping("/{id}")
    @Operation(summary = "Update rating")
    fun updateRating(
        @PathVariable id: UUID,
        @Valid @RequestBody request: UpdateRatingRequest
    ): ResponseEntity<RatingResponse> {
        logger.info("Updating rating with id: $id")
        val response = fromRating(
            ratingService.updateRating(id, request)
        )
        return ResponseEntity.ok(response)
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete rating")
    fun deleteRating(@PathVariable id: UUID): ResponseEntity<Map<String, String>> {
        logger.info("Deleting rating with id: $id")
        ratingService.deleteRating(id)
        return ResponseEntity.ok(mapOf("message" to "Rating deleted successfully"))
    }
}
