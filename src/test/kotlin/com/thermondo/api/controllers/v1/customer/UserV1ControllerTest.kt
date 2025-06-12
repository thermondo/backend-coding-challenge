package com.thermondo.api.controllers.v1.customer

import com.fasterxml.jackson.databind.ObjectMapper
import com.thermondo.api.dto.CreateUserRequest
import com.thermondo.api.dto.UpdateUserRequest
import com.thermondo.api.models.User
import com.thermondo.api.services.UserService
import io.mockk.every
import io.mockk.mockk
import io.mockk.verify
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest
import org.springframework.boot.test.context.TestConfiguration
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Primary
import org.springframework.http.MediaType
import org.springframework.test.context.ActiveProfiles
import org.springframework.test.web.servlet.MockMvc
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*
import org.springframework.test.web.servlet.result.MockMvcResultMatchers.*
import java.time.Instant
import java.util.*

@WebMvcTest(controllers = [UserV1Controller::class], excludeAutoConfiguration = [org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration::class])
@ActiveProfiles("test")
class UserV1ControllerTest {

    @Autowired
    private lateinit var mockMvc: MockMvc

    @Autowired
    private lateinit var objectMapper: ObjectMapper

    @TestConfiguration
    class TestConfig {
        @Bean
        @Primary
        fun userService(): UserService = mockk()
    }

    @Autowired
    private lateinit var userService: UserService

    @Test
    fun `should return user when it exists`() {
        val userId = UUID.randomUUID()
        val user = User(
            id = userId,
            name = "John Doe",
            email = "john.doe@some.domain",
            createdAt = Instant.now(),
            updatedAt = Instant.now()
        )

        every { userService.getUserById(userId) } returns user

        mockMvc.perform(get("/api/v1/users/{id}", userId))
            .andExpect(status().isOk)
            .andExpect(content().contentType(MediaType.APPLICATION_JSON))
            .andExpect(jsonPath("$.id").value(userId.toString()))
            .andExpect(jsonPath("$.name").value("John Doe"))
            .andExpect(jsonPath("$.email").value("john.doe@some.domain"))
    }

    @Test
    fun `should create user successfully`() {
        val userRequest = CreateUserRequest(
            name = "Jane Smith",
            email = "jane.smith@some.domain"
        )

        val createdUser = User(
            id = UUID.randomUUID(),
            name = "Jane Smith",
            email = "jane.smith@some.domain",
            createdAt = Instant.now(),
            updatedAt = Instant.now()
        )

        every { userService.createUser(userRequest) } returns createdUser

        mockMvc.perform(
            post("/api/v1/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(userRequest))
        )
            .andExpect(status().isCreated)
            .andExpect(content().contentType(MediaType.APPLICATION_JSON))
            .andExpect(jsonPath("$.name").value("Jane Smith"))
            .andExpect(jsonPath("$.email").value("jane.smith@some.domain"))
    }

    @Test
    fun `should return users list`() {
        val users = listOf(
            User(
                id = UUID.randomUUID(),
                name = "User 1",
                email = "user1@some.domain",
                createdAt = Instant.now(),
                updatedAt = Instant.now()
            ),
            User(
                id = UUID.randomUUID(),
                name = "User 2",
                email = "user2@some.domain",
                createdAt = Instant.now(),
                updatedAt = Instant.now()
            )
        )

        every { userService.getAllUsers() } returns users

        mockMvc.perform(get("/api/v1/users"))
            .andExpect(status().isOk)
            .andExpect(content().contentType(MediaType.APPLICATION_JSON))
            .andExpect(jsonPath("$").isArray)
            .andExpect(jsonPath("$.length()").value(2))
            .andExpect(jsonPath("$[0].name").value("User 1"))
            .andExpect(jsonPath("$[0].email").value("user1@some.domain"))
            .andExpect(jsonPath("$[1].name").value("User 2"))
            .andExpect(jsonPath("$[1].email").value("user2@some.domain"))
    }

    @Test
    fun `should update user successfully`() {
        val userId = UUID.randomUUID()
        val updateRequest = UpdateUserRequest(name = "Updated Name")
        val updatedUser = User(
            id = userId,
            name = "Updated Name",
            email = "john.doe@some.domain",
            createdAt = Instant.now(),
            updatedAt = Instant.now()
        )

        every { userService.updateUser(userId, updateRequest) } returns updatedUser

        mockMvc.perform(
            put("/api/v1/users/{id}", userId)
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(updateRequest))
        )
            .andExpect(status().isOk)
            .andExpect(content().contentType(MediaType.APPLICATION_JSON))
            .andExpect(jsonPath("$.id").value(userId.toString()))
            .andExpect(jsonPath("$.name").value("Updated Name"))
            .andExpect(jsonPath("$.email").value("john.doe@some.domain"))
    }

    @Test
    fun `should delete user successfully`() {
        val userId = UUID.randomUUID()

        every { userService.deleteUser(userId) } returns true

        mockMvc.perform(delete("/api/v1/users/{id}", userId))
            .andExpect(status().isOk)
            .andExpect(content().contentType(MediaType.APPLICATION_JSON))
            .andExpect(jsonPath("$.message").value("User deleted successfully"))

        verify { userService.deleteUser(userId) }
    }
}
