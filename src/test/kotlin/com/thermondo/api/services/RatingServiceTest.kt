package com.thermondo.api.services

import com.thermondo.api.common.DuplicateResourceException
import com.thermondo.api.common.ResourceNotFoundException
import com.thermondo.api.db.postgres.MovieDao
import com.thermondo.api.db.postgres.RatingDao
import com.thermondo.api.db.postgres.UserDao
import com.thermondo.api.dto.CreateRatingRequest
import com.thermondo.api.dto.UpdateRatingRequest
import com.thermondo.api.models.Movie
import com.thermondo.api.models.Rating
import com.thermondo.api.models.User
import io.mockk.every
import io.mockk.mockk
import io.mockk.verify
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.assertThrows
import org.junit.jupiter.api.Assertions.*
import org.junit.jupiter.api.BeforeEach
import java.math.BigDecimal
import java.time.Instant
import java.util.*

class RatingServiceTest {

    private val ratingDao = mockk<RatingDao>()
    private val userDao = mockk<UserDao>()
    private val movieDao = mockk<MovieDao>()
    private lateinit var ratingService: RatingService

    @BeforeEach
    fun setup() {
        ratingService = RatingService(ratingDao, userDao, movieDao)
    }

    @Test
    fun `should create rating successfully`() {
        val userId = UUID.randomUUID()
        val movieId = UUID.randomUUID()
        val request = CreateRatingRequest(
            movieId = movieId,
            ratingValue = BigDecimal("8.5"),
            review = "Great!"
        )
        val user = User(
            id = userId,
            name = "John Doe",
            email = "john.doe@some.domain",
            createdAt = Instant.now(),
            updatedAt = Instant.now()
        )
        val movie = Movie(
            id = movieId,
            title = "The Matrix",
            description = "A description",
            genre = "Sci-Fi",
            releaseYear = 1999,
            director = "The Wachowskis",
            durationMinutes = 136,
            posterUrl = "https://some.domain/poster.jpg",
            createdAt = Instant.now(),
            updatedAt = Instant.now()
        )
        val expectedRating = Rating(
            id = UUID.randomUUID(),
            userId = userId,
            movieId = movieId,
            ratingValue = request.ratingValue,
            review = request.review,
            createdAt = Instant.now(),
            updatedAt = Instant.now()
        )

        every { userDao.findById(userId) } returns user
        every { movieDao.findById(movieId) } returns movie
        every { ratingDao.existsByUserAndMovie(userId, movieId) } returns false
        every {
            ratingDao.create(
                userId = userId,
                movieId = movieId,
                ratingValue = request.ratingValue,
                review = request.review
            )
        } returns expectedRating

        val result = ratingService.createRating(userId, request)

        assertEquals(expectedRating, result)
        verify { userDao.findById(userId) }
        verify { movieDao.findById(movieId) }
        verify { ratingDao.existsByUserAndMovie(userId, movieId) }
        verify { ratingDao.create(userId, movieId, request.ratingValue, request.review) }
    }

    @Test
    fun `should throw ResourceNotFoundException when creating rating for user that does not exists`() {
        val userId = UUID.randomUUID()
        val movieId = UUID.randomUUID()
        val request = CreateRatingRequest(
            movieId = movieId,
            ratingValue = BigDecimal("8.5"),
            review = "Great!"
        )

        every { userDao.findById(userId) } returns null

        val exception = assertThrows<ResourceNotFoundException> {
            ratingService.createRating(userId, request)
        }

        assertEquals("User with id $userId not found", exception.message)
        verify { userDao.findById(userId) }
        verify(exactly = 0) { movieDao.findById(any()) }
        verify(exactly = 0) { ratingDao.existsByUserAndMovie(any(), any()) }
        verify(exactly = 0) { ratingDao.create(any(), any(), any(), any()) }
    }

    @Test
    fun `should throw ResourceNotFoundException when creating rating for a movie that does not exist`() {
        val userId = UUID.randomUUID()
        val movieId = UUID.randomUUID()
        val request = CreateRatingRequest(
            movieId = movieId,
            ratingValue = BigDecimal("8.5"),
            review = "Great!"
        )
        val user = User(
            id = userId,
            name = "John Doe",
            email = "john.doe@some.domain",
            createdAt = Instant.now(),
            updatedAt = Instant.now()
        )

        every { userDao.findById(userId) } returns user
        every { movieDao.findById(movieId) } returns null

        val exception = assertThrows<ResourceNotFoundException> {
            ratingService.createRating(userId, request)
        }

        assertEquals("Movie with id $movieId not found", exception.message)
        verify { userDao.findById(userId) }
        verify { movieDao.findById(movieId) }
        verify(exactly = 0) { ratingDao.existsByUserAndMovie(any(), any()) }
        verify(exactly = 0) { ratingDao.create(any(), any(), any(), any()) }
    }

    @Test
    fun `should throw DuplicateResourceException when user already rated the movie`() {
        val userId = UUID.randomUUID()
        val movieId = UUID.randomUUID()
        val request = CreateRatingRequest(
            movieId = movieId,
            ratingValue = BigDecimal("8.5"),
            review = "Great!"
        )
        val user = User(
            id = userId,
            name = "John Doe",
            email = "john.doe@some.domain",
            createdAt = Instant.now(),
            updatedAt = Instant.now()
        )
        val movie = Movie(
            id = movieId,
            title = "The Matrix",
            description = "A description",
            genre = "Sci-Fi",
            releaseYear = 1999,
            director = "The Wachowskis",
            durationMinutes = 136,
            posterUrl = "https://some.domain/poster.jpg",
            createdAt = Instant.now(),
            updatedAt = Instant.now()
        )

        every { userDao.findById(userId) } returns user
        every { movieDao.findById(movieId) } returns movie
        every { ratingDao.existsByUserAndMovie(userId, movieId) } returns true

        val exception = assertThrows<DuplicateResourceException> {
            ratingService.createRating(userId, request)
        }

        assertEquals("User has already rated this movie", exception.message)
        verify { userDao.findById(userId) }
        verify { movieDao.findById(movieId) }
        verify { ratingDao.existsByUserAndMovie(userId, movieId) }
        verify(exactly = 0) { ratingDao.create(any(), any(), any(), any()) }
    }

    @Test
    fun `should return rating when rating exists`() {
        val ratingId = UUID.randomUUID()
        val expectedRating = Rating(
            id = ratingId,
            userId = UUID.randomUUID(),
            movieId = UUID.randomUUID(),
            ratingValue = BigDecimal("8.5"),
            review = "Great!",
            createdAt = Instant.now(),
            updatedAt = Instant.now()
        )

        every { ratingDao.findById(ratingId) } returns expectedRating

        val result = ratingService.getRatingById(ratingId)

        assertEquals(expectedRating, result)
        verify { ratingDao.findById(ratingId) }
    }

    @Test
    fun `should return rating when rating exists for user and movie`() {
        val userId = UUID.randomUUID()
        val movieId = UUID.randomUUID()
        val expectedRating = Rating(
            id = UUID.randomUUID(),
            userId = userId,
            movieId = movieId,
            ratingValue = BigDecimal("8.5"),
            review = "Great!",
            createdAt = Instant.now(),
            updatedAt = Instant.now()
        )

        every { ratingDao.findByUserAndMovie(userId, movieId) } returns expectedRating

        val result = ratingService.getUserRating(userId, movieId)

        assertEquals(expectedRating, result)
        verify { ratingDao.findByUserAndMovie(userId, movieId) }
    }

    @Test
    fun `should throw ResourceNotFoundException when getting rating that does not exist`() {
        val userId = UUID.randomUUID()
        val movieId = UUID.randomUUID()

        every { ratingDao.findByUserAndMovie(userId, movieId) } returns null

        val exception = assertThrows<ResourceNotFoundException> {
            ratingService.getUserRating(userId, movieId)
        }

        assertEquals("Rating not found for this user and movie", exception.message)
        verify { ratingDao.findByUserAndMovie(userId, movieId) }
    }

    @Test
    fun `should return ratings when user exists`() {
        val userId = UUID.randomUUID()
        val user = User(
            id = userId,
            name = "John Doe",
            email = "john.doe@some.domain",
            createdAt = Instant.now(),
            updatedAt = Instant.now()
        )
        val ratings = listOf(
            Rating(
                id = UUID.randomUUID(),
                userId = userId,
                movieId = UUID.randomUUID(),
                ratingValue = BigDecimal("8.5"),
                review = "Great!",
                createdAt = Instant.now(),
                updatedAt = Instant.now()
            )
        )

        every { userDao.findById(userId) } returns user
        every { ratingDao.findByUserId(userId) } returns ratings

        val result = ratingService.getRatingsByUserId(userId)

        assertEquals(ratings, result)
        verify { userDao.findById(userId) }
        verify { ratingDao.findByUserId(userId) }
    }

    @Test
    fun `should throw ResourceNotFoundException when user does not exist`() {
        val userId = UUID.randomUUID()

        every { userDao.findById(userId) } returns null

        val exception = assertThrows<ResourceNotFoundException> {
            ratingService.getRatingsByUserId(userId)
        }

        assertEquals("User with id $userId not found", exception.message)
        verify { userDao.findById(userId) }
        verify(exactly = 0) { ratingDao.findByUserId(any()) }
    }

    @Test
    fun `should return ratings when movie exists`() {
        val movieId = UUID.randomUUID()
        val movie = Movie(
            id = movieId,
            title = "The Matrix",
            description = "A description",
            genre = "Sci-Fi",
            releaseYear = 1999,
            director = "Wachowskis",
            durationMinutes = 136,
            posterUrl = "https://some.domain/poster.jpg",
            createdAt = Instant.now(),
            updatedAt = Instant.now()
        )
        val ratings = listOf(
            Rating(
                id = UUID.randomUUID(),
                userId = UUID.randomUUID(),
                movieId = movieId,
                ratingValue = BigDecimal("8.5"),
                review = "Great!",
                createdAt = Instant.now(),
                updatedAt = Instant.now()
            )
        )

        every { movieDao.findById(movieId) } returns movie
        every { ratingDao.findByMovieId(movieId) } returns ratings

        val result = ratingService.getRatingsByMovieId(movieId)

        assertEquals(ratings, result)
        verify { movieDao.findById(movieId) }
        verify { ratingDao.findByMovieId(movieId) }
    }

    @Test
    fun `should throw ResourceNotFoundException when movie does not exist`() {
        val movieId = UUID.randomUUID()

        every { movieDao.findById(movieId) } returns null

        val exception = assertThrows<ResourceNotFoundException> {
            ratingService.getRatingsByMovieId(movieId)
        }

        assertEquals("Movie with id $movieId not found", exception.message)
        verify { movieDao.findById(movieId) }
        verify(exactly = 0) { ratingDao.findByMovieId(any()) }
    }

    @Test
    fun `should update rating successfully`() {
        val ratingId = UUID.randomUUID()
        val request = UpdateRatingRequest(
            ratingValue = BigDecimal("9.0"),
            review = "updated rating"
        )
        val expectedRating = Rating(
            id = ratingId,
            userId = UUID.randomUUID(),
            movieId = UUID.randomUUID(),
            ratingValue = request.ratingValue!!,
            review = request.review,
            createdAt = Instant.now(),
            updatedAt = Instant.now()
        )

        every {
            ratingDao.update(
                id = ratingId,
                ratingValue = request.ratingValue,
                review = request.review
            )
        } returns expectedRating

        val result = ratingService.updateRating(ratingId, request)

        assertEquals(expectedRating, result)
        verify { ratingDao.update(ratingId, request.ratingValue, request.review) }
    }

    @Test
    fun `should return true when rating is deleted successfully`() {
        val ratingId = UUID.randomUUID()

        every { ratingDao.delete(ratingId) } returns true

        val result = ratingService.deleteRating(ratingId)

        assertTrue(result)
        verify { ratingDao.delete(ratingId) }
    }

    @Test
    fun `should throw ResourceNotFoundException when rating does not exist`() {
        val ratingId = UUID.randomUUID()

        every { ratingDao.delete(ratingId) } returns false

        val exception = assertThrows<ResourceNotFoundException> {
            ratingService.deleteRating(ratingId)
        }

        assertEquals("Rating with id $ratingId not found", exception.message)
        verify { ratingDao.delete(ratingId) }
    }

    @Test
    fun `should return user rating profile when user exists`() {
        val userId = UUID.randomUUID()
        val user = User(
            id = userId,
            name = "John Doe",
            email = "john.doe@some.domain",
            createdAt = Instant.now(),
            updatedAt = Instant.now()
        )
        val ratings = listOf(
            Rating(
                id = UUID.randomUUID(),
                userId = userId,
                movieId = UUID.randomUUID(),
                ratingValue = BigDecimal("8.5"),
                review = "Great!",
                createdAt = Instant.now(),
                updatedAt = Instant.now(),
                movieTitle = "The Matrix",
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
                movieTitle = "The Godfather",
                userName = "John Doe"
            )
        )
        val averageRating = BigDecimal("7.75")
        val totalRatings = 2

        every { userDao.findById(userId) } returns user
        every { ratingDao.findByUserId(userId) } returns ratings
        every { ratingDao.getUserRatingStats(userId) } returns Pair(averageRating, totalRatings)

        val result = ratingService.getUserRatingProfile(userId)

        assertEquals(userId, result.userId)
        assertEquals(user.name, result.userName)
        assertEquals(totalRatings, result.totalRatings)
        assertEquals(averageRating, result.averageRating)
        assertEquals(2, result.ratings.size)
        assertEquals("The Matrix", result.ratings[0].movieTitle)
        assertEquals("The Godfather", result.ratings[1].movieTitle)

        verify { userDao.findById(userId) }
        verify { ratingDao.findByUserId(userId) }
        verify { ratingDao.getUserRatingStats(userId) }
    }
}
