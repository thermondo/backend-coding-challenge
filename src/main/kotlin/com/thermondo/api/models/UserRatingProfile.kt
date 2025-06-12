package com.thermondo.api.models

import com.thermondo.api.dto.RatingResponse
import java.math.BigDecimal
import java.util.UUID


data class UserRatingProfile(
    val userId: UUID,
    val userName: String,
    val totalRatings: Int,
    val averageRating: BigDecimal?,
    val ratings: List<Rating>
)