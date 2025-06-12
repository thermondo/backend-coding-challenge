package com.thermondo.api.services

import com.thermondo.api.common.DuplicateResourceException
import com.thermondo.api.common.ResourceNotFoundException
import com.thermondo.api.db.postgres.RatingDao
import com.thermondo.api.db.postgres.UserDao
import com.thermondo.api.db.postgres.MovieDao
import com.thermondo.api.dto.*
import com.thermondo.api.models.Rating
import com.thermondo.api.models.UserRatingProfile
import org.slf4j.LoggerFactory
import org.springframework.cache.annotation.CacheEvict
import org.springframework.cache.annotation.Cacheable
import org.springframework.stereotype.Service
import java.util.*

@Service
class RatingService(
    private val ratingDao: RatingDao,
    private val userDao: UserDao,
    private val movieDao: MovieDao,
) {
    private val logger = LoggerFactory.getLogger(RatingService::class.java)

    @CacheEvict(value = ["movies", "moviesList", "topRatedMovies"], allEntries = true)
    fun createRating(userId: UUID, request: CreateRatingRequest): Rating {
        logger.info("Creating rating for user: $userId, movie: ${request.movieId}")
        
        userDao.findById(userId) ?: throw ResourceNotFoundException("User with id $userId not found")
        
        movieDao.findById(request.movieId) ?: throw ResourceNotFoundException("Movie with id ${request.movieId} not found")
        
        if (ratingDao.existsByUserAndMovie(userId, request.movieId)) {
            throw DuplicateResourceException("User has already rated this movie")
        }
        
        val rating = ratingDao.create(
            userId = userId,
            movieId = request.movieId,
            ratingValue = request.ratingValue,
            review = request.review
        )
        
        logger.info("Successfully created rating with id: ${rating.id}")
        
        return rating
    }

    fun getRatingById(id: UUID): Rating {
        logger.debug("Fetching rating with id: $id")
        
        return ratingDao.findById(id)
            ?: throw ResourceNotFoundException("Rating with id $id not found")
    }

    fun getUserRating(userId: UUID, movieId: UUID): Rating {
        logger.debug("Fetching rating for user: $userId, movie: $movieId")
        
        return ratingDao.findByUserAndMovie(userId, movieId)
            ?: throw ResourceNotFoundException("Rating not found for this user and movie")
    }

    fun getRatingsByUserId(userId: UUID): List<Rating> {
        logger.debug("Fetching ratings for user: $userId")
        
        userDao.findById(userId) ?: throw ResourceNotFoundException("User with id $userId not found")
        
        return ratingDao.findByUserId(userId,)
    }

    fun getRatingsByMovieId(movieId: UUID): List<Rating> {
        logger.debug("Fetching ratings for movie: $movieId")
        
        movieDao.findById(movieId) ?: throw ResourceNotFoundException("Movie with id $movieId not found")
        
        return ratingDao.findByMovieId(movieId)
    }

    @CacheEvict(value = ["movies", "moviesList", "topRatedMovies"], allEntries = true)
    fun updateRating(id: UUID, request: UpdateRatingRequest): Rating {
        logger.info("Updating rating with id: $id")
        
        val rating = ratingDao.update(
            id = id,
            ratingValue = request.ratingValue,
            review = request.review
        )
        
        logger.info("Successfully updated rating with id: ${rating.id}")
        
        return rating
    }

    @CacheEvict(value = ["movies", "moviesList", "topRatedMovies"], allEntries = true)
    fun deleteRating(id: UUID): Boolean {
        logger.info("Deleting rating with id: $id")
        
        if (!ratingDao.delete(id)) {
            throw ResourceNotFoundException("Rating with id $id not found")
        }
        
        logger.info("Successfully deleted rating with id: $id")
        return true
    }

    @Cacheable(value = ["userProfile"], key = "#userId")
    fun getUserRatingProfile(userId: UUID): UserRatingProfile {
        logger.debug("Fetching rating profile for user: $userId")
        
        val user = userDao.findById(userId) 
            ?: throw ResourceNotFoundException("User with id $userId not found")
        
        val ratings = ratingDao.findByUserId(userId)
        val (averageRating, totalRatings) = ratingDao.getUserRatingStats(userId)
        
        return UserRatingProfile(
            userId = user.id,
            userName = user.name,
            totalRatings = totalRatings,
            averageRating = averageRating,
            ratings = ratings.map { rating ->
                Rating(
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
