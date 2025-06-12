package com.thermondo.api.dto

import com.thermondo.api.models.User
import jakarta.validation.constraints.Email
import jakarta.validation.constraints.NotBlank
import jakarta.validation.constraints.Size
import java.util.UUID

data class CreateUserRequest(
    @field:NotBlank(message = "Name is required")
    @field:Size(min = 2, max = 100, message = "Name must be between 2 and 100 characters")
    val name: String,
    
    @field:NotBlank(message = "Email is required")
    @field:Email(message = "Invalid email format")
    val email: String
)

data class UpdateUserRequest(
    @field:Size(min = 2, max = 100, message = "Name must be between 2 and 100 characters")
    val name: String?
)

data class UserResponse(
    val id: UUID,
    val name: String,
    val email: String
) {
    companion object {
        fun fromUser(user: User): UserResponse {
            return UserResponse(
                id = user.id,
                name = user.name,
                email = user.email
            )
        }
    }
}
