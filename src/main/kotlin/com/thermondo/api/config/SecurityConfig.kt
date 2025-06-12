package com.thermondo.api.config

import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.security.config.annotation.web.builders.HttpSecurity
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity
import org.springframework.security.web.SecurityFilterChain

@Configuration
@EnableWebSecurity
class SecurityConfig {

    @Bean
    fun filterChain(http: HttpSecurity): SecurityFilterChain {
        // TODO configure propper auth
        http
            .csrf { it.disable() }
            .authorizeHttpRequests { authz ->
                authz
                    .anyRequest().permitAll()
            }
        
        return http.build()
    }
}
