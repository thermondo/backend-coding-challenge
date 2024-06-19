import { ApiProperty } from '@nestjs/swagger';
import { IsNotEmpty, IsString, IsNumber, Min, Max } from 'class-validator';

export class CreateRatingDto {
  @ApiProperty({
    example: '6672a19edab088ffe1242d18',
    description: 'The Id of the User',
  })
  @IsNotEmpty()
  @IsString()
  userId: string;

  @ApiProperty({
    example: '6672a18f29e0e0b9ac1e0d50',
    description: 'The Id of the Movie',
  })
  @IsNotEmpty()
  @IsString()
  movieId: string;

  @ApiProperty({ example: 1, description: 'The rating of the Movie' })
  @IsNotEmpty()
  @IsNumber()
  @Min(0)
  @Max(5)
  rating: number;
}
