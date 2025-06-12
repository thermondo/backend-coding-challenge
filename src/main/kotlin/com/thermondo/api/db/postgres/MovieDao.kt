package com.thermondo.api.db.postgres

import com.thermondo.api.common.ResourceNotFoundException
import com.thermondo.api.db.postgres.tables.records.MovieRecord
import com.thermondo.api.db.postgres.tables.references.MOVIE
import com.thermondo.api.db.postgres.tables.references.RATING
import com.thermondo.api.models.Movie
import org.jooq.DSLContext
import org.jooq.Record
import org.jooq.impl.DSL
import org.springframework.stereotype.Component
import java.time.Instant
import java.util.*

@Component
class MovieDao(
    private val dslContext: DSLContext
) {
    
    fun findById(id: UUID): Movie? {
        val record = dslContext.selectFrom(MOVIE)
            .where(MOVIE.ID.eq(id))
            .fetchOne()
            ?: return null
            
        val (avgRating, totalRatings) = getRatingStats(id)
        return Movie.fromRecord(record, avgRating, totalRatings)
    }

    fun findAll(): List<Movie> {
        val query = dslContext.selectFrom(MOVIE)
        
        val movies = query.orderBy(MOVIE.CREATED_AT.desc())
            .fetch()
            
        return movies.map { movieRecord: MovieRecord ->
            val (avgRating, totalRatings) = getRatingStats(movieRecord.id!!)
            Movie.fromRecord(movieRecord, avgRating, totalRatings)
        }
    }

    fun create(title: String, description: String?, genre: String, releaseYear: Int, 
               director: String?, durationMinutes: Int?, posterUrl: String?): Movie {
        val id = UUID.randomUUID()
        val now = Instant.now()
        
        val record = dslContext.insertInto(MOVIE)
            .set(MOVIE.ID, id)
            .set(MOVIE.TITLE, title)
            .set(MOVIE.DESCRIPTION, description)
            .set(MOVIE.GENRE, genre)
            .set(MOVIE.RELEASE_YEAR, releaseYear)
            .set(MOVIE.DIRECTOR, director)
            .set(MOVIE.DURATION_MINUTES, durationMinutes)
            .set(MOVIE.POSTER_URL, posterUrl)
            .set(MOVIE.CREATED_AT, now)
            .set(MOVIE.UPDATED_AT, now)
            .returning()
            .fetchOne()
            ?: throw RuntimeException("Failed to create movie")
            
        return Movie.fromRecord(record, null, 0)
    }

    fun update(id: UUID, title: String? = null, description: String? = null, 
               genre: String? = null, releaseYear: Int? = null, director: String? = null,
               durationMinutes: Int? = null, posterUrl: String? = null): Movie {
        findById(id) ?: throw ResourceNotFoundException("Movie not found")
        val now = Instant.now()
        
        val updateStep = dslContext.update(MOVIE)
            .set(MOVIE.UPDATED_AT, now)
        
        title?.let { updateStep.set(MOVIE.TITLE, it) }
        description?.let { updateStep.set(MOVIE.DESCRIPTION, it) }
        genre?.let { updateStep.set(MOVIE.GENRE, it) }
        releaseYear?.let { updateStep.set(MOVIE.RELEASE_YEAR, it) }
        director?.let { updateStep.set(MOVIE.DIRECTOR, it) }
        durationMinutes?.let { updateStep.set(MOVIE.DURATION_MINUTES, it) }
        posterUrl?.let { updateStep.set(MOVIE.POSTER_URL, it) }
        
        updateStep.where(MOVIE.ID.eq(id)).execute()
        
        return findById(id) ?: throw RuntimeException("Failed to update movie")
    }

    fun delete(id: UUID): Boolean {
        return dslContext.deleteFrom(MOVIE)
            .where(MOVIE.ID.eq(id))
            .execute() > 0
    }

    private fun getRatingStats(movieId: UUID): Pair<Double?, Int> {
        val result = dslContext.select(
            DSL.avg(RATING.RATING_VALUE).`as`("avg_rating"),
            DSL.count(RATING.ID).`as`("total_ratings")
        )
        .from(RATING)
        .where(RATING.MOVIE_ID.eq(movieId))
        .fetchOne()

        val avgRating = result?.getValue("avg_rating") as? Double
        val totalRatings = (result?.getValue("total_ratings") as? Long)?.toInt() ?: 0

        return Pair(avgRating, totalRatings)
    }
}
