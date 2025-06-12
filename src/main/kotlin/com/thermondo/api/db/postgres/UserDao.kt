package com.thermondo.api.db.postgres

import com.thermondo.api.common.ResourceNotFoundException
import com.thermondo.api.db.postgres.tables.records.UserRecord
import com.thermondo.api.db.postgres.tables.references.USER
import com.thermondo.api.models.User
import org.jooq.DSLContext
import org.springframework.stereotype.Component
import java.time.Instant
import java.util.*

@Component
class UserDao(
    private val dslContext: DSLContext
) {
    
    fun findById(id: UUID): User? {
        return dslContext.selectFrom(USER)
            .where(USER.ID.eq(id))
            .fetchOne()
            ?.let { User.fromRecord(it) }
    }

    fun findAll(): List<User> {
        return dslContext.selectFrom(USER)
            .orderBy(USER.CREATED_AT.desc())
            .fetch()
            .map { User.fromRecord(it) }
    }

    fun create(name: String, email: String): User {
        val id = UUID.randomUUID()
        val now = Instant.now()
        
        val record = dslContext.insertInto(USER)
            .set(USER.ID, id)
            .set(USER.NAME, name)
            .set(USER.EMAIL, email)
            .set(USER.CREATED_AT, now)
            .set(USER.UPDATED_AT, now)
            .returning()
            .fetchOne()
            ?: throw RuntimeException("Failed to create user")
            
        return User.fromRecord(record)
    }

    fun update(id: UUID, name: String? = null): User {
        findById(id) ?: throw ResourceNotFoundException("User not found")
        val now = Instant.now()
        
        val updateStep = dslContext.update(USER)
            .set(USER.UPDATED_AT, now)
        
        name?.let { updateStep.set(USER.NAME, it) }
        
        updateStep.where(USER.ID.eq(id)).execute()
        
        return findById(id) ?: throw RuntimeException("Failed to update user")
    }

    fun delete(id: UUID): Boolean {
        return dslContext.deleteFrom(USER)
            .where(USER.ID.eq(id))
            .execute() > 0
    }

    fun existsByEmail(email: String): Boolean {
        return dslContext.fetchExists(
            dslContext.selectFrom(USER)
                .where(USER.EMAIL.eq(email))
        )
    }
}