// Generate JWT for backend API calls
import { SignJWT } from 'jose';

const secret = new TextEncoder().encode(process.env.BETTER_AUTH_SECRET);

export async function generateBackendToken(userId: string, email: string, name: string): Promise<string> {
  const token = await new SignJWT({
    sub: userId,
    email,
    name,
  })
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime('30d')
    .sign(secret);

  return token;
}
