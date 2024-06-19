import { Logger, Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { join } from 'path';
import { ConfigModule } from '@nestjs/config';
import { AuthController } from './auth/auth.controller';
import { AuthService } from './auth/auth.service';
import { AuthModule } from './auth/auth.module';

@Module({
  imports: [
    ConfigModule.forRoot({
      envFilePath: join(__dirname, '..', '.env'), // Path to your .env file
      isGlobal: true, // Make the configuration module global
    }),
    AuthModule,
  ],
  controllers: [AppController, AuthController],
  providers: [AuthService, Logger],
})
export class AppModule {}
