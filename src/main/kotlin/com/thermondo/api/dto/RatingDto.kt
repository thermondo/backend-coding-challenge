package com.thermondo.api.dto

import com.thermondo.api.models.Rating
import com.thermondo.api.models.UserRatingProfile
import jakarta.validation.constraints.*
import java.io.Serializable
import java.math.BigDecimal
import java.util.UUID

data class CreateRatingRequest(
    @field:NotNull(message = "Movie ID is required")
    val movieId: UUID,
    
    @field:NotNull(message = "Rating value is required")
    @field:DecimalMin(value = "1.0", message = "Rating must be at least 1.0")
    @field:DecimalMax(value = "10.0", message = "Rating cannot exceed 10.0")
    val ratingValue: BigDecimal,
    
    @field:Size(max = 1000, message = "Review cannot exceed 1000 characters")
    val review: String?
)

data class UpdateRatingRequest(
    @field:DecimalMin(value = "1.0", message = "Rating must be at least 1.0")
    @field:DecimalMax(value = "10.0", message = "Rating cannot exceed 10.0")
    val ratingValue: BigDecimal?,
    
    @field:Size(max = 1000, message = "Review cannot exceed 1000 characters")
    val review: String?
)

data class RatingResponse(
    val id: UUID,
    val userId: UUID,
    val movieId: UUID,
    val ratingValue: BigDecimal,
    val review: String?,
    val movieTitle: String?,
    val userName: String?
):Serializable {
    companion object {
        fun fromRating(rating: Rating): RatingResponse {
            return RatingResponse(
                id = rating.id,
                userId = rating.userId,
                movieId = rating.movieId,
                ratingValue = rating.ratingValue,
                review = rating.review,
                movieTitle = rating.movieTitle,
                userName = rating.userName
            )
        }
    }
}

data class UserRatingProfileResponse(
    val userId: UUID,
    val userName: String,
    val totalRatings: Int,
    val averageRating: BigDecimal?,
    val ratings: List<RatingResponse>
):Serializable {
    companion object {
        fun fromUserRatingProfile(profile: UserRatingProfile): UserRatingProfileResponse {
            return UserRatingProfileResponse(
                userId = profile.userId,
                userName = profile.userName,
                totalRatings = profile.totalRatings,
                averageRating = profile.averageRating,
                ratings = profile.ratings.map { rating ->
                    RatingResponse(
                        id = rating.id,
                        userId = rating.userId,
                        movieId = rating.movieId,
                        ratingValue = rating.ratingValue,
                        review = rating.review,
                        movieTitle = rating.movieTitle,
                        userName = rating.userName
                    )
                }
            )
        }
    }
}
