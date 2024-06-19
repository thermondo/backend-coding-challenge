import {
  Controller,
  Post,
  Body,
  HttpStatus,
  HttpException,
  Logger,
  Param,
  Get,
} from '@nestjs/common';
import { CreateRatingDto } from '../dto/create-rating.dto';
import { RatingService } from './rating.service';
import { ApiOperation, ApiResponse, ApiTags } from '@nestjs/swagger';

@ApiTags('ratings')
@Controller('ratings')
export class RatingController {
  constructor(
    private readonly ratingService: RatingService,
    private readonly logger: Logger,
  ) {}

  @Post()
  @ApiOperation({ summary: 'Create movie rating' })
  @ApiResponse({ status: 401, description: 'Unauthorized' })
  @ApiResponse({
    status: 400,
    description:
      'User ID in token does not match the user ID in the request body',
  })
  @ApiResponse({
    status: 200,
    description: 'The found record',
    type: CreateRatingDto,
  })
  @ApiResponse({ status: 400, description: 'Invalid request' })
  async upsert(@Body() createRatingDto: CreateRatingDto) {
    try {
      this.logger.log('Creating rating' + JSON.stringify(createRatingDto));
      const rating = await this.ratingService.upsert(createRatingDto);
      return { rating };
    } catch (error) {
      throw new HttpException(error.message, HttpStatus.BAD_REQUEST);
    }
  }
  @Get('user/:id')
  async getUserMoviesRating(@Param('id') id: string) {
    try {
      this.logger.log('get user ratings :' + id);
      const ratings = await this.ratingService.getUserMoviesRating(id);
      return ratings;
    } catch (error) {
      throw new HttpException(error.message, HttpStatus.BAD_REQUEST);
    }
  }
}
