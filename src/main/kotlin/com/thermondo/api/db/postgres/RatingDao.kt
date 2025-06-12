package com.thermondo.api.db.postgres

import com.thermondo.api.common.ResourceNotFoundException
import com.thermondo.api.db.postgres.tables.records.RatingRecord
import com.thermondo.api.db.postgres.tables.references.RATING
import com.thermondo.api.db.postgres.tables.references.MOVIE
import com.thermondo.api.db.postgres.tables.references.USER
import com.thermondo.api.models.Rating
import org.jooq.DSLContext
import org.jooq.Record
import org.jooq.impl.DSL
import org.springframework.stereotype.Component
import java.math.BigDecimal
import java.time.Instant
import java.util.*

@Component
class RatingDao(
    private val dslContext: DSLContext
) {
    
    fun findById(id: UUID): Rating? {
        return dslContext.select(
            RATING.asterisk(),
            MOVIE.TITLE,
            USER.NAME
        )
        .from(RATING)
        .leftJoin(MOVIE).on(RATING.MOVIE_ID.eq(MOVIE.ID))
        .leftJoin(USER).on(RATING.USER_ID.eq(USER.ID))
        .where(RATING.ID.eq(id))
        .fetchOne()
        ?.let { record ->
            val ratingRecord = record.into(RATING)
            val movieTitle = record.getValue(MOVIE.TITLE)
            val userName = record.getValue(USER.NAME)
            Rating.fromRecord(ratingRecord, movieTitle, userName)
        }
    }

    fun findByUserAndMovie(userId: UUID, movieId: UUID): Rating? {
        return dslContext.select(
            RATING.asterisk(),
            MOVIE.TITLE,
            USER.NAME
        )
        .from(RATING)
        .leftJoin(MOVIE).on(RATING.MOVIE_ID.eq(MOVIE.ID))
        .leftJoin(USER).on(RATING.USER_ID.eq(USER.ID))
        .where(RATING.USER_ID.eq(userId).and(RATING.MOVIE_ID.eq(movieId)))
        .fetchOne()
        ?.let { record ->
            val ratingRecord = record.into(RATING)
            val movieTitle = record.getValue(MOVIE.TITLE)
            val userName = record.getValue(USER.NAME)
            Rating.fromRecord(ratingRecord, movieTitle, userName)
        }
    }

    fun findByUserId(userId: UUID): List<Rating> {
        return dslContext.select(
            RATING.asterisk(),
            MOVIE.TITLE,
            USER.NAME
        )
        .from(RATING)
        .leftJoin(MOVIE).on(RATING.MOVIE_ID.eq(MOVIE.ID))
        .leftJoin(USER).on(RATING.USER_ID.eq(USER.ID))
        .where(RATING.USER_ID.eq(userId))
        .orderBy(RATING.CREATED_AT.desc())
        .fetch()
        .map { record: Record ->
            val ratingRecord = record.into(RATING)
            val movieTitle = record.getValue(MOVIE.TITLE)
            val userName = record.getValue(USER.NAME)
            Rating.fromRecord(ratingRecord, movieTitle, userName)
        }
    }

    fun findByMovieId(movieId: UUID): List<Rating> {
        return dslContext.select(
            RATING.asterisk(),
            MOVIE.TITLE,
            USER.NAME
        )
        .from(RATING)
        .leftJoin(MOVIE).on(RATING.MOVIE_ID.eq(MOVIE.ID))
        .leftJoin(USER).on(RATING.USER_ID.eq(USER.ID))
        .where(RATING.MOVIE_ID.eq(movieId))
        .orderBy(RATING.CREATED_AT.desc())
        .fetch()
        .map { record: Record ->
            val ratingRecord = record.into(RATING)
            val movieTitle = record.getValue(MOVIE.TITLE)
            val userName = record.getValue(USER.NAME)
            Rating.fromRecord(ratingRecord, movieTitle, userName)
        }
    }

    fun create(userId: UUID, movieId: UUID, ratingValue: BigDecimal, review: String?): Rating {
        val id = UUID.randomUUID()
        val now = Instant.now()
        
        val record = dslContext.insertInto(RATING)
            .set(RATING.ID, id)
            .set(RATING.USER_ID, userId)
            .set(RATING.MOVIE_ID, movieId)
            .set(RATING.RATING_VALUE, ratingValue)
            .set(RATING.REVIEW, review)
            .set(RATING.CREATED_AT, now)
            .set(RATING.UPDATED_AT, now)
            .returning()
            .fetchOne()
            ?: throw RuntimeException("Failed to create rating")
            
        return findById(record.id!!) ?: throw RuntimeException("Failed to retrieve created rating")
    }

    fun update(id: UUID, ratingValue: BigDecimal? = null, review: String? = null): Rating {
        findById(id) ?: throw ResourceNotFoundException("Rating not found")
        val now = Instant.now()
        
        val updateStep = dslContext.update(RATING)
            .set(RATING.UPDATED_AT, now)
        
        ratingValue?.let { updateStep.set(RATING.RATING_VALUE, it) }
        review?.let { updateStep.set(RATING.REVIEW, it) }
        
        updateStep.where(RATING.ID.eq(id)).execute()
        
        return findById(id) ?: throw RuntimeException("Failed to update rating")
    }

    fun delete(id: UUID): Boolean {
        return dslContext.deleteFrom(RATING)
            .where(RATING.ID.eq(id))
            .execute() > 0
    }


    fun getUserRatingStats(userId: UUID): Pair<BigDecimal?, Int> {
        val result = dslContext.select(
            DSL.avg(RATING.RATING_VALUE).`as`("avg_rating"),
            DSL.count(RATING.ID).`as`("total_ratings")
        )
        .from(RATING)
        .where(RATING.USER_ID.eq(userId))
        .fetchOne()
        
        val avgRating = result?.getValue("avg_rating") as? BigDecimal
        val totalRatings = (result?.getValue("total_ratings") as? Int) ?: 0
        
        return Pair(avgRating, totalRatings)
    }

    fun existsByUserAndMovie(userId: UUID, movieId: UUID): Boolean {
        return dslContext.fetchExists(
            dslContext.selectFrom(RATING)
                .where(RATING.USER_ID.eq(userId).and(RATING.MOVIE_ID.eq(movieId)))
        )
    }
}
