// movie.service.ts

import {
  Inject,
  Injectable,
  Logger,
  NotFoundException,
  UseInterceptors,
} from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { Movie } from './schemas/movie.schema';
import { CreateMovieDto } from './dto/create-movie.dto';
import { CACHE_MANAGER, CacheInterceptor } from '@nestjs/cache-manager';
import { Cache } from 'cache-manager';
import { MovieResponse } from './movies.model';

@Injectable()
export class MovieService {
  constructor(
    @InjectModel('Movie') private readonly movieModel: Model<Movie>,
    @Inject(CACHE_MANAGER) private cacheService: Cache,
    private readonly logger: Logger,
  ) {}

  async create(createMovieDto: CreateMovieDto): Promise<Movie> {
    const existingMovie = await this.movieModel
      .findOne({ title: createMovieDto.title })
      .exec();
    if (existingMovie) {
      throw new Error('Movie with the same title already exists');
    }
    const createdMovie = new this.movieModel(createMovieDto);
    const savedMovie = await createdMovie.save();

    return savedMovie;
  }

  @UseInterceptors(CacheInterceptor)
  async findAll(page = 1, pageSize = 10): Promise<MovieResponse> {
    const skip = (page - 1) * pageSize;

    const movies = await this.movieModel
      .find()
      .skip(skip)
      .limit(pageSize)
      .select({ __v: 0 })
      .exec();

    const formattedMovies = movies.map((movie) => ({
      id: movie._id,
      title: movie.title,
      year: movie.year,
      description: movie.description,
    }));

    const totalMovies = await this.movieModel.countDocuments().exec();
    const nextPage = Number(page) + 1;
    const hasNextPage = skip + pageSize < totalMovies;

    return {
      movies: formattedMovies,
      total: totalMovies,
      currentPage: page,
      pageSize,
      nextPage: hasNextPage ? nextPage : null,
    };
  }

  @UseInterceptors(CacheInterceptor)
  async findOne(id: string): Promise<Movie> {
    const cachedData = await this.cacheService.get<Movie>(id.toString());
    if (cachedData) {
      this.logger.log('Getting data from cache!');
      return cachedData;
    }
    const movie = await this.movieModel.findById(id).select({ __v: 0 }).exec();
    if (!movie) {
      throw new NotFoundException(`Movie with ID ${id} not found`);
    }
    await this.cacheService.set(id.toString(), movie);
    return movie;
  }

  async update(
    id: string,
    updateMovieDto: CreateMovieDto,
  ): Promise<CreateMovieDto> {
    const updatedMovie = await this.movieModel
      .findByIdAndUpdate(id, updateMovieDto, { new: true })
      .exec();
    if (!updatedMovie) {
      throw new NotFoundException(`Movie with ID ${id} not found`);
    }
    return {
      id: updatedMovie._id,
      title: updatedMovie.title,
      year: updatedMovie.year,
      description: updatedMovie.description,
    } as CreateMovieDto;
  }

  async remove(id: string): Promise<void> {
    const deletedMovie = await this.movieModel.deleteOne({ id }).exec();
    if (!deletedMovie) {
      throw new NotFoundException(`Movie with ID ${id} not found`);
    }
  }
  async exists(id: string): Promise<boolean> {
    const existingMovie = await this.movieModel.exists({ _id: id });
    this.logger.log(`Movie exists: ${existingMovie}`);
    this.logger.log(`Movie id: ${id}`);

    return !!existingMovie;
  }
}
