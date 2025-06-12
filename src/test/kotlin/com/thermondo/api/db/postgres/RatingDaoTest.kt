package com.thermondo.api.db.postgres

import com.thermondo.api.IntegrationTest
import com.thermondo.api.common.ResourceNotFoundException
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.assertThrows
import org.junit.jupiter.api.Assertions.*
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.test.annotation.Rollback
import java.math.BigDecimal
import java.time.Instant
import java.util.*

@IntegrationTest
class RatingDaoTest {
    @Autowired
    private lateinit var ratingDao: RatingDao
    
    @Autowired
    private lateinit var userDao: UserDao
    
    @Autowired
    private lateinit var movieDao: MovieDao

    @Test
    @Rollback
    fun `should create rating successfully`() {
        val user = userDao.create("Some User", "test@some.domain")
        val movie = movieDao.create("Some Movie", "Some Description", "Action", 2023, "Some Director", 120, null)
        val ratingValue = BigDecimal("8.50")
        val review = "Great!"

        val createdRating = ratingDao.create(user.id, movie.id, ratingValue, review)

        assertNotNull(createdRating.id)
        assertEquals(user.id, createdRating.userId)
        assertEquals(movie.id, createdRating.movieId)
        assertEquals(0, ratingValue.compareTo(createdRating.ratingValue))
        assertEquals(review, createdRating.review)
        assertNotNull(createdRating.createdAt)
        assertNotNull(createdRating.updatedAt)
        assertTrue(createdRating.createdAt.isBefore(Instant.now().plusSeconds(1)))
        assertTrue(createdRating.updatedAt.isBefore(Instant.now().plusSeconds(1)))
        assertEquals(movie.title, createdRating.movieTitle)
        assertEquals(user.name, createdRating.userName)
    }

    @Test
    @Rollback
    fun `should find rating by id when exists`() {
        val user = userDao.create("Some User", "test@some.domain")
        val movie = movieDao.create("Some Movie", "Some Description", "Action", 2023, "Some Director", 120, null)
        val rating = ratingDao.create(user.id, movie.id, BigDecimal("7.50"), "Good movie")

        val foundRating = ratingDao.findById(rating.id)

        assertNotNull(foundRating)
        assertEquals(rating.id, foundRating!!.id)
        assertEquals(rating.userId, foundRating.userId)
        assertEquals(rating.movieId, foundRating.movieId)
        assertEquals(0, rating.ratingValue.compareTo(foundRating.ratingValue))
        assertEquals(rating.review, foundRating.review)
        assertEquals(rating.movieTitle, foundRating.movieTitle)
        assertEquals(rating.userName, foundRating.userName)
    }

    @Test
    @Rollback
    fun `should return null when rating does not exist`() {
        val nonExistentId = UUID.randomUUID()

        val foundRating = ratingDao.findById(nonExistentId)

        assertNull(foundRating)
    }

    @Test
    @Rollback
    fun `should find rating by user and movie`() {
        val user = userDao.create("Some User", "test@some.domain")
        val movie = movieDao.create("Some Movie", "Some Description", "Action", 2023, "Some Director", 120, null)
        val rating = ratingDao.create(user.id, movie.id, BigDecimal("9.00"), "Awesome")

        val foundRating = ratingDao.findByUserAndMovie(user.id, movie.id)

        assertNotNull(foundRating)
        assertEquals(rating.id, foundRating!!.id)
        assertEquals(user.id, foundRating.userId)
        assertEquals(movie.id, foundRating.movieId)
        assertEquals(0, BigDecimal("9.00").compareTo(foundRating.ratingValue))
        assertEquals("Awesome", foundRating.review)
    }

    @Test
    @Rollback
    fun `should return null when rating for combination of user and movie does not exist`() {
        val movie = movieDao.create("Some Movie", "Some Description", "Action", 2023, "Some Director", 120, null)
        val nonExistentUserId = UUID.randomUUID()

        val foundRating = ratingDao.findByUserAndMovie(nonExistentUserId, movie.id)

        assertNull(foundRating)
    }

    @Test
    @Rollback
    fun `should find ratings by user`() {
        val user = userDao.create("Some User", "test@some.domain")
        val movie1 = movieDao.create("Some Movie 1", "Some Description 1", "Action", 2023, "Some Director 1", 120, null)
        val movie2 = movieDao.create("Some Movie 2", "Some Description 2", "Drama", 2022, "Some Director 2", 110, null)
        val movie3 = movieDao.create("Some Movie 3", "Some Description 3", "Comedy", 2021, "Some Director 3", 100, null)
        val movie4 = movieDao.create("Movie 4", "Description 4", "Horror", 2020, "Some Director 4", 95, null)
        val movie5 = movieDao.create("Movie 5", "Description 5", "Sci-Fi", 2019, "Some Director 5", 140, null)
        
        ratingDao.create(user.id, movie1.id, BigDecimal("8.00"), "Good movie")
        ratingDao.create(user.id, movie2.id, BigDecimal("7.50"), "Nice drama")
        ratingDao.create(user.id, movie3.id, BigDecimal("9.00"), "Hilarious!")
        ratingDao.create(user.id, movie4.id, BigDecimal("6.50"), "Scary")
        ratingDao.create(user.id, movie5.id, BigDecimal("8.50"), "Great sci-fi")

        val ratings = ratingDao.findByUserId(user.id)

        assertEquals(5, ratings.size)
    }

    @Test
    @Rollback
    fun `should find ratings by movie id`() {
        val user1 = userDao.create("User 1", "user1@some.domain")
        val user2 = userDao.create("User 2", "user2@some.domain")
        val user3 = userDao.create("User 3", "user3@some.domain")
        val user4 = userDao.create("User 4", "user4@some.domain")
        val user5 = userDao.create("User 5", "user5@some.domain")
        val movie = movieDao.create("Popular Movie", "Some Description", "Action", 2023, "Some Director", 120, null)
        
        ratingDao.create(user1.id, movie.id, BigDecimal("8.00"), "Good movie")
        ratingDao.create(user2.id, movie.id, BigDecimal("7.50"), "Nice action")
        ratingDao.create(user3.id, movie.id, BigDecimal("9.00"), "Amazing!")
        ratingDao.create(user4.id, movie.id, BigDecimal("6.50"), "Okay")
        ratingDao.create(user5.id, movie.id, BigDecimal("8.50"), "Great!")

        val firstPage = ratingDao.findByMovieId(movie.id)

        assertEquals(5, firstPage.size)
    }

    @Test
    @Rollback
    fun `should update rating successfully`() {
        val user = userDao.create("Some User", "test@some.domain")
        val movie = movieDao.create("Some Movie", "Some Description", "Action", 2023, "Some Director", 120, null)
        val originalRating = ratingDao.create(user.id, movie.id, BigDecimal("7.00"), "Good movie")
        val newRatingValue = BigDecimal("9.00")
        val newReview = "Amazing movie after second watch!"

        val updatedRating = ratingDao.update(originalRating.id, newRatingValue, newReview)

        assertEquals(originalRating.id, updatedRating.id)
        assertEquals(originalRating.userId, updatedRating.userId)
        assertEquals(originalRating.movieId, updatedRating.movieId)
        assertEquals(0, newRatingValue.compareTo(updatedRating.ratingValue))
        assertEquals(newReview, updatedRating.review)
        assertEquals(originalRating.createdAt, updatedRating.createdAt)
        assertTrue(updatedRating.updatedAt > originalRating.updatedAt)
    }

    @Test
    @Rollback
    fun `should throw exception when updating non-existent rating`() {
        val nonExistentId = UUID.randomUUID()

        assertThrows<ResourceNotFoundException> {
            ratingDao.update(nonExistentId, ratingValue = BigDecimal("8.00"))
        }
    }

    @Test
    @Rollback
    fun `should delete rating successfully`() {
        val user = userDao.create("Some User", "test@some.domain")
        val movie = movieDao.create("Some Movie", "Some Description", "Action", 2023, "Some Director", 120, null)
        val rating = ratingDao.create(user.id, movie.id, BigDecimal("8.00"), "Good movie")

        val deleted = ratingDao.delete(rating.id)

        assertTrue(deleted)
        assertNull(ratingDao.findById(rating.id))
    }

    @Test
    @Rollback
    fun `should return false when rating to delete does not exist`() {
        val nonExistentId = UUID.randomUUID()

        val deleted = ratingDao.delete(nonExistentId)

        assertFalse(deleted)
    }

    @Test
    @Rollback
    fun `should get user rating stats`() {
        val user = userDao.create("Some User", "test@some.domain")
        val movie1 = movieDao.create("Some Movie 1", "Some Description 1", "Action", 2023, "Some Director 1", 120, null)
        val movie2 = movieDao.create("Some Movie 2", "Some Description 2", "Drama", 2022, "Some Director 2", 110, null)
        val movie3 = movieDao.create("Some Movie 3", "Some Description 3", "Comedy", 2021, "Some Director 3", 100, null)
        
        ratingDao.create(user.id, movie1.id, BigDecimal("8.00"), "Good")
        ratingDao.create(user.id, movie2.id, BigDecimal("6.00"), "Okay")
        ratingDao.create(user.id, movie3.id, BigDecimal("9.99"), "Perfect!")

        val (averageRating, totalRatings) = ratingDao.getUserRatingStats(user.id)

        assertEquals(3, totalRatings)
        assertNotNull(averageRating)

        assertTrue(averageRating!!.toDouble() > 7.9)
        assertTrue(averageRating.toDouble() < 8.1)
    }

    @Test
    @Rollback
    fun `should return zero stats for user with no ratings`() {
        val user = userDao.create("Some User", "test@some.domain")

        val (averageRating, totalRatings) = ratingDao.getUserRatingStats(user.id)

        assertEquals(0, totalRatings)
        assertNull(averageRating)
    }

    @Test
    @Rollback
    fun `should check if rating exists by user and movie`() {
        val user = userDao.create("Some User", "test@some.domain")
        val movie1 = movieDao.create("Some Movie 1", "Some Description 1", "Action", 2023, "Some Director 1", 120, null)
        val movie2 = movieDao.create("Some Movie 2", "Some Description 2", "Drama", 2022, "Some Director 2", 110, null)
        
        ratingDao.create(user.id, movie1.id, BigDecimal("8.00"), "Good movie")

        assertTrue(ratingDao.existsByUserAndMovie(user.id, movie1.id))
        assertFalse(ratingDao.existsByUserAndMovie(user.id, movie2.id))
        assertFalse(ratingDao.existsByUserAndMovie(UUID.randomUUID(), movie1.id))
    }
}