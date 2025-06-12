package com.thermondo.api.models

import com.thermondo.api.db.postgres.tables.records.UserRecord
import java.time.Instant
import java.util.UUID

data class User (
    val id: UUID,
    val name: String,
    val email: String,
    val createdAt: Instant = Instant.now(),
    val updatedAt: Instant = Instant.now()
) {
    companion object {
        fun fromRecord(userRecord: UserRecord): User {
            return User(
                id = userRecord.id!!,
                name = userRecord.name!!,
                email = userRecord.email!!,
                createdAt = userRecord.createdAt!!,
                updatedAt = userRecord.updatedAt!!
            )
        }
    }
}
