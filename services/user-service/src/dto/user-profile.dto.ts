export class UserProfile {
  id: string;
  username: string;
  email: string;
  moviesRating: MovieRating[];
}

export interface MovieRating {
  movieId: string;
  rating: number;
}
