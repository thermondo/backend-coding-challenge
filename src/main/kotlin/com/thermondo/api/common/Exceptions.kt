package com.thermondo.api.common

class ResourceNotFoundException(message: String): Exception(message)
class DuplicateResourceException(message: String): Exception(message)
class ValidationException(message: String): Exception(message)