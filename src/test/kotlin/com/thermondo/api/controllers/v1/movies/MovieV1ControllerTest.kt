package com.thermondo.api.controllers.v1.movies

import com.fasterxml.jackson.databind.ObjectMapper
import com.thermondo.api.dto.CreateMovieRequest
import com.thermondo.api.dto.MovieResponse
import com.thermondo.api.dto.MovieSummaryResponse
import com.thermondo.api.models.Movie
import com.thermondo.api.services.MovieService
import io.mockk.every
import io.mockk.mockk
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
import java.util.*

@WebMvcTest(controllers = [MovieV1Controller::class], excludeAutoConfiguration = [org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration::class])
@ActiveProfiles("test")
class MovieV1ControllerTest {

    @Autowired
    private lateinit var mockMvc: MockMvc

    @Autowired
    private lateinit var objectMapper: ObjectMapper

    @TestConfiguration
    class TestConfig {
        @Bean
        @Primary
        fun movieService(): MovieService = mockk()
    }

    @Autowired
    private lateinit var movieService: MovieService

    @Test
    fun `should return movie when it exists`() {
        val movieId = UUID.randomUUID()
        val movie = Movie(
            id = movieId,
            title = "Some Movie",
            description = "A Some Movie",
            genre = "Action",
            releaseYear = 2023,
            director = "Test Director",
            durationMinutes = 120,
            posterUrl = "http://some.domain/poster.jpg",
            averageRating = 4.5,
            totalRatings = 10
        )

        every { movieService.getMovieById(movieId) } returns movie

        mockMvc.perform(get("/api/v1/movies/{id}", movieId))
            .andExpect(status().isOk)
            .andExpect(content().contentType(MediaType.APPLICATION_JSON))
            .andExpect(jsonPath("$.title").value("Some Movie"))
            .andExpect(jsonPath("$.genre").value("Action"))
            .andExpect(jsonPath("$.releaseYear").value(2023))
            .andExpect(jsonPath("$.averageRating").value(4.5))
    }

    @Test
    fun `should create movie successfully`() {
        val movieRequest = CreateMovieRequest(
            title = "New Movie",
            description = "A new movie",
            genre = "Comedy",
            releaseYear = 2024,
            director = "New Director",
            durationMinutes = 90,
            posterUrl = "http://some.domain/poster.jpg"
        )

        val createdMovie = Movie(
            id = UUID.randomUUID(),
            title = "New Movie",
            description = "A new movie",
            genre = "Comedy",
            releaseYear = 2024,
            director = "New Director",
            durationMinutes = 90,
            posterUrl = "http://some.domain/poster.jpg",
            averageRating = null,
            totalRatings = 0
        )

        every { movieService.createMovie(movieRequest) } returns createdMovie

        mockMvc.perform(
            post("/api/v1/movies")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(movieRequest))
        )
            .andExpect(status().isCreated)
            .andExpect(content().contentType(MediaType.APPLICATION_JSON))
            .andExpect(jsonPath("$.title").value("New Movie"))
            .andExpect(jsonPath("$.genre").value("Comedy"))
            .andExpect(jsonPath("$.releaseYear").value(2024))
    }

    @Test
    fun `should return movies list`() {
        val movies = listOf(
            Movie(
                id = UUID.randomUUID(),
                title = "Some Movie 1",
                description = "Some Description 1",
                genre = "Action",
                releaseYear = 2021,
                director = "Some Director 1",
                durationMinutes = 120,
                posterUrl = "http://some.domain/poster1.jpg",
                averageRating = 4.0,
                totalRatings = 100
            ),
            Movie(
                id = UUID.randomUUID(),
                title = "Some Movie 2",
                description = "Some Description 2",
                genre = "Comedy",
                releaseYear = 2022,
                director = "Some Director 2",
                durationMinutes = 90,
                posterUrl = "http://some.domain/poster2.jpg",
                averageRating = 3.5,
                totalRatings = 50
            )
        )

        every { movieService.getAllMovies() } returns movies

        mockMvc.perform(get("/api/v1/movies"))
            .andExpect(status().isOk)
            .andExpect(content().contentType(MediaType.APPLICATION_JSON))
            .andExpect(jsonPath("$").isArray)
            .andExpect(jsonPath("$.length()").value(2))
            .andExpect(jsonPath("$[0].title").value("Some Movie 1"))
            .andExpect(jsonPath("$[1].title").value("Some Movie 2"))
    }
}
