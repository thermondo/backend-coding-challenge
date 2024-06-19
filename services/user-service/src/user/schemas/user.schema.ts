import * as mongoose from 'mongoose';
import * as bcrypt from 'bcryptjs';

export const UserSchema = new mongoose.Schema({
  username: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  email: { type: String, required: true, unique: true },
});
export type UserDocument = User & Document;

export interface User extends mongoose.Document {
  username: string;
  password: string;
  email: string;
  createdAt: Date;
  updatedAt: Date;
}

UserSchema.pre<UserDocument>('save', async function (next) {
  this.updatedAt = new Date();
  if (this.createdAt === undefined) {
    this.createdAt = new Date();
  }
  if (!this.isModified('password')) {
    return next();
  }
  const salt = await bcrypt.genSalt(10);
  const hash = await bcrypt.hash(this.password, salt);
  this.password = hash;
  next();
});
