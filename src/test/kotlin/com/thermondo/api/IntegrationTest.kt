package com.thermondo.api

import com.thermondo.api.libs.PostgreSQLTestContainerConfiguration
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.test.context.ActiveProfiles
import org.springframework.test.context.ContextConfiguration
import org.springframework.transaction.annotation.Transactional

const val TEST_PROFILE = "test"

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Transactional
@ActiveProfiles(TEST_PROFILE)
@ContextConfiguration(initializers = [
    PostgreSQLTestContainerConfiguration::class
])
annotation class IntegrationTest