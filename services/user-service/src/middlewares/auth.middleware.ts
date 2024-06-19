import {
  Injectable,
  Logger,
  NestMiddleware,
  UnauthorizedException,
} from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';
import { ClsService } from 'nestjs-cls';

@Injectable()
export class AuthMiddleware implements NestMiddleware {
  constructor(
    private readonly logger: Logger,
    private readonly clsService: ClsService, // Inject ClsService
  ) {}

  async use(req: Request, res: Response, next: NextFunction) {
    const token = req.headers.authorization?.split(' ')[1];
    // if (!token) throw new UnauthorizedException();
    if (token) {
      try {
        await this.setAuthTokenInCls(token);
      } catch (error) {
        this.logger.error('Invalid token:', error.message);
        throw new UnauthorizedException();
      }
    }
    next();
  }

  async setAuthTokenInCls(token: string) {
    this.clsService.set('authToken', token); // Store token in ClsService context
  }
}
