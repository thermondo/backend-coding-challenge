import {
  BadRequestException,
  Injectable,
  Logger,
  UnauthorizedException,
} from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { validate } from 'class-validator';
import { Model } from 'mongoose';
import { CreateRatingDto } from '../dto/create-rating.dto';
import { Rating, RatingDocument } from '../schemas/rating.schema';
import { ValidationService } from '../validation/validation.service';
import { ClsService } from 'nestjs-cls';

@Injectable()
export class RatingService {
  constructor(
    @InjectModel(Rating.name)
    private readonly ratingModel: Model<RatingDocument>,
    private readonly validationService: ValidationService,
    private readonly logger: Logger,
    private readonly clsService: ClsService,
  ) {}

  async upsert(createRatingDto: CreateRatingDto): Promise<Rating> {
    const errors = await validate(createRatingDto);
    if (errors.length > 0) {
      throw new BadRequestException(errors);
    }
    const tokenUserId = this.clsService.get('userId');
    if (tokenUserId !== createRatingDto.userId) {
      throw new UnauthorizedException(
        'User ID in token does not match the user ID in the request body',
      );
    }
    const { userId, movieId, rating } = createRatingDto;
    const userExists = await this.validationService.checkUserExists(userId);
    if (!userExists) {
      throw new BadRequestException(`User with ID ${userId} does not exist`);
    }
    const movieExists = await this.validationService.checkMovieExists(movieId);
    this.logger.log(`Movie exists: ${movieExists}`);
    this.logger.log(`movieId: ${movieId}`);

    if (!movieExists) {
      throw new BadRequestException(`Movie with ID ${movieId} does not exist`);
    }

    // Upsert operation using findOneAndUpdate
    const filter = { userId, movieId };
    const update = { userId, movieId, rating };
    const options = { upsert: true, new: true, setDefaultsOnInsert: true };
    return this.ratingModel
      .findOneAndUpdate(filter, update, options)
      .exec()
      .then((result) => {
        if (result) {
          // Remove _id and __v from the returned document
          // eslint-disable-next-line @typescript-eslint/no-unused-vars
          const { _id, __v, ...rating } = result.toObject();
          return rating;
        }
        return null;
      });
  }

  getUserMoviesRating(id: string) {
    return this.ratingModel
      .find({ userId: id })
      .select('movieId rating -_id')
      .exec();
  }
}
