import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication } from '@nestjs/common';
import * as request from 'supertest';
import { AppModule } from '../src/app.module';

describe('AuthController (e2e)', () => {
  let app: INestApplication;

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  xdescribe('/auth/generate-token (POST)', () => {
    it('should return a JWT token when valid credentials are provided', () => {
      return request(app.getHttpServer())
        .post('/auth/generate-token')
        .send({ username: 'testuser', password: 'testpassword' })
        .expect(201)
        .expect((res) => {
          expect(res.body).toHaveProperty('token');
        });
    });

    it('should return a 401 Unauthorized when invalid credentials are provided', () => {
      return request(app.getHttpServer())
        .post('/auth/generate-token')
        .send({ username: 'testuser', password: 'wrongpassword' })
        .expect(401);
    });
  });
});
