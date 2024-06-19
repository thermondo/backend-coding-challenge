/* eslint-disable @typescript-eslint/no-unused-vars */
import { Test, TestingModule } from '@nestjs/testing';
import { AuthService } from './auth.service';
import { JwtService } from '@nestjs/jwt';
import { ConfigService } from '@nestjs/config';
import { Logger, UnauthorizedException } from '@nestjs/common';
import { LoginDto } from '../dto/login.dto';

describe('AuthService', () => {
  let service: AuthService;
  let jwtService: JwtService;
  let configService: ConfigService;
  let logger: Logger;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [AuthService, JwtService, ConfigService, Logger],
    }).compile();

    service = module.get<AuthService>(AuthService);
    jwtService = module.get<JwtService>(JwtService);
    configService = module.get<ConfigService>(ConfigService);
    logger = module.get<Logger>(Logger);
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  describe('generateToken', () => {
    it('should generate a token for a valid login', async () => {
      const loginDto: LoginDto = {
        username: 'testuser',
        password: 'testpassword',
      };
      const token = { access_token: 'generated_token' };

      jest.spyOn(service, 'generateToken').mockResolvedValue(token);

      const result = await service.generateToken(loginDto);

      expect(result).toBe(token);
      expect(service.generateToken).toHaveBeenCalledWith(loginDto);
    });
  });

  describe('validateToken', () => {
    it('should return the decoded token for a valid token', () => {
      const token = 'valid_token';
      const decodedToken = { userId: 'userId', username: 'username' };

      jest.spyOn(jwtService, 'verify').mockReturnValue(decodedToken);

      const result = service.validateToken(token);

      expect(result).toBe(decodedToken);
      expect(jwtService.verify).toHaveBeenCalledWith(token);
    });

    it('should throw an UnauthorizedException for an invalid token', () => {
      const token = 'invalid_token';

      jest.spyOn(jwtService, 'verify').mockImplementation(() => {
        throw new UnauthorizedException();
      });

      expect(() => {
        service.validateToken(token);
      }).toThrow(UnauthorizedException);
      expect(jwtService.verify).toHaveBeenCalledWith(token);
    });
  });
});
