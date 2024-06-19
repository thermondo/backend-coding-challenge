import { IsNotEmpty, IsOptional, IsString } from 'class-validator';

export class ValidateTokenDto {
  @IsNotEmpty()
  @IsString()
  token: string;

  @IsString()
  @IsOptional()
  accessLevel: string;
}
