// phase_ii/web/lib/auth-client.ts
import { createAuthClient } from "better-auth/react";
export const { signIn, signUp, signOut, useSession } = createAuthClient({
    baseURL: "http://todo.test",
});
