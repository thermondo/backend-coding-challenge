import { Controller, Post, Body, Logger, Get, Param } from '@nestjs/common';
import { UserService } from './user.service';
import { User } from './schemas/user.schema';
import { CreateUserDto } from '../dto/create-user.dto';
import { ValidateUserCredentialsDto } from '../dto/validate-user.dto';
import { ApiOperation, ApiResponse, ApiTags } from '@nestjs/swagger';
import { UserProfile } from '../dto/user-profile.dto';

@ApiTags('users')
@Controller('users')
export class UserController {
  constructor(
    private readonly userService: UserService,
    private readonly loggerService: Logger,
  ) {}

  @ApiOperation({ summary: 'Create user' })
  @ApiResponse({
    status: 200,
    description: 'The found record',
    type: CreateUserDto,
  })
  @ApiResponse({ status: 400, description: 'Invalid request' })
  @Post()
  async createUser(@Body() createUserDto: CreateUserDto): Promise<User> {
    this.loggerService.debug(
      `Creating a new user with data: ${JSON.stringify(createUserDto)}`,
    );
    return this.userService.create(createUserDto);
  }

  @ApiOperation({ summary: 'check user exists' })
  @ApiResponse({ status: 401, description: 'Unauthorized' })
  @ApiResponse({
    status: 200,
    description: 'user exists record',
    type: Boolean,
  })
  @Get(':id/exists')
  async userExists(@Param('id') id: string): Promise<boolean> {
    return this.userService.exists(id);
  }

  @ApiOperation({ summary: 'get user profile' })
  @ApiResponse({ status: 401, description: 'Unauthorized' })
  @ApiResponse({
    status: 200,
    description: 'user profile record',
    type: UserProfile,
  })
  @Get(':id/profile')
  async userProfile(@Param('id') id: string): Promise<UserProfile> {
    return this.userService.getUserProfile(id);
  }

  @ApiOperation({ summary: 'get user profile' })
  @ApiResponse({ status: 401, description: 'Unauthorized' })
  @ApiResponse({
    status: 200,
    description: 'validate user credentials',
    type: Boolean,
  })
  @Post('validate-credentials')
  async validateUser(
    @Body() validateUserCredentialsDto: ValidateUserCredentialsDto,
  ): Promise<User> {
    this.loggerService.debug(
      `validate user credentials with data: ${JSON.stringify(validateUserCredentialsDto)}`,
    );
    return this.userService.validateUserCredentials(
      validateUserCredentialsDto.username,
      validateUserCredentialsDto.password,
    );
  }
}
