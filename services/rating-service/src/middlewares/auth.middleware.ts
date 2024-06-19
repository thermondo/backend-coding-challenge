import {
  Injectable,
  Logger,
  NestMiddleware,
  UnauthorizedException,
} from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';
import { ConfigService } from '@nestjs/config';
import axios from 'axios';
import { ClsService } from 'nestjs-cls';

@Injectable()
export class AuthMiddleware implements NestMiddleware {
  private readonly authServiceUrl: string;

  constructor(
    private readonly logger: Logger,
    private readonly clsService: ClsService, // Inject ClsService
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
        await this.setAuthTokenInCls(token, user.sub);
        req['user'] = user; // Attach user information to request object
      } catch (error) {
        this.logger.error('Invalid token:', error.message);
        throw new UnauthorizedException();
      }
    }
    next();
  }
  async validateToken(
    token: string,
  ): Promise<{ username: string; sub: string }> {
    try {
      const response = await axios.post(
        `${this.authServiceUrl}/auth/validate-token`,
        {
          token,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );
      const decoded = response.data;
      return decoded;
    } catch (error) {
      this.logger.error(error);
      throw new UnauthorizedException('Invalid token');
    }
  }

  async setAuthTokenInCls(token: string, userId: string) {
    this.clsService.set('authToken', token);
    this.clsService.set('userId', userId); // Store token in ClsService context
  }
}
