plugins {
	java
	id("org.springframework.boot") version "3.5.0"
	id("io.spring.dependency-management") version "1.1.7"
	id("org.openapi.generator") version "7.12.0"
}

group = "com.entertainment"
version = "0.0.1-SNAPSHOT"

java {
	toolchain {
		languageVersion = JavaLanguageVersion.of(21)
	}
}

repositories {
	mavenCentral()
}

openApiGenerate {
	generatorName = "spring"
	inputSpec = "$rootDir/specs/movie-api-spec.yaml"
	outputDir = "${layout.buildDirectory}/generated".toString()
	apiPackage = "com.entertainment.movie.api"
	invokerPackage = "org.openapi.example.invoker"
	modelPackage = "com.entertainment.movie.dto"
}

dependencies {
	implementation("org.springframework.boot:spring-boot-starter-web")
	implementation("org.flywaydb:flyway-core")
	testImplementation("org.springframework.boot:spring-boot-starter-test")
	testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}
tasks.withType<Test> {
	useJUnitPlatform()
}

tasks.named("compileJava") {
	dependsOn(tasks.openApiGenerate)
}
