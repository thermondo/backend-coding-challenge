import {
  Injectable,
  Logger,
  NestMiddleware,
  UnauthorizedException,
} from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';
import { ConfigService } from '@nestjs/config';
import axios from 'axios';

@Injectable()
export class AuthMiddleware implements NestMiddleware {
  private readonly authServiceUrl: string;

  constructor(
    private readonly logger: Logger,
    configService: ConfigService,
  ) {
    this.authServiceUrl = configService.get<string>('AUTH_SERVICE_URL');
  }

  async use(req: Request, res: Response, next: NextFunction) {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) throw new UnauthorizedException();
    if (token) {
      try {
        const user = await this.validateToken(token);
        req['user'] = user; // Attach user information to request object
      } catch (error) {
        this.logger.error('Invalid token:', error.message);
        throw new UnauthorizedException();
      }
    }
    next();
  }
  async validateToken(token: string): Promise<string> {
    try {
      const response = await axios.post(
        `${this.authServiceUrl}/auth/validate-token`,
        {
          token,
        },
      );
      const decoded = response.data;
      return decoded;
    } catch (error) {
      this.logger.error(error);
      throw new UnauthorizedException('Invalid token');
    }
  }
}
