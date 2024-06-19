import { Logger, Module } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose';
import { RatingController } from './rating.controller';
import { Rating, RatingSchema } from '../schemas/rating.schema';
import { RatingService } from './rating.service';
import { ValidationService } from '../validation/validation.service';

@Module({
  imports: [
    MongooseModule.forFeature([{ name: Rating.name, schema: RatingSchema }]),
  ],
  controllers: [RatingController],
  providers: [RatingService, Logger, ValidationService],
})
export class RatingModule {}
