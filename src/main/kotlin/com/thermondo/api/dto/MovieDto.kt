package com.thermondo.api.dto

import com.thermondo.api.models.Movie
import jakarta.validation.constraints.*
import java.io.Serializable
import java.util.UUID

data class CreateMovieRequest(
    @field:NotBlank(message = "Title is required")
    @field:Size(min = 1, max = 200, message = "Title must be between 1 and 200 characters")
    val title: String,
    
    @field:Size(max = 1000, message = "Description cannot exceed 1000 characters")
    val description: String?,
    
    @field:NotBlank(message = "Genre is required")
    val genre: String,
    
    @field:Min(value = 1888, message = "Release year must be 1888 or later")
    @field:Max(value = 2025, message = "Release year cannot be in the far future")
    val releaseYear: Int,
    
    val director: String?,
    
    @field:Min(value = 1, message = "Duration must be at least 1 minute")
    val durationMinutes: Int?,
    
    val posterUrl: String?
)

data class UpdateMovieRequest(
    @field:Size(min = 1, max = 200, message = "Title must be between 1 and 200 characters")
    val title: String?,
    
    @field:Size(max = 1000, message = "Description cannot exceed 1000 characters")
    val description: String?,
    
    val genre: String?,
    
    @field:Min(value = 1888, message = "Release year must be 1888 or later")
    @field:Max(value = 2025, message = "Release year cannot be in the far future")
    val releaseYear: Int?,
    
    val director: String?,
    
    @field:Min(value = 1, message = "Duration must be at least 1 minute")
    val durationMinutes: Int?,
    
    val posterUrl: String?
)

data class MovieResponse(
    val id: UUID,
    val title: String,
    val description: String?,
    val genre: String,
    val releaseYear: Int,
    val director: String?,
    val durationMinutes: Int?,
    val posterUrl: String?,
    val averageRating: Double?,
    val totalRatings: Int
): Serializable {
    companion object {
        fun fromMovie(movie: Movie): MovieResponse {
            return MovieResponse(
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
    }
}

data class MovieSummaryResponse(
    val id: UUID,
    val title: String,
    val genre: String,
    val releaseYear: Int,
    val averageRating: Double?,
    val totalRatings: Int
): Serializable {
    companion object {
        fun fromMovie(movie: Movie): MovieSummaryResponse {
            return MovieSummaryResponse(
                id = movie.id,
                title = movie.title,
                genre = movie.genre,
                releaseYear = movie.releaseYear,
                averageRating = movie.averageRating,
                totalRatings = movie.totalRatings
            )
        }
    }
}
