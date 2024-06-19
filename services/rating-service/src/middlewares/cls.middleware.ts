import { Injectable, NestMiddleware } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';
import { AsyncLocalStorage } from 'async_hooks';
import { ClsService } from 'nestjs-cls';

@Injectable()
export class ClsMiddleware implements NestMiddleware {
  constructor(private readonly asyncLocalStorage: AsyncLocalStorage<any>) {} // Inject AsyncLocalStorage

  use(req: Request, res: Response, next: NextFunction) {
    this.asyncLocalStorage.run(new Map(), () => {
      next();
    });
  }
}

export const ClsServiceFactory = {
  provide: ClsService,
  useFactory: (asyncLocalStorage: AsyncLocalStorage<any>) => {
    return new ClsService(asyncLocalStorage);
  },
  inject: [AsyncLocalStorage],
};

export default ClsMiddleware;
