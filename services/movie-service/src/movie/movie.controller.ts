import {
  Controller,
  Get,
  Post,
  Put,
  Delete,
  Param,
  Body,
  NotFoundException,
  HttpException,
  HttpStatus,
  Query,
} from '@nestjs/common';
import { CreateMovieDto } from './dto/create-movie.dto';
import { MovieService } from './movie.service';
import { Movie } from './schemas/movie.schema';
import { ApiTags } from '@nestjs/swagger';

@ApiTags('movies')
@Controller('movies')
export class MovieController {
  constructor(private readonly movieService: MovieService) {}

  @Post()
  async create(@Body() createMovieDto: CreateMovieDto): Promise<Movie> {
    try {
      const movie = await this.movieService.create(createMovieDto);
      return movie;
    } catch (error) {
      throw new HttpException(error.message, HttpStatus.BAD_REQUEST);
    }
  }

  @Get()
  async findAll(@Query('page') page = 1, @Query('pageSize') pageSize = 10) {
    const {
      movies,
      total,
      currentPage,
      pageSize: returnedPageSize,
      nextPage,
    } = await this.movieService.findAll(page, pageSize);
    return { movies, total, currentPage, pageSize: returnedPageSize, nextPage };
  }

  @Get(':id/exists')
  async movieExists(@Param('id') id: string): Promise<boolean> {
    return this.movieService.exists(id);
  }

  @Get(':id')
  async findOne(@Param('id') id: string): Promise<Movie> {
    const movie = await this.movieService.findOne(id);
    if (!movie) {
      throw new NotFoundException(`Movie with ID ${id} not found`);
    }
    return movie;
  }

  @Put(':id')
  async update(
    @Param('id') id: string,
    @Body() updateMovieDto: CreateMovieDto,
  ): Promise<CreateMovieDto> {
    return this.movieService.update(id, updateMovieDto);
  }

  @Delete(':id')
  async remove(@Param('id') id: string): Promise<void> {
    return this.movieService.remove(id);
  }
}
