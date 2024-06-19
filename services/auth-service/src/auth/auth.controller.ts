import { Controller, Post, Body, Logger } from '@nestjs/common';
import { AuthService } from './auth.service';
import { LoginDto } from '../dto/login.dto';
import { ValidateTokenDto } from '../dto/validate-token.dto';
import { ApiTags } from '@nestjs/swagger';

@ApiTags('auth')
@Controller('auth')
export class AuthController {
  constructor(
    private readonly authService: AuthService,
    private readonly logger: Logger,
  ) {}

  @Post('generate-token')
  async generateToken(@Body() loginDto: LoginDto) {
    this.logger.debug(
      `[${AuthController.name} - generateToken] called: ${loginDto.username}`,
    );
    try {
      const result = this.authService.generateToken(loginDto);
      this.logger.log(
        `[${AuthController.name} - generateToken] succeeded for user : ${loginDto.username}`,
      );
      return result;
    } catch (error) {
      this.logger.error(
        `[${AuthController.name} - generateToken] throw an error for : ${loginDto.username}`,
        error,
      );
      throw error;
    }
  }
  @Post('validate-token')
  async validateToken(@Body() validateTokenDto: ValidateTokenDto) {
    this.logger.debug(
      `[${AuthController.name} - validateToken] called: ${validateTokenDto.token}`,
    );
    try {
      const result = await this.authService.validateToken(
        validateTokenDto.token,
      );
      this.logger.log(
        `[${AuthController.name} - validateToken] succeeded: ${validateTokenDto.token}`,
      );
      return result;
    } catch (error) {
      this.logger.error(
        `[${AuthController.name} - validateToken] throw an error for token : ${validateTokenDto}`,
        error,
      );
      throw error;
    }
  }
}
