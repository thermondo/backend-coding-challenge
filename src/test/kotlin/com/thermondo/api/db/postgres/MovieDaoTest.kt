package com.thermondo.api.db.postgres

import com.thermondo.api.IntegrationTest
import com.thermondo.api.common.ResourceNotFoundException
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.assertThrows
import org.junit.jupiter.api.Assertions.*
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.test.annotation.Rollback
import java.time.Instant
import java.util.*

@IntegrationTest
class MovieDaoTest {
    @Autowired
    private lateinit var movieDao: MovieDao

    @Test
    @Rollback
    fun `should create movie successfully`() {
        val title = "Some Movie"
        val description = "A Some Movie description"
        val genre = "Action"
        val releaseYear = 2023
        val director = "Test Director"
        val durationMinutes = 120
        val posterUrl = "https://some.domain/poster.jpg"

        val createdMovie = movieDao.create(title, description, genre, releaseYear, director, durationMinutes, posterUrl)

        assertNotNull(createdMovie.id)
        assertEquals(title, createdMovie.title)
        assertEquals(description, createdMovie.description)
        assertEquals(genre, createdMovie.genre)
        assertEquals(releaseYear, createdMovie.releaseYear)
        assertEquals(director, createdMovie.director)
        assertEquals(durationMinutes, createdMovie.durationMinutes)
        assertEquals(posterUrl, createdMovie.posterUrl)
        assertNotNull(createdMovie.createdAt)
        assertNotNull(createdMovie.updatedAt)
        assertTrue(createdMovie.createdAt.isBefore(Instant.now().plusSeconds(1)))
        assertTrue(createdMovie.updatedAt.isBefore(Instant.now().plusSeconds(1)))
        assertNull(createdMovie.averageRating)
        assertEquals(0, createdMovie.totalRatings)
    }

    @Test
    @Rollback
    fun `should find movie by id when exists`() {
        val movie = movieDao.create("Some Movie", "Some Description", "Drama", 2023, "Some Director", 90, null)

        val foundMovie = movieDao.findById(movie.id)

        assertNotNull(foundMovie)
        assertEquals(movie.id, foundMovie!!.id)
        assertEquals(movie.title, foundMovie.title)
        assertEquals(movie.description, foundMovie.description)
        assertEquals(movie.genre, foundMovie.genre)
        assertEquals(movie.releaseYear, foundMovie.releaseYear)
        assertEquals(movie.director, foundMovie.director)
        assertEquals(movie.durationMinutes, foundMovie.durationMinutes)
        assertEquals(movie.posterUrl, foundMovie.posterUrl)
    }

    @Test
    @Rollback
    fun `should return null when movie does not exists`() {
        val nonExistentId = UUID.randomUUID()

        val foundMovie = movieDao.findById(nonExistentId)

        assertNull(foundMovie)
    }

    @Test
    @Rollback
    fun `should find all movies`() {
        movieDao.create("Some Movie 1", "Some Description 1", "Action", 2023, "Some Director 1", 120, null)
        movieDao.create("Some Movie 2", "Some Description 2", "Drama", 2022, "Some Director 2", 110, null)
        movieDao.create("Some Movie 3", "Some Description 3", "Comedy", 2021, "Some Director 3", 100, null)
        movieDao.create("Movie 4", "Description 4", "Horror", 2020, "Some Director 4", 95, null)
        movieDao.create("Movie 5", "Description 5", "Sci-Fi", 2019, "Some Director 5", 140, null)

        val movies = movieDao.findAll()

        //Since we already have 5 movies inside a migration
        assertEquals(10, movies.size)
    }

    @Test
    @Rollback
    fun `should update movie successfully`() {
        val originalMovie = movieDao.create("Original Title", "Original Description", "Action", 2023, "Original Director", 120, null)
        val newTitle = "Updated Title"
        val newDescription = "Updated Description"
        val newGenre = "Drama"
        val newReleaseYear = 2024
        val newDirector = "Updated Director"
        val newDurationMinutes = 130
        val newPosterUrl = "https://some.domain/new-poster.jpg"

        val updatedMovie = movieDao.update(
            originalMovie.id, 
            newTitle, 
            newDescription, 
            newGenre, 
            newReleaseYear, 
            newDirector, 
            newDurationMinutes, 
            newPosterUrl
        )

        assertEquals(originalMovie.id, updatedMovie.id)
        assertEquals(newTitle, updatedMovie.title)
        assertEquals(newDescription, updatedMovie.description)
        assertEquals(newGenre, updatedMovie.genre)
        assertEquals(newReleaseYear, updatedMovie.releaseYear)
        assertEquals(newDirector, updatedMovie.director)
        assertEquals(newDurationMinutes, updatedMovie.durationMinutes)
        assertEquals(newPosterUrl, updatedMovie.posterUrl)
        assertEquals(originalMovie.createdAt, updatedMovie.createdAt)
        assertTrue(updatedMovie.updatedAt > originalMovie.updatedAt)
    }

    @Test
    @Rollback
    fun `should throw exception when movies to update does not exist`() {
        val nonExistentId = UUID.randomUUID()

        assertThrows<ResourceNotFoundException> {
            movieDao.update(nonExistentId, title = "New Title")
        }
    }

    @Test
    @Rollback
    fun `should delete movie successfully`() {
        val movie = movieDao.create("Movie to Delete", "Some Description", "Action", 2023, "Some Director", 120, null)

        val deleted = movieDao.delete(movie.id)

        assertTrue(deleted)
        assertNull(movieDao.findById(movie.id))
    }

    @Test
    @Rollback
    fun `should return false when movie to delete does not exist`() {
        val nonExistentId = UUID.randomUUID()

        val deleted = movieDao.delete(nonExistentId)

        assertFalse(deleted)
    }
}