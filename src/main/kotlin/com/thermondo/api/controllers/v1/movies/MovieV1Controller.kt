package com.thermondo.api.controllers.v1.movies

import com.thermondo.api.dto.*
import com.thermondo.api.dto.MovieResponse.Companion.fromMovie
import com.thermondo.api.dto.MovieSummaryResponse.Companion.fromMovie as movieSummaryResponseFromMovie
import com.thermondo.api.services.MovieService
import io.swagger.v3.oas.annotations.Operation
import io.swagger.v3.oas.annotations.tags.Tag
import jakarta.validation.Valid
import org.slf4j.LoggerFactory
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*
import java.util.*

@RestController
@RequestMapping("/api/v1/movies")
@Tag(name = "Movies", description = "Movie management endpoints")
class MovieV1Controller(
    private val movieService: MovieService,
) {
    private val logger = LoggerFactory.getLogger(MovieV1Controller::class.java)

    @PostMapping
    @Operation(summary = "Create a new movie")
    fun createMovie(@Valid @RequestBody request: CreateMovieRequest): ResponseEntity<MovieResponse> {
        logger.info("Creating movie with title: ${request.title}")
        val response = movieService.createMovie(request).let { movie ->
            MovieResponse(
                id = movie.id,
                title = movie.title,
                description = movie.description,
                genre = movie.genre,
                releaseYear = movie.releaseYear,
                director = movie.director,
                durationMinutes = movie.durationMinutes,
                posterUrl = movie.posterUrl,
                averageRating = movie.averageRating,
                totalRatings = movie.totalRatings
            )
        }
        return ResponseEntity.status(HttpStatus.CREATED).body(response)
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get movie by ID")
    fun getMovieById(@PathVariable id: UUID): ResponseEntity<MovieResponse> {
        logger.debug("Fetching movie with id: $id")
        val response = fromMovie(movieService.getMovieById(id))
        return ResponseEntity.ok(response)
    }

    @GetMapping
    @Operation(summary = "Get all movies")
    fun getAllMovies(
    ): ResponseEntity<List<MovieSummaryResponse>> {
        logger.debug("Fetching all movies")
        val response = movieService.getAllMovies().map { movie ->
            movieSummaryResponseFromMovie(movie)
        }
        return ResponseEntity.ok(response)
    }

    @PutMapping("/{id}")
    @Operation(summary = "Update movie")
    fun updateMovie(
        @PathVariable id: UUID,
        @Valid @RequestBody request: UpdateMovieRequest
    ): ResponseEntity<MovieResponse> {
        logger.info("Updating movie with id: $id")
        val response = fromMovie(movieService.updateMovie(id, request))
        return ResponseEntity.ok(response)
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete movie")
    fun deleteMovie(@PathVariable id: UUID): ResponseEntity<Map<String, String>> {
        logger.info("Deleting movie with id: $id")
        movieService.deleteMovie(id)
        return ResponseEntity.ok(mapOf("message" to "Movie deleted successfully"))
    }
}
