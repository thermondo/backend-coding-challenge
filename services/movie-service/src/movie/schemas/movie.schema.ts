import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document } from 'mongoose';

export type MovieDocument = Movie & Document;

@Schema()
export class Movie {
  @Prop({ required: true, unique: true })
  title: string;

  @Prop({ required: true })
  description: string;

  @Prop({ required: true })
  year: number;

  createdAt: Date;
  updatedAt: Date;
}

const MovieSchema = SchemaFactory.createForClass(Movie);
MovieSchema.pre<MovieDocument>('save', async function (next) {
  this.updatedAt = new Date();
  if (this.createdAt === undefined) {
    this.createdAt = new Date();
  }
  if (!this.isModified('password')) {
    return next();
  }
  next();
});

export { MovieSchema };
