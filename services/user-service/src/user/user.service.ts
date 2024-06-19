import {
  BadRequestException,
  Injectable,
  Logger,
  NotFoundException,
} from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { User } from './schemas/user.schema';
import { validate } from 'class-validator';
import { CreateUserDto } from '../dto/create-user.dto';
import { UserProfile } from '../dto/user-profile.dto';
import { ConfigService } from '@nestjs/config';
import axios, { AxiosResponse } from 'axios';
import { ClsService } from 'nestjs-cls';
import * as bcrypt from 'bcryptjs';

@Injectable()
export class UserService {
  rattingServiceUrl: string;
  movieServiceUrl: string;
  constructor(
    @InjectModel('User') private readonly userModel: Model<User>,
    private readonly logger: Logger,
    private readonly clsService: ClsService,
    configService: ConfigService,
  ) {
    this.rattingServiceUrl = configService.get<string>('RATING_SERVICE_URL');
    this.movieServiceUrl = configService.get<string>('MOVIE_SERVICE_URL');
  }

  async findOneWithUserName(username: string): Promise<User | undefined> {
    return this.userModel.findOne({ username }).exec();
  }

  async create(createUserDto: CreateUserDto): Promise<User> {
    const errors = await validate(createUserDto);
    this.logger.debug(`Validation errors: ${JSON.stringify(errors)}`);
    if (errors.length > 0) {
      throw new BadRequestException(errors); // Throw validation errors
    }
    // Check if user with username already exists
    const existingUser = await this.userModel.findOne({ createUserDto }).exec();
    if (existingUser) {
      throw new BadRequestException('Username already exists');
    }

    const createdUser = new this.userModel(createUserDto);
    createdUser.save();

    return {
      id: createdUser._id,
      username: createdUser.username,
      email: createdUser.email,
    } as User;
  }
  async exists(id: string): Promise<boolean> {
    const existingUser = await this.userModel.exists({ _id: id });
    return !!existingUser;
  }
  async getUserProfile(id: string): Promise<PromiseLike<UserProfile>> {
    const existingUser = await this.userModel.findOne({ _id: id });
    if (!existingUser) new NotFoundException('User not found');
    const moviesRating = await this.getMoviesRating(id);

    return {
      id: existingUser._id,
      username: existingUser.username,
      email: existingUser.email,
      moviesRating,
    } as UserProfile;
  }

  async getMoviesRating(
    id: string,
  ): Promise<PromiseLike<{ movieId: string; rating: number }[]>> {
    const authToken = this.clsService.get('authToken'); // Retrieve token from CLS context
    const response = (await axios.get(
      `${this.rattingServiceUrl}/ratings/user/${id}`,
      { headers: { Authorization: `Bearer ${authToken}` } },
    )) as AxiosResponse<{ movieId: string; rating: number }[]>;
    return response.data;
  }
  async validateUserCredentials(
    username: string,
    password: string,
  ): Promise<User | null> {
    const user = await this.userModel.findOne({ username });
    if (user && (await bcrypt.compare(password, user.password))) {
      return user; // Return the user object if password is valid
    }
    return null; // Return null if user is not found or password is invalid
  }
}
