package com.thermondo.api.db.postgres

import com.thermondo.api.IntegrationTest
import com.thermondo.api.common.ResourceNotFoundException
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.assertThrows
import org.junit.jupiter.api.Assertions.*
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.test.annotation.Rollback
import java.time.Instant
import java.util.*

@IntegrationTest
class UserDaoTest {
    @Autowired
    private lateinit var userDao: UserDao

    @Test
    @Rollback
    fun `should create user successfully`() {
        val name = "John Doe"
        val email = "john.doe@some.domain"

        val createdUser = userDao.create(name, email)

        assertNotNull(createdUser.id)
        assertEquals(name, createdUser.name)
        assertEquals(email, createdUser.email)
        assertNotNull(createdUser.createdAt)
        assertNotNull(createdUser.updatedAt)
        assertTrue(createdUser.createdAt.isBefore(Instant.now().plusSeconds(1)))
        assertTrue(createdUser.updatedAt.isBefore(Instant.now().plusSeconds(1)))
    }

    @Test
    @Rollback
    fun `should find user by id when exists`() {
        val user = userDao.create("Jane Smith", "jane.smith@some.domain")

        val foundUser = userDao.findById(user.id)

        assertNotNull(foundUser)
        assertEquals(user.id, foundUser!!.id)
        assertEquals(user.name, foundUser.name)
        assertEquals(user.email, foundUser.email)
        assertEquals(user.createdAt, foundUser.createdAt)
        assertEquals(user.updatedAt, foundUser.updatedAt)
    }

    @Test
    @Rollback
    fun `should return null when user does not exist`() {
        val nonExistentId = UUID.randomUUID()

        val foundUser = userDao.findById(nonExistentId)

        assertNull(foundUser)
    }

    @Test
    @Rollback
    fun `should find all users`() {
        val user1 = userDao.create("User One", "user1@some.domain")
        val user2 = userDao.create("User Two", "user2@some.domain")
        val user3 = userDao.create("User Three", "user3@some.domain")

        val users = userDao.findAll()

        assertTrue(users.size >= 3)
        assertTrue(users.any { it.id == user1.id })
        assertTrue(users.any { it.id == user2.id })
        assertTrue(users.any { it.id == user3.id })
    }

    @Test
    @Rollback
    fun `should update user name successfully`() {
        val originalUser = userDao.create("Original Name", "original@some.domain")
        val newName = "Updated Name"

        val updatedUser = userDao.update(originalUser.id, newName)

        assertEquals(originalUser.id, updatedUser.id)
        assertEquals(newName, updatedUser.name)
        assertEquals(originalUser.email, updatedUser.email)
        assertEquals(originalUser.createdAt, updatedUser.createdAt)
        assertTrue(updatedUser.updatedAt > originalUser.updatedAt)
    }

    @Test
    @Rollback
    fun `should throw exception when user does not exist`() {
        val nonExistentId = UUID.randomUUID()

        assertThrows<ResourceNotFoundException> {
            userDao.update(nonExistentId, "Some user")
        }
    }

    @Test
    @Rollback
    fun `should delete user successfully`() {
        val user = userDao.create("User To Delete", "delete@some.domain")

        val deleteResult = userDao.delete(user.id)

        assertTrue(deleteResult)
        assertNull(userDao.findById(user.id))
    }

    @Test
    @Rollback
    fun `should return false when deleting user that does not exist`() {
        val nonExistentId = UUID.randomUUID()

        val deleteResult = userDao.delete(nonExistentId)

        assertFalse(deleteResult)
    }

    @Test
    @Rollback
    fun `should return true when user exists by email`() {
        val email = "existing@some.domain"
        userDao.create("Existing User", email)

        val exists = userDao.existsByEmail(email)

        assertTrue(exists)
    }

    @Test
    @Rollback
    fun `should return false when user does not exist by email`() {
        val nonExistentEmail = "nonexistent@some.domain"

        val exists = userDao.existsByEmail(nonExistentEmail)

        assertFalse(exists)
    }
}