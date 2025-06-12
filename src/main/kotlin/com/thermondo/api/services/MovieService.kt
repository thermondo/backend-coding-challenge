package com.thermondo.api.services

import com.thermondo.api.common.ResourceNotFoundException
import com.thermondo.api.db.postgres.MovieDao
import com.thermondo.api.dto.*
import com.thermondo.api.models.Movie
import org.slf4j.LoggerFactory
import org.springframework.cache.annotation.Cacheable
import org.springframework.cache.annotation.CacheEvict
import org.springframework.stereotype.Service
import java.util.*

@Service
class MovieService(
    private val movieDao: MovieDao,
) {
    private val logger = LoggerFactory.getLogger(MovieService::class.java)

    fun createMovie(request: CreateMovieRequest): Movie {
        logger.info("Creating movie with title: ${request.title}")
        
        val movie = movieDao.create(
            title = request.title,
            description = request.description,
            genre = request.genre,
            releaseYear = request.releaseYear,
            director = request.director,
            durationMinutes = request.durationMinutes,
            posterUrl = request.posterUrl
        )
        
        logger.info("Successfully created movie with id: ${movie.id}")
        
        return movie
    }

    @Cacheable(value = ["movies"], key = "#id")
    fun getMovieById(id: UUID): Movie {
        logger.debug("Fetching movie with id: $id")
        
        return movieDao.findById(id)
            ?: throw ResourceNotFoundException("Movie with id $id not found")
    }

    @Cacheable(value = ["moviesList"], key = "'all'")
    fun getAllMovies(): List<Movie> {
        logger.debug("Fetching all movies")
        
        return movieDao.findAll()
    }

    @CacheEvict(value = ["movies"], key = "#id")
    fun updateMovie(id: UUID, request: UpdateMovieRequest): Movie {
        logger.info("Updating movie with id: $id")
        
        val movie = movieDao.update(
            id = id,
            title = request.title,
            description = request.description,
            genre = request.genre,
            releaseYear = request.releaseYear,
            director = request.director,
            durationMinutes = request.durationMinutes,
            posterUrl = request.posterUrl
        )
        
        logger.info("Successfully updated movie with id: ${movie.id}")
        
        return movie
    }

    @CacheEvict(value = ["movies", "moviesList", "topRatedMovies"], allEntries = true)
    fun deleteMovie(id: UUID): Boolean {
        logger.info("Deleting movie with id: $id")
        
        if (!movieDao.delete(id)) {
            throw ResourceNotFoundException("Movie with id $id not found")
        }
        
        logger.info("Successfully deleted movie with id: $id")
        return true
    }
}
