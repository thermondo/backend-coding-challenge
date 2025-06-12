package com.thermondo.api.services

import com.thermondo.api.common.DuplicateResourceException
import com.thermondo.api.common.ResourceNotFoundException
import com.thermondo.api.db.postgres.UserDao
import com.thermondo.api.dto.CreateUserRequest
import com.thermondo.api.dto.UpdateUserRequest
import com.thermondo.api.models.User
import io.mockk.every
import io.mockk.mockk
import io.mockk.verify
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.assertThrows
import org.junit.jupiter.api.Assertions.*
import org.junit.jupiter.api.BeforeEach
import java.time.Instant
import java.util.*

class UserServiceTest {

    private val userDao = mockk<UserDao>()
    private lateinit var userService: UserService

    @BeforeEach
    fun setup() {
        userService = UserService(userDao)
    }

    @Test
    fun `should create user successfully when email is unique`() {
        val request = CreateUserRequest(
            name = "John Doe",
            email = "john.doe@some.domain"
        )
        val expectedUser = User(
            id = UUID.randomUUID(),
            name = request.name,
            email = request.email,
            createdAt = Instant.now(),
            updatedAt = Instant.now()
        )

        every { userDao.existsByEmail(request.email) } returns false
        every { userDao.create(request.name, request.email) } returns expectedUser

        val result = userService.createUser(request)

        assertEquals(expectedUser, result)
        verify { userDao.existsByEmail(request.email) }
        verify { userDao.create(request.name, request.email) }
    }

    @Test
    fun `should throw DuplicateResourceException when email already exists`() {
        val request = CreateUserRequest(
            name = "John Doe",
            email = "john.doe@some.domain"
        )

        every { userDao.existsByEmail(request.email) } returns true

        val exception = assertThrows<DuplicateResourceException> {
            userService.createUser(request)
        }

        assertEquals("User with email ${request.email} already exists", exception.message)
        verify { userDao.existsByEmail(request.email) }
        verify(exactly = 0) { userDao.create(any(), any()) }
    }

    @Test
    fun `should return user when user exists`() {
        val userId = UUID.randomUUID()
        val expectedUser = User(
            id = userId,
            name = "John Doe",
            email = "john.doe@some.domain",
            createdAt = Instant.now(),
            updatedAt = Instant.now()
        )

        every { userDao.findById(userId) } returns expectedUser

        val result = userService.getUserById(userId)

        assertEquals(expectedUser, result)
        verify { userDao.findById(userId) }
    }

    @Test
    fun `should throw ResourceNotFoundException when user does not exist`() {
        val userId = UUID.randomUUID()

        every { userDao.findById(userId) } returns null

        val exception = assertThrows<ResourceNotFoundException> {
            userService.getUserById(userId)
        }

        assertEquals("User with id $userId not found", exception.message)
        verify { userDao.findById(userId) }
    }

    @Test
    fun `should return list of users`() {
        val users = listOf(
            User(
                id = UUID.randomUUID(),
                name = "John Doe",
                email = "john.doe@some.domain",
                createdAt = Instant.now(),
                updatedAt = Instant.now()
            ),
            User(
                id = UUID.randomUUID(),
                name = "Jane Smith",
                email = "jane.smith@some.domain",
                createdAt = Instant.now(),
                updatedAt = Instant.now()
            )
        )

        every { userDao.findAll() } returns users

        val result = userService.getAllUsers()

        assertEquals(users, result)
    }

    @Test
    fun `should update user successfully`() {
        val userId = UUID.randomUUID()
        val request = UpdateUserRequest(name = "Updated Name")
        val expectedUser = User(
            id = userId,
            name = "Updated Name",
            email = "john.doe@some.domain",
            createdAt = Instant.now(),
            updatedAt = Instant.now()
        )

        every { userDao.update(userId, request.name) } returns expectedUser

        val result = userService.updateUser(userId, request)

        assertEquals(expectedUser, result)
        verify { userDao.update(userId, request.name) }
    }

    @Test
    fun `should return true when user is deleted successfully`() {
        val userId = UUID.randomUUID()

        every { userDao.delete(userId) } returns true

        val result = userService.deleteUser(userId)

        assertTrue(result)
        verify { userDao.delete(userId) }
    }

    @Test
    fun `should throw ResourceNotFoundException when deleting user that does not exist`() {
        val userId = UUID.randomUUID()

        every { userDao.delete(userId) } returns false

        val exception = assertThrows<ResourceNotFoundException> {
            userService.deleteUser(userId)
        }

        assertEquals("User with id $userId not found", exception.message)
        verify { userDao.delete(userId) }
    }
}
