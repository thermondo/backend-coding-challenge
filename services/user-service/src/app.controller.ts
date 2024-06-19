import { Controller, Get } from '@nestjs/common';

@Controller()
export class AppController {
  constructor() {}

  @Get('/')
  async getHello() {
    return 'Hello from user-service';
  }
}
