import { Test, TestingModule } from '@nestjs/testing';
import { AuthController } from './auth.controller';
import { AuthService } from './auth.service';
import { Logger } from '@nestjs/common';
import { LoginDto } from '../dto/login.dto';
import { ValidateTokenDto } from '../dto/validate-token.dto';
import { JwtService } from '@nestjs/jwt';
import { createMock } from '@golevelup/ts-jest';
import { ConfigService } from '@nestjs/config';

describe('AuthController', () => {
  let controller: AuthController;
  let authService: AuthService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [AuthController],
      providers: [
        { provide: AuthService, useValue: createMock<AuthService>() },
        Logger,
        {
          provide: JwtService,
          useValue: createMock<JwtService>(),
        },
        {
          provide: ConfigService,
          useValue: createMock<ConfigService>(),
        },
      ],
    }).compile();

    controller = module.get<AuthController>(AuthController);
    authService = module.get<AuthService>(AuthService);
  });

  describe('generateToken', () => {
    it('should call authService.generateToken with the provided loginDto', async () => {
      const loginDto: LoginDto = {
        username: 'testuser',
        password: 'testpassword',
      };
      const generateTokenSpy = jest.spyOn(authService, 'generateToken');

      await controller.generateToken(loginDto);

      expect(generateTokenSpy).toHaveBeenCalledWith(loginDto);
    });
  });

  describe('validateToken', () => {
    it('should call authService.validateToken with the provided validateTokenDto', async () => {
      const validateTokenDto: ValidateTokenDto = {
        token: 'testtoken',
        accessLevel: 'testaccesslevel',
      };
      const validateTokenSpy = jest.spyOn(authService, 'validateToken');

      await controller.validateToken(validateTokenDto);

      expect(validateTokenSpy).toHaveBeenCalledWith(validateTokenDto.token);
    });
  });
});
