// auth.service.ts

import { Injectable, Logger, UnauthorizedException } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { JwtService } from '@nestjs/jwt';
import axios from 'axios';
import { LoginDto } from '../dto/login.dto';

@Injectable()
export class AuthService {
  userServiceUrl: string;
  constructor(
    private jwtService: JwtService,
    configService: ConfigService,
    private readonly logger: Logger,
  ) {
    this.userServiceUrl = configService.get<string>('USER_SERVICE_URL');
  }

  async generateToken(loginDto: LoginDto) {
    this.logger.debug(
      `[${AuthService.name} - generateToken] called for user : ${loginDto.username}`,
    );
    const { username, password } = loginDto;
    try {
      const { data } = await axios.post(
        `${this.userServiceUrl}/users/validate-credentials`,
        {
          username,
          password,
        },
      );

      if (!data) {
        this.logger.error(
          `[${AuthService.name} - generateToken] Invalid credentials for user: ${loginDto.username}`,
        );
        throw new UnauthorizedException('Invalid credentials');
      }

      // Generate JWT token
      const payload = { username: data.username, sub: data._id };
      return {
        access_token: this.jwtService.sign(payload),
      };
    } catch (error) {
      this.logger.error(
        `[${AuthService.name} - generateToken] throw an error during calling for credentials validation for user : ${loginDto.username}`,
      );
      throw new UnauthorizedException('Invalid credentials');
    }
  }
  validateToken(token: string): string {
    try {
      this.logger.debug(
        `[${AuthService.name} - validateToken] called for token : ${token}`,
      );
      const decoded = this.jwtService.verify(token);
      return decoded;
    } catch (error) {
      this.logger.error(
        `[${AuthService.name} - validateToken] throw an error during verifying the token : ${token}`,
      );
      throw new UnauthorizedException('Invalid token');
    }
  }
}
