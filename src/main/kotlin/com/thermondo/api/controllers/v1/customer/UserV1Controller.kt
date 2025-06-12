package com.thermondo.api.controllers.v1.customer

import com.thermondo.api.dto.*
import com.thermondo.api.dto.UserResponse.Companion.fromUser
import com.thermondo.api.services.UserService
import io.swagger.v3.oas.annotations.Operation
import io.swagger.v3.oas.annotations.tags.Tag
import jakarta.validation.Valid
import org.slf4j.LoggerFactory
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*
import java.util.*

@RestController
@RequestMapping("/api/v1/users")
@Tag(name = "Users", description = "User management endpoints")
class UserV1Controller (
    private val userService: UserService,
) {

    private val logger = LoggerFactory.getLogger(UserV1Controller::class.java)

    @PostMapping
    @Operation(summary = "Create a new user")
    fun createUser(@Valid @RequestBody request: CreateUserRequest): ResponseEntity<UserResponse> {
        logger.info("Creating user with email: ${request.email}")
        val response = fromUser(userService.createUser(request))
        return ResponseEntity.status(HttpStatus.CREATED).body(response)
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get user by ID")
    fun getUserById(@PathVariable id: UUID): ResponseEntity<UserResponse> {
        logger.debug("Fetching user with id: $id")
        val response = fromUser(userService.getUserById(id))
        return ResponseEntity.ok(response)
    }

    @GetMapping
    @Operation(summary = "Get all users")
    fun getAllUsers(
    ): ResponseEntity<List<UserResponse>> {
        logger.debug("Fetching all users")
        val response = userService.getAllUsers().map { user ->
            fromUser(user)
        }
        return ResponseEntity.ok(response)
    }

    @PutMapping("/{id}")
    @Operation(summary = "Update user")
    fun updateUser(
        @PathVariable id: UUID,
        @Valid @RequestBody request: UpdateUserRequest
    ): ResponseEntity<UserResponse> {
        logger.info("Updating user with id: $id")
        val response = fromUser(userService.updateUser(id, request))
        return ResponseEntity.ok(response)
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete user")
    fun deleteUser(@PathVariable id: UUID): ResponseEntity<Map<String, String>> {
        logger.info("Deleting user with id: $id")
        userService.deleteUser(id)
        return ResponseEntity.ok(mapOf("message" to "User deleted successfully"))
    }
}