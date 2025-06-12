package com.thermondo.api.models

import com.thermondo.api.db.postgres.tables.records.MovieRecord
import java.time.Instant
import java.util.UUID

data class Movie (
    val id: UUID,
    val title: String,
    val description: String?,
    val genre: String,
    val releaseYear: Int,
    val director: String?,
    val durationMinutes: Int?,
    val posterUrl: String?,
    val createdAt: Instant = Instant.now(),
    val updatedAt: Instant = Instant.now(),
    val averageRating: Double? = null,
    val totalRatings: Int = 0
) {
    companion object {
        fun fromRecord(movieRecord: MovieRecord, averageRating: Double? = null, totalRatings: Int = 0): Movie {
            return Movie(
                id = movieRecord.id!!,
                title = movieRecord.title!!,
                description = movieRecord.description,
                genre = movieRecord.genre!!,
                releaseYear = movieRecord.releaseYear!!,
                director = movieRecord.director,
                durationMinutes = movieRecord.durationMinutes,
                posterUrl = movieRecord.posterUrl,
                createdAt = movieRecord.createdAt!!,
                updatedAt = movieRecord.updatedAt!!,
                averageRating = averageRating,
                totalRatings = totalRatings
            )
        }
    }
}
