package com.thermondo.api.services

import com.thermondo.api.common.DuplicateResourceException
import com.thermondo.api.common.ResourceNotFoundException
import com.thermondo.api.db.postgres.UserDao
import com.thermondo.api.dto.*
import com.thermondo.api.models.User
import org.slf4j.LoggerFactory
import org.springframework.stereotype.Service
import java.util.*

@Service
class UserService(
    private val userDao: UserDao,
) {
    private val logger = LoggerFactory.getLogger(UserService::class.java)

    fun createUser(request: CreateUserRequest): User {
        logger.info("Creating user with email: ${request.email}")
        
        if (userDao.existsByEmail(request.email)) {
            throw DuplicateResourceException("User with email ${request.email} already exists")
        }
        
        val user = userDao.create(request.name, request.email)
        logger.info("Successfully created user with id: ${user.id}")
        
        return user
    }

    fun getUserById(id: UUID): User {
        logger.debug("Fetching user with id: $id")
        
        return userDao.findById(id)
            ?: throw ResourceNotFoundException("User with id $id not found")

    }

    fun getAllUsers(): List<User> {
        logger.debug("Fetching all users")
        
        return userDao.findAll()
    }

    fun updateUser(id: UUID, request: UpdateUserRequest): User {
        logger.info("Updating user with id: $id")
        
        val user = userDao.update(id, request.name)
        logger.info("Successfully updated user with id: ${user.id}")
        
        return user
    }

    fun deleteUser(id: UUID): Boolean {
        logger.info("Deleting user with id: $id")
        
        if (!userDao.delete(id)) {
            throw ResourceNotFoundException("User with id $id not found")
        }
        
        logger.info("Successfully deleted user with id: $id")
        return true
    }
}
