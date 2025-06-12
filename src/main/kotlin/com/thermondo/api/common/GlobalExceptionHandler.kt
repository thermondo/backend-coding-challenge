package com.thermondo.api.common

import org.slf4j.Logger
import org.slf4j.LoggerFactory
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.MethodArgumentNotValidException
import org.springframework.web.bind.annotation.ControllerAdvice
import org.springframework.web.bind.annotation.ExceptionHandler

@ControllerAdvice
class GlobalExceptionHandler {
    val log: Logger = LoggerFactory.getLogger(GlobalExceptionHandler::class.java)

    @ExceptionHandler(ResourceNotFoundException::class)
    fun handleResourceNotFound(ex: ResourceNotFoundException): ResponseEntity<ErrorResponse> {
        log.warn("Resource not found: ${ex.message}")
        return ResponseEntity(
            ErrorResponse("RESOURCE_NOT_FOUND", ex.message ?: "Resource not found"),
            HttpStatus.NOT_FOUND
        )
    }

    @ExceptionHandler(DuplicateResourceException::class)
    fun handleDuplicateResource(ex: DuplicateResourceException): ResponseEntity<ErrorResponse> {
        log.warn("Duplicate resource: ${ex.message}")
        return ResponseEntity(
            ErrorResponse("DUPLICATE_RESOURCE", ex.message ?: "Resource already exists"),
            HttpStatus.CONFLICT
        )
    }

    @ExceptionHandler(ValidationException::class)
    fun handleValidation(ex: ValidationException): ResponseEntity<ErrorResponse> {
        log.warn("Validation error: ${ex.message}")
        return ResponseEntity(
            ErrorResponse("VALIDATION_ERROR", ex.message ?: "Validation failed"),
            HttpStatus.BAD_REQUEST
        )
    }

    @ExceptionHandler(MethodArgumentNotValidException::class)
    fun handleMethodArgumentNotValid(ex: MethodArgumentNotValidException): ResponseEntity<ErrorResponse> {
        val errors = ex.bindingResult.fieldErrors.map { "${it.field}: ${it.defaultMessage}" }
        val message = "Validation failed: ${errors.joinToString(", ")}"
        log.warn("Method argument validation error: $message")
        return ResponseEntity(
            ErrorResponse("VALIDATION_ERROR", message),
            HttpStatus.BAD_REQUEST
        )
    }

    @ExceptionHandler(Exception::class)
    fun handleGeneral(ex: Exception): ResponseEntity<ErrorResponse> {
        log.error("Unexpected error: ${ex.message}", ex)
        return ResponseEntity(
            ErrorResponse("INTERNAL_ERROR", "An unexpected error occurred"),
            HttpStatus.INTERNAL_SERVER_ERROR
        )
    }
}

data class ErrorResponse(
    val code: String,
    val message: String
)