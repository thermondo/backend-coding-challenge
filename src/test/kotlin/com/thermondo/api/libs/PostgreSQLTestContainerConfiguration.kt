package com.thermondo.api.libs

import jakarta.annotation.PreDestroy
import org.springframework.boot.test.util.TestPropertyValues
import org.springframework.context.ApplicationContextInitializer
import org.springframework.context.ConfigurableApplicationContext
import org.testcontainers.containers.PostgreSQLContainer
import org.testcontainers.utility.DockerImageName

class PostgreSQLTestContainerConfiguration : ApplicationContextInitializer<ConfigurableApplicationContext> {
    companion object {
        private const val DATABASE_SCHEMA_SUFFIX = "currentSchema=public"
        private const val SPRING_DATASOURCE_PROPERTY_PREFIX = "spring.datasource"
        private const val POSTGRESQL_CONTAINER_IMAGE_NAME = "postgres:latest"
        private const val DATABASE_NAME = "thermondo"

        private val POSTGRESQL_CONTAINER =
            PostgreSQLContainer(DockerImageName.parse(POSTGRESQL_CONTAINER_IMAGE_NAME))
                .apply {
                    withDatabaseName(DATABASE_NAME)
                    withCommand("--max_connections=1000")
                    start()
                }
    }

    override fun initialize(configurableApplicationContext: ConfigurableApplicationContext) {
        TestPropertyValues.of(
            "$SPRING_DATASOURCE_PROPERTY_PREFIX.url=${POSTGRESQL_CONTAINER.jdbcUrl}&$DATABASE_SCHEMA_SUFFIX",
            "$SPRING_DATASOURCE_PROPERTY_PREFIX.username=${POSTGRESQL_CONTAINER.username}",
            "$SPRING_DATASOURCE_PROPERTY_PREFIX.password=${POSTGRESQL_CONTAINER.password}",
        ).applyTo(configurableApplicationContext)
    }
    @PreDestroy
    fun stop() {
        POSTGRESQL_CONTAINER.stop()
    }
}