import { Schema, Prop, SchemaFactory } from '@nestjs/mongoose';
import { Document } from 'mongoose';

@Schema()
export class Rating {
  @Prop({ required: true })
  userId: string;

  @Prop({ required: true })
  movieId: string;

  @Prop({ required: true })
  rating: number;

  createdAt: Date;
  updatedAt: Date;
}

export type RatingDocument = Rating & Document;
const RatingSchema = SchemaFactory.createForClass(Rating);
RatingSchema.pre<RatingDocument>('save', async function (next) {
  this.updatedAt = new Date();
  if (this.createdAt === undefined) {
    this.createdAt = new Date();
  }
  if (!this.isModified('password')) {
    return next();
  }
  next();
});
export { RatingSchema };
