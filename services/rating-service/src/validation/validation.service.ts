import { Injectable, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import axios, { AxiosResponse } from 'axios';
import { ClsService } from 'nestjs-cls';

@Injectable()
export class ValidationService {
  private readonly userServiceUrl: string;
  private readonly movieServiceUrl: string;

  constructor(
    configService: ConfigService,
    private readonly clsService: ClsService,
    private readonly logger: Logger,
  ) {
    this.userServiceUrl = configService.get<string>('USER_SERVICE_URL');
    this.movieServiceUrl = configService.get<string>('MOVIE_SERVICE_URL');
  }

  async checkUserExists(userId: string): Promise<boolean> {
    try {
      const authToken = this.clsService.get('authToken'); // Retrieve token from CLS context

      this.logger.log(`Checking user existence with token: ${authToken}`);

      const response: AxiosResponse = await axios.get(
        `${this.userServiceUrl}/users/${userId}/exists`,
        {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        },
      );
      return response.status === 200; // Returns true if user exists (status 200)
    } catch (error) {
      return false;
    }
  }

  async checkMovieExists(movieId: string): Promise<boolean> {
    try {
      const authToken = this.clsService.get('authToken'); // Retrieve token from CLS context
      const response: AxiosResponse = await axios.get(
        `${this.movieServiceUrl}/movies/${movieId}/exists`,
        {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        },
      );
      return response.status === 200; // Returns true if movie exists (status 200)
    } catch (error) {
      this.logger.error('Error checking movie existence:', error);
      return false;
    }
  }
}
