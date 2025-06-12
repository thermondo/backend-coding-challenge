package com.thermondo.api.models

import com.thermondo.api.db.postgres.tables.records.RatingRecord
import java.math.BigDecimal
import java.time.Instant
import java.util.UUID

data class Rating (
    val id: UUID,
    val userId: UUID,
    val movieId: UUID,
    val ratingValue: BigDecimal,
    val review: String?,
    val createdAt: Instant = Instant.now(),
    val updatedAt: Instant = Instant.now(),
    val movieTitle: String? = null,
    val userName: String? = null
) {
    companion object {
        fun fromRecord(ratingRecord: RatingRecord, movieTitle: String? = null, userName: String? = null): Rating {
            return Rating(
                id = ratingRecord.id!!,
                userId = ratingRecord.userId!!,
                movieId = ratingRecord.movieId!!,
                ratingValue = ratingRecord.ratingValue!!,
                review = ratingRecord.review,
                createdAt = ratingRecord.createdAt!!,
                updatedAt = ratingRecord.updatedAt!!,
                movieTitle = movieTitle,
                userName = userName
            )
        }
    }
}
