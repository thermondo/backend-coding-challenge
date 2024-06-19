import { Logger, MiddlewareConsumer, Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { RatingModule } from './ratings/rating.module';
import { MongooseModule } from '@nestjs/mongoose';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { join } from 'path';
import { ClsMiddleware, ClsModule } from 'nestjs-cls';
import { AuthMiddleware } from './middlewares/auth.middleware';

@Module({
  imports: [
    ConfigModule.forRoot({
      envFilePath: join(__dirname, '..', '.env'), // Path to your .env file
      isGlobal: true, // Make the configuration module global
    }),
    RatingModule,
    ClsModule.forRoot({
      global: true,
    }),
    MongooseModule.forRootAsync({
      imports: [ConfigModule],
      useFactory: async (configService: ConfigService) => ({
        uri: configService.get<string>('DB_URL'),
      }),
      inject: [ConfigService],
    }),
  ],
  controllers: [AppController],
  providers: [Logger],
})
export class AppModule {
  configure(consumer: MiddlewareConsumer) {
    consumer.apply(ClsMiddleware).forRoutes('*');
    consumer.apply(AuthMiddleware).forRoutes('*');
  }
}
