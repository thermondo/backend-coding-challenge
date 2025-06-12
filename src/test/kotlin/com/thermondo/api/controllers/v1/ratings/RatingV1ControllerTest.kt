package com.thermondo.api.controllers.v1.ratings

import com.fasterxml.jackson.databind.ObjectMapper
import com.thermondo.api.dto.CreateRatingRequest
import com.thermondo.api.dto.RatingResponse
import com.thermondo.api.dto.UpdateRatingRequest
import com.thermondo.api.dto.UserRatingProfileResponse
import com.thermondo.api.models.Rating
import com.thermondo.api.models.UserRatingProfile
import com.thermondo.api.services.RatingService
import io.mockk.every
import io.mockk.mockk
import io.mockk.verify
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest
import org.springframework.boot.test.context.TestConfiguration
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Primary
import org.springframework.http.MediaType
import org.springframework.test.context.ActiveProfiles
import org.springframework.test.web.servlet.MockMvc
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*
import org.springframework.test.web.servlet.result.MockMvcResultMatchers.*
import java.math.BigDecimal
import java.time.Instant
import java.util.*

@WebMvcTest(controllers = [RatingV1Controller::class], excludeAutoConfiguration = [org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration::class])
@ActiveProfiles("test")
class RatingV1ControllerTest {

    @Autowired
    private lateinit var mockMvc: MockMvc

    @Autowired
    private lateinit var objectMapper: ObjectMapper

    @TestConfiguration
    class TestConfig {
        @Bean
        @Primary
        fun ratingService(): RatingService = mockk()
    }

    @Autowired
    private lateinit var ratingService: RatingService

    @Test
    fun `should create rating successfully`() {
        val userId = UUID.randomUUID()
        val movieId = UUID.randomUUID()
        val ratingRequest = CreateRatingRequest(
            movieId = movieId,
            ratingValue = BigDecimal("8.5"),
            review = "Great!"
        )

        val createdRating = Rating(
            id = UUID.randomUUID(),
            userId = userId,
            movieId = movieId,
            ratingValue = BigDecimal("8.5"),
            review = "Great!",
            createdAt = Instant.now(),
            updatedAt = Instant.now(),
            movieTitle = "Some Movie",
            userName = "Some User"
        )

        every { ratingService.createRating(userId, ratingRequest) } returns createdRating

        mockMvc.perform(
            post("/api/v1/ratings/user/{userId}", userId)
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(ratingRequest))
        )
            .andExpect(status().isCreated)
            .andExpect(content().contentType(MediaType.APPLICATION_JSON))
            .andExpect(jsonPath("$.userId").value(userId.toString()))
            .andExpect(jsonPath("$.movieId").value(movieId.toString()))
            .andExpect(jsonPath("$.ratingValue").value(8.5))
            .andExpect(jsonPath("$.review").value("Great!"))
            .andExpect(jsonPath("$.movieTitle").value("Some Movie"))
            .andExpect(jsonPath("$.userName").value("Some User"))
    }

    @Test
    fun `should return rating when it exists`() {
        val ratingId = UUID.randomUUID()
        val userId = UUID.randomUUID()
        val movieId = UUID.randomUUID()
        
        val rating = Rating(
            id = ratingId,
            userId = userId,
            movieId = movieId,
            ratingValue = BigDecimal("7.0"),
            review = "Good movie",
            createdAt = Instant.now(),
            updatedAt = Instant.now(),
            movieTitle = "Some Movie",
            userName = "Some User"
        )

        every { ratingService.getRatingById(ratingId) } returns rating

        mockMvc.perform(get("/api/v1/ratings/{id}", ratingId))
            .andExpect(status().isOk)
            .andExpect(content().contentType(MediaType.APPLICATION_JSON))
            .andExpect(jsonPath("$.id").value(ratingId.toString()))
            .andExpect(jsonPath("$.userId").value(userId.toString()))
            .andExpect(jsonPath("$.movieId").value(movieId.toString()))
            .andExpect(jsonPath("$.ratingValue").value(7.0))
            .andExpect(jsonPath("$.review").value("Good movie"))
            .andExpect(jsonPath("$.movieTitle").value("Some Movie"))
            .andExpect(jsonPath("$.userName").value("Some User"))
    }

    @Test
    fun `should return user rating for specific movie`() {
        val userId = UUID.randomUUID()
        val movieId = UUID.randomUUID()
        val ratingId = UUID.randomUUID()

        val rating = Rating(
            id = ratingId,
            userId = userId,
            movieId = movieId,
            ratingValue = BigDecimal("9.0"),
            review = "Awesome",
            createdAt = Instant.now(),
            updatedAt = Instant.now(),
            movieTitle = "Awesome Movie",
            userName = "John Doe"
        )

        every { ratingService.getUserRating(userId, movieId) } returns rating

        mockMvc.perform(get("/api/v1/ratings/user/{userId}/movie/{movieId}", userId, movieId))
            .andExpect(status().isOk)
            .andExpect(content().contentType(MediaType.APPLICATION_JSON))
            .andExpect(jsonPath("$.id").value(ratingId.toString()))
            .andExpect(jsonPath("$.userId").value(userId.toString()))
            .andExpect(jsonPath("$.movieId").value(movieId.toString()))
            .andExpect(jsonPath("$.ratingValue").value(9.0))
            .andExpect(jsonPath("$.review").value("Awesome"))
    }

    @Test
    fun `should return ratings list for user`() {
        val userId = UUID.randomUUID()
        val ratings = listOf(
            Rating(
                id = UUID.randomUUID(),
                userId = userId,
                movieId = UUID.randomUUID(),
                ratingValue = BigDecimal("8.0"),
                review = "Good movie",
                createdAt = Instant.now(),
                updatedAt = Instant.now(),
                movieTitle = "Some Movie 1",
                userName = "Some User"
            ),
            Rating(
                id = UUID.randomUUID(),
                userId = userId,
                movieId = UUID.randomUUID(),
                ratingValue = BigDecimal("6.5"),
                review = "It is ok",
                createdAt = Instant.now(),
                updatedAt = Instant.now(),
                movieTitle = "Some Movie 2",
                userName = "Some User"
            )
        )

        every { ratingService.getRatingsByUserId(userId) } returns ratings

        mockMvc.perform(get("/api/v1/ratings/user/{userId}", userId))
            .andExpect(status().isOk)
            .andExpect(content().contentType(MediaType.APPLICATION_JSON))
            .andExpect(jsonPath("$").isArray)
            .andExpect(jsonPath("$.length()").value(2))
            .andExpect(jsonPath("$[0].userId").value(userId.toString()))
            .andExpect(jsonPath("$[0].ratingValue").value(8.0))
            .andExpect(jsonPath("$[0].review").value("Good movie"))
            .andExpect(jsonPath("$[0].movieTitle").value("Some Movie 1"))
            .andExpect(jsonPath("$[1].ratingValue").value(6.5))
            .andExpect(jsonPath("$[1].review").value("It is ok"))
            .andExpect(jsonPath("$[1].movieTitle").value("Some Movie 2"))
    }

    @Test
    fun `should return ratings list for movie`() {
        val movieId = UUID.randomUUID()
        val ratings = listOf(
            Rating(
                id = UUID.randomUUID(),
                userId = UUID.randomUUID(),
                movieId = movieId,
                ratingValue = BigDecimal("9.0"),
                review = "Amazing",
                createdAt = Instant.now(),
                updatedAt = Instant.now(),
                movieTitle = "Some Movie",
                userName = "User 1"
            ),
            Rating(
                id = UUID.randomUUID(),
                userId = UUID.randomUUID(),
                movieId = movieId,
                ratingValue = BigDecimal("7.0"),
                review = "Pretty good",
                createdAt = Instant.now(),
                updatedAt = Instant.now(),
                movieTitle = "Some Movie",
                userName = "User 2"
            )
        )

        every { ratingService.getRatingsByMovieId(movieId) } returns ratings

        mockMvc.perform(get("/api/v1/ratings/movie/{movieId}", movieId))
            .andExpect(status().isOk)
            .andExpect(content().contentType(MediaType.APPLICATION_JSON))
            .andExpect(jsonPath("$").isArray)
            .andExpect(jsonPath("$.length()").value(2))
            .andExpect(jsonPath("$[0].movieId").value(movieId.toString()))
            .andExpect(jsonPath("$[0].ratingValue").value(9.0))
            .andExpect(jsonPath("$[0].review").value("Amazing"))
            .andExpect(jsonPath("$[0].userName").value("User 1"))
            .andExpect(jsonPath("$[1].ratingValue").value(7.0))
            .andExpect(jsonPath("$[1].review").value("Pretty good"))
            .andExpect(jsonPath("$[1].userName").value("User 2"))
    }

    @Test
    fun `should return user rating profile`() {
        val userId = UUID.randomUUID()
        val userProfile = UserRatingProfile(
            userId = userId,
            userName = "John Doe",
            totalRatings = 2,
            averageRating = BigDecimal("7.75"),
            ratings = listOf(
                Rating(
                    id = UUID.randomUUID(),
                    userId = userId,
                    movieId = UUID.randomUUID(),
                    ratingValue = BigDecimal("8.5"),
                    review = "Great!",
                    createdAt = Instant.now(),
                    updatedAt = Instant.now(),
                    movieTitle = "Some Movie 1",
                    userName = "John Doe"
                ),
                Rating(
                    id = UUID.randomUUID(),
                    userId = userId,
                    movieId = UUID.randomUUID(),
                    ratingValue = BigDecimal("7.0"),
                    review = "Good movie",
                    createdAt = Instant.now(),
                    updatedAt = Instant.now(),
                    movieTitle = "Some Movie 2",
                    userName = "John Doe"
                )
            )
        )

        every { ratingService.getUserRatingProfile(userId) } returns userProfile

        mockMvc.perform(get("/api/v1/ratings/user/{userId}/profile", userId))
            .andExpect(status().isOk)
            .andExpect(content().contentType(MediaType.APPLICATION_JSON))
            .andExpect(jsonPath("$.userId").value(userId.toString()))
            .andExpect(jsonPath("$.userName").value("John Doe"))
            .andExpect(jsonPath("$.totalRatings").value(2))
            .andExpect(jsonPath("$.averageRating").value(7.75))
            .andExpect(jsonPath("$.ratings").isArray)
            .andExpect(jsonPath("$.ratings.length()").value(2))
            .andExpect(jsonPath("$.ratings[0].ratingValue").value(8.5))
            .andExpect(jsonPath("$.ratings[0].review").value("Great!"))
            .andExpect(jsonPath("$.ratings[1].ratingValue").value(7.0))
            .andExpect(jsonPath("$.ratings[1].review").value("Good movie"))
    }

    @Test
    fun `should update rating successfully`() {
        val ratingId = UUID.randomUUID()
        val updateRequest = UpdateRatingRequest(
            ratingValue = BigDecimal("9.5"),
            review = "Updated review - Sehr gut"
        )
        
        val updatedRating = Rating(
            id = ratingId,
            userId = UUID.randomUUID(),
            movieId = UUID.randomUUID(),
            ratingValue = BigDecimal("9.5"),
            review = "Updated review - Sehr gut",
            createdAt = Instant.now(),
            updatedAt = Instant.now(),
            movieTitle = "Some Movie",
            userName = "Some User"
        )

        every { ratingService.updateRating(ratingId, updateRequest) } returns updatedRating

        mockMvc.perform(
            put("/api/v1/ratings/{id}", ratingId)
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(updateRequest))
        )
            .andExpect(status().isOk)
            .andExpect(content().contentType(MediaType.APPLICATION_JSON))
            .andExpect(jsonPath("$.id").value(ratingId.toString()))
            .andExpect(jsonPath("$.ratingValue").value(9.5))
            .andExpect(jsonPath("$.review").value("Updated review - Sehr gut"))
    }

    @Test
    fun `should delete rating successfully`() {
        val ratingId = UUID.randomUUID()

        every { ratingService.deleteRating(ratingId) } returns true

        mockMvc.perform(delete("/api/v1/ratings/{id}", ratingId))
            .andExpect(status().isOk)
            .andExpect(content().contentType(MediaType.APPLICATION_JSON))
            .andExpect(jsonPath("$.message").value("Rating deleted successfully"))

        verify { ratingService.deleteRating(ratingId) }
    }
}
