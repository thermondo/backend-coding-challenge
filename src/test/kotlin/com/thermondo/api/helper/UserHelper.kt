package com.thermondo.api.helper

import com.thermondo.api.models.User
import java.util.*

fun createUser(
    name: String = "Some Name",
    email: String = "some@email.com",
): User {
    val id = UUID.randomUUID()
    return User(
        id = id,
        name = name,
        email = email,
    )
}