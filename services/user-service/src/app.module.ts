import { Logger, MiddlewareConsumer, Module } from '@nestjs/common';
import { UserModule } from './user/user.module';
import { AppController } from './app.controller';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { join } from 'path';
import { ClsMiddleware, ClsModule } from 'nestjs-cls';
import { AuthMiddleware } from './middlewares/auth.middleware';
import { MongooseModule } from '@nestjs/mongoose';

@Module({
  imports: [
    ClsModule.forRoot({
      global: true,
    }),
    ConfigModule.forRoot({
      envFilePath: join(__dirname, '..', '.env'), // Path to your .env file
      isGlobal: true, // Make the configuration module global
    }),
    MongooseModule.forRootAsync({
      imports: [ConfigModule],
      useFactory: async (configService: ConfigService) => ({
        uri: configService.get<string>('DB_URL'), // Get DB_URL from environment variables
      }),
      inject: [ConfigService], // Inject ConfigService
    }),
    UserModule,
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
