package com.thermondo.api.services

import com.thermondo.api.common.ResourceNotFoundException
import com.thermondo.api.db.postgres.MovieDao
import com.thermondo.api.dto.CreateMovieRequest
import com.thermondo.api.dto.UpdateMovieRequest
import com.thermondo.api.models.Movie
import io.mockk.every
import io.mockk.mockk
import io.mockk.verify
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.assertThrows
import org.junit.jupiter.api.Assertions.*
import org.junit.jupiter.api.BeforeEach
import java.time.Instant
import java.util.*

class MovieServiceTest {

    private val movieDao = mockk<MovieDao>()
    private lateinit var movieService: MovieService

    @BeforeEach
    fun setup() {
        movieService = MovieService(movieDao)
    }

    @Test
    fun `should create movie successfully`() {
        val request = CreateMovieRequest(
            title = "The Matrix",
            description = "A description",
            genre = "Sci-Fi",
            releaseYear = 1999,
            director = "The Wachowskis",
            durationMinutes = 136,
            posterUrl = "https://some.domain/poster.jpg"
        )
        val expectedMovie = Movie(
            id = UUID.randomUUID(),
            title = request.title,
            description = request.description,
            genre = request.genre,
            releaseYear = request.releaseYear,
            director = request.director,
            durationMinutes = request.durationMinutes,
            posterUrl = request.posterUrl,
            createdAt = Instant.now(),
            updatedAt = Instant.now()
        )

        every {
            movieDao.create(
                title = request.title,
                description = request.description,
                genre = request.genre,
                releaseYear = request.releaseYear,
                director = request.director,
                durationMinutes = request.durationMinutes,
                posterUrl = request.posterUrl
            )
        } returns expectedMovie

        val result = movieService.createMovie(request)

        assertEquals(expectedMovie, result)
        verify {
            movieDao.create(
                title = request.title,
                description = request.description,
                genre = request.genre,
                releaseYear = request.releaseYear,
                director = request.director,
                durationMinutes = request.durationMinutes,
                posterUrl = request.posterUrl
            )
        }
    }

    @Test
    fun `should return movie when movie exists`() {
        val movieId = UUID.randomUUID()
        val expectedMovie = Movie(
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

        every { movieDao.findById(movieId) } returns expectedMovie

        val result = movieService.getMovieById(movieId)

        assertEquals(expectedMovie, result)
        verify { movieDao.findById(movieId) }
    }

    @Test
    fun `should throw ResourceNotFoundException when movie does not exist`() {
        val movieId = UUID.randomUUID()

        every { movieDao.findById(movieId) } returns null

        val exception = assertThrows<ResourceNotFoundException> {
            movieService.getMovieById(movieId)
        }

        assertEquals("Movie with id $movieId not found", exception.message)
        verify { movieDao.findById(movieId) }
    }

    @Test
    fun `should update movie successfully`() {
        val movieId = UUID.randomUUID()
        val request = UpdateMovieRequest(
            title = "The Matrix Reloaded",
            description = "Updated description",
            genre = "Sci-Fi",
            releaseYear = 2003,
            director = "The Wachowskis",
            durationMinutes = 138,
            posterUrl = "https://some.domain/new-poster.jpg"
        )
        val expectedMovie = Movie(
            id = movieId,
            title = "The Matrix Reloaded",
            description = "Updated description",
            genre = "Sci-Fi",
            releaseYear = 2003,
            director = "The Wachowskis",
            durationMinutes = 138,
            posterUrl = "https://some.domain/new-poster.jpg",
            createdAt = Instant.now(),
            updatedAt = Instant.now()
        )

        every {
            movieDao.update(
                id = movieId,
                title = request.title,
                description = request.description,
                genre = request.genre,
                releaseYear = request.releaseYear,
                director = request.director,
                durationMinutes = request.durationMinutes,
                posterUrl = request.posterUrl
            )
        } returns expectedMovie

        val result = movieService.updateMovie(movieId, request)

        assertEquals(expectedMovie, result)
        verify {
            movieDao.update(
                id = movieId,
                title = request.title,
                description = request.description,
                genre = request.genre,
                releaseYear = request.releaseYear,
                director = request.director,
                durationMinutes = request.durationMinutes,
                posterUrl = request.posterUrl
            )
        }
    }

    @Test
    fun `should return true when movie is deleted successfully`() {
        val movieId = UUID.randomUUID()

        every { movieDao.delete(movieId) } returns true

        val result = movieService.deleteMovie(movieId)

        assertTrue(result)
        verify { movieDao.delete(movieId) }
    }
}
