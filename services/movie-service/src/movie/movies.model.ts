import { CreateMovieDto } from './dto/create-movie.dto';

export class MovieResponse {
  movies: CreateMovieDto[];
  total: number;
  currentPage: number;
  pageSize: number;
  nextPage: number | null;
}
