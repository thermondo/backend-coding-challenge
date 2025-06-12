import nu.studer.gradle.jooq.JooqGenerate
import org.jetbrains.kotlin.gradle.tasks.KotlinCompile
import org.testcontainers.containers.PostgreSQLContainer
import org.testcontainers.utility.DockerImageName


plugins {
	id("org.springframework.boot") version "3.2.5"
	id("io.spring.dependency-management") version "1.1.5"
	id("nu.studer.jooq") version "9.0"
	id("org.flywaydb.flyway") version "10.12.0"
	id("org.jlleitschuh.gradle.ktlint") version "12.3.0"
	kotlin("jvm") version "1.9.10"
	kotlin("plugin.spring") version "1.9.24"
	kotlin("plugin.serialization") version "1.9.23"
}

group = "com.thermondo"
version = "0.0.1-SNAPSHOT"

val jooqGeneratedSourcesPackage = "com.thermondo.api.db.postgres"

java {
	sourceCompatibility = JavaVersion.VERSION_21
}

repositories {
	mavenCentral()
}

dependencies {
	implementation("org.springframework.boot:spring-boot-starter-actuator")
	implementation("org.springframework.boot:spring-boot-starter-web")
	implementation("org.springframework.boot:spring-boot-starter-jooq")
	implementation("org.springframework.boot:spring-boot-starter-security")
	implementation("org.springframework.security:spring-security-web")
	implementation("org.springframework.security:spring-security-config")
	implementation("org.springframework:spring-webmvc")

	implementation("commons-codec:commons-codec:1.17.1")
	implementation("org.springdoc:springdoc-openapi-starter-webmvc-ui:2.6.0")


	jooqGenerator("org.postgresql:postgresql:42.7.3")
	runtimeOnly("org.postgresql:postgresql:42.7.3")
	implementation("org.flywaydb:flyway-database-postgresql:10.12.0")
	implementation("org.flywaydb:flyway-core:10.12.0")
	testImplementation("io.mockk:mockk:1.13.10")
	implementation("net.logstash.logback:logstash-logback-encoder:7.4")

	testImplementation("org.springframework.boot:spring-boot-starter-test")
	testImplementation("org.testcontainers:postgresql:1.19.7")
	testImplementation("org.testcontainers:testcontainers:1.19.7")
	testImplementation("org.testcontainers:junit-jupiter:1.19.7")
	implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
	testImplementation("org.testcontainers:jdbc:1.19.8")
	testImplementation("org.testcontainers:testcontainers-bom:1.19.7")
	developmentOnly("org.springframework.boot:spring-boot-devtools")
	implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.3")
}

buildscript {
	dependencies {
		classpath("org.testcontainers:postgresql:1.19.7")
		classpath("org.postgresql:postgresql:42.7.3")
		classpath("org.flywaydb:flyway-database-postgresql:10.12.0")
	}
}


tasks.withType<KotlinCompile> {
	kotlinOptions {
		freeCompilerArgs += "-Xjsr305=strict"
		jvmTarget = "21"
	}
}

tasks.withType<Test> {
	useJUnitPlatform()
}

val postgreSQLDriver: String = "org.postgresql.Driver"
val postgresDockerImageName: DockerImageName = DockerImageName.parse("postgres:latest")
val postgreSQLContainer =
	PostgreSQLContainer<Nothing>(postgresDockerImageName).apply {
		withDatabaseName("thermondo_db")
		withUsername("user")
		withPassword("password")
		start()
	}

flyway {
	url = postgreSQLContainer.jdbcUrl
	driver = postgreSQLDriver
	user = postgreSQLContainer.username
	password = postgreSQLContainer.password
	baselineOnMigrate = true
	locations = arrayOf("filesystem:src/main/resources/db/migration")
}


jooq {
	version.set("3.17.12")
	edition.set(nu.studer.gradle.jooq.JooqEdition.OSS)

	configurations {
		create("main") {
			generateSchemaSourceOnCompilation.set(true)
			jooqConfiguration.apply {
				logging = org.jooq.meta.jaxb.Logging.ERROR

				jdbc.apply {
					driver = postgreSQLDriver
					url = postgreSQLContainer.jdbcUrl + "/" + postgreSQLContainer.databaseName
					user = postgreSQLContainer.username
					password = postgreSQLContainer.password
					properties.add(
						org.jooq.meta.jaxb.Property().apply {
							key = "ssl"
							value = "false"
						},
					)
				}
				generator.apply {
					name = "org.jooq.codegen.KotlinGenerator"
					database.apply {
						name = "org.jooq.meta.postgres.PostgresDatabase"
						inputSchema = "public"

						forcedTypes.add(
							org.jooq.meta.jaxb.ForcedType().apply {
								name = "INSTANT"
								types = "TIMESTAMPTZ"
							},
						)
					}

					generate.apply {
						isDeprecated = false
						isRecords = true
						isPojos = false
						isImmutablePojos = false
						isPojosAsKotlinDataClasses = false
						isFluentSetters = true
						isJavaTimeTypes = true
						isKotlinNotNullRecordAttributes = true
					}

					target.apply {
						packageName = jooqGeneratedSourcesPackage
					}
				}
			}
		}
	}
}

tasks.withType<JooqGenerate> {
	dependsOn(tasks.flywayMigrate)
	allInputsDeclared.set(true)

	doLast{
		if (postgreSQLContainer.isRunning) {
			postgreSQLContainer.stop()
		}
	}
}
